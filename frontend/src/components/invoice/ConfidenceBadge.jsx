export default function ConfidenceBadge({ score }) {
  const pct = Math.round((Number(score) || 0) * 100)
  return <span className="kb-badge">Confidence: {pct}%</span>
}

