from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    volume_liters: Mapped[float | None] = mapped_column(Float)
    fat_percent: Mapped[float | None] = mapped_column(Float)

    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
    brand = relationship("Brand", backref="products")
