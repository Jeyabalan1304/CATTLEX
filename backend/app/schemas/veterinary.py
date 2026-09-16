from pydantic import BaseModel
from typing import Optional
import datetime

class AppointmentBase(BaseModel):
    cattle_id: int
    veterinarian_name: Optional[str] = "Dr. Sarah Jenkins, DVM"
    reason: str
    priority: str = "MEDIUM"  # LOW, MEDIUM, HIGH, URGENT
    scheduled_at: Optional[datetime.datetime] = None
    notes: Optional[str] = None
    status: str = "PENDING"

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    veterinarian_name: Optional[str] = None
    priority: Optional[str] = None
    scheduled_at: Optional[datetime.datetime] = None
    notes: Optional[str] = None
    status: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
