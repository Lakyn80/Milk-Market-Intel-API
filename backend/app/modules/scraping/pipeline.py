from app.modules.scraping.providers.factory import get_provider


class ScrapingPipeline:
    def __init__(self):
        self.provider = get_provider()

    def run(self) -> list[dict]:
        companies = self.provider.fetch_companies()
        return companies
