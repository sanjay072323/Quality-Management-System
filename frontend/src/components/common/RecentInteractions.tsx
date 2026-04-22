import type { Interaction } from '../../features/interactions/interactionsSlice';

export default function RecentInteractions({ items }: { items: Interaction[] }) {
  return (
    <section className="card">
      <div className="section-heading">
        <h3>Recent Interactions</h3>
        <p className="subtle">Shows what got stored through the AI workflow.</p>
      </div>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>HCP</th>
              <th>Type</th>
              <th>Channel</th>
              <th>Date</th>
              <th>Compliance</th>
            </tr>
          </thead>
          <tbody>
            {items.length === 0 ? (
              <tr>
                <td colSpan={6}>No interactions logged yet.</td>
              </tr>
            ) : (
              items.map((item) => (
                <tr key={item.id}>
                  <td>{item.id}</td>
                  <td>{item.hcp_id}</td>
                  <td>{item.interaction_type}</td>
                  <td>{item.channel}</td>
                  <td>{item.interaction_date}</td>
                  <td>{item.compliance_status}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
