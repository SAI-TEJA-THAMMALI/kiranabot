export default function SessionBadge({ sessionId }) {
  return <span className="kb-badge">Session: {sessionId || '—'}</span>
}

