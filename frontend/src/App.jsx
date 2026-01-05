import Dashboard from "./pages/Dashboard.jsx";

function App() {
  return (
    <div className="app-shell">
      <h1 style={{ marginBottom: "12px" }}>Milk Market Intel — Dashboard</h1>
      <p style={{ marginTop: 0, color: "#94a3b8" }}>
        UI-only pohled na existující CSV/JSON výstupy z analytiky (žádné nové
        výpočty v UI).
      </p>
      <Dashboard />
    </div>
  );
}

export default App;
