import pandas as pd
from sqlalchemy import text

from app.db.session import engine as sa_engine


def load_market_snapshot() -> pd.DataFrame:
    """Load market_snapshot into a DataFrame without transformations."""
    with sa_engine.connect() as conn:
        df = pd.read_sql(text("SELECT * FROM market_snapshot"), conn)
    return df
