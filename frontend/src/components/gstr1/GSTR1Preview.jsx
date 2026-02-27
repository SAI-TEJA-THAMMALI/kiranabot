import GSTR1Row from './GSTR1Row.jsx'
import ExportButton from './ExportButton.jsx'
import { useGSTR1 } from '../../hooks/useGSTR1.js'

export default function GSTR1Preview() {
  const { rows } = useGSTR1()

  return (
    <div className="kb-card">
      <div className="kb-cardHeader">
        <div>GSTR-1 Preview</div>
        <ExportButton rows={rows} />
      </div>
      {rows.length === 0 ? (
        <div className="kb-muted">No rows yet.</div>
      ) : (
        <div className="kb-gstr1">
          {rows.map((r) => (
            <GSTR1Row key={r.invoice_id} row={r} />
          ))}
        </div>
      )}
    </div>
  )
}

