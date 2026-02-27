export default function MessageBubble({ role, text, time }) {
  const isUser = role === 'user'
  const timestamp = time ?? new Date().toLocaleTimeString([], {
    hour: '2-digit', minute: '2-digit'
  })

  return (
    <div className={`kb-bubbleRow ${isUser ? 'kb-rightAlign' : 'kb-leftAlign'}`}>
      <div className={`kb-bubble ${isUser ? 'kb-user' : 'kb-bot'}`}>
        {text}
        <div className="kb-bubbleFooter">
          <span className="kb-bubbleTime">{timestamp}</span>
          {isUser && <span className="kb-ticks">✓✓</span>}
        </div>
      </div>
    </div>
  )
}