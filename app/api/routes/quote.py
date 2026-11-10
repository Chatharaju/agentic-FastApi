from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.repositories.quote_repository import QuoteRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.lead_repository import LeadRepository
from app.schemas.quote import QuoteCreate, QuoteResponse
from app.services.quote_service import QuoteService


router = APIRouter(prefix="/quotes", tags=["Quotes"])


def get_quote_service(
    db: Session = Depends(get_db),
) -> QuoteService:
    return QuoteService(
        QuoteRepository(db),
        CustomerRepository(db),
        LeadRepository(db),
    )


@router.post(
    "",
    response_model=QuoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_quote(
    data: QuoteCreate,
    service: QuoteService = Depends(get_quote_service),
):
    try:
        return service.create_quote(data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc