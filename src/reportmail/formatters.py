"""Predictable, dependency-free value formatting helpers."""

from __future__ import annotations

import math
from collections.abc import Callable
from typing import Any

from .exceptions import InvalidFormatterError

Formatter = str | Callable[[Any], Any] | None


def _number(value: Any) -> float:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        raise ValueError("Cannot format a missing value as a number")
    return float(value)


def format_integer(value: Any) -> str:
    """Format a value as a rounded integer with thousands separators."""
    return f"{_number(value):,.0f}"


def format_decimal(value: Any, decimals: int = 2) -> str:
    """Format a decimal value with fixed precision."""
    return f"{_number(value):,.{decimals}f}"


def format_percent(value: Any, decimals: int = 1) -> str:
    """Format a ratio as a percentage; 0.182 is rendered as 18.2%."""
    return f"{_number(value) * 100:.{decimals}f}%"


def _indian_group(number: float, decimals: int) -> str:
    sign = "-" if number < 0 else ""
    fixed = f"{abs(number):.{decimals}f}"
    whole, dot, fraction = fixed.partition(".")
    if len(whole) > 3:
        tail = whole[-3:]
        head = whole[:-3]
        pairs: list[str] = []
        while head:
            pairs.insert(0, head[-2:])
            head = head[:-2]
        whole = ",".join([*pairs, tail])
    return sign + whole + (dot + fraction if decimals else "")


def format_currency(value: Any, currency: str = "USD", decimals: int = 0) -> str:
    """Format USD, INR, EUR, GBP, or JPY using a currency symbol."""
    code = currency.upper()
    symbols = {"USD": "$", "INR": "₹", "EUR": "€", "GBP": "£", "JPY": "¥"}
    if code not in symbols:
        raise InvalidFormatterError(f"Unsupported currency: {currency!r}")
    number = _number(value)
    rendered = _indian_group(number, decimals) if code == "INR" else f"{number:,.{decimals}f}"
    return symbols[code] + rendered


def format_compact(value: Any, decimals: int = 1) -> str:
    """Format a number using K, M, B, or T suffixes."""
    number = _number(value)
    for threshold, suffix in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "K")):
        if abs(number) >= threshold:
            text = f"{number / threshold:.{decimals}f}".rstrip("0").rstrip(".")
            return text + suffix
    if number.is_integer():
        return str(int(number))
    return f"{number:.{decimals}f}".rstrip("0").rstrip(".")


def format_value(value: Any, format: Formatter = None, **kwargs: Any) -> str:
    """Apply a named or callable formatter, returning a string."""
    if callable(format):
        try:
            return str(format(value))
        except Exception as exc:
            raise InvalidFormatterError("Custom formatter failed") from exc
    if format is None or format == "string":
        return "" if value is None else str(value)
    formatters: dict[str, Callable[..., str]] = {
        "integer": format_integer,
        "decimal": format_decimal,
        "percent": format_percent,
        "percentage": format_percent,
        "currency": format_currency,
        "compact": format_compact,
    }
    try:
        formatter = formatters[format.lower()]
    except (KeyError, AttributeError) as exc:
        raise InvalidFormatterError(f"Unknown formatter: {format!r}") from exc
    accepted = {
        "decimal": ("decimals",),
        "percent": ("decimals",),
        "percentage": ("decimals",),
        "currency": ("currency", "decimals"),
        "compact": ("decimals",),
    }.get(format.lower(), ())
    return formatter(value, **{key: kwargs[key] for key in accepted if key in kwargs})
