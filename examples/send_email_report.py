"""Generate and send a reportmail report through an SMTP provider."""

from __future__ import annotations

import argparse
import base64
import os
import re
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from reportmail import KPI, Chart, Report, Table, Text

DATA_IMAGE_PATTERN = re.compile(
    r"data:image/(?P<subtype>png|jpeg);base64,(?P<payload>[A-Za-z0-9+/=]+)"
)


def build_report() -> Report:
    """Build the sample report used as the email body."""
    sales = pd.DataFrame(
        {
            "Region": ["East", "West", "North", "South"],
            "Revenue": [120_000, 98_000, 76_000, 64_000],
            "Orders": [580, 491, 402, 369],
        }
    )

    figure, axis = plt.subplots(figsize=(8, 4))
    axis.bar(sales["Region"], sales["Revenue"], color="#2563eb")
    axis.set_title("Revenue by region")
    axis.set_ylabel("Revenue (INR)")
    figure.tight_layout()

    return Report(
        title="Weekly Business Review",
        subtitle="Week ending 14 July 2026",
        preheader="Revenue increased 8.2% this week.",
        footer="Generated automatically with reportmail.",
    ).add(
        KPI(
            "Revenue",
            1_240_000,
            format="currency",
            currency="INR",
            change=0.082,
            change_format="percent",
            trend="up",
        ),
        KPI(
            "Orders",
            1_842,
            format="integer",
            change=0.041,
            change_format="percent",
            trend="up",
        ),
        KPI("Refund rate", 0.018, format="percent", trend="down"),
        Chart(
            figure,
            title="Regional revenue",
            alt="Bar chart showing revenue by region",
            close=True,
        ),
        Table(
            sales,
            title="Regional performance",
            formats={"Revenue": "currency", "Orders": "integer"},
            currency="INR",
        ),
        Text(
            "Revenue and order volume improved across the strongest regions.",
            title="Summary",
        ),
    )


def build_message(
    report: Report,
    sender: str,
    recipient: str,
    *,
    image_mode: str = "cid",
) -> EmailMessage:
    """Create a multipart email using CID attachments or data-URI images."""
    if image_mode not in {"cid", "data-uri"}:
        raise ValueError("image_mode must be 'cid' or 'data-uri'")

    html = report.render()
    related_images: list[tuple[str, str, bytes]] = []

    if image_mode == "cid":

        def replace_with_cid(match: re.Match[str]) -> str:
            cid = f"reportmail-chart-{len(related_images) + 1}"
            subtype = match.group("subtype")
            image_bytes = base64.b64decode(match.group("payload"), validate=True)
            related_images.append((cid, subtype, image_bytes))
            return f"cid:{cid}"

        html = DATA_IMAGE_PATTERN.sub(replace_with_cid, html)

    message = EmailMessage()
    message["Subject"] = "Weekly Business Review — 14 July 2026"
    message["From"] = sender
    message["To"] = recipient
    message.set_content(report.to_plain_text())
    message.add_alternative(html, subtype="html")

    if related_images:
        html_part = message.get_payload()[-1]
        for cid, subtype, image_bytes in related_images:
            html_part.add_related(
                image_bytes,
                maintype="image",
                subtype=subtype,
                cid=f"<{cid}>",
                filename=f"{cid}.{subtype}",
                disposition="inline",
            )
    return message


def send_message(message: EmailMessage) -> None:
    """Send a message using SMTP settings from the environment."""
    host = os.environ["SMTP_HOST"]
    port = int(os.getenv("SMTP_PORT", "587"))
    username = os.environ["SMTP_USERNAME"]
    password = os.environ["SMTP_PASSWORD"]
    security = os.getenv("SMTP_SECURITY", "starttls").lower()
    context = ssl.create_default_context()

    if security == "ssl":
        with smtplib.SMTP_SSL(host, port, context=context) as smtp:
            smtp.login(username, password)
            smtp.send_message(message)
        return

    if security not in {"starttls", "none"}:
        raise ValueError("SMTP_SECURITY must be 'starttls', 'ssl', or 'none'")

    with smtplib.SMTP(host, port) as smtp:
        smtp.ehlo()
        if security == "starttls":
            smtp.starttls(context=context)
            smtp.ehlo()
        smtp.login(username, password)
        smtp.send_message(message)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--preview",
        action="store_true",
        help="write the HTML report locally without sending email",
    )
    parser.add_argument(
        "--image-mode",
        choices=("cid", "data-uri"),
        default=os.getenv("REPORT_IMAGE_MODE", "cid"),
        help="chart delivery mode; CID is more compatible with email clients",
    )
    args = parser.parse_args()

    report = build_report()
    if args.preview:
        output = report.save(Path(__file__).with_name("email_preview.html"))
        print(f"Preview written to {output}")
        return

    sender = os.getenv("REPORT_FROM", os.getenv("SMTP_USERNAME", ""))
    recipient = os.environ.get("REPORT_TO", "")
    if not sender or not recipient:
        raise SystemExit("Set REPORT_TO and REPORT_FROM (or SMTP_USERNAME) before sending.")

    message = build_message(report, sender, recipient, image_mode=args.image_mode)
    send_message(message)
    print(f"Report sent to {recipient}")


if __name__ == "__main__":
    main()
