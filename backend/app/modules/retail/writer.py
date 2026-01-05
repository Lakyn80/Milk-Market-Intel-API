from typing import List, Dict

from sqlalchemy import Column, Integer, String, Float, DateTime, Table, MetaData, insert
from sqlalchemy.orm import Session

metadata = MetaData()

retail_offers = Table(
    "retail_offers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("company_id", Integer, nullable=True),
    Column("source", String),
    Column("source_item_id", String),
    Column("region", String),
    Column("product_name", String),
    Column("price_value", Float),
    Column("price_currency", String),
    Column("collected_at", DateTime),
)


def write_retail_offers(db: Session, offers: List[Dict]) -> None:
    """Insert offers into retail_offers (time-series; duplicates allowed)."""
    if not offers:
        return
    stmt = insert(retail_offers)
    db.execute(stmt, offers)
    db.flush()
