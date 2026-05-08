from __future__ import annotations

from pathlib import Path
import random

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_FILE = DATA_DIR / "dealer_marketing_data.xlsx"


def generate_rows(seed: int = 42, row_count: int = 180) -> list[dict]:
    random.seed(seed)

    dealers = ["北都車業", "中台汽車", "南方車坊", "東海車行", "西城汽車"]
    channels = ["Google Ads", "Facebook", "Line OA", "YouTube", "SEO"]
    car_models = ["Sedan X", "SUV Pro", "EV Lite", "Pickup Max", "City Mini"]
    regions = ["Taipei", "Taichung", "Kaohsiung", "Tainan", "Taoyuan"]

    rows: list[dict] = []
    start_date = pd.Timestamp("2025-01-01")

    for _ in range(row_count):
        date = start_date + pd.Timedelta(days=random.randint(0, 364))
        spend = random.randint(18_000, 160_000)
        impressions = random.randint(8_000, 85_000)
        ctr = random.uniform(0.006, 0.03)
        clicks = int(impressions * ctr)
        cvr = random.uniform(0.02, 0.09)
        leads = max(1, int(clicks * cvr))
        test_drives = max(0, int(leads * random.uniform(0.25, 0.65)))
        orders = max(0, int(test_drives * random.uniform(0.18, 0.45)))
        # Use attributed gross profit instead of full car price to keep ROI realistic.
        revenue = orders * random.randint(45_000, 180_000)

        rows.append(
            {
                "date": date.date().isoformat(),
                "dealer_name": random.choice(dealers),
                "region": random.choice(regions),
                "channel": random.choice(channels),
                "campaign_name": f"{random.choice(car_models)}-{random.choice(['春季', '夏日', '秋季', '年終'])}主打",
                "spend": spend,
                "impressions": impressions,
                "clicks": clicks,
                "leads": leads,
                "test_drives": test_drives,
                "orders": orders,
                "revenue": revenue,
            }
        )

    return rows


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(generate_rows())
    df = df.sort_values("date").reset_index(drop=True)
    df.to_excel(OUTPUT_FILE, index=False)

    print(f"Excel 已生成: {OUTPUT_FILE}")
    print(f"資料筆數: {len(df)}")


if __name__ == "__main__":
    main()
