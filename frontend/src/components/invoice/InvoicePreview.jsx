export default function InvoicePreview({ fields = null, confidence = 50, gstStatus = 'ok' }) {
  return (
    <div className="kb-card">
      <div className="kb-cardHeader">
        <span className="kb-cardTitle">Invoice Preview</span>
        <div className="kb-row">
          <span className="kb-badge kb-muted-badge">Conf: {confidence}%</span>
          <span className={`kb-badge ${gstStatus === 'ok' ? 'kb-ok' : 'kb-warn'}`}>
            GST {gstStatus === 'ok' ? 'OK' : 'WARN'}
          </span>
        </div>
      </div>

      {/* Confidence bar */}
      <div className="kb-confRow">
        <span>Extraction</span>
        <div className="kb-confBar">
          <div className="kb-confFill" style={{ width: `${confidence}%` }} />
        </div>
        <span>{confidence}%</span>
      </div>

      {/* Empty state — dashed upload zone */}
      {!fields ? (
        <div className="kb-uploadZone">
          <div className="kb-uploadIcon">🧾</div>
          <div className="kb-uploadTitle">No invoice yet</div>
          <div className="kb-uploadHint">
            Drop invoice here or click <strong>+</strong> in the chat
          </div>
          <div className="kb-uploadFormats">JPG · PNG · PDF supported</div>
        </div>
      ) : (
        <div className="kb-fieldsTable">
          {/* fields render here once extracted */}
          {Object.entries(fields).map(([key, val]) => (
            <div key={key} className="kb-fieldRow">
              <span className="kb-fieldKey">{key}</span>
              <span className="kb-fieldVal">{val}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}