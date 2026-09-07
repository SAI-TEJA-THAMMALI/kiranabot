import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './styles/whatsapp.css'
import './styles/chat.css'
import './styles/table.css'

class AppErrorBoundary extends React.Component {
  state = { hasError: false, error: null }
  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }
  componentDidCatch(error, info) {
    console.error('App failed to render:', error, info)
  }
  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          minHeight: '100vh', padding: 24, background: '#08101a', color: '#e2eaf0',
          fontFamily: 'system-ui, sans-serif', display: 'flex', flexDirection: 'column',
          alignItems: 'center', justifyContent: 'center', gap: 16
        }}>
          <h1 style={{ margin: 0, fontSize: 20 }}>Something went wrong</h1>
          <pre style={{ background: '#1e2f3e', padding: 16, borderRadius: 8, overflow: 'auto', maxWidth: '90%', fontSize: 12 }}>
            {this.state.error?.message || String(this.state.error)}
          </pre>
          <p style={{ margin: 0, color: '#5e7a8a', fontSize: 14 }}>Check the browser console for details.</p>
        </div>
      )
    }
    return this.props.children
  }
}

const rootEl = document.getElementById('root')
if (!rootEl) {
  document.body.innerHTML = '<div style="padding:24px;background:#08101a;color:#e2eaf0;font-family:system-ui">No #root element found. Check index.html.</div>'
} else {
  ReactDOM.createRoot(rootEl).render(
    <React.StrictMode>
      <AppErrorBoundary>
        <App />
      </AppErrorBoundary>
    </React.StrictMode>,
  )
}

