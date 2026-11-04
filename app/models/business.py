from dataclasses import dataclass, field
from typing import List

@dataclass
class Customer:
    id: str
    name: str
    phone: str
    email: str
    address: str

@dataclass
class Lead:
    id: str
    customer_id: str
    service: str
    status: str
    source: str

@dataclass
class QuoteItem:
    description: str
    quantity: int
    unit_price: float

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price

@dataclass
class Quote:
    id: str
    customer_id: str
    items: List[QuoteItem] = field(default_factory=list)
    subtotal: float = 0
    tax: float = 0
    total: float = 0
    status: str = "draft"