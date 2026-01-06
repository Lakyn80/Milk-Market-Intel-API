import plotly.express as px
import pandas as pd


def build_price_trend_plot(df: pd.DataFrame, category: str | None = None, region: str | None = None):
    data = df.copy()
    if category:
        data = data[data["category"].astype(str).str.lower() == str(category).lower()]
    if region:
        data = data[data["region"].astype(str).str.lower() == str(region).lower()]
    data = data.reset_index().rename(columns={"index": "sequence"})
    fig = px.line(
        data,
        x="sequence",
        y="price_value",
        color="category",
        title="Cenový průběh (sekvenční pořadí položek)",
    )
    fig.update_layout(template="plotly_dark", margin=dict(l=40, r=20, t=40, b=60))
    return fig
