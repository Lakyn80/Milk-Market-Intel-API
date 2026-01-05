import Plot from "react-plotly.js";

function RegionBarChart({ data, title }) {
  if (!data || data.length === 0) return null;

  const regions = data.map((row) => row.region ?? "UNKNOWN");
  const counts = data.map((row) => Number(row.product_count) || 0);

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 shadow-lg shadow-black/20">
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
          margin: { t: 20, r: 10, b: 70, l: 60 },
          paper_bgcolor: "#0f172a",
          plot_bgcolor: "#0f172a",
          font: { color: "#e5e7eb" },
          xaxis: { tickangle: -35, tickfont: { size: 11 } },
          yaxis: { gridcolor: "rgba(255,255,255,0.05)" },
        }}
        style={{ width: "100%", height: 360 }}
        useResizeHandler
        config={{ displayModeBar: false }}
      />
    </div>
  );
}

export default RegionBarChart;
