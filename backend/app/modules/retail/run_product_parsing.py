import logging
from datetime import datetime
from typing import Dict, List

from sqlalchemy import select, insert

from app.db.session import SessionLocal
from app.modules.retail.writer import retail_offers
from app.modules.retail.parsers.product_name_parser import parse_product_name
from app.modules.retail.parsed_models import retail_products_parsed


logger = logging.getLogger(__name__)


def fetch_existing_offer_ids(db) -> set[int]:
    stmt = select(retail_products_parsed.c.retail_offer_id)
    return set(db.execute(stmt).scalars().all())


def fetch_offers(db) -> List[Dict]:
    stmt = select(retail_offers)
    rows = db.execute(stmt).mappings().all()
    return rows


def main() -> None:
    inserted = 0
    skipped = 0
    total = 0

    with SessionLocal() as db:
        existing_ids = fetch_existing_offer_ids(db)
        offers = fetch_offers(db)

        for row in offers:
            total += 1
            offer_id = row.get("id")
            if offer_id in existing_ids:
                skipped += 1
                continue

            name = row.get("product_name") or ""
            parsed = parse_product_name(name)

            payload = {
                "retail_offer_id": offer_id,
                "raw_name": parsed.get("raw_name"),
                "brand": parsed.get("brand"),
                "product_type": parsed.get("product_type"),
                "flavor": parsed.get("flavor"),
                "fat_percent": parsed.get("fat_percent"),
                "package_type": parsed.get("package_type"),
                "weight_g": parsed.get("weight_g"),
                "volume_ml": parsed.get("volume_ml"),
                "region": row.get("region"),
                "source": row.get("source"),
                "parsed_at": datetime.utcnow(),
            }

            db.execute(insert(retail_products_parsed).values(payload))
            inserted += 1

        db.commit()

    print(f"Offers processed: {total}")
    print(f"Inserted parsed rows: {inserted}")
    print(f"Skipped (already parsed): {skipped}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
