import json
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[4] / "data" / "analytics"


def load_analytics() -> dict:
    """Load precomputed analytics outputs without any transformations."""
    overview = json.loads((BASE_DIR / "overview_metrics.json").read_text(encoding="utf-8"))
    regions = pd.read_csv(BASE_DIR / "region_summary.csv").to_dict(orient="records")
    categories = pd.read_csv(BASE_DIR / "category_summary.csv").to_dict(orient="records")
    prices = pd.read_csv(BASE_DIR / "price_distribution.csv").to_dict(orient="records")
    return {
        "overview": overview,
        "regions": regions,
        "categories": categories,
        "prices": prices,
    }
