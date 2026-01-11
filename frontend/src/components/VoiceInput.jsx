export default function VoiceInput({ onResult }) {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
  
    const startListening = () => {
      if (!SpeechRecognition) {
        alert("Speech recognition not supported in this browser.");
        return;
      }
  
      const recognition = new SpeechRecognition();
  
      // 🌐 Detect browser language
      const browserLang = navigator.language || "en-US";
  
      // If browser language is Hindi → hi-IN, else English
      recognition.lang = browserLang.startsWith("hi") ? "hi-IN" : "en-US";
  
      recognition.interimResults = false;
      recognition.continuous = false;
  
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        onResult(transcript);
      };
  
      recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
      };
  
      recognition.start();
    };
  
    return (
      <button
        onClick={startListening}
        style={{
          padding: "10px 15px",
          background: "#eee",
          borderRadius: "6px",
          cursor: "pointer",
        }}
      >
        🎤 Speak
      </button>
    );
  }
  