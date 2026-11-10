
from decimal import Decimal, InvalidOperation

from app.db.session import SessionLocal
from app.repositories.quote_repository import QuoteRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.lead_repository import LeadRepository
from app.schemas.quote import QuoteCreate
from app.services.quote_service import QuoteService


def create_quote(
    description: str,
    subtotal: str,
    customer_id: str | None = None,
    lead_id: str | None = None,
    tax_rate: str = "13.00",
) -> dict:
    """
    Create a draft quote for an existing customer or lead.

    Exactly one of customer_id or lead_id must be provided.

    Use the actual ID returned by search_customers or
    search_leads. Never invent an ID.
    """

    try:
        data = QuoteCreate(
            customer_id=customer_id,
            lead_id=lead_id,
            description=description,
            subtotal=Decimal(subtotal),
            tax_rate=Decimal(tax_rate),
        )

        with SessionLocal() as db:
            service = QuoteService(
                QuoteRepository(db),
                CustomerRepository(db),
                LeadRepository(db),
            )

            quote = service.create_quote(data)

            return {
                "success": True,
                "message": "Draft quote created successfully.",
                "quote": {
                    "id": str(quote.id),
                    "customer_id": (
                        str(quote.customer_id)
                        if quote.customer_id else None
                    ),
                    "lead_id": (
                        str(quote.lead_id)
                        if quote.lead_id else None
                    ),
                    "description": quote.description,
                    "subtotal": str(quote.subtotal),
                    "tax_rate": str(quote.tax_rate),
                    "tax_amount": str(quote.tax_amount),
                    "total": str(quote.total),
                    "currency": quote.currency,
                    "status": quote.status,
                },
            }

    except (ValueError, InvalidOperation) as exc:
        return {
            "success": False,
            "message": str(exc),
        }
