import { useState } from "react";
import VoiceInput from "./VoiceInput";

const SAMPLE_QUERIES = [
  "My electricity bill is very high",
  "I lost 5000 rupees in cyber fraud",
  "Police is refusing to file my FIR",
  "My PF withdrawal is delayed",
  "My passport application is stuck",
  "My college is not refunding my fees",
  "My bank charged me wrong fees",
];

export default function QueryInput({ onSubmit }) {
  const [query, setQuery] = useState("");

  const handleSampleClick = (text) => {
    setQuery(text);
    onSubmit(text); // auto submit
  };

  return (
    <div className="card">
      <textarea
        placeholder="Ask your grievance (type or speak)..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{
          width: "100%",
          height: "100px",
          padding: "12px",
          fontSize: "16px",
          borderRadius: "10px",
          border: "1px solid #ccc",
          resize: "none",
        }}
      />

      <div
        style={{
          display: "flex",
          gap: "10px",
          marginTop: "12px",
          flexWrap: "wrap",
        }}
      >
        <VoiceInput onResult={setQuery} />

        <button
          onClick={() => onSubmit(query)}
          style={{
            background: "var(--accent)",
            color: "white",
            padding: "10px 16px",
            borderRadius: "8px",
            border: "none",
            cursor: "pointer",
          }}
        >
          Submit
        </button>
      </div>

      {/* Sample Queries */}
      <div style={{ marginTop: "20px" }}>
        <p style={{ fontWeight: "600", marginBottom: "8px" }}>
          🧪 Try sample queries
        </p>

        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: "8px",
          }}
        >
          {SAMPLE_QUERIES.map((q, i) => (
            <button
              key={i}
              onClick={() => handleSampleClick(q)}
              style={{
                background: "#f1f5f9",
                border: "none",
                padding: "8px 12px",
                borderRadius: "8px",
                cursor: "pointer",
                fontSize: "14px",
              }}
            >
              {q}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
