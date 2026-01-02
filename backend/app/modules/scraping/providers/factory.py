import os

from app.modules.scraping.providers.local import LocalProvider
from app.modules.scraping.providers.two_gis import TwoGisProvider


def get_provider():
    provider = os.environ.get("SCRAPING_PROVIDER", "local").lower()

    if provider == "2gis":
        return TwoGisProvider()

    return LocalProvider()
