import csv
from pathlib import Path

from sqlalchemy import select

from app.db.session import SessionLocal
from app.modules.analytics.models import market_snapshot

EXPORT_PATH = Path(__file__).resolve().parents[2] / "data" / "market_snapshot.csv"


def main() -> None:
    EXPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with SessionLocal() as db:
        rows = db.execute(select(market_snapshot)).mappings().all()

    headers = [
        "id",
        "product_name",
        "brand_name",
        "category",
        "price_value",
        "price_currency",
        "region",
        "region_code",
        "companies_count_region",
        "collected_at",
    ]

    with EXPORT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({h: row.get(h) for h in headers})

    print(f"Exported {len(rows)} rows -> {EXPORT_PATH}")


if __name__ == "__main__":
    main()
