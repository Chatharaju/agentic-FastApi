from uuid import UUID
from app.models.customer import Customer

from sqlalchemy.orm import Session
from sqlalchemy import select

# Reads and writes records into DB
class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, customer: Customer) -> Customer:
        try: 
            self.db.add(customer)
            self.db.commit()
            self.db.refresh(customer)
            return customer
        except Exception:
            self.db.rollback()
            raise

    def get_by_id(self, customer_id: UUID) -> Customer | None:
        return self.db.get(Customer, customer_id)

    def list(self) -> list[Customer]:
        statement = select(Customer).order_by(Customer.created_at.desc())
        return list(self.db.scalars(statement).all())
    
    def search_by_name(self, name: str) -> "list[Customer]":
        statement = (
            select(Customer)
            .where(Customer.name.ilike(f"%{name}%"))
            .order_by(Customer.name.asc())
            .limit(10))
        return list(self.db.scalars(statement).all())
