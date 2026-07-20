"""Divider component."""

from dataclasses import dataclass

from .base import Component, RenderContext


@dataclass
class Divider(Component):
    """A horizontal separator."""

    def render(self, context: RenderContext) -> str:
        return (
            f'<table role="presentation" width="100%" cellspacing="0" cellpadding="0" '
            f'style="margin:8px 0 24px"><tr><td style="border-top:1px solid '
            f'{context.theme.border_color};font-size:1px;line-height:1px">&nbsp;</td></tr></table>'
        )

    def to_plain_text(self) -> str:
        return "--------------------"
