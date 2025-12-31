from datetime import date
from sqlalchemy.orm import Session

from app.modules.companies.price_models import Price
from app.modules.companies.product_models import Product


class PriceImportService:
    def __init__(self, db: Session):
        self.db = db

    def import_prices(self, product: Product, prices: list[dict]) -> int:
        count = 0
        for item in prices:
            exists = (
                self.db.query(Price)
                .filter(
                    Price.product_id == product.id,
                    Price.source == item['source'],
                    Price.scraped_at.cast(date) == date.today(),
                )
                .first()
            )
            if exists:
                continue

            price = Price(
                value=item['value'],
                currency=item.get('currency', 'RUB'),
                source=item['source'],
                region=item.get('region'),
                product_id=product.id,
            )
            self.db.add(price)
            count += 1

        self.db.commit()
        return count
