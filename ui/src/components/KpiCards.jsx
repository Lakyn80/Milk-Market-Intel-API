function formatNumber(value) {
  if (value === undefined || value === null) return "—";
  return Number(value).toLocaleString("en-US");
}

function KpiCards({ metrics }) {
  if (!metrics) return null;

  const items = [
    { label: "Total products", value: formatNumber(metrics.total_products) },
    { label: "Regions", value: formatNumber(metrics.distinct_regions) },
    { label: "Categories", value: formatNumber(metrics.distinct_categories) },
    { label: "Avg price", value: metrics.avg_price?.toFixed(2) ?? "—" },
  ];

  return (
    <div className="kpi-grid">
      {items.map((item) => (
        <div key={item.label} className="kpi">
          <div className="label">{item.label}</div>
          <div className="value">{item.value}</div>
        </div>
      ))}
    </div>
  );
}

export default KpiCards;
