"""Generate a multi-section branded report."""

from dataclasses import replace
from pathlib import Path

import pandas as pd

from reportmail import KPI, Divider, LightTheme, Report, Section, Table, Text

brand = replace(
    LightTheme(),
    primary_color="#6d28d9",
    positive_color="#047857",
    border_radius=12,
)
pipeline = pd.DataFrame(
    {
        "Stage": ["Qualified", "Proposal", "Negotiation"],
        "Deals": [34, 18, 9],
        "Value": [280_000, 195_000, 118_000],
    }
)

overview = Section("Executive overview", "Performance through 14 July").add(
    KPI("Pipeline", 593_000, format="currency", change=0.12, change_format="percent", trend="up"),
    KPI("Win rate", 0.31, format="percent", change=0.02, change_format="percent", trend="up"),
    KPI("Sales cycle", 24, suffix=" days", change=-2, change_suffix=" days", trend="down"),
    Text("Pipeline quality improved, led by mid-market opportunities."),
)
details = Section("Pipeline detail", "Open opportunities by stage").add(
    Table(pipeline, formats={"Deals": "integer", "Value": "currency"}),
    Divider(),
    Text("Negotiation-stage opportunities are on track for month-end decisions."),
)

report = Report(
    "Northstar Revenue Brief",
    subtitle="A concise weekly operating report",
    preheader="Pipeline increased 12% this week.",
    theme=brand,
    logo_url="https://dummyimage.com/320x80/6d28d9/ffffff.png&text=Northstar",
    footer="Northstar Analytics · Confidential",
).add(overview, details)

output = report.save(Path(__file__).with_suffix(".html"))
print(f"Wrote {output}")
