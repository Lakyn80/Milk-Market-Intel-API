import logging
from pathlib import Path

import pandas as pd

from app.modules.analytics.aggregations import (
    aggregate_by_category,
    aggregate_by_region,
    compute_overview_metrics,
    price_distribution,
)
from app.modules.analytics.exporters import save_csv, save_json
from app.modules.analytics.loaders import load_market_snapshot


logger = logging.getLogger(__name__)


def main() -> None:
    df = load_market_snapshot()
    print(f"Snapshot rows: {len(df)}")

    overview = compute_overview_metrics(df)
    by_region = aggregate_by_region(df)
    by_category = aggregate_by_category(df)
    distribution = price_distribution(df)

    out_dir = Path(__file__).resolve().parents[3] / "data" / "analytics"
    out_dir.mkdir(parents=True, exist_ok=True)

    save_json(overview, out_dir / "overview_metrics.json")
    save_csv(by_region, out_dir / "region_summary.csv")
    save_csv(by_category, out_dir / "category_summary.csv")
    save_csv(distribution, out_dir / "price_distribution.csv")

    # stdout summary
    def safe_text(val: object) -> str:
        text = "UNKNOWN" if pd.isna(val) else str(val)
        return text.encode("unicode_escape").decode("ascii")

    if not by_region.empty:
        top_regions = by_region.sort_values("product_count", ascending=False).head(5)
        print("Top 5 regions by product_count:")
        for _, row in top_regions.iterrows():
            region = safe_text(row["region"])
            print(f"{region}: {int(row['product_count'])}")
    else:
        print("Top 5 regions by product_count: (no data)")

    if not by_category.empty:
        top_categories = (
            by_category.dropna(subset=["avg_price"])
            .sort_values("avg_price", ascending=False)
            .head(5)
        )
        print("Top 5 categories by avg_price:")
        for _, row in top_categories.iterrows():
            cat = safe_text(row["category"])
            print(f"{cat}: {row['avg_price']:.2f}")
    else:
        print("Top 5 categories by avg_price: (no data)")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
