import { useState } from "react";

const REPORT_TYPES = [
  { value: "market_overview", label: "Market overview" },
  { value: "region_comparison", label: "Region comparison" },
  { value: "category_deep_dive", label: "Category deep dive" },
];

const DEFAULT_LANG_OPTIONS = [
  { code: "cs", label: "Čeština" },
  { code: "en", label: "English" },
  { code: "ru", label: "Русский" },
];

function ReportForm({
  labels,
  lang,
  languageOptions,
  onLangChange,
  onSubmit,
  loading,
}) {
  const [type, setType] = useState("market_overview");
  const [regions, setRegions] = useState("");
  const [category, setCategory] = useState("");
  const options = languageOptions?.length ? languageOptions : DEFAULT_LANG_OPTIONS;

  const handleSubmit = (e) => {
    e.preventDefault();
    const payload = {
      type,
      lang,
    };
    if (type === "region_comparison" && regions.trim()) {
      payload.regions = regions.split(/[,\\s]+/).filter(Boolean);
    }
    if (type === "category_deep_dive" && category.trim()) {
      payload.category = category.trim();
    }
    onSubmit(payload);
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div className="flex flex-col gap-1">
          <label className="text-sm text-slate-300">{labels.reportType}</label>
          <select
            className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:border-slate-500 focus:outline-none"
            value={type}
            onChange={(e) => setType(e.target.value)}
          >
            {REPORT_TYPES.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {labels.types[opt.value]}
              </option>
            ))}
          </select>
        </div>
        <div className="flex flex-col gap-1">
          <label className="text-sm text-slate-300">{labels.language}</label>
          <select
            className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:border-slate-500 focus:outline-none"
            value={lang}
            onChange={(e) => onLangChange(e.target.value)}
          >
            {options.map((option) => (
              <option key={option.code} value={option.code}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {type === "region_comparison" && (
        <div className="flex flex-col gap-1">
          <label className="text-sm text-slate-300">{labels.regions}</label>
          <input
            className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:border-slate-500 focus:outline-none"
            placeholder={labels.regionsPlaceholder}
            value={regions}
            onChange={(e) => setRegions(e.target.value)}
          />
        </div>
      )}

      {type === "category_deep_dive" && (
        <div className="flex flex-col gap-1">
          <label className="text-sm text-slate-300">{labels.category}</label>
          <input
            className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:border-slate-500 focus:outline-none"
            placeholder={labels.categoryPlaceholder}
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          />
        </div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="self-start rounded-lg bg-blue-500 px-4 py-2 text-sm font-semibold text-white shadow hover:bg-blue-400 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {loading ? labels.loading : labels.submit}
      </button>
    </form>
  );
}

export default ReportForm;
