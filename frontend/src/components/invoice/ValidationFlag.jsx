export default function ValidationFlag({ ok }) {
  return (
    <span className={`kb-badge ${ok ? 'kb-ok' : 'kb-warn'}`}>
      {ok ? 'GST OK' : 'Needs review'}
    </span>
  )
}

