import csv
from pathlib import Path
from typing import Dict

from app.db.session import SessionLocal
from app.modules.regions.models import Region

# Adjusted path to top-level data/ directory.
DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "rosstat_regions.csv"


def upsert_region(db, row: Dict) -> None:
    name = row.get("name")
    if not name:
        return

    region = db.query(Region).filter(Region.name == name).first()
    if region:
        # update basic fields if changed
        changed = False
        for field in ["country", "federal_district", "center_lat", "center_lon"]:
            if field in row and row[field] is not None:
                if getattr(region, field, None) != row[field]:
                    setattr(region, field, row[field])
                    changed = True
        if changed:
            db.add(region)
        return

    new_region = Region(
        name=name,
        country=row.get("country") or "RU",
        federal_district=row.get("federal_district"),
        center_lat=row.get("center_lat"),
        center_lon=row.get("center_lon"),
    )
    db.add(new_region)


def load_csv() -> list[Dict]:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"CSV file not found: {DATA_PATH}")
    rows = []
    with DATA_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(
                {
                    "name": r.get("name"),
                    "country": r.get("country") or "RU",
                    "federal_district": r.get("federal_district"),
                    "center_lat": float(r["center_lat"]) if r.get("center_lat") else None,
                    "center_lon": float(r["center_lon"]) if r.get("center_lon") else None,
                }
            )
    return rows


def main() -> None:
    rows = load_csv()
    inserted = 0
    updated = 0
    with SessionLocal() as db:
        for r in rows:
            before = db.query(Region).filter(Region.name == r["name"]).first()
            upsert_region(db, r)
            after = db.query(Region).filter(Region.name == r["name"]).first()
            if before is None and after is not None:
                inserted += 1
            elif before is not None and after is not None:
                updated += 1
        db.commit()
    print(f"Regions processed: {len(rows)}")
    print(f"Inserted: {inserted}, Updated: {updated}")


if __name__ == "__main__":
    main()
