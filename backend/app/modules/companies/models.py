from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    country: Mapped[str] = mapped_column(String(100))
    region: Mapped[str | None] = mapped_column(String(150))
    website: Mapped[str | None] = mapped_column(String(255))

    brands: Mapped[list["Brand"]] = relationship(back_populates="company")


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))

    company: Mapped["Company"] = relationship(back_populates="brands")
    products: Mapped[list["Product"]] = relationship(back_populates="brand")

    __table_args__ = (
        UniqueConstraint("name", "company_id", name="uq_brand_company"),
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)

    volume_liters: Mapped[float | None] = mapped_column(Float)
    fat_percent: Mapped[float | None] = mapped_column(Float)

    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))

    brand: Mapped["Brand"] = relationship(back_populates="products")
    prices: Mapped[list["Price"]] = relationship(back_populates="product")


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(10))

    source: Mapped[str] = mapped_column(String(255))
    region: Mapped[str | None] = mapped_column(String(150))

    scraped_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    product: Mapped["Product"] = relationship(back_populates="prices")


class Market(Base):
    __tablename__ = "markets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    country: Mapped[str] = mapped_column(String(50))
