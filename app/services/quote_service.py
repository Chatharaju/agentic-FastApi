
from decimal import Decimal, ROUND_HALF_UP
from uuid import uuid4

from app.models.quote import Quote
from app.repositories.quote_repository import QuoteRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.lead_repository import LeadRepository
from app.schemas.quote import QuoteCreate


class QuoteService:
    def __init__(
        self,
        quote_repository: QuoteRepository,
        customer_repository: CustomerRepository,
        lead_repository: LeadRepository,
    ):
        self.quote_repository = quote_repository
        self.customer_repository = customer_repository
        self.lead_repository = lead_repository

    def create_quote(self, data: QuoteCreate) -> Quote:

        # Validate customer or lead
        if data.customer_id is not None:
            customer = self.customer_repository.get_by_id(
                data.customer_id
            )
            if customer is None:
                raise ValueError("Customer not found.")

        if data.lead_id is not None:
            lead = self.lead_repository.get_by_id(data.lead_id)
            if lead is None:
                raise ValueError("Lead not found.")

        # Calculate tax and total using Decimal
        subtotal = data.subtotal.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        tax_amount = (
            subtotal * data.tax_rate / Decimal("100")
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        total = subtotal + tax_amount

        # Create quote database object
        quote = Quote(
            id=uuid4(),
            customer_id=data.customer_id,
            lead_id=data.lead_id,
            description=data.description,
            subtotal=subtotal,
            tax_rate=data.tax_rate,
            tax_amount=tax_amount,
            total=total,
            currency="CAD",
            status="draft",
        )

        return self.quote_repository.create(quote)
