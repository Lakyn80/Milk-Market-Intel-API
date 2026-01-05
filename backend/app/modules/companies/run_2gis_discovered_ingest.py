import os
import random
import time
from datetime import datetime
from typing import Dict, Tuple

import httpx
from dotenv import load_dotenv
from sqlalchemy import select, update, insert

from app.db.session import SessionLocal
from app.modules.regions.models import Region
from app.modules.scraping.providers.two_gis import TwoGisProvider
from app.modules.companies.models_discovered import CompanyDiscovered
from app.modules.scraping.normalization.company_name import canonical_company_name


def _get_region_point(region: Region) -> Tuple[float | None, float | None]:
    return region.center_lat, region.center_lon


def upsert_company(db, item: Dict) -> Tuple[bool, bool]:
    """Returns (inserted, updated)."""
    ext_id = item.get("external_id")
    if not ext_id:
        return False, False

    source = "2gis"

    stmt = select(CompanyDiscovered).where(
        CompanyDiscovered.source == source,
        CompanyDiscovered.external_id == str(ext_id),
    )
    existing = db.execute(stmt).scalar_one_or_none()

    now = datetime.utcnow()
    base_fields = {
        "source": source,
        "external_id": str(ext_id),
        "name": item.get("name"),
        "canonical_name": canonical_company_name(item.get("name") or "") if item.get("name") else None,
        "country": item.get("country") or "RU",
        "region": item.get("region"),
        "address": item.get("address"),
        "lat": item.get("lat"),
        "lon": item.get("lon"),
        "website": item.get("website"),
        "phone": item.get("phone"),
        "query": item.get("query"),
        "discovered_at": now,
    }

    if existing:
        # Update only provided fields if they are non-empty.
        update_data = {}
        for key in ["region", "address", "lat", "lon", "website", "phone", "canonical_name", "query", "name"]:
            val = base_fields.get(key)
            if val:
                update_data[key] = val
        if update_data:
            update_data["discovered_at"] = now
            db.execute(
                update(CompanyDiscovered)
                .where(CompanyDiscovered.id == existing.id)
                .values(**update_data)
            )
            return False, True
        return False, False

    db.execute(insert(CompanyDiscovered).values(**base_fields))
    return True, False


def fetch_for_region(region: Region, query: str, max_results: int | None = None) -> Tuple[int, int, int, int]:
    # Set env for provider
    if region.center_lat is None or region.center_lon is None:
        print(f"Skipping region {region.name}: missing coordinates")
        return 0, 0, 0

    os.environ["TWO_GIS_REGION"] = region.name
    os.environ["TWO_GIS_POINT"] = f"{region.center_lon},{region.center_lat}"
    if query:
        os.environ["TWO_GIS_QUERY"] = query

    provider = TwoGisProvider()
    # Adjust max_results if provided
    if max_results:
        provider.max_results = max_results

    inserted = 0
    updated = 0
    skipped = 0

    with SessionLocal() as db:
        # Throttle before request
        time.sleep(random.uniform(0.8, 1.5))

        def run_fetch(with_retry: bool = False):
            try:
                return provider.fetch_companies()
            except Exception as exc:
                msg = str(exc)
                transient = isinstance(exc, httpx.ConnectError) or any(
                    code in msg for code in ("429", "500", "502", "503")
                )
                if transient and not with_retry:
                    time.sleep(random.uniform(3.0, 6.0))
                    return run_fetch(with_retry=True)
                raise

        items = run_fetch()

        for item in items:
            ins, upd = upsert_company(db, item)
            if ins:
                inserted += 1
            elif upd:
                updated += 1
            else:
                skipped += 1

        db.commit()

    return inserted + updated + skipped, inserted, updated, skipped


def main() -> None:
    # Load environment variables from backend/.env if present
    load_dotenv()

    with SessionLocal() as db:
        regions = db.query(Region).all()

    query = os.environ.get("TWO_GIS_QUERY", "завод")
    total_all = inserted_all = updated_all = skipped_all = 0
    errors: list[str] = []

    for region in regions:
        try:
            count, inserted, updated, skipped = fetch_for_region(region, query)
            total_all += count
            inserted_all += inserted
            updated_all += updated
            skipped_all += skipped
            print(f"Region: {region.name} | fetched: {count} | inserted: {inserted} | updated: {updated} | skipped: {skipped}")
        except Exception as exc:
            msg = f"Region: {region.name} failed: {exc}"
            errors.append(msg)
            print(msg)
            continue

    print("\n=== SUMMARY ===")
    print(f"Total records processed: {total_all}")
    print(f"Inserted: {inserted_all}")
    print(f"Updated: {updated_all}")
    print(f"Skipped: {skipped_all}")
    if errors:
        print("Errors:")
        for e in errors:
            print(f"- {e}")


if __name__ == "__main__":
    main()
