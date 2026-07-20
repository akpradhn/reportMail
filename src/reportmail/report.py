"""Top-level report API."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from .components import Component, RenderContext
from .exceptions import RenderingError
from .rendering import render_components, render_document
from .themes import LightTheme, Theme


class Report:
    """An email-first report composed from reusable components."""

    def __init__(
        self,
        title: str,
        subtitle: str | None = None,
        preheader: str | None = None,
        theme: Theme | None = None,
        logo_url: str | None = None,
        footer: str | None = None,
        width: int = 760,
    ) -> None:
        if not title:
            raise ValueError("Report title cannot be empty")
        if width < 320 or width > 2000:
            raise ValueError("Report width must be between 320 and 2000 pixels")
        if theme is not None and not isinstance(theme, Theme):
            raise TypeError("theme must be a Theme instance")
        if logo_url:
            scheme = urlparse(logo_url).scheme.lower()
            if scheme not in {"http", "https", "cid", "data"}:
                raise ValueError("logo_url must use http, https, cid, or data")
        self.title = title
        self.subtitle = subtitle
        self.preheader = preheader
        self.theme = theme or LightTheme()
        self.logo_url = logo_url
        self.footer = footer
        self.width = width
        self.components: list[Component] = []

    def add(self, *components: Component) -> Report:
        """Append components and return this report for fluent chaining."""
        if not all(isinstance(component, Component) for component in components):
            raise TypeError("Report.add accepts Component instances only")
        self.components.extend(components)
        return self

    def clear(self) -> Report:
        """Remove every component and return this report."""
        self.components.clear()
        return self

    def render_body(self) -> str:
        """Render only the component body."""
        try:
            return render_components(self.components, RenderContext(self.theme, self.width))
        except RenderingError:
            raise
        except Exception as exc:
            raise RenderingError("Could not render report body") from exc

    def render(self) -> str:
        """Render a complete HTML email document."""
        return render_document(
            title=self.title,
            subtitle=self.subtitle,
            preheader=self.preheader,
            logo_url=self.logo_url,
            footer=self.footer,
            body=self.render_body(),
            theme=self.theme,
            width=self.width,
        )

    def save(self, path: str | Path) -> Path:
        """Write UTF-8 HTML to a non-directory path and return its resolved path."""
        destination = Path(path).expanduser()
        if destination.exists() and destination.is_dir():
            raise RenderingError(f"Output path is a directory: {destination}")
        if not destination.parent.exists():
            raise RenderingError(f"Output directory does not exist: {destination.parent}")
        try:
            destination.write_text(self.render(), encoding="utf-8")
        except OSError as exc:
            raise RenderingError(f"Could not save report to {destination}") from exc
        return destination.resolve()

    def to_plain_text(self) -> str:
        """Return a provider-independent plain-text fallback."""
        header = "\n".join(part for part in (self.title, self.subtitle) if part)
        body = "\n\n".join(
            filter(None, (component.to_plain_text() for component in self.components))
        )
        return "\n\n".join(filter(None, (header, body, self.footer)))
