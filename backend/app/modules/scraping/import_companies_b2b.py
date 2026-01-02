from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.modules.scraping.pipeline import ScrapingPipeline
from app.modules.companies.models import Company


def get_or_create_company(
    db: Session,
    *,
    name: str,
    country: str,
    region: str,
    website: str | None,
) -> Company:
    company = (
        db.query(Company)
        .filter(Company.name == name)
        .filter(Company.region == region)
        .first()
    )

    if company:
        # update website if missing
        if website and not company.website:
            company.website = website
        return company

    company = Company(
        name=name,
        country=country,
        region=region,
        website=website,
    )
    db.add(company)
    return company


def main() -> None:
    db = SessionLocal()

    try:
        items = ScrapingPipeline().run()
        inserted = 0

        for item in items:
            company = get_or_create_company(
                db,
                name=item["canonical_name"],
                country=item.get("country"),
                region=item.get("region"),
                website=item.get("website"),
            )

            if company.id is None:
                inserted += 1

        db.commit()

        print(f"B2B companies processed: {len(items)}")
        print(f"New companies inserted: {inserted}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
