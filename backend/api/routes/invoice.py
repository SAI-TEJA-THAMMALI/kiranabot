from fastapi import APIRouter

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post("")
def create_invoice():
    return {"invoice_id": "demo_invoice"}

@router.get("/{invoice_id}")
def get_invoice(invoice_id: str):
    return {"invoice_id": invoice_id}

