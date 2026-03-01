import GSTR1Row from './GSTR1Row.jsx'
import ExportButton from './ExportButton.jsx'
import { useGSTR1 } from '../../hooks/useGSTR1.js'

export default function GSTR1Preview() {
  const { rows } = useGSTR1()

  return (
    <div className="kb-card">
      <div className="kb-cardHeader">
        <div>GSTR-1 Preview</div>
      </div>
      <div className="kb-gstr1ExportRow">
        <ExportButton rows={rows} />
      </div>
      {rows.length === 0 ? (
        <div className="kb-muted">
          {/* Skeleton placeholder table */}
<div className="kb-gstr-skeleton">
  <div className="kb-gstr-thead">
    <span>GSTIN</span>
    <span>Invoice No</span>
    <span>Taxable</span>
    <span>GST</span>
    </div>
      <div className="kb-gstr-row kb-gstr-ghost">
        <span /><span /><span /><span />
      </div>
      <div className="kb-gstr-row kb-gstr-ghost" style={{opacity:0.6}}>
        <span /><span /><span /><span />
      </div>
      <div className="kb-gstr-row kb-gstr-ghost" style={{opacity:0.35}}>
        <span /><span /><span /><span />
      </div>
      <div className="kb-gstr-hint">
        Upload invoices to populate rows
      </div>
    </div>
        </div>
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

