import { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import { loadCsv } from "../loaders/loadCsv.js";
import { PLOT_CONFIG, PLOT_HOVER_LABELS } from "./plotConfig";

const PRICE_DISTRIBUTION_PATH = "/data/analytics/price_distribution.csv";
const MEDIAN_CACHE = {
  region: null,
  category: null,
  loading: null,
};

const DTYPE_MAP = {
  f8: Float64Array,
  f4: Float32Array,
  i4: Int32Array,
  i2: Int16Array,
  i1: Int8Array,
  u4: Uint32Array,
  u2: Uint16Array,
  u1: Uint8Array,
};

function decodeBinaryArray(encoded) {
  if (!encoded || typeof encoded !== "object" || !encoded.bdata || !encoded.dtype) {
    return encoded;
  }
  const raw = atob(encoded.bdata);
  const buffer = new ArrayBuffer(raw.length);
  const view = new Uint8Array(buffer);
  for (let i = 0; i < raw.length; i += 1) {
    view[i] = raw.charCodeAt(i);
  }
  const ArrayType = DTYPE_MAP[encoded.dtype] || Float64Array;
  const data = new ArrayType(buffer);
  const shape = encoded.shape
    ? String(encoded.shape)
        .split(",")
        .map((value) => Number.parseInt(value.trim(), 10))
        .filter((value) => Number.isFinite(value))
    : [];
  if (shape.length <= 1) {
    return Array.from(data);
  }
  const [rows, cols] = shape;
  const matrix = [];
  for (let row = 0; row < rows; row += 1) {
    const start = row * cols;
    matrix.push(Array.from(data.slice(start, start + cols)));
  }
  return matrix;
}

function localizeHoverTemplate(template, labels) {
  if (!template || !labels) return template;
  const entries = Object.entries(labels).sort((a, b) => b[0].length - a[0].length);
  return entries.reduce(
    (acc, [key, value]) => acc.split(`${key}=`).join(`${value}=`),
    template,
  );
}

function replaceHoverMetricKey(template, metric) {
  if (!template || metric === "avg_price") return template;
  return template.replace(/avg_price=%\{y\}/g, `${metric}=%{y}`);
}

function getCustomDataMatrix(customdata) {
  if (Array.isArray(customdata)) return customdata;
  return decodeBinaryArray(customdata);
}

function extractMetricFromCustomdata(customdata, index) {
  const matrix = getCustomDataMatrix(customdata);
  if (!Array.isArray(matrix) || !Array.isArray(matrix[0])) return null;
  return matrix.map((row) => row[index]);
}

function computeMedian(values) {
  if (!values.length) return null;
  values.sort((a, b) => a - b);
  const mid = Math.floor(values.length / 2);
  if (values.length % 2) return values[mid];
  return (values[mid - 1] + values[mid]) / 2;
}

function buildMedianMap(buckets) {
  const output = new Map();
  buckets.forEach((values, key) => {
    output.set(key, computeMedian(values));
  });
  return output;
}

async function ensureMedianMaps() {
  if (MEDIAN_CACHE.region && MEDIAN_CACHE.category) {
    return MEDIAN_CACHE;
  }
  if (MEDIAN_CACHE.loading) {
    return MEDIAN_CACHE.loading;
  }

  MEDIAN_CACHE.loading = loadCsv(PRICE_DISTRIBUTION_PATH)
    .then((rows) => {
      const regionBuckets = new Map();
      const categoryBuckets = new Map();

      rows.forEach((row) => {
        const price = Number(row.price_value);
        if (!Number.isFinite(price)) return;

        const regionKey = row.region ? String(row.region).trim() : "";
        if (regionKey) {
          const bucket = regionBuckets.get(regionKey) || [];
          bucket.push(price);
          regionBuckets.set(regionKey, bucket);
        }

        const categoryKey = row.category ? String(row.category).trim() : "";
        if (categoryKey) {
          const bucket = categoryBuckets.get(categoryKey) || [];
          bucket.push(price);
          categoryBuckets.set(categoryKey, bucket);
        }
      });

      MEDIAN_CACHE.region = buildMedianMap(regionBuckets);
      MEDIAN_CACHE.category = buildMedianMap(categoryBuckets);
      return MEDIAN_CACHE;
    })
    .finally(() => {
      MEDIAN_CACHE.loading = null;
    });

  return MEDIAN_CACHE.loading;
}

function getMetricValues(trace, cfg, metric, medianMaps) {
  if (metric === "avg_price") return null;
  if (metric === "median_price") {
    const source = cfg.metricSource;
    const map =
      source === "region"
        ? medianMaps?.region
        : source === "category"
          ? medianMaps?.category
          : null;
    if (!map) return null;
    const xValues = Array.isArray(trace.x) ? trace.x : decodeBinaryArray(trace.x);
    if (!Array.isArray(xValues)) return null;
    return xValues.map((value) => {
      if (value === null || value === undefined) return null;
      const key = String(value);
      return map.get(key) ?? null;
    });
  }

  const index = cfg.metricColumns?.[metric];
  if (index === undefined) return null;
  return extractMetricFromCustomdata(trace.customdata, index);
}

function prepareFigure(figure, cfg, lang, metric, medianMaps) {
  if (!figure) return figure;
  const layout = { ...figure.layout };
  const layoutLabels = cfg?.layout;
  const langKey = layoutLabels?.title?.[lang] ? lang : "en";

  if (layoutLabels?.title?.[langKey]) {
    layout.title = { ...(layout.title || {}), text: layoutLabels.title[langKey] };
  }
  if (layoutLabels?.x?.[langKey]) {
    layout.xaxis = {
      ...(layout.xaxis || {}),
      title: { ...(layout.xaxis?.title || {}), text: layoutLabels.x[langKey] },
    };
  }
  if (layoutLabels?.y?.[langKey]) {
    layout.yaxis = {
      ...(layout.yaxis || {}),
      title: { ...(layout.yaxis?.title || {}), text: layoutLabels.y[langKey] },
    };
  }
  if (layoutLabels?.legend?.[langKey]) {
    layout.legend = {
      ...(layout.legend || {}),
      title: { ...(layout.legend?.title || {}), text: layoutLabels.legend[langKey] },
    };
  }

  const hoverLabels = PLOT_HOVER_LABELS[lang] || PLOT_HOVER_LABELS.en;
  const applyMetric = cfg?.inputs?.includes("metric");
  let metricApplied = false;

  const data = Array.isArray(figure.data)
    ? figure.data.map((trace) => {
        const updated = { ...trace };
        if (applyMetric) {
          const metricValues = getMetricValues(updated, cfg, metric, medianMaps);
          if (Array.isArray(metricValues)) {
            updated.y = metricValues;
            updated.hovertemplate = replaceHoverMetricKey(updated.hovertemplate, metric);
            metricApplied = true;
          }
        }
        updated.hovertemplate = localizeHoverTemplate(updated.hovertemplate, hoverLabels);
        return updated;
      })
    : figure.data;

  if (metricApplied) {
    const metricLabel = hoverLabels[metric];
    if (metricLabel) {
      layout.yaxis = {
        ...(layout.yaxis || {}),
        title: { ...(layout.yaxis?.title || {}), text: metricLabel },
      };
    }
  }

  return { ...figure, layout, data };
}

function PlotRenderer({ selection, labels, lang }) {
  const [figure, setFigure] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let isActive = true;
    if (!selection?.plot) return undefined;
    const cfg = PLOT_CONFIG[selection.plot];
    if (!cfg) return undefined;

    const metric = selection.metric || "avg_price";

    async function loadFigure() {
      setLoading(true);
      setError("");
      setFigure(null);

      try {
        const url = `/data/analytics/plots/${cfg.file}`;
        const resp = await fetch(url);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();
        const medianMaps =
          metric === "median_price" && cfg.inputs.includes("metric")
            ? await ensureMedianMaps()
            : null;
        const nextFigure = prepareFigure(data, cfg, lang, metric, medianMaps);
        if (isActive) {
          setFigure(nextFigure);
        }
      } catch (err) {
        if (isActive) {
          setError(err.message);
        }
      } finally {
        if (isActive) {
          setLoading(false);
        }
      }
    }

    loadFigure();
    return () => {
      isActive = false;
    };
  }, [selection, lang]);

  if (loading) {
    return <div className="text-sm text-slate-300">{labels.loading}</div>;
  }
  if (error) {
    return (
      <div className="text-sm text-red-400">
        {labels.error}: {error}
      </div>
    );
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
