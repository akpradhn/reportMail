# reportmail

`reportmail` is an open-source, email-first Python package for polished analytics reports. It turns KPIs, Matplotlib charts, pandas DataFrames, prose, and branding into responsive HTML suitable for Gmail, Outlook, Apple Mail, and mobile clients. It uses no JavaScript, embeds charts as images, and supplies a plain-text fallback.

## Installation

```bash
pip install reportmail
```

Python 3.10 or newer is required.

## Quick start

```python
import pandas as pd
import matplotlib.pyplot as plt

from reportmail import Chart, KPI, LightTheme, Report, Table, Text

sales = pd.DataFrame({
    "Region": ["East", "West", "North", "South"],
    "Revenue": [120000, 98000, 76000, 64000],
    "Orders": [580, 491, 402, 369],
})

figure, axis = plt.subplots(figsize=(8, 4))
axis.bar(sales["Region"], sales["Revenue"])
axis.set_title("Revenue by region")

report = (
    Report(
        title="Weekly Business Review",
        subtitle="Week ending 14 July 2026",
        preheader="Revenue increased 8.2% this week.",
        theme=LightTheme(),
    )
    .add(
        KPI("Revenue", 1_240_000, format="currency", currency="INR",
            change=0.082, change_format="percent", trend="up"),
        KPI("Orders", 1_842, format="integer", change=0.041,
            change_format="percent", trend="up"),
        KPI("Refund rate", 0.018, format="percent", change=-0.003,
            change_format="percent", trend="down"),
    )
    .add(Chart(figure, title="Regional revenue", alt="Bar chart of revenue by region"))
    .add(Table(sales, title="Regional performance",
               formats={"Revenue": "currency", "Orders": "integer"}, currency="INR"))
    .add(Text("Revenue and order volume improved.", title="Summary"))
)

html = report.render()
report.save("weekly-report.html")
```

## KPI cards

Adjacent KPIs are automatically placed three per desktop row and stacked on narrow screens. Trends include words and arrows, not colour alone.

```python
KPI(
    label="Revenue",
    value=1_240_000,
    format="currency",
    currency="INR",
    change=0.082,
    change_format="percent",
    trend="up",
    help_text="Compared with last week",
)
```

Percentage formatters consistently interpret input as a ratio: `0.182` becomes `18.2%`. To display percentage points already expressed as `1.8`, use a callable such as `lambda value: f"{value:.1f}%"`.

## Charts

`Chart` accepts a `matplotlib.figure.Figure`, exports PNG or JPEG entirely in memory, and embeds a base64 data URI. The figure remains open unless `close=True` is set.

```python
figure, axis = plt.subplots()
axis.plot(["Jan", "Feb", "Mar"], [10, 13, 18])
report.add(Chart(figure, title="Monthly growth", alt="Growth from January to March"))
```

Many email providers support data URIs inconsistently. If yours strips them, host images or convert data URIs to content-ID attachments in your sending integration. reportmail deliberately does not send email.

## DataFrame tables

Tables escape headers and cells, alternate row backgrounds, scroll horizontally on small screens, handle empty data, and report truncation.

```python
Table(
    sales,
    max_rows=20,
    formats={"Revenue": "currency", "Orders": "integer"},
    currency="INR",
    highlight={
        "Revenue": {"type": "color_scale", "min": "#fee2e2", "max": "#dcfce7"},
        "Growth": {"type": "positive_negative"},
    },
)
```

Named formatters are `integer`, `decimal`, `percent`/`percentage`, `currency`, and `compact`. A formatter may also be a callable receiving the cell value.

## Themes and branding

Use `LightTheme`, `DarkTheme`, subclass `Theme`, or make a modified immutable copy:

```python
from dataclasses import replace
from reportmail import LightTheme, Report

brand = replace(LightTheme(), primary_color="#7c3aed", border_radius=12)
report = Report("Company update", theme=brand,
                logo_url="https://example.com/logo.png", footer="Example, Inc.")
```

Theme fields cover background, surface, text, muted text, borders, primary, positive, negative and neutral colours, font family, border radius, and preferred report width. The explicit `Report(width=...)` controls rendered width.

## Sections and layout

`Section(title, subtitle).add(...)` groups components and is fluent. `Divider()` and `Spacer(height=16)` provide simple layout controls.

## Saving and sending

`report.render()` returns complete HTML, `report.render_body()` returns the inner content, `report.save(path)` writes UTF-8 HTML, and `report.to_plain_text()` creates a fallback:

```python
html = report.render()
plain_text = report.to_plain_text()

send_email(subject="Weekly report", html=html, text=plain_text)
```

Use any provider SDK or MIME library; reportmail remains provider-independent and does not implement SMTP.

For a complete SMTP example, first generate a local preview:

```bash
python examples/send_email_report.py --preview
```

Then configure your provider and send it:

```bash
export SMTP_HOST="smtp.example.com"
export SMTP_PORT="587"
export SMTP_SECURITY="starttls"
export SMTP_USERNAME="reports@example.com"
export SMTP_PASSWORD="your-app-password"
export REPORT_FROM="reports@example.com"
export REPORT_TO="recipient@example.com"

python examples/send_email_report.py
```

Charts can be delivered in either mode:

```bash
# Recommended for Gmail, Outlook, and most email clients
python examples/send_email_report.py --image-mode cid

# Keep self-contained base64 data URIs (some clients may block them)
python examples/send_email_report.py --image-mode data-uri
```

The same choice can be set with `REPORT_IMAGE_MODE=cid` or
`REPORT_IMAGE_MODE=data-uri`. Local HTML previews always remain self-contained.

## Email-client limitations

Email HTML is less capable than browser HTML. reportmail uses wrapper tables and important inline styles, but clients may vary in border-radius, dark-mode recolouring, web image blocking, data-URI support, and horizontal scrolling. Test real messages with the clients your recipients use. Keep tables reasonably narrow and always provide meaningful chart alt text.

## Security

Titles, labels, prose, table values, alt text, preheaders, and footers are escaped by default. `Text(..., allow_html=True)` bypasses escaping and must only receive trusted, pre-sanitised HTML. Custom formatters execute Python code supplied by the application, so do not accept formatter callables from untrusted users. Logo URLs are restricted to HTTP(S), CID, or data schemes.

## Development

```bash
git clone <repository-url>
cd reportmail
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
```

Runnable reports live in `examples/`; each writes an HTML file beside the script.

## Roadmap

- Optional Plotly static-image export
- Content-ID image attachment helpers
- More conditional table formatting rules
- Additional tested email templates and accessibility checks
- Provider integration recipes without coupling the core package

## License

MIT
# reportMail
