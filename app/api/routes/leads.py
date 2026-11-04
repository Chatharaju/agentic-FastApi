from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.repositories.lead_repository import LeadRepository
from app.schemas.lead import LeadCreate, LeadResponse
from app.services.lead_service import LeadService

router = APIRouter(prefix="/leads", tags=["Leads"])

#The routes must create repositories using the request's database session.
def get_lead_service(
    db: Session = Depends(get_db),
) -> LeadService:
    return LeadService(LeadRepository(db))


@router.post(
    "",
    response_model=LeadResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_lead(
    data: LeadCreate,
    service: LeadService = Depends(get_lead_service),
):
    return service.create_lead(data)


@router.get("", response_model=list[LeadResponse])
def list_leads(
    service: LeadService = Depends(get_lead_service),
):
    return service.list_leads()


@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(
    lead_id: UUID,
    service: LeadService = Depends(get_lead_service),
):
    lead = service.get_lead(lead_id)

    if lead is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found.",
        )

    return lead