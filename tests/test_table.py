import pandas as pd

from reportmail import LightTheme, Report, Table
from reportmail.components import RenderContext


def test_empty_dataframe_and_escaping() -> None:
    empty = Table(pd.DataFrame(), empty_message="Nothing <yet>")
    assert "Nothing &lt;yet&gt;" in Report("Table").add(empty).render()


def test_table_truncation_formatting_and_escaping() -> None:
    frame = pd.DataFrame({"Name": ["<b>A</b>", "B", "C"], "Revenue": [1000, 2000, 3000]})
    html = Report("Table").add(Table(frame, max_rows=2, formats={"Revenue": "currency"})).render()
    assert "&lt;b&gt;A&lt;/b&gt;" in html
    assert "<b>A</b>" not in html
    assert "$1,000" in html
    assert "Showing 2 of 3 rows." in html


def test_custom_formatter_and_conditional_highlights() -> None:
    frame = pd.DataFrame({"Growth": [-1, 2], "Revenue": [10, 20]})
    html = Table(
        frame,
        formats={"Growth": lambda value: f"{value:+d}"},
        highlight={
            "Growth": {"type": "positive_negative"},
            "Revenue": {"type": "color_scale", "min": "#000000", "max": "#ffffff"},
        },
    ).render(RenderContext(LightTheme(), 760))
    assert ">-1<" in html and ">+2<" in html
    assert "background-color:#fee2e2" in html
    assert "background-color:#ffffff" in html


def test_plain_text_table() -> None:
    text = Table(pd.DataFrame({"A": [1]}), title="Values").to_plain_text()
    assert "Values" in text and "A" in text and "1" in text
