from uuid import UUID

from db.models import Job
from repositories.job_repository import JobRepository


class JobService:

    def __init__(self, repository: JobRepository):
        self.repository = repository

    def get_job(self, job_id: UUID):
        return self.repository.get_by_id(job_id)

    def get_invoice_job(self, invoice_id: UUID):
        return self.repository.get_by_invoice_id(invoice_id)

    def get_jobs_by_status(self, status: str):
        return self.repository.get_by_status(status)

    def create_job(self, job: Job):
        return self.repository.create(job)

    def update_status(self, job_id: UUID, status: str):
        return self.repository.update_status(job_id, status)

    def increment_retry_count(self, job_id: UUID):
        return self.repository.increment_retry_count(job_id)