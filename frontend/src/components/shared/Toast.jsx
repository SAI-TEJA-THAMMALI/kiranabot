import { useEffect, useState } from 'react'

export default function Toast({ message, type = 'success', onClose }) {
  const [visible, setVisible] = useState(true)

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false)
      setTimeout(onClose, 300)
    }, 3000)
    return () => clearTimeout(timer)
  }, [])

  const icon = type === 'success' ? '✅' : type === 'warning' ? '⚠️' : '❌'

  return (
    <div className={`kb-toast kb-toast-${type} ${visible ? 'kb-toast-in' : 'kb-toast-out'}`}>
      <span className="kb-toast-icon">{icon}</span>
      <span className="kb-toast-text">{message}</span>
    </div>
  )
}