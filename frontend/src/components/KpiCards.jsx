import { Layers, MapPin, Package2, Wallet } from "lucide-react";
import StatCard from "./layout/StatCard.jsx";

function formatNumber(value, locale) {
  if (value === undefined || value === null) return "—";
  return Number(value).toLocaleString(locale || "en");
}

function KpiCards({ metrics, labels, locale }) {
  if (!metrics) return null;

  const items = [
    { label: labels.totalProducts, value: formatNumber(metrics.total_products, locale), icon: Package2 },
    { label: labels.regions, value: formatNumber(metrics.distinct_regions, locale), icon: MapPin },
    { label: labels.categories, value: formatNumber(metrics.distinct_categories, locale), icon: Layers },
    {
      label: labels.avgPrice,
      value:
        metrics.avg_price === null || metrics.avg_price === undefined
          ? "—"
          : metrics.avg_price.toLocaleString(locale || "en", {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            }),
      icon: Wallet,
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {items.map((item) => (
        <StatCard key={item.label} icon={item.icon} label={item.label} value={item.value} />
      ))}
    </div>
  );
}

export default KpiCards;
