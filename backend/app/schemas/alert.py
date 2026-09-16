from pydantic import BaseModel
from typing import Optional
import datetime

class AlertBase(BaseModel):
    cattle_id: int
    type: str
    severity: str
    message: str
    status: str = "ACTIVE"

class AlertCreate(AlertBase):
    pass

class AlertResponse(AlertBase):
    id: int
    created_at: datetime.datetime
    resolved_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True
