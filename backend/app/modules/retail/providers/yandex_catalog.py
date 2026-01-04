from __future__ import annotations

import json
import random
import time
import uuid
from typing import Dict, List, Optional
from urllib.parse import parse_qs, urlparse

import httpx
from bs4 import BeautifulSoup


class YandexMarketCatalogProvider:
    """
    Lightweight scraper for Yandex Market catalog listing pages.

    - Works without auth by parsing server-side JSON patches embedded
      inside `data-zone-name="productSnippet"` blocks.
    - Designed for category pages (e.g. https://market.yandex.ru/catalog--molochnye-produkty/54650/list?hid=91308).
    - Returns product identity + price; brand/manufacturer are not always present
      in the snippet JSON, so they may be None.
    """

    def __init__(self, *, region: Optional[str] = "213", timeout: float = 20.0) -> None:
        self.region = region
        self.timeout = timeout

    def _build_headers(self) -> Dict[str, str]:
        # Desktop UA keeps layout stable; add Accept-Language to reduce captcha risk.
        return {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Referer": "https://market.yandex.ru/",
        }

    def _make_client(self) -> httpx.Client:
        # Fresh yandexuid per session slightly lowers block rate.
        cookies = {"yandexuid": str(uuid.uuid4().int)[:19]}
        return httpx.Client(
            headers=self._build_headers(),
            timeout=self.timeout,
            follow_redirects=True,
            cookies=cookies,
        )

    @staticmethod
    def _parse_price(price_obj: Optional[Dict]) -> Optional[float]:
        if not isinstance(price_obj, dict):
            return None
        raw = price_obj.get("value") or price_obj.get("amount")
        if raw is None:
            return None
        try:
            # Values sometimes come as strings with spaces.
            return float(str(raw).replace(" ", "").replace(",", "."))
        except Exception:
            return None

    def _extract_products_from_html(self, html: str, category: str) -> List[Dict]:
        soup = BeautifulSoup(html, "html.parser")
        snippets = soup.find_all(attrs={"data-zone-name": "productSnippet"})

        products: List[Dict] = []

        for snip in snippets:
            product: Dict[str, Optional[str | float]] = {
                "source": "yandex_market_catalog",
                "category": category,
                "product_id": None,
                "sku_id": None,
                "offer_id": None,
                "name": None,
                "brand": None,
                "price_value": None,
                "price_currency": None,
            }

            for nf in snip.find_all("noframes"):
                try:
                    data = json.loads(nf.get_text(strip=False))
                except Exception:
                    continue

                for widget_payload in (data.get("widgets") or {}).values():
                    if not isinstance(widget_payload, dict):
                        continue
                    # Each widget payload is a dict keyed by a dynamic path.
                    inner = next(iter(widget_payload.values()), {})
                    if not isinstance(inner, dict):
                        continue

                    if inner.get("productId") and not product["product_id"]:
                        product["product_id"] = str(inner.get("productId"))
                    if inner.get("skuId") and not product["sku_id"]:
                        product["sku_id"] = str(inner.get("skuId"))
                    if inner.get("offerId") and not product["offer_id"]:
                        product["offer_id"] = str(inner.get("offerId"))
                    if inner.get("title") and not product["name"]:
                        product["name"] = str(inner.get("title"))

                    # Vendor/brand fields appear sporadically.
                    for key in ("brand", "vendorName", "vendor", "manufacturer"):
                        if inner.get(key) and not product["brand"]:
                            product["brand"] = str(inner.get(key))

                    if inner.get("price") and product["price_value"] is None:
                        price_val = self._parse_price(inner.get("price"))
                        if price_val is not None:
                            product["price_value"] = price_val
                            product["price_currency"] = str(
                                inner.get("price", {}).get("currency") or "RUB"
                            ).replace("RUR", "RUB")

            if product["name"]:
                products.append(product)

        return products

    def fetch_category(
        self,
        category_url: str,
        *,
        page_limit: Optional[int] = 1,
        page_start: int = 1,
        throttle_seconds: float = 1.0,
        region_lr: Optional[str] = None,
        per_page_callback=None,
    ) -> List[Dict]:
        """
        Scrape products from a Yandex Market category listing.

        Args:
            category_url: Full URL of the category listing (hid param recommended).
            page_limit: Max number of pages to walk.
            page_start: Starting page index (1-based).
            throttle_seconds: Sleep between page fetches to reduce rate-limit risk.
            per_page_callback: Optional callable(list[dict]) invoked after each page.
        """
        # Keep hid (if present) to avoid losing category context when appending params.
        parsed = urlparse(category_url)
        base_query = parse_qs(parsed.query)

        results: List[Dict] = []

        with self._make_client() as client:
            page = page_start
            while True:
                params = {**base_query, "page": page}
                effective_lr = region_lr or self.region
                if effective_lr:
                    params["lr"] = effective_lr

                resp = client.get(category_url, params=params)
                if resp.status_code != 200:
                    break

                products = self._extract_products_from_html(
                    resp.text,
                    category=category_url,
                )
                if not products:
                    break

                if callable(per_page_callback):
                    try:
                        per_page_callback(products)
                    except Exception:
                        # Ignore callback errors to keep scraping running.
                        pass

                results.extend(products)

                # Stop if we reached configured page_limit (None/<=0 means "all pages until empty").
                if page_limit is not None and page_limit > 0 and page - page_start + 1 >= page_limit:
                    break

                page += 1
                if throttle_seconds > 0:
                    time.sleep(throttle_seconds + random.uniform(0, 0.3))

        return results
