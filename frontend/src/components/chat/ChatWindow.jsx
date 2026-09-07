import { useRef, useEffect, useState } from 'react'
import { useChat } from '../../hooks/useChat.js'
import ChatHeader from './ChatHeader.jsx'
import MessageBubble from './MessageBubble.jsx'
import TypingIndicator from './TypingIndicator.jsx'
import InputBar from './InputBar.jsx'

export default function ChatWindow() {
  const { messages, isTyping, sendMessage, invoiceCount, clearChat, handleUpload } = useChat()
  const chatRef = useRef(null)
  const [isDragging, setIsDragging] = useState(false)

  function handleFileSelect(file) {
    // Directly trigger backend upload with real File object
    // No text message needed - upload handler will add messages
    handleUpload(file)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    e.dataTransfer.dropEffect = 'copy' // Show copy cursor
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const files = e.dataTransfer.files
    if (files.length > 0) {
      // Handle first file (could loop for multiple files)
      handleUpload(files[0])
    }
  }

  // Scroll to bottom when messages or typing state changes
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight
    }
  }, [messages, isTyping])

  return (
    <div
      className={`kb-chatWindow ${isDragging ? 'drag-over' : ''}`}
      ref={chatRef}
      onDragover={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <ChatHeader
        title="KiranaBot"
        invoiceCount={invoiceCount ?? 0}
        isTyping={isTyping}
        onClear={clearChat}
      />
      <div className="kb-chatBody">
        <div className="kb-dateChip">
          <span>
            {new Date().toLocaleDateString('en-IN', {
              day: 'numeric', month: 'long', year: 'numeric'
            }).toUpperCase()}
          </span>
        </div>
        {messages.map((m) => (
          <MessageBubble key={m.id} role={m.role} text={m.text} time={m.time} />
        ))}
        {isTyping ? <TypingIndicator /> : null}
      </div>
      <InputBar onSend={sendMessage} onFileSelect={handleFileSelect} />
    </div>
  )
}