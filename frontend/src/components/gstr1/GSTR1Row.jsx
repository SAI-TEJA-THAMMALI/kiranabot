export default function GSTR1Row({ row }) {
  return (
    <div className="kb-gstr1Row">
      <div className="kb-strong">{row.invoice_id}</div>
      <div className="kb-muted">{row.gstin || 'GSTIN: —'}</div>
    </div>
  )
}

