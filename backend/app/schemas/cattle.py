from pydantic import BaseModel, ConfigDict
from typing import Optional, Union, Any
import datetime

class CattleBase(BaseModel):
    tag_id: str
    cattle_id: Optional[str] = None
    name: str
    breed: str
    age: int
    sex: str = "Female"
    weight: float
    farm_id: Optional[str] = "FARM-01"
    farm: Optional[str] = "FARM-01"
    location: Optional[str] = "Pasture Grid Alpha"
    status: str = "HEALTHY"

class CattleCreate(CattleBase):
    pass

class CattleUpdate(BaseModel):
    cattle_id: Optional[str] = None
    name: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    weight: Optional[float] = None
    farm_id: Optional[str] = None
    farm: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None

class CattleResponse(CattleBase):
    id: int
    registration_date: Optional[datetime.datetime] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class CattleSummary(CattleResponse):
    latest_temperature: Optional[float] = None
    latest_heart_rate: Optional[float] = None
    latest_activity: Optional[float] = None
    risk_score: Optional[float] = None
    active_alerts_count: Optional[int] = 0
