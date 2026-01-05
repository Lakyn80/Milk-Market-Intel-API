from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    MetaData,
    Table,
)

metadata = MetaData()

retail_products_parsed = Table(
    "retail_products_parsed",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("retail_offer_id", Integer, ForeignKey("retail_offers.id"), nullable=False),
    Column("raw_name", String),
    Column("brand", String),
    Column("product_type", String),
    Column("flavor", String),
    Column("fat_percent", Float),
    Column("package_type", String),
    Column("weight_g", Integer),
    Column("volume_ml", Integer),
    Column("region", String),
    Column("source", String),
    Column("parsed_at", DateTime, default=datetime.utcnow),
    UniqueConstraint("retail_offer_id", name="uq_retail_products_parsed_offer"),
)
