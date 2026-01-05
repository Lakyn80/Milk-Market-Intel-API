function SectionCard({ title, description, children, className = "" }) {
  return (
    <section
      className={`rounded-2xl border border-slate-800 bg-slate-900/70 p-5 shadow-lg shadow-black/20 ${className}`}
    >
      {(title || description) && (
        <header className="mb-4">
          {title && <h3 className="text-lg font-semibold text-slate-50">{title}</h3>}
          {description && <p className="text-sm text-slate-400 mt-1">{description}</p>}
        </header>
      )}
      {children}
    </section>
  );
}

export default SectionCard;
