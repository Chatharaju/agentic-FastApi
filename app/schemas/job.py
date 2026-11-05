from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class JobCreate(BaseModel):
    customer_id: UUID
    lead_id: UUID | None = None

    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    scheduled_at: datetime | None = None


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_id: UUID
    lead_id: UUID | None
    title: str
    description: str | None
    status: str
    scheduled_at: datetime | None
    created_at: datetime