import { useState } from "react";
import { buildReport } from "../api/reportsApi";
import ReportForm from "../components/ReportForm.jsx";
import ReportViewer from "../components/ReportViewer.jsx";
import ReportActions from "../components/ReportActions.jsx";

const LABELS = {
  cs: {
    title: "Report builder",
    subtitle: "Generuj textové reporty nad předpočítanými daty (LLM nic nepočítá).",
    form: {
      reportType: "Typ reportu",
      types: {
        market_overview: "Přehled trhu",
        region_comparison: "Porovnání regionů",
        category_deep_dive: "Detail kategorie",
      },
      language: "Jazyk",
      regions: "Regiony (čárkou nebo mezerou)",
      regionsPlaceholder: "Moscow 54",
      category: "Kategorie",
      categoryPlaceholder: "йогурт",
      submit: "Vytvořit report",
      loading: "Pracuji...",
    },
    viewer: {
      title: "Report",
      empty: "Zatím žádný report.",
      meta: "Metadata",
    },
    actions: {
      copy: "Kopírovat",
      downloadTxt: "Stáhnout TXT",
      downloadMd: "Stáhnout MD",
    },
    error: "Chyba při generování reportu",
  },
  en: {
    title: "Report builder",
    subtitle: "Generate text reports on precomputed data (LLM does not calculate).",
    form: {
      reportType: "Report type",
      types: {
        market_overview: "Market overview",
        region_comparison: "Region comparison",
        category_deep_dive: "Category deep dive",
      },
      language: "Language",
      regions: "Regions (comma or space separated)",
      regionsPlaceholder: "Moscow 54",
      category: "Category",
      categoryPlaceholder: "йогурт",
      submit: "Build report",
      loading: "Working...",
    },
    viewer: {
      title: "Report",
      empty: "No report yet.",
      meta: "Metadata",
    },
    actions: {
      copy: "Copy",
      downloadTxt: "Download TXT",
      downloadMd: "Download MD",
    },
    error: "Error while generating report",
  },
  ru: {
    title: "Конструктор отчётов",
    subtitle: "Генерируйте текстовые отчёты по готовым данным (LLM не считает).",
    form: {
      reportType: "Тип отчёта",
      types: {
        market_overview: "Обзор рынка",
        region_comparison: "Сравнение регионов",
        category_deep_dive: "Категория подробно",
      },
      language: "Язык",
      regions: "Регионы (через запятую или пробел)",
      regionsPlaceholder: "Moscow 54",
      category: "Категория",
      categoryPlaceholder: "йогурт",
      submit: "Собрать отчёт",
      loading: "Думаю...",
    },
    viewer: {
      title: "Отчёт",
      empty: "Отчёта пока нет.",
      meta: "Метаданные",
    },
    actions: {
      copy: "Копировать",
      downloadTxt: "Скачать TXT",
      downloadMd: "Скачать MD",
    },
    error: "Ошибка при генерации отчёта",
  },
};

function ReportsPage({ lang, onLangChange }) {
  const t = LABELS[lang] || LABELS.en;
  const [reportText, setReportText] = useState("");
  const [meta, setMeta] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (payload) => {
    setLoading(true);
    setError("");
    setReportText("");
    setMeta({});
    try {
      const resp = await buildReport(payload);
      setReportText(resp.report_text || "");
      setMeta(resp.meta || {});
    } catch (err) {
      setError(err.message || t.error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-1">
        <h2 className="text-xl font-semibold text-slate-50">{t.title}</h2>
        <p className="text-sm text-slate-400">{t.subtitle}</p>
      </div>

      <ReportForm
        labels={t.form}
        lang={lang}
        onLangChange={onLangChange}
        onSubmit={handleSubmit}
        loading={loading}
      />

      {error && (
        <div className="rounded-lg border border-red-500/50 bg-red-900/30 px-3 py-2 text-sm text-red-100">
          {t.error}: {error}
        </div>
      )}

      <ReportActions labels={t.actions} reportText={reportText} />
      <ReportViewer labels={t.viewer} reportText={reportText} meta={meta} />
    </div>
  );
}

export default ReportsPage;
