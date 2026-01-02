from pathlib import Path
from typing import List, Dict, Tuple

from dotenv import load_dotenv

from app.modules.scraping.providers.factory import get_provider
from app.modules.scraping.normalization import (
    normalize_weight,
    normalize_currency,
)
from app.modules.scraping.filters.dairy_b2b import is_dairy_b2b
from app.modules.scraping.normalization.company_name import canonical_company_name


DOTENV_PATH = Path(__file__).resolve().parents[3] / ".env"
if DOTENV_PATH.exists():
    load_dotenv(DOTENV_PATH, override=True)


class ScrapingPipeline:
    def __init__(self) -> None:
        self.provider = get_provider()

    def run(self) -> List[Dict]:
        raw_items = self.provider.fetch_companies()

        dedup: Dict[Tuple[str, str], Dict] = {}

        for item in raw_items:
            name = item.get("name", "")

            ok, score, reasons = is_dairy_b2b(name)
            if not ok:
                continue

            canonical = canonical_company_name(name)
            key = (canonical, item.get("region", ""))

            weight, unit = normalize_weight(
                item.get("weight"),
                item.get("unit"),
            )
            price_value, currency = normalize_currency(
                item.get("price_value"),
                item.get("price_currency"),
            )

            if key not in dedup:
                item["canonical_name"] = canonical
                item["weight"] = weight
                item["unit"] = unit
                item["price_value"] = price_value
                item["price_currency"] = currency
                item["_score"] = score
                item["_score_reasons"] = reasons
                item["_variants"] = [name]

                dedup[key] = item
            else:
                dedup[key]["_variants"].append(name)

        return list(dedup.values())
