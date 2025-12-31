from typing import List, Dict

from app.modules.scraping.providers.provider_base import ProviderBase


class RegistryProvider(ProviderBase):
    """
    Registry provider – B2B výrobci (skeleton).
    Zatím vrací hardcoded data pro ověření pipeline.
    """

    def fetch_companies(self) -> List[Dict]:
        return [
            {
                "name": "Тестовый молочный завод",
                "country": "RU",
                "region": "Moscow",
                "website": None,
                "price_value": None,
                "price_currency": None,
            }
        ]

    def search_companies(self, query: str) -> List[Dict]:
        # Pro skeleton ignorujeme query a vracíme totéž
        return self.fetch_companies()
