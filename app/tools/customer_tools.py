from app.db.session import SessionLocal
from app.repositories.customer_repository import CustomerRepository
from app.services.customer_service import CustomerService


def search_customers(name: str) -> dict:
    """
    Search for existing customers by name in the database.

    Use this tool when a business owner wants to find
    a customer by their name.
    """

    if not name or not name.strip():
        return {
            "success": False,
            "message": "Customer name is required.",
        }

    # Create a database session for this tool invocation.
    with SessionLocal() as db:

        repository = CustomerRepository(db)
        service = CustomerService(repository)

        customers = service.search_customers(name.strip())

        return {
            "success": True,
            "count": len(customers),
            "customers": [
                {
                    "id": str(customer.id),
                    "name": customer.name,
                    "email": customer.email,
                    "phone": customer.phone,
                    "address": customer.address,
                }
                for customer in customers
            ],
        }