export default function FieldsTable({ fields }) {
  const entries = Object.entries(fields)
  if (entries.length === 0) {
    return <div className="kb-muted">No extracted fields yet.</div>
  }

  return (
    <table className="kb-table">
      <thead>
        <tr>
          <th>Field</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        {entries.map(([k, v]) => (
          <tr key={k}>
            <td>{k}</td>
            <td>{String(v)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

