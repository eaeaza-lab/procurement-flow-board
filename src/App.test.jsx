import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import App from './App.jsx';
import { fetchRequests } from './api.js';

vi.mock('./api.js', () => ({ fetchRequests: vi.fn() }));

const requests = [
  { id: 'req-aster', title: 'Request-Aster', stage: 'quoted', margin_cents: 24000, margin_percent: 33.33, delivery_delay_days: 0, is_delivery_delayed: false },
  { id: 'req-birch', title: 'Request-Birch', stage: 'approved', margin_cents: 57000, margin_percent: 32.02, delivery_delay_days: 3, is_delivery_delayed: true },
];

describe('Procurement board', () => {
  afterEach(cleanup);
  beforeEach(() => { fetchRequests.mockResolvedValue(requests); });

  it('groups local requests by every workflow stage and shows risk indicators', async () => {
    render(<App />);
    expect(await screen.findByText('Request-Aster')).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Requested' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Paid' })).toBeInTheDocument();
    expect(screen.getByRole('article', { name: 'Request-Birch' })).toHaveTextContent('3d late');
    expect(screen.getAllByLabelText('1 requests')).toHaveLength(2);
  });

  it('filters cards by title or request ID', async () => {
    const user = userEvent.setup();
    render(<App />);
    await screen.findByText('Request-Aster');
    await user.type(screen.getByRole('searchbox', { name: 'Search requests' }), 'birch');
    expect(screen.queryByText('Request-Aster')).not.toBeInTheDocument();
    expect(screen.getByText('Request-Birch')).toBeInTheDocument();
  });
});
