export default function SampleQueries({ onSelect }) {
    const samples = [
      "My electricity bill is very high",
      "I lost 5000 rupees in cyber fraud",
      "Police is refusing to file my FIR",
      "My PF withdrawal is delayed",
      "My passport application is stuck",
      "My college is not refunding my fees",
      "My bank charged me wrong fees",
    ];
  
    return (
      <div className="sample-box">
        <p className="sample-title">🧪 Try sample queries</p>
        <div className="sample-grid">
          {samples.map((q, i) => (
            <button
              key={i}
              className="sample-btn"
              onClick={() => onSelect(q)}
            >
              {q}
            </button>
          ))}
        </div>
      </div>
    );
  }
  