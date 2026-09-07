const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const API = {

  health: async () => {
    try {
      const r = await fetch(`${BASE}/ping`)
      return await r.json()
    } catch {
      return { status: 'offline' }
    }
  },

  createSession: async (period) => {
    try {
      const r = await fetch(
        `${BASE}/create-session?period=${period}`,
        { method: 'POST' }
      )
      return await r.json()
    } catch {
      return { id: `local-${Date.now()}`, period }
    }
  },

  uploadInvoice: async (file, sessionId) => {
    try {
      const form = new FormData()
      form.append('file', file)
      form.append('session_id', sessionId || 'default')
      const r = await fetch(
        `${BASE}/upload-invoice`,
        { method: 'POST', body: form }
      )
      return await r.json()
    } catch (e) {
      return { status: 'error', message: e.message }
    }
  },

  exportGSTR1: async (sessionId) => {
    try {
      const r = await fetch(
        `${BASE}/export-gstr1/${sessionId}`
      )
      if (!r.ok) throw new Error('Export failed')
      const blob = await r.blob()
      const url  = URL.createObjectURL(blob)
      const a    = document.createElement('a')
      a.href     = url
      a.download = `GSTR1_${sessionId}.csv`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
      return { status: 'downloaded' }
    } catch (e) {
      return { status: 'error', message: e.message }
    }
  }
}