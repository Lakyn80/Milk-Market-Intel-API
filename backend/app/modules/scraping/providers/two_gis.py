import os
from typing import Any, Dict, List, Optional

import httpx

from app.modules.scraping.providers.provider_base import ProviderBase


CATALOG_ITEMS_URL = "https://catalog.api.2gis.com/3.0/items"


def _get_first_website(item: Dict[str, Any]) -> Optional[str]:
    for cg in item.get("contact_groups", []) or []:
        for c in cg.get("contacts", []) or []:
            if (c.get("type") or "").lower() == "website":
                values = c.get("value")
                if isinstance(values, list) and values:
                    return str(values[0])
                if isinstance(values, str) and values:
                    return values
    return None


class TwoGisProvider(ProviderBase):
    """
    2GIS Places API provider (B2B discovery).
    Docs: https://docs.2gis.com/en/api/search/places/overview
    """

    def __init__(self) -> None:
        self.api_key = os.environ.get("TWO_GIS_API_KEY", "").strip()
        self.country = os.environ.get("TWO_GIS_COUNTRY", "RU").strip()
        self.region = os.environ.get("TWO_GIS_REGION", "Moscow").strip()

        self.point = os.environ.get("TWO_GIS_POINT", "").strip()
        self.radius = int(os.environ.get("TWO_GIS_RADIUS", "40000"))
        self.query = os.environ.get("TWO_GIS_QUERY", "завод").strip()

        raw_page_size = int(os.environ.get("TWO_GIS_PAGE_SIZE", "10"))
        self.page_size = min(raw_page_size, 10)
        self.max_results = int(os.environ.get("TWO_GIS_MAX_RESULTS", "50"))
        self.timeout = float(os.environ.get("TWO_GIS_TIMEOUT", "20"))

    def search_companies(self, query: str) -> List[Dict]:
        return self.fetch_companies()

    def fetch_companies(self) -> List[Dict]:
        if not self.api_key:
            raise RuntimeError("TWO_GIS_API_KEY is not set")
        if not self.point:
            raise RuntimeError("TWO_GIS_POINT is not set (expected 'lon,lat')")

        results: List[Dict] = []
        page = 1

        with httpx.Client(
            timeout=self.timeout,
            headers={"User-Agent": "milk-market-intel/1.0"},
        ) as client:
            while len(results) < self.max_results:
                params = {
                    "key": self.api_key,
                    "q": self.query,
                    "point": self.point,
                    "radius": self.radius,
                    "page": page,
                    "page_size": self.page_size,
                    "type": "branch",
                }

                resp = client.get(CATALOG_ITEMS_URL, params=params)

                # === HTTP-LEVEL ===
                if resp.status_code == 404:
                    break

                if resp.status_code != 200:
                    raise RuntimeError(
                        f"2GIS HTTP error ({resp.status_code}): {resp.text}"
                    )

                data = resp.json()

                # === META-LEVEL ===
                meta = data.get("meta") or {}
                code = meta.get("code")

                if code == 404:
                    # 2GIS: Results not found → konec dat
                    break

                if meta.get("error"):
                    message = meta["error"].get("message") or "Unknown 2GIS error"
                    raise RuntimeError(f"2GIS API error ({code}): {message}")

                items = (data.get("result") or {}).get("items") or []
                if not items:
                    break

                for it in items:
                    name = it.get("name")
                    if not name:
                        continue

                    website = _get_first_website(it)

                    results.append(
                        {
                            "name": str(name),
                            "country": self.country,
                            "region": self.region,
                            "website": website,
                            "price_value": None,
                            "price_currency": None,
                        }
                    )

                    if len(results) >= self.max_results:
                        break

                page += 1

        return results
