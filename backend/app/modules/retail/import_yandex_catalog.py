import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List

from sqlalchemy import insert, select

from app.db.session import SessionLocal
from app.modules.retail.writer import retail_offers


DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "yandex_catalog.json"


def load_items(path: Path) -> List[Dict]:
    if not path.exists():
        raise FileNotFoundError(f"Input JSON not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Accept either {"items": [...]} or a raw list.
    if isinstance(data, dict):
        items = data.get("items") or []
    else:
        items = data

    if not isinstance(items, list):
        raise ValueError("Invalid JSON structure: expected a list of items")
    return items


def dedupe_exists(
    db,
    *,
    source: str,
    region: str | None,
    product_name: str,
    price_value: float,
) -> bool:
    stmt = (
        select(retail_offers.c.id)
        .where(
            retail_offers.c.source == source,
            retail_offers.c.region == region,
            retail_offers.c.product_name == product_name,
            retail_offers.c.price_value == price_value,
        )
        .limit(1)
    )
    return db.execute(stmt).scalar_one_or_none() is not None


def import_items(items: Iterable[Dict]) -> Dict[str, int]:
    inserted = 0
    skipped = 0
    total = 0

    with SessionLocal() as db:
        for item in items:
            total += 1

            name = str(item.get("name") or "").strip()
            if not name:
                skipped += 1
                continue

            price_value = item.get("price_value")
            if price_value is None:
                skipped += 1
                continue
            try:
                price_value = float(price_value)
            except Exception:
                skipped += 1
                continue

            source = "yandex_market_catalog"
            price_currency = item.get("price_currency") or "RUB"
            region = str(item.get("region") or "").strip() or None

            if dedupe_exists(
                db,
                source=source,
                region=region,
                product_name=name,
                price_value=price_value,
            ):
                skipped += 1
                continue

            payload = {
                "company_id": None,
                "source": source,
                "source_item_id": item.get("product_id"),
                "region": region,
                "product_name": name,
                "price_value": price_value,
                "price_currency": price_currency,
                "collected_at": datetime.utcnow(),
            }

            db.execute(insert(retail_offers).values(payload))
            inserted += 1

        db.commit()

    return {"total": total, "inserted": inserted, "skipped": skipped}


def main() -> None:
    items = load_items(DATA_PATH)
    stats = import_items(items)
    print(f"Items read: {stats['total']}")
    print(f"Inserted: {stats['inserted']}")
    print(f"Skipped (duplicates by source+region+name+price or missing fields): {stats['skipped']}")


if __name__ == "__main__":
    main()
