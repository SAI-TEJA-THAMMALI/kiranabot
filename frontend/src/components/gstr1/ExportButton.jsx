import { downloadCsv } from '../../services/csvDownload.js'

export default function ExportButton({ rows }) {
  function handleExport() {
    downloadCsv('gstr1.csv', rows)
  }

  return (
    <button className="kb-btn" type="button" onClick={handleExport}>
      Export CSV
    </button>
  )
}

