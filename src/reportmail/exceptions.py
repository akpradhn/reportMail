"""Exceptions raised by reportmail."""


class ReportMailError(Exception):
    """Base exception for package errors."""


class RenderingError(ReportMailError):
    """Raised when a report or component cannot be rendered."""


class UnsupportedChartError(RenderingError):
    """Raised when a chart object or image format is unsupported."""


class InvalidFormatterError(ReportMailError):
    """Raised when an unknown or invalid formatter is requested."""
