from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import SessionLocal
from app.modules.scraping.pipeline import ScrapingPipeline
from app.modules.companies.models import (
    Company,
    Brand,
    Product,
    Price,
)


def get_or_create_company(
    db: Session,
    name: str,
    country: str | None,
    region: str | None,
    website: str | None,
) -> Company:
    company = db.query(Company).filter_by(name=name).first()
    if company:
        return company

    company = Company(
        name=name,
        country=country or "RU",
        region=region,
        website=website,
    )
    db.add(company)
    db.flush()
    return company


def get_or_create_brand(db: Session, name: str, company: Company) -> Brand:
    brand = (
        db.query(Brand)
        .filter_by(name=name, company_id=company.id)
        .first()
    )
    if brand:
        return brand

    brand = Brand(
        name=name,
        company_id=company.id,
    )
    db.add(brand)
    db.flush()
    return brand


def get_or_create_product(
    db: Session,
    name: str,
    brand: Brand,
    volume_liters: float | None,
    fat_percent: float | None,
) -> Product:
    product = (
        db.query(Product)
        .filter_by(name=name, brand_id=brand.id)
        .first()
    )
    if product:
        return product

    product = Product(
        name=name,
        brand_id=brand.id,
        volume_liters=volume_liters,
        fat_percent=fat_percent,
    )
    db.add(product)
    db.flush()
    return product


def main() -> None:
    db: Session = SessionLocal()

    try:
        items = ScrapingPipeline().run()

        for item in items:
            company = get_or_create_company(
                db,
                name=item["name"],
                country=item.get("country"),
                region=item.get("region"),
                website=item.get("website"),
            )

            brand = get_or_create_brand(
                db,
                name=item.get("brand", company.name),
                company=company,
            )

            product = get_or_create_product(
                db,
                name=item.get("product_name", "UNKNOWN_PRODUCT"),
                brand=brand,
                volume_liters=item.get("volume_liters"),
                fat_percent=item.get("fat_percent"),
            )

            if item.get("price_value") is not None:
                price = Price(
                    product_id=product.id,
                    value=item["price_value"],
                    currency=item.get("price_currency", "RUB"),
                    source=item.get("market", "local"),
                    region=item.get("region"),
                    scraped_at=datetime.utcnow(),
                )
                db.add(price)

        db.commit()
        print("IMPORT OK")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
