from __future__ import annotations

from pathlib import Path
import json

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "marketing_dashboard.json"
OUTPUT_FILE = BASE_DIR / "output" / "marketing_report.pdf"


def currency(v: float) -> str:
    return f"NT$ {v:,.0f}"


def percent(v: float) -> str:
    return f"{v * 100:.2f}%"


def render_cover(pdf: PdfPages, data: dict) -> None:
    kpis = data["kpis"]
    meta = data["meta"]

    fig = plt.figure(figsize=(11.69, 8.27))  # A4 Landscape
    ax = fig.add_subplot(111)
    ax.axis("off")

    lines = [
        "Auto Marketing Dashboard Report",
        "",
        f"Source file: {meta['source_file']}",
        f"Date range: {meta['date_range']['start']} ~ {meta['date_range']['end']}",
        f"Row count: {meta['row_count']}",
        "",
        f"Total spend: {currency(kpis['spend'])}",
        f"Total revenue: {currency(kpis['revenue'])}",
        f"Total profit: {currency(kpis['profit'])}",
        f"ROI: {percent(kpis['roi'])}",
    ]
    ax.text(0.05, 0.9, "\n".join(lines), va="top", fontsize=16, family="sans-serif")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def render_trend(pdf: PdfPages, data: dict) -> None:
    weekly = data["weekly_trend"]
    weeks = [item["week_end"] for item in weekly]
    spends = [item["spend"] for item in weekly]
    revenues = [item["revenue"] for item in weekly]

    fig, ax = plt.subplots(figsize=(11.69, 8.27))
    ax.plot(weeks, spends, marker="o", label="Spend")
    ax.plot(weeks, revenues, marker="o", label="Revenue")
    ax.set_title("Weekly Spend vs Revenue")
    ax.set_xlabel("Week End")
    ax.set_ylabel("Amount (NTD)")
    ax.grid(alpha=0.25)
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    fig.tight_layout()
    pdf.savefig(fig)
    plt.close(fig)


def render_channel(pdf: PdfPages, data: dict) -> None:
    rows = data["channel_performance"]
    channels = [r["channel"] for r in rows]
    spends = [r["spend"] for r in rows]
    leads = [r["leads"] for r in rows]

    fig, axes = plt.subplots(1, 2, figsize=(11.69, 8.27))
    axes[0].bar(channels, spends)
    axes[0].set_title("Channel Spend")
    axes[0].tick_params(axis="x", rotation=30)

    axes[1].bar(channels, leads)
    axes[1].set_title("Channel Leads")
    axes[1].tick_params(axis="x", rotation=30)

    fig.tight_layout()
    pdf.savefig(fig)
    plt.close(fig)


def render_region(pdf: PdfPages, data: dict) -> None:
    rows = data["region_performance"]
    labels = [r["region"] for r in rows]
    revenue = [r["revenue"] for r in rows]

    fig, ax = plt.subplots(figsize=(11.69, 8.27))
    ax.pie(revenue, labels=labels, autopct="%1.1f%%", startangle=140)
    ax.set_title("Region Revenue Share")
    fig.tight_layout()
    pdf.savefig(fig)
    plt.close(fig)


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"找不到 JSON 檔案: {DATA_FILE}")

    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with PdfPages(OUTPUT_FILE) as pdf:
        render_cover(pdf, data)
        render_trend(pdf, data)
        render_channel(pdf, data)
        render_region(pdf, data)

    print(f"PDF 報告已輸出: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
