import pandas as pd
from sqlalchemy import create_engine, text

from app.db.session import engine as sa_engine


def load_market_snapshot() -> pd.DataFrame:
    """Load market_snapshot into DataFrame, filter out null price/region."""
    with sa_engine.connect() as conn:
        df = pd.read_sql(text("SELECT * FROM market_snapshot"), conn)
    df = df[df["price_value"].notna() & df["region"].notna()]
    return df


def compute_overview_metrics(df: pd.DataFrame) -> dict:
    return {
        "total_products": int(len(df)),
        "total_brands": int(df["brand_name"].dropna().nunique()),
        "total_regions": int(df["region"].dropna().nunique()),
        "avg_price_overall": float(df["price_value"].mean()) if not df.empty else None,
        "median_price_overall": float(df["price_value"].median()) if not df.empty else None,
    }


def prices_by_region(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby(["region", "region_code"], dropna=False)["price_value"]
        .agg(["mean", "median", "min", "max", "count"])
        .reset_index()
    )
    grouped.rename(
        columns={
            "mean": "avg_price",
            "median": "median_price",
            "min": "min_price",
            "max": "max_price",
            "count": "product_count",
        },
        inplace=True,
    )
    return grouped


def prices_by_category(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby(["category"], dropna=False)["price_value"]
        .agg(["mean", "median", "count"])
        .reset_index()
    )
    grouped.rename(
        columns={
            "mean": "avg_price",
            "median": "median_price",
            "count": "product_count",
        },
        inplace=True,
    )
    return grouped


def brand_distribution(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby(["brand_name"], dropna=False)
        .agg(product_count=("product_name", "count"), regions_count=("region", "nunique"))
        .reset_index()
    )
    return grouped
