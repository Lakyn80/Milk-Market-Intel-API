import plotly.express as px
import pandas as pd


def build_category_distribution_plot(df: pd.DataFrame, metric: str = "avg_price", categories: list[str] | None = None):
    data = df.copy()
    if categories:
        lowered = {str(c).lower() for c in categories}
        data = data[data["category"].astype(str).str.lower().isin(lowered)]
    fig = px.bar(
        data,
        x="category",
        y=metric,
        hover_data=["min_price", "max_price", "product_count"],
        title="Ceny podle kategorií",
    )
    fig.update_layout(template="plotly_dark", margin=dict(l=40, r=20, t=40, b=80), xaxis_tickangle=-40)
    return fig
