"""Theme definitions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    """Base theme. Use ``dataclasses.replace`` for small customisations."""

    background_color: str = "#f3f4f6"
    surface_color: str = "#ffffff"
    text_color: str = "#111827"
    muted_text_color: str = "#6b7280"
    border_color: str = "#e5e7eb"
    primary_color: str = "#2563eb"
    positive_color: str = "#15803d"
    negative_color: str = "#b91c1c"
    neutral_color: str = "#6b7280"
    font_family: str = "Arial, Helvetica, sans-serif"
    border_radius: int = 8
    report_width: int = 760
