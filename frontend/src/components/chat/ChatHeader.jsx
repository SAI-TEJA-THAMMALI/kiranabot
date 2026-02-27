export default function ChatHeader({ title }) {
  return (
    <>
      {/* Main header */}
      <div className="kb-chatHeader">
        <div className="kb-chatAvatar">🛒</div>
        <div className="kb-chatHeaderInfo">
          <div className="kb-chatTitle">{title}</div>
          <div className="kb-chatSub">online</div>
        </div>
        <div className="kb-headerActions">
          {/* Search icon */}
          <button className="kb-iconBtn" title="Search">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
              <path d="M15.009 13.805h-.636l-.22-.219a5.184 5.184 0 0 0 1.256-3.386 5.207 5.207 0 1 0-5.207 5.208 5.183 5.183 0 0 0 3.385-1.255l.221.22v.635l4.004 3.999 1.194-1.195-3.997-4.007zm-4.808 0a3.605 3.605 0 1 1 0-7.21 3.605 3.605 0 0 1 0 7.21z"/>
            </svg>
          </button>
          {/* Menu icon */}
          <button className="kb-iconBtn" title="Menu">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
              <path d="M12 7a2 2 0 1 0-.001-4.001A2 2 0 0 0 12 7zm0 2a2 2 0 1 0-.001 3.999A2 2 0 0 0 12 9zm0 6a2 2 0 1 0-.001 3.999A2 2 0 0 0 12 15z"/>
            </svg>
          </button>
        </div>
      </div>

      {/* Session bar below header */}
      <div className="kb-sessionBar">
        <div className="kb-sessionPill">
          <span className="kb-sessionDot" />
          Feb 2026 · Session #A3F2
        </div>
        <span className="kb-invoiceCount">0 invoices processed</span>
      </div>
    </>
  )
}