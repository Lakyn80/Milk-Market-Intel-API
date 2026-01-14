import { useState } from "react";
import { PLOT_CONFIG } from "./plotConfig";

function PlotSelector({ labels, lang, onChange }) {
  const [plot, setPlot] = useState("price_by_region");
  const [metric, setMetric] = useState("avg_price");
  const [regions, setRegions] = useState("");
  const [categories, setCategories] = useState("");
  const [category, setCategory] = useState("");
  const [region, setRegion] = useState("");

  const handleApply = (e) => {
    e.preventDefault();
    const payload = { plot, metric, regions, categories, category, region };
    onChange(payload);
  };

  const cfg = PLOT_CONFIG[plot];

  return (
    <form className="flex flex-col gap-3" onSubmit={handleApply}>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div className="flex flex-col gap-1">
          <label className="text-sm text-slate-300">{labels.plotType}</label>
          <select
            value={plot}
            onChange={(e) => setPlot(e.target.value)}
            className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:border-slate-500 focus:outline-none"
          >
            {Object.entries(PLOT_CONFIG).map(([key, cfg]) => (
              <option key={key} value={key}>
                {cfg.labels?.[lang] || cfg.labels?.en || key}
              </option>
            ))}
          </select>
        </div>
        {cfg.inputs.includes("metric") && (
          <div className="flex flex-col gap-1">
            <label className="text-sm text-slate-300">{labels.metric}</label>
            <select
              value={metric}
              onChange={(e) => setMetric(e.target.value)}
              className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:border-slate-500 focus:outline-none"
            >
              <option value="avg_price">{labels.metrics.avg_price}</option>
              <option value="median_price">{labels.metrics.median_price}</option>
              <option value="min_price">{labels.metrics.min_price}</option>
              <option value="max_price">{labels.metrics.max_price}</option>
            </select>
          </div>
        )}
      </div>

      {cfg.inputs.includes("regions") && (
        <div className="flex flex-col gap-1">
          <label className="text-sm text-slate-300">{labels.regions}</label>
          <input
            value={regions}
            onChange={(e) => setRegions(e.target.value)}
            placeholder={labels.regionsPlaceholder}
            className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:border-slate-500 focus:outline-none"
          />
        </div>
      )}

      {cfg.inputs.includes("categories") && (
        <div className="flex flex-col gap-1">
          <label className="text-sm text-slate-300">{labels.categories}</label>
          <input
            value={categories}
            onChange={(e) => setCategories(e.target.value)}
            placeholder={labels.categoriesPlaceholder}
            className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:border-slate-500 focus:outline-none"
          />
        </div>
      )}

      {cfg.inputs.includes("category") && (
        <div className="flex flex-col gap-1">
          <label className="text-sm text-slate-300">{labels.category}</label>
          <input
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            placeholder={labels.categoryPlaceholder}
            className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:border-slate-500 focus:outline-none"
          />
        </div>
      )}

      {cfg.inputs.includes("region") && (
        <div className="flex flex-col gap-1">
          <label className="text-sm text-slate-300">{labels.region}</label>
          <input
            value={region}
            onChange={(e) => setRegion(e.target.value)}
            placeholder={labels.regionPlaceholder}
            className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:border-slate-500 focus:outline-none"
          />
        </div>
      )}

      <button
        type="submit"
        className="self-start rounded-lg bg-indigo-500 px-4 py-2 text-sm font-semibold text-white shadow hover:bg-indigo-400"
      >
        {labels.apply}
      </button>
    </form>
  );
}

export default PlotSelector;
