from __future__ import annotations

from pathlib import Path
import json

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_FILE = DATA_DIR / "dealer_marketing_data.xlsx"
OUTPUT_FILE = DATA_DIR / "marketing_dashboard.json"


def pct(numerator: float, denominator: float) -> float:
    return 0.0 if denominator == 0 else numerator / denominator


def build_payload(df: pd.DataFrame) -> dict:
    total_spend = float(df["spend"].sum())
    total_revenue = float(df["revenue"].sum())
    total_impressions = float(df["impressions"].sum())
    total_clicks = float(df["clicks"].sum())
    total_leads = float(df["leads"].sum())
    total_orders = float(df["orders"].sum())

    df["date"] = pd.to_datetime(df["date"])
    weekly = (
        df.set_index("date")[["spend", "revenue", "leads", "orders"]]
        .resample("W")
        .sum()
        .reset_index()
    )

    top_campaigns = (
        df.groupby("campaign_name", as_index=False)
        .agg(spend=("spend", "sum"), revenue=("revenue", "sum"), leads=("leads", "sum"), orders=("orders", "sum"))
        .assign(roi=lambda x: (x["revenue"] - x["spend"]) / x["spend"])
        .sort_values("revenue", ascending=False)
        .head(8)
    )

    region_perf = (
        df.groupby("region", as_index=False)
        .agg(spend=("spend", "sum"), revenue=("revenue", "sum"), leads=("leads", "sum"), orders=("orders", "sum"))
        .assign(roi=lambda x: (x["revenue"] - x["spend"]) / x["spend"])
        .sort_values("revenue", ascending=False)
    )

    channel_perf = (
        df.groupby("channel", as_index=False)
        .agg(spend=("spend", "sum"), impressions=("impressions", "sum"), clicks=("clicks", "sum"), leads=("leads", "sum"), orders=("orders", "sum"))
        .assign(
            ctr=lambda x: x["clicks"] / x["impressions"],
            cpl=lambda x: x["spend"] / x["leads"],
            cpa=lambda x: x["spend"] / x["orders"],
        )
        .sort_values("spend", ascending=False)
    )

    payload = {
        "meta": {
            "source_file": str(INPUT_FILE.name),
            "row_count": int(len(df)),
            "date_range": {
                "start": df["date"].min().date().isoformat(),
                "end": df["date"].max().date().isoformat(),
            },
        },
        "kpis": {
            "spend": round(total_spend, 2),
            "revenue": round(total_revenue, 2),
            "profit": round(total_revenue - total_spend, 2),
            "roi": round(pct(total_revenue - total_spend, total_spend), 4),
            "impressions": int(total_impressions),
            "clicks": int(total_clicks),
            "ctr": round(pct(total_clicks, total_impressions), 4),
            "leads": int(total_leads),
            "orders": int(total_orders),
            "lead_rate": round(pct(total_leads, total_clicks), 4),
            "close_rate": round(pct(total_orders, total_leads), 4),
            "cpl": round(pct(total_spend, total_leads), 2),
            "cpa": round(pct(total_spend, total_orders), 2),
        },
        "funnel": {
            "impressions": int(total_impressions),
            "clicks": int(total_clicks),
            "leads": int(total_leads),
            "test_drives": int(df["test_drives"].sum()),
            "orders": int(total_orders),
        },
        "weekly_trend": [
            {
                "week_end": row["date"].date().isoformat(),
                "spend": float(row["spend"]),
                "revenue": float(row["revenue"]),
                "leads": int(row["leads"]),
                "orders": int(row["orders"]),
            }
            for _, row in weekly.iterrows()
        ],
        "top_campaigns": top_campaigns.round(4).to_dict(orient="records"),
        "region_performance": region_perf.round(4).to_dict(orient="records"),
        "channel_performance": channel_perf.round(4).to_dict(orient="records"),
    }
    return payload


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"找不到 Excel 檔案: {INPUT_FILE}")

    df = pd.read_excel(INPUT_FILE)
    payload = build_payload(df)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"JSON 已輸出: {OUTPUT_FILE}")
    print(f"KPI ROI: {payload['kpis']['roi']:.2%}")


if __name__ == "__main__":
    main()
