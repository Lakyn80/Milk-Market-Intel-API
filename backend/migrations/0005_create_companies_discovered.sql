CREATE TABLE IF NOT EXISTS companies_discovered (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL DEFAULT '2gis',
    external_id TEXT NOT NULL,
    name TEXT NOT NULL,
    canonical_name TEXT,
    country TEXT,
    region TEXT,
    address TEXT,
    lat REAL,
    lon REAL,
    website TEXT,
    phone TEXT,
    query TEXT,
    discovered_at DATETIME,
    CONSTRAINT uq_companies_discovered_source_extid UNIQUE (source, external_id)
);
