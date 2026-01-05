-- Migration: create retail_offers table for time-series retail data
-- DB: SQLite (current dev); adjust types if porting to Postgres/MySQL.

CREATE TABLE IF NOT EXISTS retail_offers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    source TEXT NOT NULL,
    source_item_id TEXT,
    region TEXT,
    product_name TEXT,
    price_value REAL,
    price_currency TEXT,
    collected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (company_id, source, source_item_id, collected_at),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS ix_retail_offers_company_id ON retail_offers (company_id);
CREATE INDEX IF NOT EXISTS ix_retail_offers_collected_at ON retail_offers (collected_at);
CREATE INDEX IF NOT EXISTS ix_retail_offers_region ON retail_offers (region);
CREATE INDEX IF NOT EXISTS ix_retail_offers_source ON retail_offers (source);
