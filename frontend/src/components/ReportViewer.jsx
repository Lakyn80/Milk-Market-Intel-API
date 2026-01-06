function ReportViewer({ labels, reportText, meta }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 shadow-lg shadow-black/20">
      <h3 className="text-base font-semibold text-slate-100 mb-2">{labels.title}</h3>
      {reportText ? (
        <pre className="whitespace-pre-wrap text-sm text-slate-100 leading-relaxed">{reportText}</pre>
      ) : (
        <div className="text-sm text-slate-400">{labels.empty}</div>
      )}
      {meta && Object.keys(meta).length > 0 && (
        <div className="mt-3 text-xs text-slate-400">
          <div className="font-semibold text-slate-300 mb-1">{labels.meta}</div>
          <pre className="whitespace-pre-wrap">{JSON.stringify(meta, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default ReportViewer;
