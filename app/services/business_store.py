from app.models.business import Customer, Lead, Quote

customers = [
    Customer(
        id="CUST-001",
        name="John Smith",
        phone="416-555-0101",
        email="john.smith@example.com",
        address="123 Main Street, Toronto, ON",
    ),
    Customer(
        id="CUST-002",
        name="Sarah Johnson",
        phone="905-555-0202",
        email="sarah.johnson@example.com",
        address="45 King Street, Mississauga, ON",
    ),
]

leads: list[Lead] = []

quotes: list[Quote] = []