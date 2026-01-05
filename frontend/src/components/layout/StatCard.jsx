function StatCard({ icon: Icon, label, value, hint }) {
  return (
    <div className="flex items-start gap-3 rounded-xl border border-slate-800 bg-gradient-to-br from-slate-900/80 via-slate-900 to-slate-950 px-4 py-4 shadow">
      {Icon && (
        <div className="mt-1 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-slate-800 text-slate-200">
          <Icon size={20} />
        </div>
      )}
      <div className="flex-1">
        <div className="text-xs uppercase tracking-wide text-slate-400">{label}</div>
        <div className="text-2xl font-semibold text-slate-50">{value}</div>
        {hint && <div className="text-xs text-slate-500 mt-1">{hint}</div>}
      </div>
    </div>
  );
}

export default StatCard;
