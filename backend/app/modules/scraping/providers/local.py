from app.modules.scraping.providers.provider_base import ProviderBase


class LocalProvider(ProviderBase):
    def fetch_companies(self) -> list[dict]:
        return [
            {
                "name": "Demo Milk Company",
                "country": "RU",
                "region": "Moscow",
                "website": "https://example.com",
            }
        ]
