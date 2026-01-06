import json
from pathlib import Path

import pandas as pd

from app.modules.analytics.plots.plot_registry import PLOTS

BASE_DIR = Path(__file__).resolve().parents[3] / "data" / "analytics"
OUT_DIR = BASE_DIR / "plots"


def load_sources():
    region_summary = pd.read_csv(BASE_DIR / "region_summary.csv")
    category_summary = pd.read_csv(BASE_DIR / "category_summary.csv")
    price_distribution = pd.read_csv(BASE_DIR / "price_distribution.csv")
    overview = json.loads((BASE_DIR / "overview_metrics.json").read_text(encoding="utf-8"))
    return {
        "region_summary": region_summary,
        "category_summary": category_summary,
        "price_distribution": price_distribution,
        "overview": overview,
    }


def build_all():
    sources = load_sources()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # price_by_region
    fig = PLOTS["price_by_region"]["builder"](sources["region_summary"])
    (OUT_DIR / "price_by_region.json").write_text(fig.to_json(), encoding="utf-8")

    # category_distribution
    fig = PLOTS["category_distribution"]["builder"](sources["category_summary"])
    (OUT_DIR / "category_distribution.json").write_text(fig.to_json(), encoding="utf-8")

    # price_trend
    fig = PLOTS["price_trend"]["builder"](sources["price_distribution"])
    (OUT_DIR / "price_trend.json").write_text(fig.to_json(), encoding="utf-8")


def main():
    build_all()
    print(f"Plots exported to: {OUT_DIR}")


if __name__ == "__main__":
    main()
