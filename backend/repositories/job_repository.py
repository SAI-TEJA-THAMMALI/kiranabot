from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models.job import Job

class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, job: Job):
        """Creates a new job and returns the created Job object."""
        self.db.add(job)
        self.db.flush()
        self.db.refresh(job)
        return job

    def get_by_id(self, job_id: UUID):
        """Retrieves a job by its UUID."""
        stmt = select(Job).where(Job.job_id == job_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_pending_jobs(self):
        """Retrieves all jobs with 'Queued' status."""
        return self.get_by_status("Queued")

    def get_by_status(self, status: str):
        """Retrieves all jobs with a specific status."""
        stmt = select(Job).where(Job.status == status)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def update_status(self, job_id: UUID, status: str):
        """Updates the status of a job. Returns updated Job or None if not found."""
        job = self.get_by_id(job_id)
        if job is None:
            return None

        job.status = status
        self.db.flush()
        self.db.refresh(job)
        return job

    def increment_retry_count(self, job_id: UUID):
        """Increments the retry count for a job. Returns updated Job or None if not found."""
        job = self.get_by_id(job_id)
        if job is None:
            return None

        job.retry_count += 1
        self.db.flush()
        self.db.refresh(job)
        return job

    def get_by_invoice_id(self, invoice_id: UUID):
        """Retrieves a job associated with a specific invoice."""
        stmt = select(Job).where(Job.invoice_id == invoice_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()
