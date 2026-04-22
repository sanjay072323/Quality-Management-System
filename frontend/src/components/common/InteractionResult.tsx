import type { Interaction } from '../../features/interactions/interactionsSlice';

export default function InteractionResult({ data }: { data?: Interaction }) {
  if (!data) {
    return (
      <section className="card result-card">
        <h3>AI Output</h3>
        <p className="subtle">Submit a form or a chat interaction to view the saved AI-enriched result.</p>
      </section>
    );
  }

  return (
    <section className="card result-card">
      <div className="result-top">
        <h3>Saved Interaction #{data.id}</h3>
        <span className={`status ${data.compliance_status === 'reviewed' ? 'ok' : 'warn'}`}>
          {data.compliance_status}
        </span>
      </div>
      <div className="result-block">
        <strong>AI Summary</strong>
        <p>{data.ai_summary}</p>
      </div>
      <div className="result-block">
        <strong>Topics</strong>
        <p>{data.key_topics}</p>
      </div>
      <div className="result-block">
        <strong>Next Best Action</strong>
        <p>{data.next_best_action}</p>
      </div>
      <div className="result-block">
        <strong>Follow-up Email</strong>
        <pre>{data.follow_up_email}</pre>
      </div>
    </section>
  );
}
