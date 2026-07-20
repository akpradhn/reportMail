"""Section component."""

from __future__ import annotations

from dataclasses import dataclass, field

from reportmail.utils import escape_html

from .base import Component, RenderContext
from .kpi import KPI, render_kpi_group


@dataclass
class Section(Component):
    """A fluent grouping of related components."""

    title: str | None = None
    subtitle: str | None = None
    components: list[Component] = field(default_factory=list, init=False, repr=False)

    def add(self, *components: Component) -> Section:
        if not all(isinstance(component, Component) for component in components):
            raise TypeError("Section.add accepts Component instances only")
        self.components.extend(components)
        return self

    def render(self, context: RenderContext) -> str:
        heading = (
            f'<h2 style="margin:0;color:{context.theme.text_color};font-size:22px;line-height:30px">'
            f"{escape_html(self.title)}</h2>"
            if self.title
            else ""
        )
        subtitle = (
            f'<p style="margin:4px 0 0;color:{context.theme.muted_text_color};font-size:14px;line-height:21px">'
            f"{escape_html(self.subtitle)}</p>"
            if self.subtitle
            else ""
        )
        output: list[str] = []
        pending: list[KPI] = []
        for component in self.components:
            if isinstance(component, KPI):
                pending.append(component)
            else:
                if pending:
                    output.append(render_kpi_group(pending, context))
                    pending = []
                output.append(component.render(context))
        if pending:
            output.append(render_kpi_group(pending, context))
        return (
            f'<div style="margin:0 0 28px"><div style="margin:0 0 16px">{heading}{subtitle}</div>'
            f"{''.join(output)}</div>"
        )

    def to_plain_text(self) -> str:
        heading = "\n".join(item for item in (self.title, self.subtitle) if item)
        body = "\n\n".join(filter(None, (item.to_plain_text() for item in self.components)))
        return "\n\n".join(filter(None, (heading, body)))
