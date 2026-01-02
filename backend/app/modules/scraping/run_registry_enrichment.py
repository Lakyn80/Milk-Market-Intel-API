import argparse
import json
from typing import Iterable

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.modules.companies.models import Company
from app.modules.scraping.providers.registry import RegistryEnrichmentProvider


def enrich_single(name: str) -> dict:
    provider = RegistryEnrichmentProvider()
    data = provider.enrich_company(name)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return data


def enrich_all(companies: Iterable[Company]) -> None:
    provider = RegistryEnrichmentProvider()
    processed = 0
    for company in companies:
        data = provider.enrich_company(company.name)
        processed += 1
        print(json.dumps({"company": company.name, **data}, ensure_ascii=False))
    print(f"Enriched (printed) companies: {processed}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Registry enrichment (Rusprofile) for single company or all companies in DB. Prints only; no DB writes."
    )
    parser.add_argument("--name", help="Company name to enrich (single mode).")
    parser.add_argument("--all", action="store_true", help="Enrich all companies from DB (print only).")
    args = parser.parse_args()

    if not args.name and not args.all:
        parser.error("Specify --name for single enrichment or --all to process all companies.")

    if args.name:
        enrich_single(args.name)
        return

    with SessionLocal() as session:  # type: Session
        companies = session.query(Company).all()
        enrich_all(companies)


if __name__ == "__main__":
    main()
