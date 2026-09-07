from db.supabase_client import get_supabase

def save_invoice(data: dict) -> dict:
    try:
        db = get_supabase()
        extraction = data.get("extraction", {})
        record = {
            "session_id": data.get("session_id"),
            "filename": data.get("filename"),
            "seller_name": extraction.get("seller_name"),
            "seller_gstin": extraction.get("seller_gstin"),
            "buyer_gstin": extraction.get("buyer_gstin"),
            "invoice_number": extraction.get("invoice_number"),
            "invoice_date": extraction.get("invoice_date"),
            "taxable_value": extraction.get("taxable_value"),
            "gst_rate": extraction.get("gst_rate"),
            "cgst": extraction.get("cgst"),
            "sgst": extraction.get("sgst"),
            "igst": extraction.get("igst") or 0,
            "total": extraction.get("total"),
            "hsn_code": extraction.get("hsn_code"),
            "classification": data.get("classification"),
            "gstin_valid": data.get("gstin_valid", False),
            "tax_valid": data.get("tax_valid", False),
        }
        result = db.table("invoices").insert(record).execute()
        return result.data[0] if result.data else {}
    except Exception as e:
        print(f"Save invoice error: {e}")
        return {"id": "offline-invoice"}

def get_invoices(session_id: str) -> list:
    try:
        db = get_supabase()
        result = db.table("invoices").select(
            "*"
        ).eq("session_id", session_id).execute()
        return result.data or []
    except Exception as e:
        print(f"Get invoices error: {e}")
        return []