from app.modules.scraping.providers.provider_base import ProviderBase


class LocalProvider(ProviderBase):
    def search_companies(self) -> list[dict]:
        return [
            {
                "name": "Demo Company",
                "country": "RU",
                "region": "Moscow",
                "website": "https://example.com",
            }
        ]

    def fetch_companies(self) -> list[dict]:
        return self.search_companies()
