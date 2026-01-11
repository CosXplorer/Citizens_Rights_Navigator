import ReactMarkdown from "react-markdown";

export default function ResponseCard({ response }) {
  return (
    <div className="card">
      <ReactMarkdown>{response}</ReactMarkdown>
    </div>
  );
}
