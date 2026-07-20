from reportmail import KPI, Report


def test_kpi_formatting_and_escaping() -> None:
    html = (
        Report("Safe")
        .add(
            KPI(
                "Revenue <script>",
                1_240_000,
                format="currency",
                currency="INR",
                change=0.082,
                change_format="percent",
                trend="up",
            )
        )
        .render()
    )
    assert "₹12,40,000" in html
    assert "8.2%" in html
    assert "Up" in html and "↑" in html
    assert "Revenue &lt;script&gt;" in html
    assert "Revenue <script>" not in html


def test_kpis_are_grouped_three_per_row_with_mobile_class() -> None:
    body = Report("KPIs").add(*(KPI(str(i), i) for i in range(4))).render_body()
    assert body.count('class="rm-kpi-cell"') == 4
    assert body.count('class="rm-kpi-spacer"') == 2
    assert body.count("<tr>") >= 2
    assert 'class="rm-kpi-grid"' in body


def test_kpi_plain_text_communicates_trend() -> None:
    text = KPI("Orders", 42, change=-0.1, change_format="percent", trend="down").to_plain_text()
    assert text == "Orders: 42 (down: -10.0%)"
