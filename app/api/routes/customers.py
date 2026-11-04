from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])

#The routes must create repositories using the request's database session.
def get_customer_service(
    db: Session = Depends(get_db),
) -> CustomerService:
    return CustomerService(CustomerRepository(db))


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    data: CustomerCreate,
    service: CustomerService = Depends(get_customer_service),
):
    return service.create_customer(data)


@router.get("", response_model=list[CustomerResponse])
def list_customers(
    service: CustomerService = Depends(get_customer_service),
):
    return service.list_customers()


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: UUID,
    service: CustomerService = Depends(get_customer_service),
):
    customer = service.get_customer(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found.",
        )

    return customer