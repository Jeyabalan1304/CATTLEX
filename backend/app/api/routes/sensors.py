from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.sensor import SensorReadingCreate, SensorReadingResponse
from app.services import sensor_service
from app.iot.mqtt_client import mqtt_manager

router = APIRouter(prefix="/sensors", tags=["Sensor Telemetry"])

@router.post("/readings")
def ingest_reading(reading_in: SensorReadingCreate, db: Session = Depends(get_db)):
    """
    Direct HTTP ingestion of IoT sensor packet (used by collar nodes or simulator).
    Triggers the CATTLEX automated telemetry and health workflow.
    """
    res = mqtt_manager.process_telemetry(reading_in.dict())
    return {
        "status": "success",
        "detail": "Reading ingested and processed through CATTLEX risk pipeline",
        "data": res
    }

@router.get("/{cattle_id}", response_model=List[SensorReadingResponse])
def get_sensor_history(cattle_id: int, limit: int = 50, db: Session = Depends(get_db)):
    readings = sensor_service.get_readings_for_cattle(db, cattle_id, limit=limit)
    return readings

@router.get("/{cattle_id}/latest", response_model=SensorReadingResponse)
def get_latest_sensor_value(cattle_id: int, db: Session = Depends(get_db)):
    reading = sensor_service.get_latest_reading(db, cattle_id)
    if not reading:
        raise HTTPException(status_code=404, detail="No sensor readings found for this cattle")
    return reading
