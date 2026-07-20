"""Internal utilities."""

from html import escape
from typing import Any


def escape_html(value: Any, *, quote: bool = True) -> str:
    """Escape an arbitrary value for safe HTML output."""
    return escape("" if value is None else str(value), quote=quote)


def inline_style(**properties: str | int | None) -> str:
    """Build a compact inline CSS declaration from underscore-separated keys."""
    return ";".join(
        f"{key.replace('_', '-')}:{value}" for key, value in properties.items() if value is not None
    )
