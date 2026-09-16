/**
 * Minimal, dependency-free domain seam for the later React and FastAPI layers.
 * Names and amounts intentionally represent demo-only, synthetic data.
 */
export const workflowStages = [
  'requested',
  'quoted',
  'approved',
  'delivered',
  'paid',
];

export function createSyntheticFixture() {
  return {
    purchaseRequest: { id: 'req-aster', title: 'Request-Aster', stage: 'quoted' },
    supplierQuote: { id: 'quote-aster', requestId: 'req-aster', quotedCost: 480 },
    approval: { id: 'approval-aster', requestId: 'req-aster', state: 'pending' },
    delivery: { id: 'delivery-aster', requestId: 'req-aster', dueDate: '2030-01-15' },
    payment: { id: 'payment-aster', requestId: 'req-aster', state: 'unpaid' },
  };
}
