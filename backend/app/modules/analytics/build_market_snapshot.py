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


def normalize_name(value) -> str | None:
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    s = re.sub(r"\\s+", " ", s)
    return s


def build_region_maps(db):
    code_to_name = {}
    name_to_code = {}
    stmt = select(Region.id, Region.name)
    for region_id, name in db.execute(stmt):
        norm_name = normalize_name(name)
        if not norm_name:
            continue
        code = str(region_id)
        code_to_name[code] = norm_name
        name_to_code[norm_name.lower()] = code
    return code_to_name, name_to_code


def resolve_region(value, code_to_name, name_to_code):
    if value is None:
        return None, None
    raw = str(value).strip()
    if not raw:
        return None, None
    # numeric code
    if raw.isdigit() and raw in code_to_name:
        name = code_to_name[raw]
        return name, raw
    norm = normalize_name(raw)
    if not norm:
        return None, None
    code = name_to_code.get(norm.lower())
    return norm, code


def build_company_counts(db) -> dict[str, int]:
    counts = defaultdict(int)
    stmt = select(CompanyDiscovered.region, func.count(func.distinct(CompanyDiscovered.id)))
    stmt = stmt.group_by(CompanyDiscovered.region)
    for region, cnt in db.execute(stmt):
        norm = normalize_name(region)
        if norm:
            counts[norm] += cnt
    return counts


def main() -> None:
    with SessionLocal() as db:
        # rebuild snapshot: delete all rows
        db.execute(delete(market_snapshot))

        code_to_name, name_to_code = build_region_maps(db)
        company_counts = build_company_counts(db)

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
            region_name, reg_code = resolve_region(row.get("region"), code_to_name, name_to_code)
            count = company_counts.get(region_name, 0) if region_name else 0
            collected_at = row.get("parsed_at") or datetime.utcnow()
            to_insert.append(
                {
                    "product_name": row.get("product_name"),
                    "brand_name": row.get("brand_name"),
                    "category": row.get("category"),
                    "price_value": row.get("price_value"),
                    "price_currency": row.get("price_currency"),
                    "region": region_name,
                    "region_code": reg_code,
                    "companies_count_region": count,
                    "collected_at": collected_at.isoformat() if hasattr(collected_at, "isoformat") else str(collected_at),
                }
            )

        # ensure region is string and not null
        for r in to_insert:
            if r["region"] is None:
                r["region"] = ""
            else:
                r["region"] = str(r["region"])

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
