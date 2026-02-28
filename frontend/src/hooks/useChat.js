import { useState, useEffect } from 'react'
import { API } from '../services/api.js'
import { showToast } from '../components/shared/ToastContainer.jsx'

// Global session shared across hooks
window.__kbSession = window.__kbSession || null

const makeMsg = (role, text) => ({
  id:   Date.now() + Math.random(),
  role,
  text,
  time: new Date().toLocaleTimeString(
    'en-IN',
    { hour: '2-digit', minute: '2-digit', hour12: true }
  )
})

export function useChat() {
  const [messages, setMessages]         = useState([])
  const [isTyping, setIsTyping]         = useState(false)
  const [invoiceCount, setInvoiceCount] = useState(0)

  // ── Real upload to backend ─────────────────────
  const handleUpload = async (file) => {
    addMsg('user', `📎 ${file.name}`)
    setIsTyping(true)
    addMsg('bot', '🔍 Reading your invoice...')

    const result = await API.uploadInvoice(
      file,
      window.__kbSession || 'default'
    )

    setIsTyping(false)

    // Preflight failed
    if (result.status === 'preflight_failed') {
      addMsg('bot', `📸 ${result.message}`)
      showToast(result.message, 'error')
      return
    }

    // Success
    if (result.status === 'success') {
      setInvoiceCount(c => c + 1)

      addMsg('bot',
        result.chat_response ||
        `✅ Invoice processed!\n` +
        `Added as ${result.validation
          ?.classification?.type || 'B2CS'}.`
      )

      showToast('Invoice processed!', 'success')

      // Broadcast to InvoicePreview + GSTR1Preview
      window.dispatchEvent(
        new CustomEvent('invoice-uploaded', {
          detail: result
        })
      )
      return
    }

    // Error
    addMsg('bot', '❌ Could not process. Please try again.')
    showToast('Upload failed', 'error')
  }

  // ── Init session on mount + listen for kb-file-upload ──
  useEffect(() => {
    const fileHandler = (e) => {
      const file = e.detail
      if (file instanceof File) handleUpload(file)
    }
    init()
    window.addEventListener('kb-file-upload', fileHandler)
    return () =>
      window.removeEventListener('kb-file-upload', fileHandler)
  }, [])

  const init = async () => {
    const health  = await API.health()
    const session = await API.createSession('2026-02')
    window.__kbSession = session.id

    addMsg('bot',
      '👋 Namaste! I am KiranaBot.\n' +
      'Upload any GST invoice photo and I will\n' +
      'extract all fields and prepare your GSTR-1 draft.'
    )

    if (health.status !== 'working') {
      addMsg('bot',
        '⚠️ Backend offline. Make sure server is\n' +
        'running on port 8000.'
      )
    }
  }

  const addMsg = (role, text) =>
    setMessages(prev => [...prev, makeMsg(role, text)])

  // ── Called by ChatWindow ───────────────────────
  const sendMessage = (textOrFile) => {

    // Real File object from input
    if (textOrFile instanceof File) {
      handleUpload(textOrFile)
      return
    }

    if (typeof textOrFile === 'string') {

      // "📎 filename.jpg" — Person 3 sends filename as text
      // We intercept it and trigger upload with fake file
      if (textOrFile.startsWith('📎')) {
        addMsg('user', textOrFile)
        // Cannot upload without real File object
        // Show helpful message instead
        addMsg('bot',
          '📎 Invoice received! Processing...\n' +
          'Note: Connect AttachmentButton to pass\n' +
          'File object directly for real extraction.'
        )
        return
      }

      // Plain text
      if (textOrFile.trim()) {
        addMsg('user', textOrFile)
        setTimeout(() => {
          addMsg('bot',
            '📎 Please upload an invoice photo\n' +
            'using the attachment button below.'
          )
        }, 600)
      }
    }
  }

  // ── Expose upload for AttachmentButton direct call ──
  return {
    messages,
    isTyping,
    invoiceCount,
    sendMessage,
    handleUpload   // expose so AttachmentButton can call directly
  }
}