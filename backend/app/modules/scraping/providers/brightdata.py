from typing import Iterable, Dict, Any
from app.modules.scraping.providers.provider_base import ProviderBase


class BrightDataProvider(ProviderBase):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def search_companies(self, query: str) -> Iterable[Dict[str, Any]]:
        # TODO: implement Bright Data API call
        # for now return mock structure
        return [
            {
                "name": "???????? ???????? ??????",
                "country": "RU",
                "region": "?????????? ???????",
                "source": "brightdata",
                "raw": {"query": query},
            }
        ]
