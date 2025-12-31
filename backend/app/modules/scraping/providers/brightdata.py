import os
import time
from typing import Iterable, Dict, Any
from app.modules.scraping.providers.provider_base import ProviderBase


class BrightDataProvider(ProviderBase):
    def __init__(self):
        self.api_key = os.getenv("BRIGHTDATA_API_KEY")
        self.country = os.getenv("BRIGHTDATA_COUNTRY", "RU")
        self.rate_limit = int(os.getenv("BRIGHTDATA_RATE_LIMIT", "1"))
        self.timeout = int(os.getenv("BRIGHTDATA_TIMEOUT", "30"))

    def search_companies(self, query: str) -> Iterable[Dict[str, Any]]:
        if not self.api_key:
            raise RuntimeError("BRIGHTDATA_API_KEY is not set")

        # RATE LIMIT (requests per second)
        time.sleep(1 / max(self.rate_limit, 1))

        # TODO: reálné Bright Data volání (Yandex / 2GIS)
        # ZATÍM návrat struktury
        return [
            {
                "name": "Молочный комбинат Реальный",
                "country": self.country,
                "region": "Москва",
                "source": "brightdata",
                "raw": {"query": query},
            }
        ]
