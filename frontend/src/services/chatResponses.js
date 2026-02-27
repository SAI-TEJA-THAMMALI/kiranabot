export function getDemoReply(userText) {
  if (userText.toLowerCase().includes('hello')) return 'Hello! Send an invoice photo.'
  if (userText.toLowerCase().includes('gst')) return 'GST looks consistent (demo placeholder).'
  return 'Got it. I can extract fields and generate GSTR-1 (demo placeholder).'
}

