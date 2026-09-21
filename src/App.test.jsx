import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import App from './App.jsx';
import { fetchRequestDetail, fetchRequests } from './api.js';

vi.mock('./api.js', () => ({ fetchRequestDetail: vi.fn(), fetchRequests: vi.fn() }));

const requests = [
  { id: 'req-aster', title: 'Request-Aster', stage: 'quoted', margin_cents: 24000, margin_percent: 33.33, delivery_delay_days: 0, is_delivery_delayed: false },
  { id: 'req-birch', title: 'Request-Birch', stage: 'approved', margin_cents: 57000, margin_percent: 32.02, delivery_delay_days: 3, is_delivery_delayed: true },
];

describe('Procurement board', () => {
  afterEach(cleanup);
  beforeEach(() => {
    fetchRequests.mockResolvedValue(requests);
    fetchRequestDetail.mockResolvedValue({ ...requests[0], quotes: [{ id: 'quote-aster', quoted_cost_cents: 48000, valid_until: '2030-02-01' }], approvals: [], deliveries: [], payments: [] });
  });

  it('groups local requests by every workflow stage and shows risk indicators', async () => {
    render(<App />);
    expect((await screen.findAllByText('Request-Aster'))[0]).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Requested' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Paid' })).toBeInTheDocument();
    expect(screen.getByRole('article', { name: 'Request-Birch' })).toHaveTextContent('3d late');
    expect(screen.getAllByLabelText('1 requests')).toHaveLength(2);
  });

  it('filters cards by title or request ID', async () => {
    const user = userEvent.setup();
    render(<App />);
    await screen.findAllByText('Request-Aster');
    await user.type(screen.getByRole('searchbox', { name: 'Search requests' }), 'birch');
    expect(screen.queryByText('Request-Aster')).not.toBeInTheDocument();
    expect(screen.getAllByText('Request-Birch')[0]).toBeInTheDocument();
  });

  it('sorts and filters the request table, then opens linked details', async () => {
    const user = userEvent.setup();
    render(<App />);
    await screen.findAllByText('Request-Aster');
    await user.click(screen.getByRole('button', { name: 'Title' }));
    expect(screen.getAllByRole('row')[1]).toHaveTextContent('Request-Aster');
    await user.selectOptions(screen.getByLabelText('Filter stage'), 'approved');
    expect(screen.getByRole('table')).toHaveTextContent('Request-Birch');
    expect(screen.getByRole('table')).not.toHaveTextContent('Request-Aster');
    await user.click(screen.getAllByRole('button', { name: 'View details' })[0]);
    expect(await screen.findByLabelText('Request detail')).toHaveTextContent('Quotes');
    expect(fetchRequestDetail).toHaveBeenCalledWith('req-birch');
  });
});
