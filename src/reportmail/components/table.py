"""Pandas DataFrame table component."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from numbers import Real
from typing import Any

import pandas as pd

from reportmail.formatters import format_value
from reportmail.utils import escape_html

from .base import Component, RenderContext


def _hex_rgb(color: str) -> tuple[int, int, int]:
    raw = color.lstrip("#")
    if len(raw) != 6:
        raise ValueError("Highlight colours must use six-digit hex notation")
    return tuple(int(raw[index : index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]


def _blend(start: str, end: str, ratio: float) -> str:
    low, high = _hex_rgb(start), _hex_rgb(end)
    values = (
        round(a + (b - a) * max(0.0, min(1.0, ratio))) for a, b in zip(low, high, strict=True)
    )
    return "#" + "".join(f"{value:02x}" for value in values)


@dataclass
class Table(Component):
    """A safely escaped, responsive DataFrame table."""

    data: pd.DataFrame
    title: str | None = None
    index: bool = False
    max_rows: int = 25
    formats: dict[str, str | Callable[[Any], Any]] | None = None
    currency: str = "USD"
    highlight: dict[str, dict[str, Any]] | None = None
    empty_message: str = "No data available"

    def __post_init__(self) -> None:
        if not isinstance(self.data, pd.DataFrame):
            raise TypeError("Table data must be a pandas DataFrame")
        if self.max_rows < 1:
            raise ValueError("max_rows must be at least 1")

    def _cell_style(self, column: str, value: Any) -> str:
        rule = (self.highlight or {}).get(column)
        if not rule or not isinstance(value, Real) or pd.isna(value):
            return ""
        numeric_value = float(value)
        if rule.get("type") == "positive_negative":
            color = "#dcfce7" if numeric_value > 0 else "#fee2e2" if numeric_value < 0 else ""
            return f"background-color:{color};" if color else ""
        if rule.get("type") == "color_scale":
            numeric = pd.to_numeric(self.data[column], errors="coerce").dropna()
            if numeric.empty:
                return ""
            minimum, maximum = float(numeric.min()), float(numeric.max())
            ratio = 0.5 if maximum == minimum else (numeric_value - minimum) / (maximum - minimum)
            color = _blend(rule.get("min", "#fee2e2"), rule.get("max", "#dcfce7"), ratio)
            return f"background-color:{color};"
        return ""

    def _formatted(self, column: str, value: Any) -> str:
        if pd.isna(value):
            return ""
        formatter = (self.formats or {}).get(column)
        return format_value(value, formatter, currency=self.currency)

    def render(self, context: RenderContext) -> str:
        theme = context.theme
        heading = (
            f'<h2 style="margin:0 0 12px;color:{theme.text_color};font-size:20px;line-height:28px">'
            f"{escape_html(self.title)}</h2>"
            if self.title
            else ""
        )
        if self.data.empty:
            return (
                f'<div style="margin:0 0 24px">{heading}<div style="padding:20px;border:1px solid '
                f'{theme.border_color};color:{theme.muted_text_color};text-align:center">'
                f"{escape_html(self.empty_message)}</div></div>"
            )
        visible = self.data.head(self.max_rows)
        columns = list(visible.columns)
        header_cells = ""
        if self.index:
            header_cells += '<th scope="col" style="padding:10px 12px;text-align:left">Index</th>'
        header_cells += "".join(
            f'<th scope="col" style="padding:10px 12px;text-align:left;white-space:nowrap">'
            f"{escape_html(column)}</th>"
            for column in columns
        )
        rows: list[str] = []
        for row_number, (idx, row) in enumerate(visible.iterrows()):
            background = theme.surface_color if row_number % 2 == 0 else theme.background_color
            cells = ""
            if self.index:
                cells += f'<td style="padding:10px 12px;white-space:nowrap">{escape_html(idx)}</td>'
            for column in columns:
                cells += (
                    f'<td style="padding:10px 12px;border-top:1px solid {theme.border_color};'
                    f'white-space:nowrap;{self._cell_style(str(column), row[column])}">'
                    f"{escape_html(self._formatted(str(column), row[column]))}</td>"
                )
            rows.append(f'<tr style="background:{background}">{cells}</tr>')
        truncated = ""
        if len(self.data) > self.max_rows:
            truncated = (
                f'<p style="margin:8px 0 0;color:{theme.muted_text_color};font-size:12px">'
                f"Showing {self.max_rows} of {len(self.data)} rows.</p>"
            )
        return (
            f'<div style="margin:0 0 24px">{heading}<div class="rm-table-scroll" '
            f'style="overflow-x:auto;border:1px solid {theme.border_color};border-radius:'
            f'{theme.border_radius}px"><table width="100%" cellspacing="0" cellpadding="0" '
            f'style="border-collapse:collapse;color:{theme.text_color};font-size:13px;line-height:19px">'
            f'<thead><tr style="background:{theme.primary_color};color:#ffffff">{header_cells}</tr></thead>'
            f"<tbody>{''.join(rows)}</tbody></table></div>{truncated}</div>"
        )

    def to_plain_text(self) -> str:
        parts = [self.title] if self.title else []
        if self.data.empty:
            parts.append(self.empty_message)
        else:
            parts.append(self.data.head(self.max_rows).to_string(index=self.index))
            if len(self.data) > self.max_rows:
                parts.append(f"Showing {self.max_rows} of {len(self.data)} rows.")
        return "\n".join(parts)
