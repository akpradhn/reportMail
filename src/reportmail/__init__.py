"""Email-first HTML reports for Python."""

from .components import KPI, Chart, Component, Divider, Section, Spacer, Table, Text
from .exceptions import (
    InvalidFormatterError,
    RenderingError,
    ReportMailError,
    UnsupportedChartError,
)
from .report import Report
from .themes import DarkTheme, LightTheme, Theme

__version__ = "0.1.0"

__all__ = [
    "Chart",
    "Component",
    "DarkTheme",
    "Divider",
    "InvalidFormatterError",
    "KPI",
    "LightTheme",
    "RenderingError",
    "Report",
    "ReportMailError",
    "Section",
    "Spacer",
    "Table",
    "Text",
    "Theme",
    "UnsupportedChartError",
    "__version__",
]
