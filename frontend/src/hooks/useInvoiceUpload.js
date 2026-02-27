import { useMemo } from 'react'

export function useInvoiceUpload() {
  return useMemo(
    () => ({
      invoice: { fields: {}, confidence: 0.5 },
      validation: { valid: true, issues: [] },
    }),
    [],
  )
}

