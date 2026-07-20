"""KPI card component."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal

from reportmail.formatters import format_value
from reportmail.utils import escape_html

from .base import Component, RenderContext


@dataclass
class KPI(Component):
    """A key performance indicator with an optional change signal."""

    label: str
    value: Any
    change: Any | None = None
    trend: Literal["up", "down", "neutral"] = "neutral"
    format: str | Callable[[Any], Any] | None = None
    change_format: str | Callable[[Any], Any] | None = None
    prefix: str = ""
    suffix: str = ""
    change_prefix: str = ""
    change_suffix: str = ""
    currency: str = "USD"
    help_text: str | None = None

    def __post_init__(self) -> None:
        if self.trend not in {"up", "down", "neutral"}:
            raise ValueError("trend must be 'up', 'down', or 'neutral'")

    def _main_value(self) -> str:
        return (
            self.prefix
            + format_value(self.value, self.format, currency=self.currency)
            + self.suffix
        )

    def _change_value(self) -> str:
        if self.change is None:
            return ""
        return (
            self.change_prefix
            + format_value(self.change, self.change_format, currency=self.currency)
            + self.change_suffix
        )

    def render_card(self, context: RenderContext) -> str:
        theme = context.theme
        states = {
            "up": ("↑", "Up", theme.positive_color),
            "down": ("↓", "Down", theme.negative_color),
            "neutral": ("→", "Neutral", theme.neutral_color),
        }
        arrow, word, color = states[self.trend]
        change = ""
        if self.change is not None:
            change = (
                f'<div style="margin-top:8px;color:{color};font-size:13px;line-height:18px">'
                f'<span aria-hidden="true">{arrow}</span> {word} '
                f"{escape_html(self._change_value())}</div>"
            )
        help_text = (
            f'<div style="margin-top:6px;color:{theme.muted_text_color};font-size:12px;line-height:17px">'
            f"{escape_html(self.help_text)}</div>"
            if self.help_text
            else ""
        )
        return (
            f'<table role="presentation" width="100%" cellspacing="0" cellpadding="0" '
            f'style="background:{theme.surface_color};border:1px solid {theme.border_color};'
            f'border-radius:{theme.border_radius}px"><tr><td style="padding:18px">'
            f'<div style="color:{theme.muted_text_color};font-size:12px;line-height:18px;'
            f'text-transform:uppercase;letter-spacing:.04em">{escape_html(self.label)}</div>'
            f'<div style="margin-top:5px;color:{theme.text_color};font-size:26px;font-weight:700;'
            f'line-height:32px">{escape_html(self._main_value())}</div>{change}{help_text}</td></tr></table>'
        )

    def render(self, context: RenderContext) -> str:
        return f'<div style="margin:0 0 16px">{self.render_card(context)}</div>'

    def to_plain_text(self) -> str:
        result = f"{self.label}: {self._main_value()}"
        if self.change is not None:
            result += f" ({self.trend}: {self._change_value()})"
        if self.help_text:
            result += f" — {self.help_text}"
        return result


def render_kpi_group(kpis: list[KPI], context: RenderContext) -> str:
    """Render KPI cards in email-safe rows of three."""
    rows: list[str] = []
    for offset in range(0, len(kpis), 3):
        chunk = kpis[offset : offset + 3]
        cells = "".join(
            '<td class="rm-kpi-cell" width="33.33%" valign="top" '
            f'style="padding:0 6px 12px">{kpi.render_card(context)}</td>'
            for kpi in chunk
        )
        cells += "".join(
            '<td class="rm-kpi-spacer" width="33.33%" style="padding:0 6px 12px"></td>'
            for _ in range(3 - len(chunk))
        )
        rows.append(f"<tr>{cells}</tr>")
    return (
        '<table class="rm-kpi-grid" role="presentation" width="100%" cellspacing="0" '
        f'cellpadding="0" style="margin:0 -6px 12px">{"".join(rows)}</table>'
    )
