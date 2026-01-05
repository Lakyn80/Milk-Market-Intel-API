from datetime import datetime
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    MetaData,
)

metadata = MetaData()

brand_company_matches = Table(
    "brand_company_matches",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("brand_name", String, nullable=False),
    Column("company_discovered_id", Integer, ForeignKey("companies_discovered.id"), nullable=False),
    Column("company_name", String),
    Column("brand_region", String),
    Column("company_region", String),
    Column("match_method", String),
    Column("confidence_score", Integer),
    Column("created_at", DateTime, default=datetime.utcnow),
    UniqueConstraint("brand_name", "company_discovered_id", "match_method", name="uq_brand_company"),
)
