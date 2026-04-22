import { FormEvent, useState } from 'react';
import { useAppDispatch, useAppSelector } from '../../app/hooks';
import { createChatInteraction } from '../../features/interactions/interactionsSlice';

export default function ChatLogger() {
  const dispatch = useAppDispatch();
  const hcps = useAppSelector((state) => state.hcps.items);
  const submitting = useAppSelector((state) => state.interactions.submitting);
  const [hcpId, setHcpId] = useState<number>(1);
  const [transcript, setTranscript] = useState(
    'I met Dr. Aisha today. She asked about long-term efficacy, wanted more evidence on outcomes, and said she may consider the therapy for selected patients if we share approved data. Please log this and suggest the best follow-up.',
  );

  const onSubmit = (event: FormEvent) => {
    event.preventDefault();
    dispatch(
      createChatInteraction({
        hcp_id: Number(hcpId),
        transcript,
        interaction_date: new Date().toISOString().slice(0, 10),
      }),
    );
  };

  return (
    <section className="card">
      <div className="section-heading">
        <h3>Conversational Chat Mode</h3>
        <p className="subtle">Free-text assistant that converts field notes into structured CRM data.</p>
      </div>
      <form onSubmit={onSubmit} className="chat-layout">
        <label>
          HCP
          <select value={hcpId} onChange={(e) => setHcpId(Number(e.target.value))}>
            {hcps.map((hcp) => (
              <option key={hcp.id} value={hcp.id}>
                {hcp.full_name} — {hcp.city}
              </option>
            ))}
          </select>
        </label>
        <label>
          Conversation / Visit Notes
          <textarea rows={10} value={transcript} onChange={(e) => setTranscript(e.target.value)} />
        </label>
        <button className="secondary-btn" disabled={submitting} type="submit">
          {submitting ? 'Processing...' : 'Convert Chat to Logged Interaction'}
        </button>
      </form>
    </section>
  );
}
