import { Fragment, useState } from "react";
import { Listbox, Transition } from "@headlessui/react";
import { Globe2, ChevronsUpDown } from "lucide-react";
import Dashboard from "./pages/Dashboard.jsx";
import ReportsPage from "./pages/ReportsPage.jsx";
import PageLayout from "./components/layout/PageLayout.jsx";
import PlotSelector from "./bi/PlotSelector.jsx";
import PlotRenderer from "./bi/PlotRenderer.jsx";

const LANG_CODES = ["cs", "en", "ru"];

const LANGUAGE_LABELS = {
  cs: {
    cs: "Čeština",
    en: "Angličtina",
    ru: "Ruština",
  },
  en: {
    cs: "Czech",
    en: "English",
    ru: "Russian",
  },
  ru: {
    cs: "Чешский",
    en: "Английский",
    ru: "Русский",
  },
};

const TEXTS = {
  en: {
    badge: "B2B Analytics Dashboard",
    title: "Milk Market Intel — Dashboard",
    subtitle:
      "Read-only view of precomputed analytics CSV/JSON outputs (no calculations in UI).",
    language: "Language",
    biTitle: "BI visualizations",
    plotLabels: {
      plotType: "Plot type",
      metric: "Metric",
      metrics: {
        avg_price: "Average",
        median_price: "Median",
        min_price: "Minimum",
        max_price: "Maximum",
      },
      regions: "Regions",
      regionsPlaceholder: "Moscow 54",
      categories: "Categories",
      categoriesPlaceholder: "milk yogurt",
      category: "Category",
      categoryPlaceholder: "milk",
      region: "Region",
      regionPlaceholder: "Moscow",
      apply: "Load chart",
    },
    plotStatus: {
      loading: "Loading chart...",
      error: "Error",
      empty: "Select a chart to view.",
    },
  },
  cs: {
    badge: "B2B analytický přehled",
    title: "Milk Market Intel — Přehled",
    subtitle: "Pouze čtení hotových CSV/JSON z analytiky (žádné výpočty v UI).",
    language: "Jazyk",
    biTitle: "BI vizualizace",
    plotLabels: {
      plotType: "Typ grafu",
      metric: "Metrika",
      metrics: {
        avg_price: "Průměr",
        median_price: "Medián",
        min_price: "Minimum",
        max_price: "Maximum",
      },
      regions: "Regiony",
      regionsPlaceholder: "Moskva 54",
      categories: "Kategorie",
      categoriesPlaceholder: "mléko jogurt",
      category: "Kategorie",
      categoryPlaceholder: "mléko",
      region: "Region",
      regionPlaceholder: "Moskva",
      apply: "Načíst graf",
    },
    plotStatus: {
      loading: "Načítám graf...",
      error: "Chyba",
      empty: "Vyber graf pro zobrazení.",
    },
  },
  ru: {
    badge: "B2B аналитическая панель",
    title: "Milk Market Intel — Дашборд",
    subtitle:
      "Только чтение готовых CSV/JSON из аналитики (никаких вычислений в UI).",
    language: "Язык",
    biTitle: "BI визуализации",
    plotLabels: {
      plotType: "Тип графика",
      metric: "Метрика",
      metrics: {
        avg_price: "Среднее",
        median_price: "Медиана",
        min_price: "Минимум",
        max_price: "Максимум",
      },
      regions: "Регионы",
      regionsPlaceholder: "Москва 54",
      categories: "Категории",
      categoriesPlaceholder: "молоко йогурт",
      category: "Категория",
      categoryPlaceholder: "молоко",
      region: "Регион",
      regionPlaceholder: "Москва",
      apply: "Загрузить график",
    },
    plotStatus: {
      loading: "Загружаю график...",
      error: "Ошибка",
      empty: "Выберите график для просмотра.",
    },
  },
};

function App() {
  const [lang, setLang] = useState("cs");
  const [selectedPlot, setSelectedPlot] = useState({ plot: "price_by_region" });
  const t = TEXTS[lang] || TEXTS.en;
  const languageOptions = LANG_CODES.map((code) => ({
    code,
    label: LANGUAGE_LABELS[lang]?.[code] || LANGUAGE_LABELS.en[code] || code.toUpperCase(),
  }));

  return (
    <PageLayout>
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full bg-slate-800/60 px-3 py-1 text-xs text-slate-300">
            <Globe2 size={14} />
            {t.badge}
          </div>
          <h1 className="text-2xl font-bold mt-2 text-slate-50">{t.title}</h1>
          <p className="text-sm text-slate-400">{t.subtitle}</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-slate-300 text-sm">{t.language}:</span>
          <Listbox value={lang} onChange={setLang}>
            <div className="relative w-40">
              <Listbox.Button className="relative w-full cursor-default rounded-lg border border-slate-700 bg-slate-900 py-2 pl-3 pr-10 text-left text-sm text-slate-100 shadow-sm hover:border-slate-500">
                <span className="block truncate">
                  {languageOptions.find((o) => o.code === lang)?.label || lang.toUpperCase()}
                </span>
                <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2 text-slate-400">
                  <ChevronsUpDown size={16} />
                </span>
              </Listbox.Button>
              <Transition
                as={Fragment}
                leave="transition ease-in duration-100"
                leaveFrom="opacity-100"
                leaveTo="opacity-0"
              >
                <Listbox.Options className="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-slate-900 py-1 text-sm shadow-lg ring-1 ring-slate-700 ring-opacity-5 focus:outline-none">
                  {languageOptions.map((option) => (
                    <Listbox.Option
                      key={option.code}
                      className={({ active }) =>
                        `relative cursor-default select-none py-2 pl-3 pr-4 ${
                          active ? "bg-slate-800 text-slate-50" : "text-slate-200"
                        }`
                      }
                      value={option.code}
                    >
                      {option.label}
                    </Listbox.Option>
                  ))}
                </Listbox.Options>
              </Transition>
            </div>
          </Listbox>
        </div>
      </div>
      <Dashboard lang={lang} languageOptions={languageOptions} />
      <div className="h-px w-full bg-slate-800 my-4"></div>
      <ReportsPage
        lang={lang}
        onLangChange={setLang}
        languageOptions={languageOptions}
      />
      <div className="h-px w-full bg-slate-800 my-4"></div>
      <div className="space-y-4">
        <h2 className="text-xl font-semibold text-slate-50">{t.biTitle}</h2>
        <PlotSelector
          labels={t.plotLabels}
          lang={lang}
          onChange={(sel) => setSelectedPlot(sel)}
        />
        <PlotRenderer selection={selectedPlot} labels={t.plotStatus} lang={lang} />
      </div>
    </PageLayout>
  );
}

export default App;
