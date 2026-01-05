function formatNumber(value, locale) {
  if (value === undefined || value === null) return "—";
  return Number(value).toLocaleString(locale || "en");
}

function KpiCards({ metrics, labels, locale }) {
  if (!metrics) return null;

  const items = [
    { label: labels.totalProducts, value: formatNumber(metrics.total_products, locale) },
    { label: labels.regions, value: formatNumber(metrics.distinct_regions, locale) },
    { label: labels.categories, value: formatNumber(metrics.distinct_categories, locale) },
    {
      label: labels.avgPrice,
      value:
        metrics.avg_price === null || metrics.avg_price === undefined
          ? "—"
          : metrics.avg_price.toLocaleString(locale || "en", {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            }),
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
      {items.map((item) => (
        <div
          key={item.label}
          className="rounded-lg border border-slate-800 bg-slate-900/70 px-3 py-3 shadow"
        >
          <div className="text-xs uppercase tracking-wide text-slate-400">{item.label}</div>
          <div className="text-2xl font-bold mt-1 text-slate-50">{item.value}</div>
        </div>
      ))}
    </div>
  );
}

export default KpiCards;
