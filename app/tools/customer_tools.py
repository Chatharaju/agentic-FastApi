from app.services.business_store import customers


def search_customers(name: str) -> dict:
    """
    Search customers by name.
    """

    results = [
        customer
        for customer in customers
        if name.lower() in customer.name.lower()
    ]

    return {
        "count": len(results),
        "customers": [
            {
                "id": customer.id,
                "name": customer.name,
                "phone": customer.phone,
                "email": customer.email,
                "address": customer.address,
            }
            for customer in results
        ],
    }