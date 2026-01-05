import json
import logging
import time
from pathlib import Path
from typing import List, Dict

from app.db.session import SessionLocal
from app.modules.retail.providers.wildberries import WildberriesRetailProvider
from app.modules.retail.writer import write_retail_offers

logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "retail_queries_ru.json"


def load_queries() -> List[str]:
    with DATA_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    queries = data.get("queries", [])
    # Omezení na prvních 5 dotazů kvůli rate-limitům.
    return queries[:5]


def fetch_for_query(provider: WildberriesRetailProvider, query: str) -> List[Dict]:
    try:
        return provider.fetch_offers(product_query=query, region="Moscow")
    except Exception as exc:  # pragma: no cover - runtime guard
        logger.warning("Failed to fetch offers for query=%s: %s", query, exc)
        return []


def main() -> None:
    queries = load_queries()
    provider = WildberriesRetailProvider()

    with SessionLocal() as db:
        all_offers: List[Dict] = []

        for q in queries:
            offers = fetch_for_query(provider, q)
            if offers:
                for o in offers:
                    o["company_id"] = None
                    if not o.get("region"):
                        o["region"] = "Moscow"
                all_offers.extend(offers)
            # Softer pacing to reduce 429 responses.
            time.sleep(5.0)

        if all_offers:
            write_retail_offers(db, all_offers)
            db.commit()
            print(f"Inserted offers: {len(all_offers)}")
        else:
            print("No offers collected.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
