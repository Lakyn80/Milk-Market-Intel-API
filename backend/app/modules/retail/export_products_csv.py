import csv
from pathlib import Path

from sqlalchemy import select, join

from app.db.session import SessionLocal
from app.modules.retail.writer import retail_offers
from app.modules.retail.parsed_models import retail_products_parsed


EXPORT_PATH = Path(__file__).resolve().parents[2] / "exports" / "retail_products_parsed.csv"


def main() -> None:
    EXPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with SessionLocal() as db:
        j = join(retail_products_parsed, retail_offers, retail_products_parsed.c.retail_offer_id == retail_offers.c.id)
        stmt = select(
            retail_products_parsed.c.id,
            retail_products_parsed.c.retail_offer_id,
            retail_products_parsed.c.raw_name,
            retail_products_parsed.c.brand,
            retail_products_parsed.c.product_type,
            retail_products_parsed.c.flavor,
            retail_products_parsed.c.fat_percent,
            retail_products_parsed.c.package_type,
            retail_products_parsed.c.weight_g,
            retail_products_parsed.c.volume_ml,
            retail_products_parsed.c.region,
            retail_products_parsed.c.source,
            retail_products_parsed.c.parsed_at,
            retail_offers.c.price_value,
            retail_offers.c.price_currency,
        ).select_from(j)

        rows = db.execute(stmt).mappings().all()

    headers = [
        "id",
        "retail_offer_id",
        "raw_name",
        "brand",
        "product_type",
        "flavor",
        "fat_percent",
        "package_type",
        "weight_g",
        "volume_ml",
        "region",
        "source",
        "parsed_at",
        "price_value",
        "price_currency",
    ]

    with EXPORT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({h: row.get(h) for h in headers})

    print(f"Exported {len(rows)} rows -> {EXPORT_PATH}")


if __name__ == "__main__":
    main()
