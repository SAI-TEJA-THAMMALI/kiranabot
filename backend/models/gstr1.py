from pydantic import BaseModel

class GSTR1Row(BaseModel):
    invoice_id: str
    gstin: str | None = None
    taxable_value: float | None = None
    tax: float | None = None

