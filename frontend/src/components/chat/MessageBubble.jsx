export default function MessageBubble({ role, text }) {
  const isUser = role === 'user'
  return (
    <div className={`kb-bubbleRow ${isUser ? 'kb-rightAlign' : 'kb-leftAlign'}`}>
      <div className={`kb-bubble ${isUser ? 'kb-user' : 'kb-bot'}`}>{text}</div>
    </div>
  )
}

