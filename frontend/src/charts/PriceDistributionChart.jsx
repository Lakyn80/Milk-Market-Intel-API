import Plot from "react-plotly.js";

function PriceDistributionChart({ data, title }) {
  if (!data || data.length === 0) return null;

  const prices = data
    .map((row) => Number(row.price_value))
    .filter((v) => Number.isFinite(v));

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/70 p-4 shadow">
      <h3 className="text-base font-semibold text-slate-100 mb-2">{title}</h3>
      <Plot
        data={[
          {
            type: "histogram",
            x: prices,
            marker: { color: "#34d399" },
            nbinsx: 30,
          },
        ]}
        layout={{
          autosize: true,
          margin: { t: 20, r: 10, b: 50, l: 50 },
          paper_bgcolor: "#111827",
          plot_bgcolor: "#111827",
          font: { color: "#e5e7eb" },
          bargap: 0.05,
        }}
        style={{ width: "100%", height: 360 }}
        useResizeHandler
        config={{ displayModeBar: false }}
      />
    </div>
  );
}

export default PriceDistributionChart;
