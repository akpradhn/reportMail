"""Default light theme."""

from dataclasses import dataclass

from .base import Theme


@dataclass(frozen=True)
class LightTheme(Theme):
    """Bright theme suitable for most reports."""
