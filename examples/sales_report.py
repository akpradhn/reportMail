"""Generate a monthly sales report."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from reportmail import KPI, Chart, Report, Table, Text

monthly = pd.DataFrame(
    {
        "Month": ["Feb", "Mar", "Apr", "May", "Jun", "Jul"],
        "Revenue": [82_000, 88_500, 91_000, 97_200, 103_400, 112_000],
        "Growth": [0.02, 0.079, 0.028, 0.068, 0.064, 0.083],
    }
)
figure, axis = plt.subplots(figsize=(8, 4))
axis.plot(monthly["Month"], monthly["Revenue"], marker="o", color="#2563eb")
axis.set_title("Monthly revenue trend")
axis.grid(axis="y", alpha=0.25)
figure.tight_layout()

report = Report("Sales Performance", subtitle="July 2026", footer="Internal sales analytics").add(
    KPI("Revenue", 112_000, format="currency", change=0.083, change_format="percent", trend="up"),
    KPI("Orders", 2_240, format="integer", change=0.051, change_format="percent", trend="up"),
    KPI(
        "Average order value",
        50,
        format="currency",
        change=0.03,
        change_format="percent",
        trend="up",
    ),
    Chart(
        figure, title="Revenue trend", alt="Revenue rising from February through July", close=True
    ),
    Table(
        monthly,
        title="Monthly growth",
        formats={"Revenue": "currency", "Growth": "percent"},
        highlight={"Growth": {"type": "positive_negative"}},
    ),
    Text("July delivered the strongest revenue and order volume in the period.", title="Takeaway"),
)

output = report.save(Path(__file__).with_suffix(".html"))
print(f"Wrote {output}")
