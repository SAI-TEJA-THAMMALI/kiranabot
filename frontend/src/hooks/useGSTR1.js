import { useState, useEffect } from 'react'
import { API } from '../services/api.js'
import { showToast } from '../components/shared/ToastContainer.jsx'

export function useGSTR1() {
  const [rows, setRows]               = useState([])
  const [isExporting, setIsExporting] = useState(false)

  // Listen for successful uploads from useChat
  useEffect(() => {
    const handler = (e) => {
      const result = e.detail
      if (result?.status !== 'success') return

      const ext = result.extraction || {}
      const val = result.validation  || {}

      setRows(prev => [...prev, {
        invoice_id:     result.invoice_id  || Date.now(),
        gstin:          ext.seller_gstin   || '—',
        invoice_number: ext.invoice_number || '—',
        invoice_date:   ext.invoice_date   || '—',
        taxable_value:  ext.taxable_value  || 0,
        cgst:           ext.cgst           || 0,
        sgst:           ext.sgst           || 0,
        igst:           ext.igst           || 0,
        total:          ext.total          || 0,
        gst_rate:       ext.gst_rate       || 18,
        type:           val.classification
                          ?.type           || 'B2CS',
        gstin_valid:    val.gstin
                          ?.valid          || false
      }])
    }

    window.addEventListener('invoice-uploaded', handler)
    return () =>
      window.removeEventListener('invoice-uploaded', handler)
  }, [])

  const exportCSV = async () => {
    if (rows.length === 0) {
      showToast('No invoices to export yet', 'error')
      return
    }
    setIsExporting(true)
    const result = await API.exportGSTR1(
      window.__kbSession || 'default'
    )
    setIsExporting(false)

    if (result.status === 'downloaded') {
      showToast(
        `GSTR-1 exported — ${rows.length} invoice(s)`,
        'success'
      )
    } else {
      showToast('Export failed. Try again.', 'error')
    }
  }

  return { rows, isExporting, exportCSV }
}