import { useChat } from '../../hooks/useChat.js'
import ChatHeader from './ChatHeader.jsx'
import MessageBubble from './MessageBubble.jsx'
import TypingIndicator from './TypingIndicator.jsx'
import InputBar from './InputBar.jsx'

export default function ChatWindow() {
  const { messages, isTyping, sendMessage, invoiceCount } = useChat()

  function handleFileSelect(file) {
    sendMessage(`📎 ${file.name}`)     // keeps chat bubble
    console.log('File ready to upload:', file)
    // Directly trigger backend upload with real File object
    window.dispatchEvent(new CustomEvent('kb-file-upload', {
      detail: file
    }))
  }

  return (
    <div className="kb-chatWindow">
      <ChatHeader title="KiranaBot" invoiceCount={invoiceCount ?? 0} isTyping={isTyping} />
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