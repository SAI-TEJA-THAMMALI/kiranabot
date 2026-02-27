import { useChat } from '../../hooks/useChat.js'
import ChatHeader from './ChatHeader.jsx'
import MessageBubble from './MessageBubble.jsx'
import TypingIndicator from './TypingIndicator.jsx'
import InputBar from './InputBar.jsx'

export default function ChatWindow() {
  const { messages, isTyping, sendMessage } = useChat()

  return (
    <div className="kb-chatWindow">
      <ChatHeader title="KiranaBot" />
      <div className="kb-chatBody">
        {messages.map((m) => (
          <MessageBubble key={m.id} role={m.role} text={m.text} />
        ))}
        {isTyping ? <TypingIndicator /> : null}
      </div>
      <InputBar onSend={sendMessage} />
    </div>
  )
}

