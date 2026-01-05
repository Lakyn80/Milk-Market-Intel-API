from __future__ import annotations

import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import quote

import httpx


class OzonRetailProvider:
    """
    Retail provider for Ozon (product benchmark, no company binding).
    Uses public composer JSON endpoint; light retry/throttling to avoid 429.
    """

    SEARCH_URL = "https://www.ozon.ru/api/composer-api.bx/page/json/v2"

    def __init__(self, timeout: float = 20.0) -> None:
        self.timeout = timeout

    def fetch_offers(self, product_query: str, region: str = "Moscow") -> List[Dict]:
        # Nepřed-enkódujeme; httpx se postará o escapování při sestavení URL.
        url_param = f"/search?text={product_query}"
        params = {"url": url_param}
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://www.ozon.ru",
            "Referer": f"https://www.ozon.ru/search/?text={quote(product_query)}",
            "Connection": "keep-alive",
            "X-O3-App-Name": "dweb_browser",
            "X-O3-App-Version": "unknown",
            "X-Ozon-Routing-Mode": "0",
        }

        data: Optional[Dict] = None
        for attempt in (1, 2):
            try:
                with httpx.Client(headers=headers, timeout=self.timeout) as client:
                    resp = client.get(self.SEARCH_URL, params=params)
                    if resp.status_code == 429:
                        if attempt == 1:
                            time.sleep(2.0)
                            continue
                        return []
                    resp.raise_for_status()
                    data = resp.json()
                    break
            except Exception:
                if attempt == 2:
                    return []
                time.sleep(2.0)
                continue

        return self._parse_offers(data or {}, region)

    def _parse_offers(self, payload: Dict, region: str) -> List[Dict]:
        offers: List[Dict] = []
        widget_states = payload.get("widgetStates") or {}

        # widgetStates values jsou stringy s JSONem; vyparsujeme vše, co má "items".
        for raw in widget_states.values():
            parsed = self._safe_loads(raw)
            if not isinstance(parsed, dict):
                continue

            # Kandidáti na list produktů
            candidates = []
            if isinstance(parsed.get("items"), list):
                candidates = parsed["items"]
            elif isinstance(parsed.get("itemsV2"), list):
                candidates = parsed["itemsV2"]
            elif isinstance(parsed.get("products"), list):
                candidates = parsed["products"]

            for item in candidates:
                price_value = self._extract_price(item)
                name = self._extract_name(item)
                if price_value is None or not name:
                    continue

                offers.append(
                    {
                        "company_id": None,
                        "source": "ozon",
                        "product_name": name,
                        "price_value": price_value,
                        "price_currency": "RUB",
                        "region": region,
                        "collected_at": datetime.utcnow(),
                    }
                )

        return offers

    @staticmethod
    def _safe_loads(raw: object) -> Optional[Dict]:
        if not isinstance(raw, str):
            return None
        raw = raw.strip()
        if not raw.startswith("{"):
            return None
        try:
            return json.loads(raw)
        except Exception:
            return None

    @staticmethod
    def _extract_price(item: Dict) -> Optional[float]:
        if not isinstance(item, dict):
            return None

        price_raw = None

        # common placements
        price_block = item.get("price") or item.get("finalPrice") or item.get("priceValue")
        if isinstance(price_block, dict):
            price_raw = (
                price_block.get("price")
                or price_block.get("currentPrice")
                or price_block.get("value")
                or price_block.get("priceValue")
            )
        elif isinstance(price_block, (int, float)):
            price_raw = price_block

        if price_raw is None:
            # Sometimes under "cellTrackingInfo"
            ct = item.get("cellTrackingInfo") if isinstance(item.get("cellTrackingInfo"), dict) else None
            if ct:
                price_raw = ct.get("price") or ct.get("finalPrice")

        if price_raw is None:
            return None

        try:
            return float(price_raw)
        except Exception:
            return None

    @staticmethod
    def _extract_name(item: Dict) -> Optional[str]:
        if not isinstance(item, dict):
            return None
        name = (
            item.get("name")
            or item.get("title")
            or item.get("cellTrackingInfo", {}).get("product_title")
            or item.get("cellTrackingInfo", {}).get("title")
        )
        if name:
            return str(name)
        return None
