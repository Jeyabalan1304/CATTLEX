from pydantic import BaseModel, Field
from typing import Optional
import datetime

class SensorReadingBase(BaseModel):
    cattle_id: int
    temperature: float = Field(..., ge=20.0, le=48.0, description="Cattle body temperature in Celsius")
    heart_rate: float = Field(..., ge=20.0, le=220.0, description="Heart rate in beats per minute")
    respiratory_rate: float = Field(..., ge=5.0, le=100.0, description="Respiratory rate in breaths per minute")
    activity_level: float = Field(..., ge=0.0, le=1.0, description="Normalized activity level from 0.0 to 1.0")
    feed_intake: float = Field(..., ge=0.0, le=60.0, description="Daily feed intake in kg")
    water_intake: float = Field(..., ge=0.0, le=200.0, description="Daily water intake in liters")
    ambient_temperature: Optional[float] = Field(default=24.0, ge=-20.0, le=60.0)
    humidity: Optional[float] = Field(default=60.0, ge=0.0, le=100.0)
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class SensorReadingCreate(SensorReadingBase):
    pass

class SensorReadingResponse(SensorReadingBase):
    id: int
    timestamp: datetime.datetime

    class Config:
        from_attributes = True

class SensorTelemetryBatch(BaseModel):
    readings: list[SensorReadingCreate]
