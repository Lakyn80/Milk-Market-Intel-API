from typing import List, Dict, Optional

import httpx
from bs4 import BeautifulSoup
from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, select, desc
from sqlalchemy.orm import Session


# Minimal table mapping to read registry status; nezávislé na modelech.
metadata = MetaData()

company_registry = Table(
    "company_registry",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("company_id", Integer, nullable=False),
    Column("source", String),
    Column("status_norm", String),
    Column("fetched_at", DateTime),
)


class YandexMarketRetailProvider:
    """
    Retail ingest provider pro Yandex Market (single-company flow).
    - Neprovádí zápis do DB.
    - Vrací list normalizovaných nabídek.
    - Respektuje status firmy (ACTIVE) podle company_registry (source=rusprofile) pokud company_id není None.
    """

    BASE_URL = "https://m.market.yandex.ru/search"

    def _is_active(self, db: Session, company_id: int) -> bool:
        stmt = (
            select(company_registry.c.status_norm)
            .where(
                company_registry.c.company_id == company_id,
                company_registry.c.source == "rusprofile",
            )
            .order_by(desc(company_registry.c.fetched_at))
            .limit(1)
        )
        row = db.execute(stmt).scalar_one_or_none()
        return row == "ACTIVE"

    def fetch_offers(
        self,
        db: Session,
        company_id: Optional[int],
        company_name: str,
        region: Optional[str] = None,
    ) -> List[Dict]:
        # 1) Gate podle registry statusu
        if company_id is not None and not self._is_active(db, company_id):
            return []

        params = {
            "text": company_name,
        }
        if region:
            params["lr"] = region  # Yandex region code

        headers = {
            # Mobile UA, aby m.market nevracelo redirect na desktop
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 10; Mobile) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0 Mobile Safari/537.36"
            )
        }

        with httpx.Client(headers=headers, timeout=15.0, follow_redirects=True) as client:
            resp = client.get(self.BASE_URL, params=params)
            resp.raise_for_status()
            html = resp.text

        offers = self._parse_ssr_json(html, region or "Moscow")
        return offers

    def _parse_ssr_json(self, html: str, region: str) -> List[Dict]:
        soup = BeautifulSoup(html, "html.parser")
        scripts = soup.find_all("script")

        candidates = []
        for s in scripts:
            content = s.string or ""
            if not content:
                continue
            if any(key in content for key in ("__INITIAL_STATE__", "__NEXT_DATA__", "apiaryState", "search", "offers", "price")):
                candidates.append(content)

        for content in candidates:
            data = self._extract_json(content)
            if not data:
                continue
            offers = self._extract_offers_from_state(data, region)
            if offers:
                return offers

        return []

    def _extract_json(self, content: str) -> Optional[Dict]:
        import json
        import re

        # Hledej explicitní přiřazení JSONu: window.__INITIAL_STATE__ = {...};
        patterns = [
            r"__INITIAL_STATE__\s*=\s*(\{.*?\});",
            r"__NEXT_DATA__\s*=\s*(\{.*?\});",
            r"apiaryState\s*=\s*(\{.*?\});",
            r"window.state\s*=\s*(\{.*?\});",
            r"(\{.*\})",
        ]
        for pat in patterns:
            m = re.search(pat, content, flags=re.DOTALL)
            if not m:
                continue
            snippet = m.group(1)
            try:
                return json.loads(snippet)
            except Exception:
                continue
        return None

    def _extract_offers_from_state(self, state: Dict, region: str) -> List[Dict]:
        offers: List[Dict] = []

        def walk(obj):
            if isinstance(obj, dict):
                # hledáme struktury s cenou a názvem
                name = obj.get("name") or obj.get("title")
                price = obj.get("price") or obj.get("cpaPrice") or obj.get("rawPrice")
                market_sku = obj.get("marketSku") or obj.get("sku") or obj.get("id")

                if name and price:
                    val = self._extract_price_value(price)
                    if val is not None:
                        offers.append(
                            {
                                "source": "yandex_market",
                                "source_item_id": str(market_sku) if market_sku else None,
                                "region": region,
                                "product_name": str(name),
                                "price_value": val,
                                "price_currency": "RUB",
                            }
                        )

                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for v in obj:
                    walk(v)

        walk(state)
        return offers

    @staticmethod
    def _extract_price_value(price_obj) -> Optional[float]:
        import re

        if isinstance(price_obj, (int, float)):
            return float(price_obj)
        if isinstance(price_obj, str):
            digits = re.findall(r"[\d]+", price_obj.replace(",", "."))
            if not digits:
                return None
            try:
                return float("".join(digits))
            except ValueError:
                return None
        if isinstance(price_obj, dict):
            val = price_obj.get("value") or price_obj.get("amount") or price_obj.get("rawValue")
            if isinstance(val, (int, float)):
                return float(val)
            if isinstance(val, str):
                digits = re.findall(r"[\d]+", val.replace(",", "."))
                if not digits:
                    return None
                try:
                    return float("".join(digits))
                except ValueError:
                    return None
        return None
