from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    country = Column(String(50), nullable=False)
    federal_district = Column(String(100), nullable=True)

    center_lat = Column(Float, nullable=True)
    center_lon = Column(Float, nullable=True)
