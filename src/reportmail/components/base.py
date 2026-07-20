"""Base component contracts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from reportmail.themes import Theme


@dataclass(frozen=True)
class RenderContext:
    """Rendering configuration shared by all components."""

    theme: Theme
    width: int


class Component(ABC):
    """Abstract report component."""

    @abstractmethod
    def render(self, context: RenderContext) -> str:
        """Render email-safe HTML."""

    @abstractmethod
    def to_plain_text(self) -> str:
        """Render a useful plain-text representation."""
