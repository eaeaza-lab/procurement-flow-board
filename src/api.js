/** Fetches only from the companion local FastAPI service through Vite's local proxy. */
export async function fetchRequests() {
  const response = await fetch('/api/requests');
  if (!response.ok) {
    throw new Error(`The local board data could not be loaded (${response.status}).`);
  }
  return response.json();
}

export async function fetchRequestDetail(requestId) {
  const response = await fetch(`/api/requests/${encodeURIComponent(requestId)}`);
  if (!response.ok) {
    throw new Error(`The local request detail could not be loaded (${response.status}).`);
  }
  return response.json();
}
