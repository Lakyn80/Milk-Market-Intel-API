export const PLOT_CONFIG = {
  price_by_region: {
    file: "price_by_region.json",
    inputs: ["metric", "regions"],
    metricSource: "region",
    metricColumns: {
      min_price: 1,
      max_price: 2,
    },
    labels: {
      cs: "Cena podle regionu",
      en: "Price by region",
      ru: "Цена по регионам",
    },
    layout: {
      title: {
        cs: "Cena podle regionu",
        en: "Price by region",
        ru: "Цена по регионам",
      },
      x: {
        cs: "Region",
        en: "Region",
        ru: "Регион",
      },
      y: {
        cs: "Průměrná cena",
        en: "Average price",
        ru: "Средняя цена",
      },
    },
  },
  category_distribution: {
    file: "category_distribution.json",
    inputs: ["metric", "categories"],
    metricSource: "category",
    metricColumns: {
      min_price: 0,
      max_price: 1,
    },
    labels: {
      cs: "Ceny podle kategorií",
      en: "Prices by category",
      ru: "Цены по категориям",
    },
    layout: {
      title: {
        cs: "Ceny podle kategorií",
        en: "Prices by category",
        ru: "Цены по категориям",
      },
      x: {
        cs: "Kategorie",
        en: "Category",
        ru: "Категория",
      },
      y: {
        cs: "Průměrná cena",
        en: "Average price",
        ru: "Средняя цена",
      },
    },
  },
  price_trend: {
    file: "price_trend.json",
    inputs: ["category", "region"],
    labels: {
      cs: "Cenový trend",
      en: "Price trend",
      ru: "Ценовой тренд",
    },
    layout: {
      title: {
        cs: "Cenový trend",
        en: "Price trend",
        ru: "Ценовой тренд",
      },
      x: {
        cs: "Pořadí",
        en: "Sequence",
        ru: "Порядок",
      },
      y: {
        cs: "Cena",
        en: "Price",
        ru: "Цена",
      },
      legend: {
        cs: "Kategorie",
        en: "Category",
        ru: "Категория",
      },
    },
  },
};

export const PLOT_HOVER_LABELS = {
  cs: {
    region: "Region",
    avg_price: "Průměrná cena",
    median_price: "Medián ceny",
    region_code: "Kód regionu",
    min_price: "Min. cena",
    max_price: "Max. cena",
    product_count: "Počet produktů",
    category: "Kategorie",
    sequence: "Pořadí",
    price_value: "Cena",
  },
  en: {
    region: "Region",
    avg_price: "Average price",
    median_price: "Median price",
    region_code: "Region code",
    min_price: "Min price",
    max_price: "Max price",
    product_count: "Product count",
    category: "Category",
    sequence: "Sequence",
    price_value: "Price",
  },
  ru: {
    region: "Регион",
    avg_price: "Средняя цена",
    median_price: "Медианная цена",
    region_code: "Код региона",
    min_price: "Мин. цена",
    max_price: "Макс. цена",
    product_count: "Количество товаров",
    category: "Категория",
    sequence: "Порядок",
    price_value: "Цена",
  },
};
