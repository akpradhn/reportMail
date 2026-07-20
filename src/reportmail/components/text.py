"""Text component."""

from __future__ import annotations

from dataclasses import dataclass

from reportmail.utils import escape_html

from .base import Component, RenderContext


@dataclass
class Text(Component):
    """A block of prose. ``allow_html`` must only be used with trusted input."""

    text: str
    title: str | None = None
    allow_html: bool = False

    def render(self, context: RenderContext) -> str:
        theme = context.theme
        title = (
            f'<h2 style="margin:0 0 12px;color:{theme.text_color};font-size:20px;line-height:28px">'
            f"{escape_html(self.title)}</h2>"
            if self.title
            else ""
        )
        if self.allow_html:
            body = self.text
        else:
            paragraphs = self.text.split("\n\n")
            body = "".join(
                f'<p style="margin:0 0 12px;color:{theme.text_color};font-size:15px;line-height:24px">'
                f"{escape_html(paragraph).replace(chr(10), '<br>')}</p>"
                for paragraph in paragraphs
            )
        return f'<div style="margin:0 0 24px">{title}{body}</div>'

    def to_plain_text(self) -> str:
        return "\n".join(part for part in (self.title, self.text) if part)
