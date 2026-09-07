import { useState } from 'react'
import Toast from './Toast.jsx'

let addToastGlobal = null

export function showToast(message, type = 'success') {
  if (addToastGlobal) addToastGlobal(message, type)
}

export default function ToastContainer() {
  const [toasts, setToasts] = useState([])

  addToastGlobal = (message, type) => {
    const id = Date.now()
    setToasts(prev => [...prev, { id, message, type }])
  }

  function remove(id) {
    setToasts(prev => prev.filter(t => t.id !== id))
  }

  return (
    <div className="kb-toast-container">
      {toasts.map(t => (
        <Toast
          key={t.id}
          message={t.message}
          type={t.type}
          onClose={() => remove(t.id)}
        />
      ))}
    </div>
  )
}