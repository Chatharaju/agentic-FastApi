from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

#A schema describes the data your API accepts or returns.
#ConfigDict helps to read SQLAlchmey objects coming from DB (Allow Pydantic to serialize SQLAlchemy models)
class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    address: str | None = Field(default=None, max_length=500)


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    email: EmailStr | None
    phone: str | None
    address: str | None
    created_at: datetime