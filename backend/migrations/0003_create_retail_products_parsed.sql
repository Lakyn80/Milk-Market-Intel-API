CREATE TABLE IF NOT EXISTS retail_products_parsed (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    retail_offer_id INTEGER NOT NULL,
    raw_name TEXT,
    brand TEXT,
    product_type TEXT,
    flavor TEXT,
    fat_percent REAL,
    package_type TEXT,
    weight_g INTEGER,
    volume_ml INTEGER,
    region TEXT,
    source TEXT,
    parsed_at DATETIME,
    CONSTRAINT fk_retail_offer FOREIGN KEY (retail_offer_id) REFERENCES retail_offers(id),
    CONSTRAINT uq_retail_products_parsed_offer UNIQUE (retail_offer_id)
);
