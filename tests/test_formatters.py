import pytest

from reportmail import InvalidFormatterError
from reportmail.formatters import (
    format_compact,
    format_currency,
    format_decimal,
    format_integer,
    format_percent,
    format_value,
)


def test_number_formatters() -> None:
    assert format_integer(1842) == "1,842"
    assert format_decimal(1234.567) == "1,234.57"
    assert format_percent(0.182) == "18.2%"
    assert format_compact(1_240_000) == "1.2M"


def test_supported_currency_and_indian_grouping() -> None:
    assert format_currency(1_240_000, "INR") == "₹12,40,000"
    assert format_currency(12.5, "EUR", decimals=2) == "€12.50"


def test_callable_and_invalid_formatter() -> None:
    assert format_value(3, lambda value: f"x{value}") == "x3"
    with pytest.raises(InvalidFormatterError, match="Unknown"):
        format_value(3, "mystery")
    with pytest.raises(InvalidFormatterError, match="Custom"):
        format_value(3, lambda _: 1 / 0)
