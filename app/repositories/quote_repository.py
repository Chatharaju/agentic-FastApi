
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.quote import Quote


class QuoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, quote: Quote) -> Quote:
        try:
            self.db.add(quote)
            self.db.commit()
            self.db.refresh(quote)
            return quote
        except Exception:
            self.db.rollback()
            raise

    def get_by_id(self, quote_id: UUID) -> Quote | None:
        return self.db.get(Quote, quote_id)

    def list(self) -> list[Quote]:
        statement = select(Quote).order_by(Quote.created_at.desc())
        return list(self.db.scalars(statement).all())
