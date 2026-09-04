from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Invoice


class InvoiceRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, invoice_id: UUID):
        stmt = select(Invoice).where(Invoice.id == invoice_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_user_id(self, user_id: UUID):
        stmt = select(Invoice).where(Invoice.user_id == user_id)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_by_file_hash(self, file_hash: str):
        stmt = select(Invoice).where(Invoice.file_hash == file_hash)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()
    def create(self, invoice: Invoice):
        self.db.add(invoice)
        self.db.flush()
        self.db.refresh(invoice)
        return invoice