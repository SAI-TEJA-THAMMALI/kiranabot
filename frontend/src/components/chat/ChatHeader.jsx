export default function ChatHeader({ title, invoiceCount = 0, isTyping = false, onClear }) {
  const now = new Date()
  const month = now.toLocaleString('default', { month: 'long' })
  const year = now.getFullYear()
  const sessionId = 'A3F2'

  return (
    <>
      {/* Main header */}
      <div className="kb-chatHeader">
        <div className="kb-chatAvatar">🛒</div>
        <div className="kb-chatHeaderInfo">
          <div className="kb-chatTitle">{title}</div>
          <div className="kb-chatSub">
            {isTyping ? 'KiranaBot is reading your invoice...' : 'online'}
          </div>
        </div>
        <div className="kb-headerActions">
          {/* Invoice counter badge */}
          {invoiceCount > 0 && (
            <div className="kb-invoiceBadge">
              {invoiceCount} invoice{invoiceCount > 1 ? 's' : ''} processed
            </div>
          )}
          {/* Clear chat button */}
          {onClear && (
            <button
              className="kb-clearBtn"
              onClick={onClear}
              title="Clear chat"
              aria-label="Clear chat"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
              </svg>
            </button>
          )}
        </div>
      </div>

      {/* Session bar */}
      <div className="kb-sessionBar">
        <div className="kb-sessionPill">
          <span className="kb-sessionDot" />
          📅 {month} {year} · Session #{sessionId}
        </div>
        <span className="kb-invoiceCount">
          {invoiceCount === 0
            ? '0 invoices processed'
            : `${invoiceCount} invoice${invoiceCount > 1 ? 's' : ''} processed`}
        </span>
      </div>
    </>
  )
}