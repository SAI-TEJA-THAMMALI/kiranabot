import { useState } from 'react'
import AttachmentButton from './AttachmentButton.jsx'

export default function InputBar({ onSend, onFileSelect }){
  const [text, setText] = useState('')

  function handleSend() {
    if (!text.trim()) return
    onSend(text.trim())
    setText('')
  }

  return (
    <div className="kb-inputBar">
      <div className="kb-inputWrap">

        <input
          className="kb-input"
          placeholder="Type a message"
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
        />

        {/* Attach button */}
        <AttachmentButton onFileSelect={onFileSelect} />

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