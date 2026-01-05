function PageLayout({ children }) {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-6xl mx-auto px-6 py-6 flex flex-col gap-5">
        {children}
      </div>
    </div>
  );
}

export default PageLayout;
