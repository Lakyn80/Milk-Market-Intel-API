from typing import List, Dict, Optional

import random
import time

import httpx

WB_SEARCH_URL = "https://search.wb.ru/exactmatch/ru/common/v4/search"


class WildberriesRetailProvider:
    """
    Retail provider for Wildberries (product benchmark, no company binding).
    Uses public JSON search endpoint with light throttling to ease rate limits.
    """

    @staticmethod
    def _sleep_with_jitter(base: float) -> None:
        time.sleep(base + random.uniform(0.3, 0.8))

    def fetch_offers(self, product_query: str, region: str = "Moscow") -> List[Dict]:
        params = {
            "query": product_query,
            "page": 1,  # WB pagination starts at 1
            "appType": 1,
            "curr": "rub",
            "dest": "-1257786",  # Moscow destination code
            "sort": "popular",
            "resultset": "catalog",
            "spp": "0",
            "locale": "ru",
            "ucl": "1",
            "regions": "68,64,4,38,30,33,70,86,75,31,1,22,66,110,48,80",
            "stores": "117673,122258,507,3158,117501,120602,6159,2737",
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://www.wildberries.ru",
            "Referer": f"https://www.wildberries.ru/catalog?searchText={product_query}",
            "Host": "search.wb.ru",
            "Connection": "keep-alive",
            "X-Requested-With": "XMLHttpRequest",
        }

        data = None
        for attempt in (1, 2):  # single retry for 429/temporary failures
            try:
                with httpx.Client(headers=headers, timeout=20.0) as client:
                    resp = client.get(WB_SEARCH_URL, params=params)
                    if resp.status_code == 429:
                        if attempt == 1:
                            self._sleep_with_jitter(5.0)
                            continue
                        return []
                    resp.raise_for_status()
                    data = resp.json()
                    break
            except Exception:
                if attempt == 2:
                    return []
                self._sleep_with_jitter(5.0)
                continue

        products = (data.get("data") or {}).get("products") or []
        offers: List[Dict] = []

        for p in products:
            price_raw: Optional[int] = p.get("salePriceU") or p.get("priceU")
            name = p.get("name")
            item_id = p.get("id")

            if not price_raw or not name or not item_id:
                continue

            price_value = float(price_raw) / 100.0

            offers.append(
                {
                    "source": "wildberries",
                    "source_item_id": str(item_id),
                    "region": region,
                    "product_name": str(name),
                    "price_value": price_value,
                    "price_currency": "RUB",
                }
            )

        return offers
