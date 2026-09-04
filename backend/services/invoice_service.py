from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.models import Invoice
from repositories.invoice_repository import InvoiceRepository
from repositories.job_repository import JobRepository

class InvoiceService:
    def __init__(self, invoice_repo: InvoiceRepository, job_repo: JobRepository):
        self.invoice_repo = invoice_repo
        self.job_repo = job_repo
        self.db: Session = invoice_repo.db

    def get_invoice(self, invoice_id: UUID):
        return self.invoice_repo.get_by_id(invoice_id)

    def get_user_invoices(self, user_id: UUID):
        return self.invoice_repo.get_by_user_id(user_id)

    def check_duplicate(self, file_hash: str):
        return self.invoice_repo.get_by_file_hash(file_hash)

    def create_invoice_with_job(self, invoice: Invoice, job_data: dict):
        """
        Atomic operation to create an Invoice and its associated processing Job.

        Concepts:
        - Transaction Boundary: The service layer controls when the DB transaction is committed.
        - Atomicity: If job creation fails, the invoice creation is rolled back.
        - Flush vs Commit: flush() sends changes to DB to get generated IDs without ending the transaction.
        """
        try:
            # 1. Duplicate check
            existing_invoice = self.check_duplicate(invoice.file_hash)
            if existing_invoice:
                return {"status": "duplicate", "invoice": existing_invoice}

            # 2. Create Invoice
            # This calls self.db.add() and self.db.flush() internally
            new_invoice = self.invoice_repo.create(invoice)

            # 3. Create associated Job
            # We use the ID obtained from the flushed invoice
            from db.models.job import Job
            job = Job(
                invoice_id=new_invoice.id,
                **job_data
            )
            self.job_repo.create(job)

            # 4. Commit the entire transaction
            self.db.commit()
            return {"status": "created", "invoice": new_invoice, "job": job}

        except SQLAlchemyError as e:
            # Rollback any changes if any step fails
            self.db.rollback()
            # Log error here in real app
            raise e
        except Exception as e:
            self.db.rollback()
            raise e
