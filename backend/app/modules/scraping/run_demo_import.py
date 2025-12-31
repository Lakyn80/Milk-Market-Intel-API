from datetime import datetime

from app.db.base import Base
from app.db.session import engine, SessionLocal
import app.db.models  # noqa

from app.modules.scraping.pipeline import ScrapingPipeline
from app.modules.scraping.providers.brightdata import BrightDataProvider
from app.modules.scraping.service import ScrapingService

from app.modules.companies.brand_models import Brand
from app.modules.companies.product_models import Product
from app.modules.companies.price_models import Price


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1) Scraping pipeline (stub provider)
        provider = BrightDataProvider(api_key=None)
        pipeline = ScrapingPipeline(provider)
        service = ScrapingService(pipeline, db)

        imported = service.import_companies("молочный комбинат")
        print(f"Companies imported: {imported}")

        # 2) Demo B2C data
        company = db.query(Brand).join(Brand.company).first().company

        brand = Brand(name="Пример Молоко", company_id=company.id)
        db.add(brand)
        db.commit()
        db.refresh(brand)

        product = Product(
            name="Молоко пастеризованное 3.2%",
            volume_liters=1.0,
            fat_percent=3.2,
            brand_id=brand.id,
        )
        db.add(product)
        db.commit()
        db.refresh(product)

        prices = [
            {"value": 109.90, "currency": "RUB", "source": "ozon", "region": "Москва"},
            {"value": 104.50, "currency": "RUB", "source": "wildberries", "region": "Москва"},
            {"value": 99.90, "currency": "RUB", "source": "magnit", "region": "Москва"},
        ]

        for p in prices:
            db.add(
                Price(
                    value=float(p["value"]),
                    currency=p.get("currency", "RUB"),
                    source=p["source"],
                    region=p.get("region"),
                    scraped_at=datetime.utcnow(),
                    product_id=product.id,
                )
            )

        db.commit()
        print("OK: pipeline to DB complete")

    finally:
        db.close()


if __name__ == "__main__":
    main()
