const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}`)
  if (!res.ok) throw new Error(`Request failed: ${res.status}`)
  return await res.json()
}

