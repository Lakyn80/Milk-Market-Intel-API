import pandas as pd


def _filtered(df: pd.DataFrame) -> pd.DataFrame:
    """Return rows with non-null price_value for numeric aggregations."""
    return df[df["price_value"].notna()].copy()


def compute_overview_metrics(df: pd.DataFrame) -> dict:
    data = _filtered(df)
    return {
        "total_products": int(len(data)),
        "distinct_regions": int(data["region"].dropna().nunique()),
        "distinct_categories": int(data["category"].dropna().nunique()),
        "avg_price": float(data["price_value"].mean()) if not data.empty else None,
        "min_price": float(data["price_value"].min()) if not data.empty else None,
        "max_price": float(data["price_value"].max()) if not data.empty else None,
    }


def aggregate_by_region(df: pd.DataFrame) -> pd.DataFrame:
    data = _filtered(df)
    grouped = (
        data.groupby(["region", "region_code"], dropna=False)["price_value"]
        .agg(["count", "mean", "min", "max"])
        .reset_index()
    )
    grouped.rename(
        columns={
            "count": "product_count",
            "mean": "avg_price",
            "min": "min_price",
            "max": "max_price",
        },
        inplace=True,
    )
    return grouped


def aggregate_by_category(df: pd.DataFrame) -> pd.DataFrame:
    data = _filtered(df)
    grouped = (
        data.groupby(["category"], dropna=False)["price_value"]
        .agg(["count", "mean", "min", "max"])
        .reset_index()
    )
    grouped.rename(
        columns={
            "count": "product_count",
            "mean": "avg_price",
            "min": "min_price",
            "max": "max_price",
        },
        inplace=True,
    )
    return grouped


def price_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Return per-item price distribution with region/category for UI histograms."""
    data = _filtered(df)
    return data[["region", "category", "price_value"]].copy()
