from datetime import datetime
from typing import Dict, Optional

from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from app.modules.companies.models import Company  # only for FK reference
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData


# Define minimal table metadata to avoid altering Company model.
metadata = MetaData()

company_registry = Table(
    "company_registry",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("company_id", Integer, nullable=False),
    Column("source", String),
    Column("source_url", String),
    Column("legal_form", String),
    Column("legal_name", String),
    Column("ogrn", String),
    Column("inn", String),
    Column("status_raw", String),
    Column("status_norm", String),
    Column("address_raw", String),
    Column("address_norm", String),
    Column("fetched_at", DateTime),
)


STATUS_MAP = {
    "Действующая": "ACTIVE",
    "В процессе ликвидации": "LIQUIDATING",
    "Ликвидирована": "CLOSED",
    "Банкротство": "BANKRUPT",
    "Реорганизация": "REORG",
}


def _normalize_status(status_raw: Optional[str]) -> str:
    if not status_raw:
        return "UNKNOWN"
    for key, val in STATUS_MAP.items():
        if key in status_raw:
            return val
    return "UNKNOWN"


def write_registry_entry(db: Session, company_id: int, source: str, data: Dict) -> None:
    """
    Upsert registry entry for a single company.
    - Uses (company_id, source) as uniqueness.
    - Maps status_raw -> status_norm.
    - Writes fetched_at = now.
    """
    status_raw = data.get("status")
    status_norm = _normalize_status(status_raw)

    row = {
        "company_id": company_id,
        "source": source,
        "source_url": data.get("source_url"),
        "legal_form": data.get("legal_form"),
        "legal_name": data.get("legal_name"),
        "ogrn": data.get("ogrn"),
        "inn": data.get("inn"),
        "status_raw": status_raw,
        "status_norm": status_norm,
        "address_raw": data.get("address"),
        "address_norm": data.get("address"),  # placeholder until normalization is added
        "fetched_at": datetime.utcnow(),
    }

    stmt_select = select(company_registry.c.id).where(
        (company_registry.c.company_id == company_id) & (company_registry.c.source == source)
    )
    existing = db.execute(stmt_select).scalar_one_or_none()

    if existing:
        stmt_update = (
            update(company_registry)
            .where(company_registry.c.id == existing)
            .values(**row)
        )
        db.execute(stmt_update)
    else:
        stmt_insert = insert(company_registry).values(**row)
        db.execute(stmt_insert)

    db.flush()
