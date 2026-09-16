from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.models.sensor import SensorReading
from app.schemas.sensor import SensorReadingCreate

def record_reading(db: Session, reading_in: SensorReadingCreate) -> SensorReading:
    reading = SensorReading(**reading_in.dict())
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading

def get_readings_for_cattle(db: Session, cattle_id: int, limit: int = 50) -> List[SensorReading]:
    return db.query(SensorReading).filter(
        SensorReading.cattle_id == cattle_id
    ).order_by(desc(SensorReading.timestamp)).limit(limit).all()

def get_latest_reading(db: Session, cattle_id: int) -> Optional[SensorReading]:
    return db.query(SensorReading).filter(
        SensorReading.cattle_id == cattle_id
    ).order_by(desc(SensorReading.timestamp)).first()
