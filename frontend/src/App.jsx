import ChatWindow from './components/chat/ChatWindow.jsx'
import InvoicePreview from './components/invoice/InvoicePreview.jsx'
import GSTR1Preview from './components/gstr1/GSTR1Preview.jsx'

export default function App() {
  return (
    <div className="kb-app">
      <div className="kb-left">
        <ChatWindow />
      </div>
      <div className="kb-right">
        <InvoicePreview />
        <GSTR1Preview />
      </div>
    </div>
  )
}

