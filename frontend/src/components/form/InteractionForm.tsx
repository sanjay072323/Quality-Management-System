import { FormEvent, useMemo, useState } from 'react';
import { useAppDispatch, useAppSelector } from '../../app/hooks';
import { createFormInteraction } from '../../features/interactions/interactionsSlice';

export default function InteractionForm() {
  const dispatch = useAppDispatch();
  const hcps = useAppSelector((state) => state.hcps.items);
  const submitting = useAppSelector((state) => state.interactions.submitting);
  const defaultHcp = useMemo(() => hcps[0]?.id ?? 1, [hcps]);
  const [form, setForm] = useState({
    hcp_id: defaultHcp,
    interaction_type: 'Visit',
    channel: 'In-person',
    interaction_date: new Date().toISOString().slice(0, 10),
    raw_notes:
      'Discussed treatment adherence, physician requested outcome data for moderate-risk patients, and asked whether samples are available for eligible patients.',
  });

  const onSubmit = (event: FormEvent) => {
    event.preventDefault();
    dispatch(createFormInteraction({ ...form, hcp_id: Number(form.hcp_id) }));
  };

  return (
    <section className="card">
      <div className="section-heading">
        <h3>Structured Form Mode</h3>
        <p className="subtle">Fast entry for reps who already know what fields to fill.</p>
      </div>
      <form className="grid-form" onSubmit={onSubmit}>
        <label>
          HCP
          <select value={form.hcp_id} onChange={(e) => setForm({ ...form, hcp_id: Number(e.target.value) })}>
            {hcps.map((hcp) => (
              <option key={hcp.id} value={hcp.id}>
                {hcp.full_name} — {hcp.specialty}
              </option>
            ))}
          </select>
        </label>
        <label>
          Interaction Type
          <select value={form.interaction_type} onChange={(e) => setForm({ ...form, interaction_type: e.target.value })}>
            <option>Visit</option>
            <option>Call</option>
            <option>Email</option>
            <option>CME Discussion</option>
          </select>
        </label>
        <label>
          Channel
          <select value={form.channel} onChange={(e) => setForm({ ...form, channel: e.target.value })}>
            <option>In-person</option>
            <option>Phone</option>
            <option>Email</option>
            <option>Virtual</option>
          </select>
        </label>
        <label>
          Interaction Date
          <input
            type="date"
            value={form.interaction_date}
            onChange={(e) => setForm({ ...form, interaction_date: e.target.value })}
          />
        </label>
        <label className="span-2">
          Raw Notes
          <textarea
            rows={8}
            value={form.raw_notes}
            onChange={(e) => setForm({ ...form, raw_notes: e.target.value })}
          />
        </label>
        <button className="primary-btn span-2" disabled={submitting} type="submit">
          {submitting ? 'Submitting...' : 'Log Interaction with AI'}
        </button>
      </form>
    </section>
  );
}
