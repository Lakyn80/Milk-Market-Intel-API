from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Float,
    MetaData,
)

metadata = MetaData()

market_snapshot = Table(
    "market_snapshot",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("product_name", String),
    Column("brand_name", String),
    Column("category", String),
    Column("price_value", Float),
    Column("price_currency", String),
    Column("region", String),
    Column("region_code", String),
    Column("companies_count_region", Integer),
    Column("collected_at", String),
)
