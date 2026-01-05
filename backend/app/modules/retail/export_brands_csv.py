import csv
from pathlib import Path

from sqlalchemy import select

from app.db.session import SessionLocal
from app.modules.retail.brand_models import brands_raw


EXPORT_PATH = Path(__file__).resolve().parents[2] / "exports" / "brands_raw.csv"


def main() -> None:
    EXPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with SessionLocal() as db:
        stmt = select(
            brands_raw.c.brand_name,
            brands_raw.c.confidence,
            brands_raw.c.extraction_method,
            brands_raw.c.region,
            brands_raw.c.example_product,
            brands_raw.c.source,
        )
        rows = db.execute(stmt).mappings().all()

    headers = [
        "brand_name",
        "confidence",
        "extraction_method",
        "region",
        "example_product",
        "source",
    ]

    with EXPORT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({h: row.get(h) for h in headers})

    print(f"Exported {len(rows)} rows -> {EXPORT_PATH}")


if __name__ == "__main__":
    main()
