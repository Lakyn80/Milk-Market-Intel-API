from datetime import datetime
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    UniqueConstraint,
    MetaData,
)

metadata = MetaData()

brands_raw = Table(
    "brands_raw",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("brand_name", String, nullable=False),
    Column("source", String),
    Column("extraction_method", String),
    Column("confidence", String),
    Column("example_product", String),
    Column("region", String),
    Column("created_at", DateTime, default=datetime.utcnow),
    UniqueConstraint("brand_name", "region", name="uq_brands_raw"),
)
