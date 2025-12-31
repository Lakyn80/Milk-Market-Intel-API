from typing import List, Dict

from app.modules.scraping.providers.factory import get_provider
from app.modules.scraping.normalization import (
    normalize_weight,
    normalize_currency,
)


class ScrapingPipeline:
    def __init__(self) -> None:
        self.provider = get_provider()

    def run(self) -> List[Dict]:
        raw_items = self.provider.fetch_companies()
        normalized_items: List[Dict] = []

        for item in raw_items:
            weight, unit = normalize_weight(
                item.get("weight"),
                item.get("unit"),
            )

            price_value, currency = normalize_currency(
                item.get("price_value"),
                item.get("price_currency"),
            )

            item["weight"] = weight
            item["unit"] = unit
            item["price_value"] = price_value
            item["price_currency"] = currency

            normalized_items.append(item)

        return normalized_items
