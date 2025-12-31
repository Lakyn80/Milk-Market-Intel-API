from datetime import datetime

from app.db.base import Base
from app.db.session import engine, SessionLocal

# zaregistruje modely (Company/Brand/Product/Price)
import app.db.models  # noqa: F401

from app.modules.companies.models import Company
from app.modules.companies.brand_models import Brand
from app.modules.companies.product_models import Product
from app.modules.companies.price_models import Price


def main() -> None:
    # vytvoø tabulky pokud nejsou
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 1) Company (B2B výrobce)
        company_name = "??? ???????? ???????? ??????"
        company = db.query(Company).filter(Company.name == company_name).first()
        if not company:
            company = Company(
                name=company_name,
                country="RU",
                region="?????????? ???????",
                website=None,
            )
            db.add(company)
            db.commit()
            db.refresh(company)

        # 2) Brand (znaèka)
        brand_name = "?????? ??????"
        brand = (
            db.query(Brand)
            .filter(Brand.company_id == company.id, Brand.name == brand_name)
            .first()
        )
        if not brand:
            brand = Brand(name=brand_name, company_id=company.id)
            db.add(brand)
            db.commit()
            db.refresh(brand)

        # 3) Product (konkrétní mléko)
        product_name = "?????? ??????????????? 3.2%"
        product = (
            db.query(Product)
            .filter(Product.brand_id == brand.id, Product.name == product_name)
            .first()
        )
        if not product:
            product = Product(
                name=product_name,
                volume_liters=1.0,
                fat_percent=3.2,
                brand_id=brand.id,
            )
            db.add(product)
            db.commit()
            db.refresh(product)

        # 4) Prices (mock retail zdroje)
        prices = [
            {"value": 109.90, "currency": "RUB", "source": "ozon", "region": "??????"},
            {"value": 104.50, "currency": "RUB", "source": "wildberries", "region": "??????"},
            {"value": 99.90, "currency": "RUB", "source": "magnit", "region": "??????"},
        ]

        inserted = 0
        for p in prices:
            price = Price(
                value=float(p["value"]),
                currency=p.get("currency", "RUB"),
                source=p["source"],
                region=p.get("region"),
                scraped_at=datetime.utcnow(),
                product_id=product.id,
            )
            db.add(price)
            inserted += 1

        db.commit()

        print("OK")
        print(f"Company: {company.id} {company.name}")
        print(f"Brand:   {brand.id} {brand.name}")
        print(f"Product: {product.id} {product.name}")
        print(f"Prices inserted: {inserted}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
