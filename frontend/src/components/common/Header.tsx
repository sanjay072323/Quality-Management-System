export default function Header() {
  return (
    <header className="header">
      <div>
        <p className="eyebrow">Life Sciences • AI-First CRM</p>
        <h1>HCP Log Interaction Screen</h1>
        <p className="subtle">
          Dual mode logging for field representatives: structured form or conversational AI assistant.
        </p>
      </div>
      <div className="badge-group">
        <span className="badge">React</span>
        <span className="badge">Redux</span>
        <span className="badge">FastAPI</span>
        <span className="badge">LangGraph</span>
        <span className="badge">Groq</span>
      </div>
    </header>
  );
}
