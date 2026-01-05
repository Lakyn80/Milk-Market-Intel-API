import { useEffect, useState } from "react";
import CategoryBarChart from "../charts/CategoryBarChart.jsx";
import PriceDistributionChart from "../charts/PriceDistributionChart.jsx";
import RegionBarChart from "../charts/RegionBarChart.jsx";
import KpiCards from "../components/KpiCards.jsx";
import { loadCsv } from "../loaders/loadCsv.js";
import { loadJson } from "../loaders/loadJson.js";

const BASE = "../../../backend/data/analytics";

const PATHS = {
  overview: `${BASE}/overview_metrics.json`,
  region: `${BASE}/region_summary.csv`,
  category: `${BASE}/category_summary.csv`,
  distribution: `${BASE}/price_distribution.csv`,
};

function Dashboard() {
  const [overview, setOverview] = useState(null);
  const [regionData, setRegionData] = useState([]);
  const [categoryData, setCategoryData] = useState([]);
  const [distributionData, setDistributionData] = useState([]);
  const [error, setError] = useState(null);

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
        setError(err.message || "Data load failed");
      }
    }
    loadAll();
  }, []);

  if (error) {
    return <div className="card">Chyba načítání dat: {error}</div>;
  }

  return (
    <div className="grid">
      <div className="card">
        <h3 className="chart-title">Klíčové metriky</h3>
        <KpiCards metrics={overview} />
      </div>
      <div className="grid two">
        <RegionBarChart data={regionData} />
        <CategoryBarChart data={categoryData} />
      </div>
      <PriceDistributionChart data={distributionData} />
    </div>
  );
}

export default Dashboard;
