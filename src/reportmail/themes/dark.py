"""Dark email theme."""

from dataclasses import dataclass

from .base import Theme


@dataclass(frozen=True)
class DarkTheme(Theme):
    """Dark theme using high-contrast colours."""

    background_color: str = "#111827"
    surface_color: str = "#1f2937"
    text_color: str = "#f9fafb"
    muted_text_color: str = "#d1d5db"
    border_color: str = "#374151"
    primary_color: str = "#60a5fa"
    positive_color: str = "#4ade80"
    negative_color: str = "#f87171"
    neutral_color: str = "#d1d5db"
