-- Migration: create company_registry table for registry enrichment
-- DB: SQLite (current dev); adjust types if porting to Postgres/MySQL.

CREATE TABLE IF NOT EXISTS company_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    source TEXT NOT NULL,
    source_url TEXT,
    legal_form TEXT,
    legal_name TEXT,
    ogrn TEXT,
    inn TEXT,
    status_raw TEXT,
    status_norm TEXT,
    address_raw TEXT,
    address_norm TEXT,
    fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (company_id, source),
    CHECK (status_norm IN ('ACTIVE', 'LIQUIDATING', 'CLOSED', 'BANKRUPT', 'REORG', 'UNKNOWN')),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS ix_company_registry_company_id ON company_registry (company_id);
CREATE INDEX IF NOT EXISTS ix_company_registry_status_norm ON company_registry (status_norm);
