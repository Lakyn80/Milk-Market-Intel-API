from sqlalchemy.orm import Session
from app.modules.scraping.pipeline import ScrapingPipeline
from app.modules.companies.repository import CompanyRepository


class ScrapingService:
    def __init__(self, pipeline: ScrapingPipeline, db: Session):
        self.pipeline = pipeline
        self.repo = CompanyRepository(db)

    def import_companies(self, query: str) -> int:
        count = 0
        for item in self.pipeline.find_companies(query):
            if not self.repo.get_by_name(item["name"]):
                self.repo.create(
                    name=item["name"],
                    country=item.get("country", "RU"),
                    region=item.get("region"),
                    website=item.get("website"),
                )
                count += 1
        return count
