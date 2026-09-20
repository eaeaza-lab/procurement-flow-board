/** Fetches only from the companion local FastAPI service through Vite's local proxy. */
export async function fetchRequests() {
  const response = await fetch('/api/requests');
  if (!response.ok) {
    throw new Error(`The local board data could not be loaded (${response.status}).`);
  }
  return response.json();
}
