from app.modules.analytics.plots.price_by_region import build_price_by_region_plot
from app.modules.analytics.plots.category_distribution import build_category_distribution_plot
from app.modules.analytics.plots.price_trend import build_price_trend_plot

PLOTS = {
    "price_by_region": {
        "label": "Průměrná cena podle regionu",
        "inputs": ["metric", "regions"],
        "builder": build_price_by_region_plot,
    },
    "category_distribution": {
        "label": "Ceny podle kategorií",
        "inputs": ["metric", "categories"],
        "builder": build_category_distribution_plot,
    },
    "price_trend": {
        "label": "Cenový trend (sekvenční)",
        "inputs": ["category", "region"],
        "builder": build_price_trend_plot,
    },
}
