import { useState } from 'react'

export default function MessageBubble({ role, text, time }) {
  const isUser = role === 'user'
  const [copied, setCopied] = useState(false)

  // use passed time, or generate now as fallback
  const timestamp = time ?? new Date().toLocaleTimeString('en-IN', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  })

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      // Optionally show a toast
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  return (
    <div className={`kb-bubbleRow ${isUser ? 'kb-right-align' : 'kb-left-align'}`}>
      <div className={`kb-bubble ${isUser ? 'user' : 'bot'}`}>
        {text}
        <div className="kb-bubbleFooter">
          <span className="kb-bubbleTime">{timestamp}</span>
          {isUser && <span className="kb-ticks">✓✓</span>}
          <button
            className="kb-copyBtn"
            onClick={copyToClipboard}
            title={copied ? 'Copied!' : 'Copy'}
            aria-label={copied ? 'Copied!' : 'Copy text'}
          >
            {copied ? '✓' : '📋'}
          </button>
        </div>
      </div>
    </div>
  )
}