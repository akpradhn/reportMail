"""Spacer component."""

from dataclasses import dataclass

from .base import Component, RenderContext


@dataclass
class Spacer(Component):
    """Fixed vertical space."""

    height: int = 16

    def __post_init__(self) -> None:
        if self.height < 0 or self.height > 1000:
            raise ValueError("Spacer height must be between 0 and 1000")

    def render(self, context: RenderContext) -> str:
        return f'<div aria-hidden="true" style="height:{self.height}px;line-height:{self.height}px">&nbsp;</div>'

    def to_plain_text(self) -> str:
        return ""
