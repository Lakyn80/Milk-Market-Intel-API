import re
from collections import defaultdict
from datetime import datetime

from sqlalchemy import delete, insert, select, join, func

from app.db.session import SessionLocal
from app.modules.analytics.models import market_snapshot
from app.modules.retail.parsed_models import retail_products_parsed
from app.modules.retail.writer import retail_offers
from app.modules.companies.models_discovered import CompanyDiscovered
from app.modules.regions.models import Region


def normalize_region(value) -> str | None:
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    s_lower = s.lower()
    # Moscow variants
    if s_lower in {"213", "moscow", "москва"}:
        return "Moscow"
    if s_lower in {"moscow oblast", "moscow region"}:
        return "Moscow Oblast"

    # If numeric lr, leave as-is
    if s_lower.isdigit():
        return s

    # Title-case other regions
    s = re.sub(r"\\s+", " ", s)
    return s.title()


def region_code(value) -> str | None:
    if value is None:
        return None
    s = str(value).strip().lower()
    if not s:
        return None
    if s.isdigit():
        return s
    if s in {"moscow", "москва"}:
        return "213"
    if s in {"moscow oblast", "moscow region"}:
        return "50"
    if s in {"saint petersburg", "санкт-петербург", "st. petersburg"}:
        return "2"
    return None


def build_region_lookup(db) -> set[str]:
    stmt = select(Region.name)
    regions = set()
    for (name,) in db.execute(stmt):
        norm = normalize_region(name)
        if norm:
            regions.add(norm)
    return regions


def build_company_counts(db) -> dict[str, int]:
    counts = defaultdict(int)
    stmt = select(CompanyDiscovered.region, func.count(func.distinct(CompanyDiscovered.id)))
    stmt = stmt.group_by(CompanyDiscovered.region)
    for region, cnt in db.execute(stmt):
        region_norm = normalize_region(region)
        if region_norm:
            counts[region_norm] += cnt
    return counts


def main() -> None:
    with SessionLocal() as db:
        # rebuild snapshot: delete all rows
        db.execute(delete(market_snapshot))

        company_counts = build_company_counts(db)
        region_lookup = build_region_lookup(db)

        j = join(retail_products_parsed, retail_offers, retail_products_parsed.c.retail_offer_id == retail_offers.c.id)
        stmt = select(
            retail_products_parsed.c.raw_name.label("product_name"),
            retail_products_parsed.c.brand.label("brand_name"),
            retail_products_parsed.c.product_type.label("category"),
            retail_offers.c.price_value,
            retail_offers.c.price_currency,
            retail_products_parsed.c.region,
            retail_products_parsed.c.parsed_at,
        ).select_from(j)

        rows = db.execute(stmt).mappings().all()

        to_insert = []
        for row in rows:
            region_norm = normalize_region(row.get("region"))
            reg_code = region_code(row.get("region")) or region_code(region_norm)
            if not reg_code and region_norm:
                # If region exists in lookup, use normalized name as code surrogate
                if region_norm in region_lookup:
                    reg_code = region_norm
            count = company_counts.get(region_norm, 0) if region_norm else 0
            collected_at = row.get("parsed_at") or datetime.utcnow()
            to_insert.append(
                {
                    "product_name": row.get("product_name"),
                    "brand_name": row.get("brand_name"),
                    "category": row.get("category"),
                    "price_value": row.get("price_value"),
                    "price_currency": row.get("price_currency"),
                    "region": region_norm,
                    "region_code": reg_code,
                    "companies_count_region": count,
                    "collected_at": collected_at.isoformat() if hasattr(collected_at, "isoformat") else str(collected_at),
                }
            )

        if to_insert:
            db.execute(insert(market_snapshot), to_insert)
        db.commit()

        # stats
        total = len(to_insert)
        # top 10 regions by product count
        region_counts = defaultdict(int)
        for r in to_insert:
            if r["region"]:
                region_counts[r["region"]] += 1
        top_regions = sorted(region_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    print(f"market_snapshot rows: {total}")
    print("Top 10 regions by product count:")
    for reg, cnt in top_regions:
        print(f"{reg}: {cnt}")


if __name__ == "__main__":
    main()
