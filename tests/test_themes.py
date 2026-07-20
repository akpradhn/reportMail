from dataclasses import replace

from reportmail import DarkTheme, LightTheme, Report, Text


def test_dark_theme_is_applied() -> None:
    html = Report("Dark", theme=DarkTheme()).add(Text("Body")).render()
    assert "background:#111827" in html
    assert "color:#f9fafb" in html


def test_theme_can_be_customised_with_replace() -> None:
    theme = replace(LightTheme(), primary_color="#123456")
    assert theme.primary_color == "#123456"
