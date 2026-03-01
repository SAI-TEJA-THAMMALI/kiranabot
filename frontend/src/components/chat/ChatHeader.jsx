export default function ChatHeader({ title, invoiceCount = 0, isTyping = false }) {
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