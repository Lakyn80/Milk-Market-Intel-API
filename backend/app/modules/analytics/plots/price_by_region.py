import plotly.express as px
import pandas as pd


def build_price_by_region_plot(df: pd.DataFrame, metric: str = "avg_price", regions: list[str] | None = None):
    data = df.copy()
    if regions:
        lowered = {str(r).lower() for r in regions}
        data = data[data["region"].astype(str).str.lower().isin(lowered)]
    fig = px.bar(
        data,
        x="region",
        y=metric,
        hover_data=["region_code", "min_price", "max_price", "product_count"],
        title="Průměrná cena podle regionu",
    )
    fig.update_layout(template="plotly_dark", margin=dict(l=40, r=20, t=40, b=80))
    return fig
