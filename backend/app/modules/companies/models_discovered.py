from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    UniqueConstraint,
)

from app.db.base import Base


class CompanyDiscovered(Base):
    __tablename__ = "companies_discovered"

    id = Column(Integer, primary_key=True)
    source = Column(String(50), nullable=False, default="2gis")
    external_id = Column(String(100), nullable=False)
    name = Column(String(255), nullable=False)
    canonical_name = Column(String(255), nullable=True)
    country = Column(String(50), nullable=True, default="RU")
    region = Column(String(150), nullable=True)
    address = Column(String(255), nullable=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    website = Column(String(255), nullable=True)
    phone = Column(String(100), nullable=True)
    query = Column(String(255), nullable=True)
    discovered_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_companies_discovered_source_extid"),
    )
