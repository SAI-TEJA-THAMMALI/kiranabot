import uuid
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import pytest

from db.models import Base, User, Invoice, Job
from repositories.user_repository import UserRepository
from repositories.invoice_repository import InvoiceRepository
from repositories.job_repository import JobRepository
from services.invoice_service import InvoiceService

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def test_invoice_job_atomic_creation():
    db = SessionLocal()
    user_repo = UserRepository(db)
    invoice_repo = InvoiceRepository(db)
    job_repo = JobRepository(db)
    invoice_service = InvoiceService(invoice_repo, job_repo)

    try:
        # 1. Create a test user
        user_id = uuid.uuid4()
        test_user = User(
            id=user_id,
            email=f"test_{user_id}@example.com",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(test_user)
        db.commit()

        # 2. Success case: Create invoice and job
        invoice = Invoice(
            user_id=user_id,
            file_hash="test_hash_123",
            filename="test_invoice.pdf",
            status="Processing"
        )
        job_data = {"status": "Queued"}

        result = invoice_service.create_invoice_with_job(invoice, job_data)

        assert result["status"] == "created"
        assert result["invoice"].id is not None
        assert result["job"].job_id is not None

        # Verify in DB
        db_invoice = db.execute(select(Invoice).where(Invoice.file_hash == "test_hash_123")).scalar_one()
        assert db_invoice is not None

        db_job = db.execute(select(Job).where(Job.invoice_id == db_invoice.id)).scalar_one()
        assert db_job is not None

        # 3. Failure case: Simulate error during job creation
        # We can do this by passing invalid job_data that causes a DB error
        # (e.g., missing a required field or wrong type)

        bad_invoice = Invoice(
            user_id=user_id,
            file_hash="test_hash_fail",
            filename="fail_invoice.pdf",
            status="Processing"
        )

        # Force failure by passing an object instead of a dict for job_data
        # which will cause an error when unpacking **job_data in the service
        with pytest.raises(Exception):
            invoice_service.create_invoice_with_job(bad_invoice, "not-a-dict")

        # Verify that the 'bad_invoice' was NOT created (atomic rollback)
        failed_invoice = db.execute(select(Invoice).where(Invoice.file_hash == "test_hash_fail")).scalar_one_or_none()
        assert failed_invoice is None

        print("\nIntegration test passed: Atomicity verified!")

    finally:
        db.close()

if __name__ == "__main__":
    test_invoice_job_atomic_creation()
