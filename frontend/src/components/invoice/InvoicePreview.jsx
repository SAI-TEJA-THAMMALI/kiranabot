import FieldsTable from './FieldsTable.jsx'
import ConfidenceBadge from './ConfidenceBadge.jsx'
import ValidationFlag from './ValidationFlag.jsx'
import { useInvoiceUpload } from '../../hooks/useInvoiceUpload.js'

export default function InvoicePreview() {
  const { invoice, validation } = useInvoiceUpload()

  return (
    <div className="kb-card">
      <div className="kb-cardHeader">
        <div>Invoice Preview</div>
        <div className="kb-row">
          <ConfidenceBadge score={invoice?.confidence ?? 0.5} />
          <ValidationFlag ok={validation?.valid ?? true} />
        </div>
      </div>
      <FieldsTable fields={invoice?.fields ?? {}} />
    </div>
  )
}

