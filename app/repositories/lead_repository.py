from uuid import UUID

from app.models.lead import Lead

from sqlalchemy.orm import Session
from sqlalchemy import select

# Reads and writes records into DB
class LeadRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, lead: Lead) -> Lead:
      try:
          self.db.add(lead)
          self.db.commit()
          self.db.refresh(lead)
          return lead
      except Exception:
          self.db.rollback()
          raise

    def get_by_id(self, lead_id: UUID) -> Lead | None:
        return self.db.get(Lead, lead_id)

    def list(self) -> list[Lead]:
        statement = select(Lead).order_by(Lead.created_at.desc())
        return list(self.db.scalars(statement).all())

    def search_by_name(self, name: str) -> "list[Lead]":
        statement = (
            select(Lead)
            .where(Lead.name.ilike(f"%{name}%"))
            .order_by(Lead.created_at.desc())
            .limit(10)
        )
        return list(self.db.scalars(statement).all())