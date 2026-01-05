import Plot from "react-plotly.js";

function RegionBarChart({ data, title }) {
  if (!data || data.length === 0) return null;

  const regions = data.map((row) => row.region ?? "UNKNOWN");
  const counts = data.map((row) => Number(row.product_count) || 0);

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/70 p-4 shadow">
      <h3 className="text-base font-semibold text-slate-100 mb-2">{title}</h3>
      <Plot
        data={[
          {
            type: "bar",
            x: regions,
            y: counts,
            marker: { color: "#38bdf8" },
          },
        ]}
        layout={{
          autosize: true,
          margin: { t: 20, r: 10, b: 60, l: 50 },
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

export default RegionBarChart;
