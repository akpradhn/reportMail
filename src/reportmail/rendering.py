"""Email document rendering helpers."""

from __future__ import annotations

from collections.abc import Iterable

from .components import KPI, Component, RenderContext
from .components.kpi import render_kpi_group
from .themes import Theme
from .utils import escape_html


def render_components(components: Iterable[Component], context: RenderContext) -> str:
    """Render components while collecting adjacent KPIs into rows."""
    output: list[str] = []
    pending: list[KPI] = []
    for component in components:
        if isinstance(component, KPI):
            pending.append(component)
            continue
        if pending:
            output.append(render_kpi_group(pending, context))
            pending = []
        output.append(component.render(context))
    if pending:
        output.append(render_kpi_group(pending, context))
    return "".join(output)


def render_document(
    *,
    title: str,
    subtitle: str | None,
    preheader: str | None,
    logo_url: str | None,
    footer: str | None,
    body: str,
    theme: Theme,
    width: int,
) -> str:
    """Wrap a report body in a complete, responsive email document."""
    logo = (
        f'<img src="{escape_html(logo_url)}" alt="Company logo" style="display:block;max-width:180px;'
        f'max-height:60px;height:auto;border:0;margin:0 0 18px" />'
        if logo_url
        else ""
    )
    subtitle_html = (
        f'<p style="margin:6px 0 0;color:{theme.muted_text_color};font-size:15px;line-height:22px">'
        f"{escape_html(subtitle)}</p>"
        if subtitle
        else ""
    )
    preheader_html = (
        '<div style="display:none;font-size:1px;color:#ffffff;line-height:1px;max-height:0;'
        f'max-width:0;opacity:0;overflow:hidden;mso-hide:all">{escape_html(preheader)}&#847; &#847; &#847;</div>'
        if preheader
        else ""
    )
    footer_html = (
        f'<tr><td style="padding:22px 28px;color:{theme.muted_text_color};font-size:12px;'
        f'line-height:18px;text-align:center">{escape_html(footer)}</td></tr>'
        if footer
        else ""
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="x-apple-disable-message-reformatting">
  <title>{escape_html(title)}</title>
  <style>
    body {{ margin:0 !important; padding:0 !important; width:100% !important; }}
    table {{ border-spacing:0; }} img {{ -ms-interpolation-mode:bicubic; }}
    @media only screen and (max-width: 620px) {{
      .rm-container {{ width:100% !important; }}
      .rm-content {{ padding:22px 16px !important; }}
      .rm-kpi-grid, .rm-kpi-grid tbody, .rm-kpi-grid tr {{ display:block !important; width:100% !important; }}
      .rm-kpi-cell {{ display:block !important; width:auto !important; padding:0 0 12px !important; }}
      .rm-kpi-spacer {{ display:none !important; }}
      .rm-table-scroll {{ overflow-x:auto !important; -webkit-overflow-scrolling:touch; }}
    }}
  </style>
</head>
<body style="margin:0;padding:0;background:{theme.background_color};font-family:{theme.font_family};">
  {preheader_html}
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="width:100%;background:{theme.background_color}">
    <tr><td align="center" style="padding:24px 10px">
      <!--[if mso]><table role="presentation" width="{width}"><tr><td><![endif]-->
      <table class="rm-container" role="presentation" width="{width}" cellspacing="0" cellpadding="0" style="width:100%;max-width:{width}px;background:{theme.surface_color};border:1px solid {theme.border_color};border-radius:{theme.border_radius}px">
        <tr><td style="padding:28px 28px 22px;border-bottom:1px solid {theme.border_color}">
          {logo}
          <h1 style="margin:0;color:{theme.text_color};font-size:28px;line-height:36px">{escape_html(title)}</h1>
          {subtitle_html}
        </td></tr>
        <tr><td class="rm-content" style="padding:28px;color:{theme.text_color}">{body}</td></tr>
        {footer_html}
      </table>
      <!--[if mso]></td></tr></table><![endif]-->
    </td></tr>
  </table>
</body>
</html>"""
