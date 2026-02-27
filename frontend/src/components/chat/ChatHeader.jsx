export default function ChatHeader({ title }) {
  return (
    <div className="kb-chatHeader">
      <div className="kb-chatAvatar">🛒</div>
      <div className="kb-chatHeaderInfo">
        <div className="kb-chatTitle">{title}</div>
        <div className="kb-chatSub">
          <span className="kb-onlineDot" />
          GST invoice assistant · demo
        </div>
      </div>
    </div>
  )
}