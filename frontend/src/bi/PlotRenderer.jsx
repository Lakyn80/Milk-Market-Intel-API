import { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import { PLOT_CONFIG } from "./plotConfig";

function PlotRenderer({ selection, labels }) {
  const [figure, setFigure] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!selection?.plot) return;
    const cfg = PLOT_CONFIG[selection.plot];
    if (!cfg) return;

    setLoading(true);
    setError("");
    setFigure(null);

    const url = `/data/analytics/plots/${cfg.file}`;
    fetch(url)
      .then((resp) => {
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        return resp.json();
      })
      .then((data) => setFigure(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [selection]);

  if (loading) {
    return <div className="text-sm text-slate-300">{labels.loading}</div>;
  }
  if (error) {
    return <div className="text-sm text-red-400">{labels.error}: {error}</div>;
  }
  if (!figure) {
    return <div className="text-sm text-slate-400">{labels.empty}</div>;
  }

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 shadow-lg shadow-black/20">
      <Plot
        data={figure.data}
        layout={figure.layout}
        config={{ displayModeBar: false, responsive: true }}
        style={{ width: "100%", height: "100%" }}
        useResizeHandler
      />
    </div>
  );
}

export default PlotRenderer;
