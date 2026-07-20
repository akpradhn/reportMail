from pathlib import Path

import pytest

from reportmail import KPI, Divider, RenderingError, Report, Section, Spacer, Text


def test_full_report_escaping_mobile_css_and_preheader() -> None:
    report = Report(
        "Report <Q3>",
        subtitle="Results & outlook",
        preheader="Secret <preview>",
        footer="Team & company",
    ).add(Text("Hello <script>"), Divider(), Spacer(4))
    html = report.render()
    assert html.startswith("<!doctype html>")
    assert "Report &lt;Q3&gt;" in html
    assert "Hello &lt;script&gt;" in html
    assert "Secret &lt;preview&gt;" in html
    assert "@media only screen and (max-width: 620px)" in html
    assert "rm-kpi-cell" in html
    assert ".rm-kpi-spacer { display:none !important; }" in html


def test_plain_text_sections_and_clear() -> None:
    section = Section("Metrics", "This week").add(KPI("Orders", 10), Text("All good"))
    report = Report("Weekly", subtitle="Monday", footer="Fin").add(section)
    text = report.to_plain_text()
    assert "Weekly\nMonday" in text
    assert "Metrics\nThis week" in text
    assert "Orders: 10" in text
    assert text.endswith("Fin")
    assert report.clear() is report and not report.components


def test_add_is_fluent_and_rejects_non_components() -> None:
    report = Report("Test")
    assert report.add(Text("x")) is report
    with pytest.raises(TypeError):
        report.add("not a component")  # type: ignore[arg-type]


def test_save_and_path_validation(tmp_path: Path) -> None:
    destination = Report("Saved").save(tmp_path / "report.html")
    assert destination.read_text(encoding="utf-8").startswith("<!doctype html>")
    with pytest.raises(RenderingError, match="directory"):
        Report("Bad").save(tmp_path)
    with pytest.raises(RenderingError, match="does not exist"):
        Report("Bad").save(tmp_path / "missing" / "report.html")


def test_trusted_html_is_opt_in() -> None:
    escaped = Report("x").add(Text("<strong>x</strong>")).render_body()
    trusted = Report("x").add(Text("<strong>x</strong>", allow_html=True)).render_body()
    assert "&lt;strong&gt;" in escaped
    assert "<strong>x</strong>" in trusted


def test_report_validation() -> None:
    with pytest.raises(ValueError):
        Report("")
    with pytest.raises(ValueError):
        Report("x", logo_url="javascript:alert(1)")
