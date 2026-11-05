from uuid import uuid4

from app.models.jobs import Job
from app.repositories.job_repository import JobRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.lead_repository import LeadRepository
from app.schemas.job import JobCreate


class JobService:
    def __init__(
        self,
        job_repository: JobRepository,
        customer_repository: CustomerRepository,
        lead_repository: LeadRepository,
    ):
        self.job_repository = job_repository
        self.customer_repository = customer_repository
        self.lead_repository = lead_repository

    def create_job(self, data: JobCreate) -> Job:

        # Validate customer
        customer = self.customer_repository.get_by_id(data.customer_id)

        if customer is None:
            raise ValueError("Customer not found.")

        # Validate optional lead
        if data.lead_id is not None:
            lead = self.lead_repository.get_by_id(data.lead_id)

            if lead is None:
                raise ValueError("Lead not found.")

        # Create Job database object
        job = Job(
            id=uuid4(),
            customer_id=data.customer_id,
            lead_id=data.lead_id,
            title=data.title,
            description=data.description,
            scheduled_at=data.scheduled_at,
        )

        return self.job_repository.create(job)