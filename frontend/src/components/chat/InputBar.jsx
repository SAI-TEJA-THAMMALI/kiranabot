import { useState } from 'react'
import AttachmentButton from './AttachmentButton.jsx'

export default function InputBar({ onSend }) {
  const [text, setText] = useState('')

  function handleSend() {
    if (!text.trim()) return
    onSend(text.trim())
    setText('')
  }

  return (
    <div className="kb-inputBar">
      <div className="kb-inputWrap">

        {/* Emoji button */}
        <button className="kb-emojiBtn" title="Emoji">
          <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
            <path d="M9.153 11.603c.795 0 1.439-.879 1.439-1.962s-.644-1.962-1.439-1.962-1.439.879-1.439 1.962.644 1.962 1.439 1.962zm-3.204 1.362c-.026-.307-.131 5.218 6.063 5.551 6.066-.25 6.066-5.551 6.066-5.551-6.078 1.416-12.129 0-12.129 0zm11.363 1.108s-.669 1.959-5.051 1.959c-3.505 0-5.388-1.164-5.607-1.959 0 0 5.912 1.055 10.658 0zM11.804 1.011C5.609 1.011.978 6.033.978 12.228s4.826 10.761 11.021 10.761S23.02 18.423 23.02 12.228c.001-6.195-5.021-11.217-11.216-11.217zM12 21.354c-5.273 0-9.381-4.412-9.381-9.127 0-4.716 3.942-9.442 9.215-9.442 5.273 0 9.381 4.726 9.381 9.441S17.273 21.354 12 21.354zm3.108-9.751c.795 0 1.439-.879 1.439-1.962s-.644-1.962-1.439-1.962-1.439.879-1.439 1.962.644 1.962 1.439 1.962z"/>
          </svg>
        </button>

        <input
          className="kb-input"
          placeholder="Type a message"
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
        />

        {/* Attach button */}
        <AttachmentButton />

      </div>

      {/* Send button */}
      <button className="kb-sendBtn" onClick={handleSend} title="Send">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
          <path d="M1.101 21.757 23.8 12.028 1.101 2.3l.011 7.912 13.623 1.816-13.623 1.817-.011 7.912z"/>
        </svg>
      </button>
    </div>
  )
}