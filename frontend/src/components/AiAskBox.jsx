import { useEffect, useState } from "react";

const API_URL = "/api/v1/ai/ask";

const DEFAULT_LANG_OPTIONS = [
  { code: "cs", label: "Čeština" },
  { code: "en", label: "English" },
  { code: "ru", label: "Русский" },
];

function AiAskBox({ labels, defaultLang = "cs", languageOptions }) {
  const [question, setQuestion] = useState("");
  const [lang, setLang] = useState(defaultLang);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const options = languageOptions?.length ? languageOptions : DEFAULT_LANG_OPTIONS;

  useEffect(() => {
    setLang(defaultLang);
  }, [defaultLang]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setAnswer("");
    try {
      const resp = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, lang }),
      });
      if (!resp.ok) {
        throw new Error(`HTTP ${resp.status}`);
      }
      const data = await resp.json();
      setAnswer(data.answer || "");
    } catch (err) {
      setError(err.message || labels.error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 shadow-lg shadow-black/20">
      <h3 className="text-base font-semibold text-slate-100 mb-2">{labels.title}</h3>
      <p className="text-sm text-slate-400 mb-3">{labels.subtitle}</p>
      <form className="flex flex-col gap-3" onSubmit={handleSubmit}>
        <textarea
          className="min-h-[100px] rounded-lg border border-slate-700 bg-slate-950 p-3 text-slate-100 focus:border-slate-400 focus:outline-none"
          placeholder={labels.placeholder}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          required
        />
        <div className="flex flex-wrap items-center gap-3">
          <select
            className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:border-slate-500 focus:outline-none"
            value={lang}
            onChange={(e) => setLang(e.target.value)}
          >
            {options.map((option) => (
              <option key={option.code} value={option.code}>
                {option.label}
              </option>
            ))}
          </select>
          <button
            type="submit"
            disabled={loading}
            className="rounded-lg bg-blue-500 px-4 py-2 text-sm font-semibold text-white shadow hover:bg-blue-400 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? labels.loading : labels.submit}
          </button>
        </div>
      </form>
      {error && <div className="mt-3 text-sm text-red-400">{labels.error}: {error}</div>}
      {answer && (
        <div className="mt-4 rounded-lg border border-slate-800 bg-slate-950 p-3 text-sm text-slate-100 whitespace-pre-wrap">
          {answer}
        </div>
      )}
    </div>
  );
}

export default AiAskBox;
