CREATE TABLE IF NOT EXISTS brands_raw (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_name TEXT NOT NULL,
    source TEXT,
    extraction_method TEXT,
    confidence TEXT,
    example_product TEXT,
    region TEXT,
    created_at DATETIME,
    CONSTRAINT uq_brands_raw UNIQUE (brand_name, region)
);
