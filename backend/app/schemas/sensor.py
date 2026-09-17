from pydantic import BaseModel, Field, ConfigDict, root_validator
from typing import Optional, Union, Any
import datetime

class SensorReadingBase(BaseModel):
    cattle_id: Union[int, str]
    temperature: float = Field(..., ge=30.0, le=45.0, description="Cattle body temperature in Celsius (normal: 38.0-39.3)")
    heart_rate: float = Field(..., ge=25.0, le=220.0, description="Heart rate in beats per minute (normal: 48-84)")
    respiratory_rate: float = Field(..., ge=8.0, le=90.0, description="Respiratory rate in breaths per minute (normal: 24-36)")
    activity_level: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Normalized activity level from 0.0 to 1.0")
    activity: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Normalized activity level from 0.0 to 1.0")
    feed_intake: float = Field(..., ge=0.0, le=60.0, description="Daily feed intake in kg (normal: 14-25)")
    water_intake: float = Field(..., ge=0.0, le=200.0, description="Daily water intake in liters (normal: 40-90)")
    ambient_temperature: Optional[float] = Field(default=24.0, ge=-25.0, le=65.0)
    humidity: Optional[float] = Field(default=60.0, ge=0.0, le=100.0)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timestamp: Optional[Any] = None

class SensorReadingCreate(SensorReadingBase):
    pass

class SensorReadingResponse(BaseModel):
    id: Optional[int] = None
    cattle_id: Any
    temperature: float
    heart_rate: float
    respiratory_rate: float
    activity: Optional[float] = 0.8
    activity_level: Optional[float] = 0.8
    feed_intake: float
    water_intake: float
    ambient_temperature: Optional[float] = 24.0
    humidity: Optional[float] = 60.0
    timestamp: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class SensorTelemetryBatch(BaseModel):
    readings: list[SensorReadingCreate]
