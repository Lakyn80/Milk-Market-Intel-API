import Plot from "react-plotly.js";

function CategoryBarChart({ data, title }) {
  if (!data || data.length === 0) return null;

  const categories = data.map((row) => row.category || "UNKNOWN");
  const avgPrices = data.map((row) => Number(row.avg_price) || 0);

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/70 p-4 shadow">
      <h3 className="text-base font-semibold text-slate-100 mb-2">{title}</h3>
      <Plot
        data={[
          {
            type: "bar",
            x: categories,
            y: avgPrices,
            marker: { color: "#a78bfa" },
          },
        ]}
        layout={{
          autosize: true,
          margin: { t: 20, r: 10, b: 80, l: 60 },
          paper_bgcolor: "#111827",
          plot_bgcolor: "#111827",
          font: { color: "#e5e7eb" },
          xaxis: { tickangle: -35 },
        }}
        style={{ width: "100%", height: 360 }}
        useResizeHandler
        config={{ displayModeBar: false }}
      />
    </div>
  );
}

export default CategoryBarChart;
