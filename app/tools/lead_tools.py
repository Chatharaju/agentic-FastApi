from app.db.session import SessionLocal
from app.repositories.lead_repository import LeadRepository
from app.services.lead_service import LeadService


def search_leads(name: str) -> dict:
    """
    Search for existing business leads by name.

    Use this tool when a business owner wants to
    find an enquiry or potential customer.
    """

    if not name or not name.strip():
        return {
            "success": False,
            "message": "Lead name is required.",
        }

    with SessionLocal() as db:
        repository = LeadRepository(db)
        service = LeadService(repository)

        leads = service.search_leads(name.strip())

        return {
            "success": True,
            "count": len(leads),
            "leads": [
                {
                    "id": str(lead.id),
                    "name": lead.name,
                    "email": lead.email,
                    "phone": lead.phone,
                    "service_type": lead.service_type,
                    "description": lead.description,
                    "status": lead.status,
                }
                for lead in leads
            ],
        }