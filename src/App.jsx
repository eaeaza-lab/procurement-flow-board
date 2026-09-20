import { useEffect, useMemo, useState } from 'react';

import { fetchRequests } from './api.js';

export const STAGES = [
  { id: 'requested', label: 'Requested' },
  { id: 'quoted', label: 'Quoted' },
  { id: 'approved', label: 'Approved' },
  { id: 'delivered', label: 'Delivered' },
  { id: 'paid', label: 'Paid' },
];

export function formatCurrency(cents) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
  }).format(cents / 100);
}

function statusLabel(request) {
  if (request.is_delivery_delayed) return `${request.delivery_delay_days}d late`;
  if (request.margin_percent !== null && request.margin_percent < 20) return 'Low margin';
  return 'On track';
}

function RequestCard({ request }) {
  const lowMargin = request.margin_percent !== null && request.margin_percent < 20;
  const status = statusLabel(request);

  return (
    <article className="request-card" aria-label={request.title}>
      <div className="card-title-row">
        <h3>{request.title}</h3>
        <span className={`indicator ${request.is_delivery_delayed ? 'is-late' : lowMargin ? 'is-risk' : 'is-ok'}`}>
          {status}
        </span>
      </div>
      <p className="request-id">{request.id}</p>
      <dl className="metrics">
        <div><dt>Margin</dt><dd>{formatCurrency(request.margin_cents)}</dd></div>
        <div><dt>Margin rate</dt><dd>{request.margin_percent === null ? '—' : `${request.margin_percent}%`}</dd></div>
      </dl>
    </article>
  );
}

export default function App() {
  const [requests, setRequests] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    fetchRequests()
      .then((items) => active && setRequests(items))
      .catch((reason) => active && setError(reason.message))
      .finally(() => active && setLoading(false));
    return () => { active = false; };
  }, []);

  const filteredRequests = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();
    if (!normalizedQuery) return requests;
    return requests.filter(({ id, title }) =>
      `${id} ${title}`.toLowerCase().includes(normalizedQuery),
    );
  }, [query, requests]);

  return (
    <main className="app-shell">
      <header className="app-header">
        <div>
          <p className="eyebrow">Local demo workspace</p>
          <h1>Procurement flow</h1>
        </div>
        <label className="search-label" htmlFor="request-search">
          <span>Search requests</span>
          <input id="request-search" type="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Title or request ID" />
        </label>
      </header>

      {loading && <p role="status" className="message">Loading local requests…</p>}
      {error && <p role="alert" className="message error">{error}</p>}
      {!loading && !error && (
        <section className="board" aria-label="Procurement stages">
          {STAGES.map((stage) => {
            const cards = filteredRequests.filter((request) => request.stage === stage.id);
            return (
              <section className="stage-column" key={stage.id} aria-labelledby={`${stage.id}-heading`}>
                <header><h2 id={`${stage.id}-heading`}>{stage.label}</h2><span aria-label={`${cards.length} requests`}>{cards.length}</span></header>
                <div className="card-stack">
                  {cards.map((request) => <RequestCard key={request.id} request={request} />)}
                  {cards.length === 0 && <p className="empty-stage">No matching requests</p>}
                </div>
              </section>
            );
          })}
        </section>
      )}
    </main>
  );
}
