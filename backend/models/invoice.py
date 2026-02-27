from pydantic import BaseModel

class Invoice(BaseModel):
    invoice_id: str | None = None
    fields: dict = {}

