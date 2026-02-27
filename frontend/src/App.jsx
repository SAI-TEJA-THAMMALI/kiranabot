import './styles/whatsapp.css'
import './styles/chat.css'
import ChatWindow from './components/chat/ChatWindow.jsx'
import InvoicePreview from './components/invoice/InvoicePreview.jsx'
import GSTR1Preview from './components/gstr1/GSTR1Preview.jsx'

export default function App() {
  return (
    <div className="kb-app">
      <div className="kb-shell">
        <div className="kb-left">
          <ChatWindow />
        </div>
        <div className="kb-right">
          <div className="kb-sidePanel">
            <InvoicePreview />
            <GSTR1Preview />
          </div>
        </div>
      </div>
    </div>
  )
}

