import { useEffect, useState } from "react";
import Header from "./components/Header";
import QueryInput from "./components/QueryInput";
import ResponseCard from "./components/ResponseCard";
import { askGrievance } from "./services/api";

function App() {
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState("EN");
  const [dark, setDark] = useState(false);

  useEffect(() => {
    document.documentElement.setAttribute(
      "data-theme",
      dark ? "dark" : "light"
    );
  }, [dark]);

  const handleQuery = async (query) => {
    if (!query.trim()) return;

    setLoading(true);
    setResponse("");

    try {
      const data = await askGrievance(query);
      setResponse(data.response);
    } catch {
      setResponse("❌ Could not connect to backend");
    }

    setLoading(false);
  };

  return (
    <div style={{ maxWidth: "900px", margin: "auto", padding: "20px" }}>
      <Header
        language={language}
        setLanguage={setLanguage}
        dark={dark}
        setDark={setDark}
      />

      <QueryInput onSubmit={handleQuery} />

      {loading && <p>⏳ Processing...</p>}
      {response && <ResponseCard response={response} />}
    </div>
  );
}

export default App;
