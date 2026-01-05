CREATE TABLE IF NOT EXISTS brand_company_matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_name TEXT NOT NULL,
    company_discovered_id INTEGER NOT NULL,
    company_name TEXT,
    brand_region TEXT,
    company_region TEXT,
    match_method TEXT,
    confidence_score INTEGER,
    created_at DATETIME,
    CONSTRAINT fk_brand_company_company FOREIGN KEY (company_discovered_id) REFERENCES companies_discovered(id),
    CONSTRAINT uq_brand_company UNIQUE (brand_name, company_discovered_id, match_method)
);
