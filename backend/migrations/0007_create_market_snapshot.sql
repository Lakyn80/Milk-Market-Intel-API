CREATE TABLE IF NOT EXISTS market_snapshot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    brand_name TEXT,
    category TEXT,
    price_value REAL,
    price_currency TEXT,
    region TEXT,
    companies_count_region INTEGER,
    collected_at TEXT
);
