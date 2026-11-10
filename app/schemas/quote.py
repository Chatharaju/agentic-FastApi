
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class QuoteCreate(BaseModel):
    customer_id: UUID | None = None
    lead_id: UUID | None = None

    description: str = Field(min_length=1)
    subtotal: Decimal = Field(gt=0, max_digits=12, decimal_places=2)

    tax_rate: Decimal = Field(
        default=Decimal("13.00"),
        ge=0,
        le=100,
        max_digits=5,
        decimal_places=2,
    )

    @model_validator(mode="after")
    def validate_recipient(self):
        if (self.customer_id is None) == (self.lead_id is None):
            raise ValueError(
                "Provide exactly one of customer_id or lead_id."
            )
        return self


class QuoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_id: UUID | None
    lead_id: UUID | None
    description: str
    subtotal: Decimal
    tax_rate: Decimal
    tax_amount: Decimal
    total: Decimal
    currency: str
    status: str
