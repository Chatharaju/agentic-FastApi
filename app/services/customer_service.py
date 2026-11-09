from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate

#The service contains the business logic for creating and retrieving Customers.
#inject the database-backed repository
class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def create_customer(self, data: CustomerCreate) -> Customer:
        customer = Customer(
            id=uuid4(),
            name=data.name,
            email=str(data.email) if data.email else None,
            phone=data.phone,
            address=data.address,
            created_at=datetime.now(timezone.utc),
        )
        return self.repository.create(customer)

    def get_customer(self, customer_id: UUID) -> Customer | None:
        return self.repository.get_by_id(customer_id)

    def list_customers(self) -> list[Customer]:
        return self.repository.list()
    
    def search_customers(self, name: str) -> list:
        return self.repository.search_by_name(name)