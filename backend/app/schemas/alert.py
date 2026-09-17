from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
import datetime

class AlertBase(BaseModel):
    cattle_id: Any
    type: Optional[str] = "HEALTH_RISK"
    alert_type: Optional[str] = None
    severity: str
    message: str
    status: str = "OPEN"

class AlertCreate(AlertBase):
    pass

class AlertResponse(BaseModel):
    id: int
    cattle_id: Any
    type: Optional[str] = "HEALTH_RISK"
    alert_type: Optional[str] = None
    severity: str
    message: str
    status: str
    timestamp: Optional[datetime.datetime] = None
    created_at: Optional[datetime.datetime] = None
    acknowledged_at: Optional[datetime.datetime] = None
    resolved_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)
