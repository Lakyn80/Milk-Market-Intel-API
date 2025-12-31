from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    country: Mapped[str | None] = mapped_column(String(50))
    region: Mapped[str | None] = mapped_column(String(100))
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


class Market(Base):
    __tablename__ = "markets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    country: Mapped[str] = mapped_column(String(50))

    prices: Mapped[list["Price"]] = relationship(back_populates="market")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))

    weight: Mapped[float | None] = mapped_column(Float)
    unit: Mapped[str | None] = mapped_column(String(20))
    package_type: Mapped[str | None] = mapped_column(String(50))

    brand: Mapped["Brand"] = relationship(back_populates="products")
    prices: Mapped[list["Price"]] = relationship(back_populates="product")


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    market_id: Mapped[int] = mapped_column(ForeignKey("markets.id"))

    value: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(10))
    collected_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )

    source_url: Mapped[str | None] = mapped_column(String(500))

    product: Mapped["Product"] = relationship(back_populates="prices")
    market: Mapped["Market"] = relationship(back_populates="prices")
