function toCsv(rows) {
  if (!rows || rows.length === 0) return ''
  const headers = Array.from(
    new Set(rows.flatMap((r) => Object.keys(r || {}))),
  ).sort()
  const escape = (v) => `"${String(v ?? '').replaceAll('"', '""')}"`
  const lines = [headers.map(escape).join(',')]
  for (const r of rows) {
    lines.push(headers.map((h) => escape(r?.[h])).join(','))
  }
  return lines.join('\n')
}

export function downloadCsv(filename, rows) {
  const csv = toCsv(rows)
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

