import { useState } from "react";
import Dashboard from "./pages/Dashboard.jsx";

const TEXTS = {
  en: {
    title: "Milk Market Intel — Dashboard",
    subtitle:
      "Read-only view of existing analytics CSV/JSON outputs (no calculations in UI).",
    language: "Language",
  },
  cs: {
    title: "Milk Market Intel — Dashboard",
    subtitle:
      "Jen čtení existujících CSV/JSON výstupů z analytiky (žádné výpočty v UI).",
    language: "Jazyk",
  },
  ru: {
    title: "Milk Market Intel — Дашборд",
    subtitle:
      "Только чтение готовых CSV/JSON из аналитики (никаких вычислений в UI).",
    language: "Язык",
  },
};

function App() {
  const [lang, setLang] = useState("cs");
  const t = TEXTS[lang];

  return (
    <div className="max-w-6xl mx-auto px-6 py-6">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between mb-4">
        <div>
          <h1 className="text-2xl font-bold">{t.title}</h1>
          <p className="text-sm text-slate-400">{t.subtitle}</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-slate-300 text-sm">{t.language}:</span>
          <div className="flex gap-2">
            {["cs", "en", "ru"].map((code) => (
              <button
                key={code}
                onClick={() => setLang(code)}
                className={`px-3 py-1 rounded border text-sm ${
                  lang === code
                    ? "bg-slate-200 text-slate-900 border-slate-300"
                    : "border-slate-700 text-slate-200 hover:border-slate-400"
                }`}
              >
                {code.toUpperCase()}
              </button>
            ))}
          </div>
        </div>
      </div>
      <Dashboard lang={lang} />
    </div>
  );
}

export default App;
