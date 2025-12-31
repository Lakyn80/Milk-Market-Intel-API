from sqlalchemy import String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="RUB")
    source: Mapped[str] = mapped_column(String(255))
    region: Mapped[str | None] = mapped_column(String(150))
    scraped_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product = relationship("Product", backref="prices")
