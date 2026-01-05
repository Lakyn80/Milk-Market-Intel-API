import logging
import re
from datetime import datetime
from typing import Dict, Iterable, List, Tuple, Set

from sqlalchemy import select, insert

from app.db.session import SessionLocal
from app.modules.matching.models import brand_company_matches
from app.modules.companies.models_discovered import CompanyDiscovered
from app.modules.retail.parsed_models import retail_products_parsed

logger = logging.getLogger(__name__)


LEGAL_WORDS = [
    "ооо",
    "ао",
    "пао",
    "зао",
    "ип",
    "молочный завод",
    "молкомбинат",
    "завод",
]


def normalize(text: str) -> str:
    s = text.lower()
    # remove quotes
    s = s.replace("«", "").replace("»", "").replace('"', "").replace("'", "")
    # remove legal/entity words
    for w in LEGAL_WORDS:
        s = re.sub(rf"\\b{re.escape(w)}\\b", " ", s)
    # remove punctuation
    s = re.sub(r"[.,;:()\\[\\]{}]", " ", s)
    s = re.sub(r"\\s+", " ", s).strip()
    return s


def token_overlap(a: str, b: str) -> bool:
    tokens_a = {t for t in re.split(r"\\s+", a) if len(t) >= 4}
    tokens_b = {t for t in re.split(r"\\s+", b) if len(t) >= 4}
    return bool(tokens_a & tokens_b)


def match_brand_to_company(brand_norm: str, comp_norm: str) -> Tuple[str | None, int]:
    # A) exact_name
    if brand_norm == comp_norm:
        return "exact_name", 100
    # B) normalized_exact (part/whole)
    if brand_norm in comp_norm or comp_norm in brand_norm:
        return "normalized_exact", 85
    # C) substring (len>=5)
    if (len(brand_norm) >= 5 and brand_norm in comp_norm) or (len(comp_norm) >= 5 and comp_norm in brand_norm):
        return "substring", 70
    # D) token_overlap (>=1 token)
    if token_overlap(brand_norm, comp_norm):
        return "token_overlap", 50
    return None, 0


def load_brands(db) -> List[Tuple[str, str | None]]:
    stmt = (
        select(retail_products_parsed.c.brand, retail_products_parsed.c.region)
        .where(retail_products_parsed.c.brand.isnot(None))
    )
    rows = db.execute(stmt).all()
    brands = set()
    for b, region in rows:
        if b and len(str(b).strip()) >= 3:
            brands.add((str(b).strip(), region))
    return list(brands)


def load_companies(db) -> List[Dict]:
    stmt = select(CompanyDiscovered)
    return db.execute(stmt).mappings().all()


def fetch_existing(db) -> Set[Tuple[str, int, str]]:
    stmt = select(
        brand_company_matches.c.brand_name,
        brand_company_matches.c.company_discovered_id,
        brand_company_matches.c.match_method,
    )
    return set(db.execute(stmt).all())


def main() -> None:
    inserted = 0
    skipped = 0
    method_stats: Dict[str, int] = {}

    with SessionLocal() as db:
        existing = fetch_existing(db)
        brands = load_brands(db)
        companies = load_companies(db)

        for brand_raw, brand_region in brands:
            brand_norm = normalize(brand_raw)
            if not brand_norm or len(brand_norm) < 3:
                continue

            for comp in companies:
                comp_name = comp.get("name") or ""
                comp_norm = normalize(comp_name)
                if not comp_norm:
                    continue

                method, score = match_brand_to_company(brand_norm, comp_norm)
                if not method:
                    continue

                # Region bonus
                if brand_region and comp.get("region") and brand_region == comp.get("region"):
                    score = min(100, score + 10)

                key = (brand_raw, comp["id"], method)
                if key in existing:
                    skipped += 1
                    continue

                payload = {
                    "brand_name": brand_raw,
                    "company_discovered_id": comp["id"],
                    "company_name": comp_name,
                    "brand_region": brand_region,
                    "company_region": comp.get("region"),
                    "match_method": method,
                    "confidence_score": score,
                    "created_at": datetime.utcnow(),
                }
                db.execute(insert(brand_company_matches).values(payload))
                existing.add(key)
                inserted += 1
                method_stats[method] = method_stats.get(method, 0) + 1

        db.commit()

    print(f"Brands processed: {len(brands)}")
    print(f"Matches inserted: {inserted}")
    print(f"Skipped (existing): {skipped}")
    print("By method:", method_stats)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
