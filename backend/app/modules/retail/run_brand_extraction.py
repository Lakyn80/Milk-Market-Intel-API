import logging
from datetime import datetime
from typing import Dict, List

from sqlalchemy import select, insert

from app.db.session import SessionLocal
from app.modules.retail.brand_models import brands_raw
from app.modules.retail.parsed_models import retail_products_parsed
from app.modules.retail.brand_extraction import choose_brand

logger = logging.getLogger(__name__)


def fetch_existing(db) -> set[tuple[str, str]]:
    stmt = select(brands_raw.c.brand_name, brands_raw.c.region)
    return set((row[0], row[1]) for row in db.execute(stmt).all())


def fetch_parsed(db) -> List[Dict]:
    stmt = select(
        retail_products_parsed.c.id,
        retail_products_parsed.c.raw_name,
        retail_products_parsed.c.brand,
        retail_products_parsed.c.product_type,
        retail_products_parsed.c.region,
        retail_products_parsed.c.source,
    )
    return db.execute(stmt).mappings().all()


def main() -> None:
    inserted = 0
    skipped = 0
    total = 0

    with SessionLocal() as db:
        existing = fetch_existing(db)
        rows = fetch_parsed(db)

        for row in rows:
            total += 1
            raw_name = row.get("raw_name") or ""
            product_type = row.get("product_type")
            region = row.get("region")
            source = row.get("source") or "yandex_market"
            parsed_brand = row.get("brand")

            brand_info = choose_brand(parsed_brand, raw_name, product_type)
            brand_name = brand_info.get("brand_name")
            if not brand_name:
                skipped += 1
                continue

            key = (brand_name, region)
            if key in existing:
                skipped += 1
                continue

            payload = {
                "brand_name": brand_name,
                "source": source,
                "extraction_method": brand_info.get("extraction_method"),
                "confidence": brand_info.get("confidence"),
                "example_product": raw_name,
                "region": region,
                "created_at": datetime.utcnow(),
            }

            db.execute(insert(brands_raw).values(payload))
            existing.add(key)
            inserted += 1

        db.commit()

    print(f"Parsed products processed: {total}")
    print(f"Inserted brands: {inserted}")
    print(f"Skipped (existing/no brand): {skipped}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
