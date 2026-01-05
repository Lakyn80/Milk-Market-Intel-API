import { useEffect, useMemo, useState } from "react";
import CategoryBarChart from "../charts/CategoryBarChart.jsx";
import PriceDistributionChart from "../charts/PriceDistributionChart.jsx";
import RegionBarChart from "../charts/RegionBarChart.jsx";
import KpiCards from "../components/KpiCards.jsx";
import { loadCsv } from "../loaders/loadCsv.js";
import { loadJson } from "../loaders/loadJson.js";
import { exportCsv, exportJson } from "../reports/exporters.js";
import AiAskBox from "../components/AiAskBox.jsx";

const BASE = "/data/analytics";

const PATHS = {
  overview: `${BASE}/overview_metrics.json`,
  region: `${BASE}/region_summary.csv`,
  category: `${BASE}/category_summary.csv`,
  distribution: `${BASE}/price_distribution.csv`,
};

const LABELS = {
  cs: {
    headline: "Klíčové metriky",
    kpis: {
      totalProducts: "Produkty",
      regions: "Regiony",
      categories: "Kategorie",
      avgPrice: "Průměrná cena",
    },
    charts: {
      regions: "Produkty podle regionu",
      categories: "Průměrná cena podle kategorie",
      distribution: "Distribuce cen (histogram)",
    },
    exports: {
      title: "Export reportů",
      csv: "Export CSV",
      json: "Export JSON",
    },
    error: "Chyba načítání dat",
    ai: {
      title: "AI analýza trhu",
      subtitle: "Zeptej se na předpočítanou analytiku. Model pouze interpretuje existující data.",
      placeholder: "např. Které regiony mají nejvíce produktů?",
      submit: "Zeptat se AI",
      loading: "Pracuji...",
      error: "Chyba",
    },
  },
  en: {
    headline: "Key metrics",
    kpis: {
      totalProducts: "Products",
      regions: "Regions",
      categories: "Categories",
      avgPrice: "Avg price",
    },
    charts: {
      regions: "Products by region",
      categories: "Average price by category",
      distribution: "Price distribution (histogram)",
    },
    exports: {
      title: "Export reports",
      csv: "Export CSV",
      json: "Export JSON",
    },
    error: "Data load failed",
    ai: {
      title: "AI market analysis",
      subtitle: "Ask a question about the precomputed analytics. The model will only interpret existing data.",
      placeholder: "e.g., Which regions have the highest product counts?",
      submit: "Ask AI",
      loading: "Working...",
      error: "Error",
    },
  },
  ru: {
    headline: "Ключевые метрики",
    kpis: {
      totalProducts: "Продукты",
      regions: "Регионы",
      categories: "Категории",
      avgPrice: "Средняя цена",
    },
    charts: {
      regions: "Товары по регионам",
      categories: "Средняя цена по категориям",
      distribution: "Распределение цен (гистограмма)",
    },
    exports: {
      title: "Экспорт отчётов",
      csv: "Экспорт CSV",
      json: "Экспорт JSON",
    },
    error: "Ошибка загрузки данных",
    ai: {
      title: "AI анализ рынка",
      subtitle: "Задай вопрос по готовой аналитике. Модель только интерпретирует уже посчитанные данные.",
      placeholder: "например: Какие регионы лидируют по числу товаров?",
      submit: "Спросить ИИ",
      loading: "Думаю...",
      error: "Ошибка",
    },
  },
};

function Dashboard({ lang }) {
  const [overview, setOverview] = useState(null);
  const [regionData, setRegionData] = useState([]);
  const [categoryData, setCategoryData] = useState([]);
  const [distributionData, setDistributionData] = useState([]);
  const [error, setError] = useState(null);

  const labels = useMemo(() => LABELS[lang] ?? LABELS.cs, [lang]);

  useEffect(() => {
    async function loadAll() {
      try {
        const [overviewJson, regionCsv, categoryCsv, distributionCsv] =
          await Promise.all([
            loadJson(PATHS.overview),
            loadCsv(PATHS.region),
            loadCsv(PATHS.category),
            loadCsv(PATHS.distribution),
          ]);
        setOverview(overviewJson);
        setRegionData(regionCsv);
        setCategoryData(categoryCsv);
        setDistributionData(distributionCsv);
      } catch (err) {
        setError(err.message || labels.error);
      }
    }
    loadAll();
  }, [lang, labels.error]);

  if (error) {
    return (
      <div className="rounded-xl border border-red-500/40 bg-red-900/20 p-4 text-red-100">
        {labels.error}: {error}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="rounded-xl border border-slate-800 bg-slate-900/70 p-4 shadow">
        <h3 className="text-base font-semibold text-slate-100 mb-2">
          {labels.headline}
        </h3>
        <KpiCards metrics={overview} labels={labels.kpis} locale={lang} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <RegionBarChart data={regionData} title={labels.charts.regions} />
        <CategoryBarChart data={categoryData} title={labels.charts.categories} />
      </div>

      <PriceDistributionChart
        data={distributionData}
        title={labels.charts.distribution}
      />

      <div className="rounded-xl border border-slate-800 bg-slate-900/70 p-4 shadow">
        <h3 className="text-base font-semibold text-slate-100 mb-3">
          {labels.exports.title}
        </h3>
        <div className="flex flex-wrap gap-3">
          <button
            className="rounded border border-slate-700 px-3 py-2 text-sm text-slate-100 hover:border-slate-500"
            onClick={() => exportCsv(PATHS.region, "region_summary.csv")}
          >
            {labels.exports.csv} (Region)
          </button>
          <button
            className="rounded border border-slate-700 px-3 py-2 text-sm text-slate-100 hover:border-slate-500"
            onClick={() => exportCsv(PATHS.category, "category_summary.csv")}
          >
            {labels.exports.csv} (Category)
          </button>
          <button
            className="rounded border border-slate-700 px-3 py-2 text-sm text-slate-100 hover:border-slate-500"
            onClick={() => exportCsv(PATHS.distribution, "price_distribution.csv")}
          >
            {labels.exports.csv} (Prices)
          </button>
          <button
            className="rounded border border-slate-700 px-3 py-2 text-sm text-slate-100 hover:border-slate-500"
            onClick={() => exportJson(PATHS.overview, "overview_metrics.json")}
          >
            {labels.exports.json}
          </button>
        </div>
      </div>

      <AiAskBox labels={labels.ai} />
    </div>
  );
}

export default Dashboard;
