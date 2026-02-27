import { useState } from 'react'
import AttachmentButton from './AttachmentButton.jsx'

export default function InputBar({ onSend }) {
  const [text, setText] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    const trimmed = text.trim()
    if (!trimmed) return
    onSend(trimmed)
    setText('')
  }

  return (
    <form className="kb-inputBar" onSubmit={handleSubmit}>
      <AttachmentButton onClick={() => alert('Upload demo placeholder')} />
      <input
        className="kb-input"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type a message…"
      />
      <button className="kb-sendBtn" type="submit">
        Send
      </button>
    </form>
  )
}

