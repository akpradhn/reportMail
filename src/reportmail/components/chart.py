"""Matplotlib chart component."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from io import BytesIO
from typing import Any, Literal

from reportmail.exceptions import RenderingError, UnsupportedChartError
from reportmail.utils import escape_html

from .base import Component, RenderContext


@dataclass
class Chart(Component):
    """A Matplotlib figure embedded as an in-memory data URI."""

    figure: Any
    title: str | None = None
    alt: str = "Analytics chart"
    width: int = 1100
    dpi: int = 150
    image_format: Literal["png", "jpeg"] = "png"
    close: bool = False

    def _image_data(self) -> str:
        if self.image_format not in {"png", "jpeg"}:
            raise UnsupportedChartError(f"Unsupported chart image format: {self.image_format!r}")
        try:
            from matplotlib.figure import Figure
        except ImportError as exc:  # pragma: no cover - declared dependency
            raise UnsupportedChartError("Matplotlib is required to render charts") from exc
        if not isinstance(self.figure, Figure):
            raise UnsupportedChartError(
                "Chart currently supports matplotlib.figure.Figure objects only"
            )
        buffer = BytesIO()
        try:
            self.figure.savefig(
                buffer,
                format=self.image_format,
                dpi=self.dpi,
                bbox_inches="tight",
                facecolor="white",
            )
            if self.close:
                from matplotlib import pyplot as plt

                plt.close(self.figure)
        except Exception as exc:
            raise RenderingError("Matplotlib could not export the chart") from exc
        mime = "image/jpeg" if self.image_format == "jpeg" else "image/png"
        return f"data:{mime};base64,{base64.b64encode(buffer.getvalue()).decode('ascii')}"

    def render(self, context: RenderContext) -> str:
        heading = (
            f'<h2 style="margin:0 0 12px;color:{context.theme.text_color};font-size:20px;line-height:28px">'
            f"{escape_html(self.title)}</h2>"
            if self.title
            else ""
        )
        return (
            f'<div style="margin:0 0 24px">{heading}<img src="{self._image_data()}" '
            f'alt="{escape_html(self.alt)}" width="{self.width}" style="display:block;width:100%;'
            f'max-width:{self.width}px;height:auto;border:0" /></div>'
        )

    def to_plain_text(self) -> str:
        return self.title or self.alt
