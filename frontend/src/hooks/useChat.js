import { useState } from 'react'

function getTime() {
  return new Date().toLocaleTimeString('en-IN', {
    hour: '2-digit', minute: '2-digit', hour12: true
  })
}

const INITIAL_MESSAGES = [
  {
    id: 1,
    role: 'bot',
    text: 'Namaste! 🙏 Upload a GST invoice photo and I\'ll extract all fields for your GSTR-1 filing.',
    time: getTime()
  }
]

export function useChat() {
  const [messages, setMessages]       = useState(INITIAL_MESSAGES)
  const [isTyping, setIsTyping]       = useState(false)
  const [invoiceCount, setInvoiceCount] = useState(0)

  function sendMessage(text) {
    if (!text.trim()) return

    const userMsg = {
      id: Date.now(),
      role: 'user',
      text: text.trim(),
      time: getTime()
    }

    setMessages(prev => [...prev, userMsg])
    setIsTyping(true)

    // if message contains "invoice" bump the counter (replace with real logic)
    if (text.toLowerCase().includes('invoice')) {
      setInvoiceCount(c => c + 1)
    }

    setTimeout(() => {
      setIsTyping(false)
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'bot',
        text: 'Please share the invoice image and I\'ll extract the GST fields automatically 📄',
        time: getTime()
      }])
    }, 1500)
  }

  return { messages, isTyping, sendMessage, invoiceCount }
}