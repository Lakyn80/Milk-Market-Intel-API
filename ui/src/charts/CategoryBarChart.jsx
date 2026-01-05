import Plot from "react-plotly.js";

function CategoryBarChart({ data }) {
  if (!data || data.length === 0) return null;

  const categories = data.map((row) => row.category || "UNKNOWN");
  const avgPrices = data.map((row) => Number(row.avg_price) || 0);

  return (
    <div className="card">
      <h3 className="chart-title">Průměrná cena podle kategorie</h3>
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
