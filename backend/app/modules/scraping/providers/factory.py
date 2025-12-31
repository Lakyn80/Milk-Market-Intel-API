import os

from app.modules.scraping.providers.provider_base import ProviderBase
from app.modules.scraping.providers.local import LocalProvider
from app.modules.scraping.providers.brightdata import BrightDataProvider


def get_provider() -> ProviderBase:
    provider = os.getenv("SCRAPING_PROVIDER", "local").lower()

    if provider == "brightdata":
        return BrightDataProvider()

    return LocalProvider()
