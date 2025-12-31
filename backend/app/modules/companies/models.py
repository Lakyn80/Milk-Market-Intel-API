from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Company(Base):
    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    country: Mapped[str] = mapped_column(String(100), default='RU')
    region: Mapped[str | None] = mapped_column(String(150))
    website: Mapped[str | None] = mapped_column(String(255))
