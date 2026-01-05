import logging
from pathlib import Path

from app.modules.analytics.pandas_metrics import (
    load_market_snapshot,
    compute_overview_metrics,
    prices_by_region,
    prices_by_category,
    brand_distribution,
)
from app.modules.analytics.exports import export_csv, export_json


logger = logging.getLogger(__name__)


def main() -> None:
    df = load_market_snapshot()
    print(f"Snapshot rows: {len(df)}")

    overview = compute_overview_metrics(df)
    by_region = prices_by_region(df)
    by_category = prices_by_category(df)
    brands = brand_distribution(df)

    out_dir = Path(__file__).resolve().parents[2] / "data" / "analytics"
    export_json(overview, out_dir / "overview_metrics.json")
    export_csv(by_region, out_dir / "prices_by_region.csv")
    export_csv(by_category, out_dir / "prices_by_category.csv")
    export_csv(brands, out_dir / "brand_distribution.csv")

    # stdout summary
    top_regions = by_region.sort_values("product_count", ascending=False).head(5)
    top_categories = by_category.sort_values("avg_price", ascending=False).head(5)

    print("Top 5 regions by product_count:")
    for _, row in top_regions.iterrows():
        print(f"{row['region']}: {int(row['product_count'])}")

    print("Top 5 categories by avg_price:")
    for _, row in top_categories.iterrows():
        cat = row['category'] if pd.notna(row['category']) else 'UNKNOWN'
        print(f"{cat}: {row['avg_price']:.2f}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import pandas as pd  # local import for summary formatting
    main()
