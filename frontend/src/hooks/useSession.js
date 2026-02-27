import { useMemo } from 'react'

export function useSession() {
  return useMemo(() => ({ sessionId: 'demo_session' }), [])
}

