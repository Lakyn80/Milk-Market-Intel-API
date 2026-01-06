function ReportActions({ labels, reportText }) {
  const disabled = !reportText;

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(reportText);
    } catch (err) {
      console.error("Copy failed", err);
    }
  };

  const download = (ext) => {
    const blob = new Blob([reportText], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `report.${ext}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 shadow-lg shadow-black/20 flex flex-wrap gap-3">
      <button
        disabled={disabled}
        onClick={handleCopy}
        className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-100 hover:border-slate-500 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {labels.copy}
      </button>
      <button
        disabled={disabled}
        onClick={() => download("txt")}
        className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-100 hover:border-slate-500 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {labels.downloadTxt}
      </button>
      <button
        disabled={disabled}
        onClick={() => download("md")}
        className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-100 hover:border-slate-500 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {labels.downloadMd}
      </button>
    </div>
  );
}

export default ReportActions;
