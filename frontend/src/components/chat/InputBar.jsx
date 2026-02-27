import { useRef, useState } from 'react'
import AttachmentButton from './AttachmentButton.jsx'

export default function InputBar({ onSend }) {
  const [text, setText] = useState('')
  const fileInputRef = useRef(null)

  function handleSubmit(e) {
    e.preventDefault()
    const trimmed = text.trim()
    if (!trimmed) return
    onSend(trimmed)
    setText('')
  }

  function handleAttachClick() {
    if (fileInputRef.current) {
      fileInputRef.current.click()
    }
  }

  function handleFileChange(e) {
    const file = e.target.files?.[0]
    if (!file) return

    // For now we just echo that an invoice was selected into the chat.
    onSend(`📄 Invoice selected: ${file.name}`)

    // reset input so selecting the same file again still triggers change
    e.target.value = ''
  }

  return (
    <form className="kb-inputBar" onSubmit={handleSubmit}>
      <AttachmentButton onClick={handleAttachClick} />
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
      <input
        className="kb-input"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type a message…"
      />
      <button className="kb-sendBtn" type="submit">
        ➤
      </button>
    </form>
  )
}

