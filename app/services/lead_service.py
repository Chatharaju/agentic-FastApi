from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.models.lead import Lead
from app.repositories.lead_repository import LeadRepository
from app.schemas.lead import LeadCreate

#The service contains the business logic for creating and retrieving leads.
#inject the database-backed repository
class LeadService:
    def __init__(self, repository: LeadRepository):
        self.repository = repository

    def create_lead(self, data: LeadCreate) -> Lead:
        lead = Lead(
            id=uuid4(),
            name=data.name,
            email=str(data.email) if data.email else None,
            phone=data.phone,
            service_type=data.service_type,
            description=data.description,
            status="new",
            created_at=datetime.now(timezone.utc),
        )
        return self.repository.create(lead)

    def get_lead(self, lead_id: UUID) -> Lead | None:
        return self.repository.get_by_id(lead_id)

    def list_leads(self) -> list[Lead]:
        return self.repository.list()