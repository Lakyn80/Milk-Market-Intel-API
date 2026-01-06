import { Fragment, useState } from "react";
import { Listbox, Transition } from "@headlessui/react";
import { Globe2, ChevronsUpDown } from "lucide-react";
import Dashboard from "./pages/Dashboard.jsx";
import ReportsPage from "./pages/ReportsPage.jsx";
import PageLayout from "./components/layout/PageLayout.jsx";

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

const LANG_OPTIONS = [
  { code: "cs", label: "Čeština" },
  { code: "en", label: "English" },
  { code: "ru", label: "Русский" },
];

function App() {
  const [lang, setLang] = useState("cs");
  const t = TEXTS[lang];

  return (
    <PageLayout>
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full bg-slate-800/60 px-3 py-1 text-xs text-slate-300">
            <Globe2 size={14} />
            B2B Analytics Dashboard
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
                  {LANG_OPTIONS.find((o) => o.code === lang)?.label || lang.toUpperCase()}
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
                  {LANG_OPTIONS.map((option) => (
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
      <Dashboard lang={lang} />
      <div className="h-px w-full bg-slate-800 my-4"></div>
      <ReportsPage lang={lang} onLangChange={setLang} />
    </PageLayout>
  );
}

export default App;
