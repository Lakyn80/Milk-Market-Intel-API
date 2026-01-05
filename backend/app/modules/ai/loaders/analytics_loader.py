import json
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[4] / "data" / "analytics"


def load_analytics() -> dict:
    """Load precomputed analytics outputs from CSV/JSON without transformations."""
    region_summary = pd.read_csv(BASE_DIR / "region_summary.csv").to_dict(orient="records")
    category_summary = pd.read_csv(BASE_DIR / "category_summary.csv").to_dict(orient="records")
    price_distribution = pd.read_csv(BASE_DIR / "price_distribution.csv").to_dict(orient="records")
    overview_metrics = json.loads((BASE_DIR / "overview_metrics.json").read_text(encoding="utf-8"))

    return {
        "overview_metrics": overview_metrics,
        "region_summary": region_summary,
        "category_summary": category_summary,
        "price_distribution": price_distribution,
    }
