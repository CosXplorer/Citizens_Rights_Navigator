export default function Header({ language, setLanguage, dark, setDark }) {
  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        gap: "10px",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: "20px",
      }}
    >
      <h1 style={{ fontSize: "22px", margin: 0 }}>
        🧑‍⚖️ Citizen Grievance Navigator AI
      </h1>

      <div
        style={{
          display: "flex",
          gap: "8px",
          flexWrap: "wrap",
        }}
      >
        <button
          onClick={() => setLanguage(language === "EN" ? "HI" : "EN")}
          style={{ padding: "8px 12px" }}
        >
          🌐 {language}
        </button>

        <button
          onClick={() => setDark(!dark)}
          style={{ padding: "8px 12px" }}
        >
          {dark ? "☀️ Light" : "🌙 Dark"}
        </button>
      </div>
    </div>
  );
}
