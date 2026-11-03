from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

LEAD_STATUSES = {"New", "Contacted", "Interested", "Qualified", "Converted", "Lost"}

class LeadCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    company: str | None = Field(default=None, max_length=150)
    source: str | None = Field(default=None, max_length=80)
    status: str = "New"
    notes: str | None = None

class LeadUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    company: str | None = Field(default=None, max_length=150)
    source: str | None = Field(default=None, max_length=80)
    status: str | None = None
    notes: str | None = None

class LeadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str | None
    phone: str | None
    company: str | None
    source: str | None
    status: str
    notes: str | None
    created_at: datetime
    updated_at: datetime

class FollowUpCreate(BaseModel):
    due_date: date
    description: str = Field(min_length=1, max_length=500)

class FollowUpUpdate(BaseModel):
    status: str = Field(pattern="^(Pending|Completed|Cancelled)$")

class FollowUpOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    lead_id: int
    due_date: date
    description: str
    status: str
    created_at: datetime

class InteractionCreate(BaseModel):
    interaction_type: str = Field(min_length=1, max_length=50)
    details: str = Field(min_length=1)

class InteractionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    lead_id: int
    interaction_type: str
    details: str
    interacted_at: datetime
