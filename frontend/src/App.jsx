import { useState, useEffect } from 'react'
import './styles/whatsapp.css'
import './styles/chat.css'
import ChatWindow     from './components/chat/ChatWindow.jsx'
import InvoicePreview from './components/invoice/InvoicePreview.jsx'
import GSTR1Preview   from './components/gstr1/GSTR1Preview.jsx'
import ToastContainer from './components/shared/ToastContainer.jsx'

export default function App() {
  const [invoiceFields, setInvoiceFields] = useState(null)
  const [confidence, setConfidence]       = useState(0)
  const [gstStatus, setGstStatus]         = useState('ok')

  useEffect(() => {
    const handler = (e) => {
      const result = e.detail
      if (result?.status !== 'success') return

      // Calculate 0-100 confidence score from HIGH/MEDIUM/LOW
      const conf   = result.confidence || {}
      const vals   = Object.values(conf)
      const score  = vals.length === 0 ? 75 : Math.round(
        (vals.filter(v => v === 'HIGH').length   * 100 +
         vals.filter(v => v === 'MEDIUM').length *  60 +
         vals.filter(v => v === 'LOW').length    *  20)
        / vals.length
      )

      // Remove null/empty fields before display
      const fields = Object.fromEntries(
        Object.entries(result.extraction || {})
          .filter(([, v]) =>
            v !== null && v !== undefined &&
            v !== '' && v !== 0
          )
      )

      setInvoiceFields(fields)
      setConfidence(score)
      setGstStatus(
        result.validation?.gstin?.valid ? 'ok' : 'warn'
      )
    }

    window.addEventListener('invoice-uploaded', handler)
    return () =>
      window.removeEventListener('invoice-uploaded', handler)
  }, [])

  return (
    <div className="kb-app">
      <div className="kb-shell">
        <div className="kb-left">
          <ChatWindow />
        </div>
        <div className="kb-right">
          <div className="kb-sidePanel">
            <InvoicePreview
              fields={invoiceFields}
              confidence={confidence}
              gstStatus={gstStatus}
            />
            <GSTR1Preview />
          </div>
        </div>
      </div>
      <ToastContainer />
    </div>
  )
}