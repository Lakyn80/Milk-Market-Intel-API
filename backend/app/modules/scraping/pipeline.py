from typing import Iterable, Dict, Any
from app.modules.scraping.providers.provider_base import ProviderBase


class ScrapingPipeline:
    def __init__(self, provider: ProviderBase):
        self.provider = provider

    def find_companies(self, query: str) -> Iterable[Dict[str, Any]]:
        return self.provider.search_companies(query)
