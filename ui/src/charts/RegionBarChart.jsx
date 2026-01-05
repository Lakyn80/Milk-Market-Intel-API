import Plot from "react-plotly.js";

function RegionBarChart({ data }) {
  if (!data || data.length === 0) return null;

  const regions = data.map((row) => row.region ?? "UNKNOWN");
  const counts = data.map((row) => Number(row.product_count) || 0);

  return (
    <div className="card">
      <h3 className="chart-title">Produkty podle regionu</h3>
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
