export const PLOT_CONFIG = {
  price_by_region: {
    label: "Průměrná cena podle regionu",
    file: "price_by_region.json",
    inputs: ["metric", "regions"],
  },
  category_distribution: {
    label: "Ceny podle kategorií",
    file: "category_distribution.json",
    inputs: ["metric", "categories"],
  },
  price_trend: {
    label: "Cenový trend",
    file: "price_trend.json",
    inputs: ["category", "region"],
  },
};
