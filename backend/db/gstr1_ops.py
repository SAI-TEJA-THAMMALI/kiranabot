def build_gstr1_rows(invoices: list[dict]) -> list[dict]:
    return [{"invoice_id": inv.get("invoice_id", "")} for inv in invoices]

