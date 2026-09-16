from pydantic import BaseModel
from typing import Optional
import datetime

class CattleBase(BaseModel):
    tag_id: str
    name: str
    breed: str
    age: int
    sex: str = "Female"
    weight: float
    farm_id: str = "FARM-01"
    status: str = "HEALTHY"

class CattleCreate(CattleBase):
    pass

class CattleUpdate(BaseModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    weight: Optional[float] = None
    farm_id: Optional[str] = None
    status: Optional[str] = None

class CattleResponse(CattleBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

class CattleSummary(CattleResponse):
    latest_temperature: Optional[float] = None
    latest_heart_rate: Optional[float] = None
    latest_activity: Optional[float] = None
    risk_score: Optional[float] = None
    active_alerts_count: Optional[int] = 0
