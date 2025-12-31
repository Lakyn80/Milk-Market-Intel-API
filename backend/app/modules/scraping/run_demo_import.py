from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.modules.scraping.pipeline import ScrapingPipeline
from app.modules.companies.models import Company


def main() -> None:
    db: Session = SessionLocal()

    try:
        pipeline = ScrapingPipeline()
        companies_data = pipeline.run()

        inserted = 0

        for data in companies_data:
            company = Company(
                name=data["name"],
                country=data.get("country"),
                region=data.get("region"),
                website=data.get("website"),
            )
            db.add(company)
            inserted += 1

        db.commit()

        print(f"Companies imported: {inserted}")
        print("OK: pipeline to DB complete")

    finally:
        db.close()


if __name__ == "__main__":
    main()
