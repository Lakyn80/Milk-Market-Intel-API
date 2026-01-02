from app.db.session import SessionLocal
from app.modules.regions.models import Region
from app.modules.companies.models import Company
from app.modules.scraping.pipeline import ScrapingPipeline
import os


def get_or_create_company(db, *, name, country, region, website):
    company = (
        db.query(Company)
        .filter(Company.name == name)
        .filter(Company.region == region)
        .first()
    )

    if company:
        if website and not company.website:
            company.website = website
        return company, False

    company = Company(
        name=name,
        country=country,
        region=region,
        website=website,
    )
    db.add(company)
    return company, True


def main():
    db = SessionLocal()
    regions = db.query(Region).all()

    pipeline = ScrapingPipeline()
    total = 0
    inserted = 0

    for region in regions:
        print(f'\\n=== REGION: {region.name} ===')

        os.environ['SCRAPING_PROVIDER'] = '2gis'
        os.environ['REGION_NAME'] = region.name
        os.environ['REGION_CENTER_LAT'] = str(region.center_lat)
        os.environ['REGION_CENTER_LON'] = str(region.center_lon)

        items = pipeline.run()
        print(f'Items fetched: {len(items)}')

        for item in items:
            company, is_new = get_or_create_company(
                db,
                name=item['canonical_name'],
                country=item.get('country', 'RU'),
                region=region.name,
                website=item.get('website'),
            )
            total += 1
            if is_new:
                inserted += 1

        db.commit()

    db.close()

    print('\\n=== SUMMARY ===')
    print(f'Processed items: {total}')
    print(f'New companies inserted: {inserted}')


if __name__ == '__main__':
    main()
