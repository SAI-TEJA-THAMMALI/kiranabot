import { useMemo, useState } from 'react'
import { getDemoReply } from '../services/chatResponses.js'

export function useChat() {
  const [isTyping, setIsTyping] = useState(false)
  const [messages, setMessages] = useState(() => [
    { id: 'm1', role: 'bot', text: 'Upload an invoice photo to begin (demo).' },
  ])

  function sendMessage(text) {
    const id = crypto.randomUUID?.() || String(Date.now())
    setMessages((m) => [...m, { id, role: 'user', text }])
    setIsTyping(true)
    setTimeout(() => {
      setMessages((m) => [
        ...m,
        { id: `${id}-r`, role: 'bot', text: getDemoReply(text) },
      ])
      setIsTyping(false)
    }, 400)
  }

  return useMemo(
    () => ({ messages, isTyping, sendMessage }),
    [messages, isTyping],
  )
}

