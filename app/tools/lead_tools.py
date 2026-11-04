from app.models.business import Lead
from app.services.business_store import leads


def create_lead(
    customer_id: str,
    service: str,
    source: str = "ai_assistant",
) -> dict:
    """
    Create a new lead for a customer.
    """

    lead_id = f"LEAD-{len(leads) + 1:03d}"

    lead = Lead(
        id=lead_id,
        customer_id=customer_id,
        service=service,
        status="new",
        source=source,
    )

    leads.append(lead)

    return {
        "success": True,
        "lead": {
            "id": lead.id,
            "customer_id": lead.customer_id,
            "service": lead.service,
            "status": lead.status,
            "source": lead.source,
        },
    }


def get_customer_leads(customer_id: str) -> dict:
    """
    Get leads belonging to a customer.
    """

    customer_leads = [
        lead
        for lead in leads
        if lead.customer_id == customer_id
    ]

    return {
        "count": len(customer_leads),
        "leads": [
            {
                "id": lead.id,
                "customer_id": lead.customer_id,
                "service": lead.service,
                "status": lead.status,
                "source": lead.source,
            }
            for lead in customer_leads
        ],
    }