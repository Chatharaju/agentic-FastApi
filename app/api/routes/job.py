from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.repositories.job_repository import JobRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.lead_repository import LeadRepository
from app.schemas.job import JobCreate, JobResponse
from app.services.job_service import JobService


router = APIRouter(prefix="/jobs", tags=["Jobs"])


def get_job_service(
    db: Session = Depends(get_db),
) -> JobService:
    return JobService(
        JobRepository(db),
        CustomerRepository(db),
        LeadRepository(db),
    )


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    data: JobCreate,
    service: JobService = Depends(get_job_service),
):
    try:
        return service.create_job(data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc