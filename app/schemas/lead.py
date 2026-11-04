from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

#This defines the data the API accepts and returns.
#ConfigDict helps to read SQLAlchmey objects coming from DB (Allow Pydantic to serialize SQLAlchemy models)
class LeadCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    service_type: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=2000)


class LeadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    email: EmailStr | None
    phone: str | None
    service_type: str
    description: str | None
    status: str
    created_at: datetime