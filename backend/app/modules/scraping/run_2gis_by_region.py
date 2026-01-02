from app.db.session import SessionLocal
from app.modules.regions.models import Region
from app.modules.scraping.pipeline import ScrapingPipeline
import os

def main():
    db = SessionLocal()
    regions = db.query(Region).all()
    print(f'Regions loaded: {len(regions)}')

    pipeline = ScrapingPipeline()

    for region in regions:
        print(f'\\n=== REGION: {region.name} ===')

        # Předání regionu provideru přes ENV
        os.environ['SCRAPING_PROVIDER'] = '2gis'
        os.environ['REGION_NAME'] = region.name
        os.environ['REGION_CENTER_LAT'] = str(region.center_lat)
        os.environ['REGION_CENTER_LON'] = str(region.center_lon)

        items = pipeline.run()

        print(f'Found items: {len(items)}')

    db.close()


if __name__ == '__main__':
    main()
