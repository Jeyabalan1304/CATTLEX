from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.database import get_db
from app.schemas.cattle import CattleCreate, CattleUpdate, CattleResponse, CattleSummary
from app.services import cattle_service
from app.db.models.sensor import SensorReading
from app.db.models.prediction import HealthPrediction
from app.db.models.alert import Alert

router = APIRouter(prefix="/cattle", tags=["Cattle Management"])

@router.get("", response_model=List[CattleSummary])
def list_cattle(db: Session = Depends(get_db)):
    all_cattle = cattle_service.get_all_cattle(db)
    summaries = []
    for c in all_cattle:
        latest_reading = db.query(SensorReading).filter(
            SensorReading.cattle_id == c.id
        ).order_by(desc(SensorReading.timestamp)).first()

        latest_pred = db.query(HealthPrediction).filter(
            HealthPrediction.cattle_id == c.id
        ).order_by(desc(HealthPrediction.timestamp)).first()

        active_alerts = db.query(Alert).filter(
            Alert.cattle_id == c.id,
            Alert.status == "ACTIVE"
        ).count()

        summaries.append({
            "id": c.id,
            "tag_id": c.tag_id,
            "name": c.name,
            "breed": c.breed,
            "age": c.age,
            "sex": c.sex,
            "weight": c.weight,
            "farm_id": c.farm_id,
            "status": c.status,
            "created_at": c.created_at,
            "updated_at": c.updated_at,
            "latest_temperature": latest_reading.temperature if latest_reading else None,
            "latest_heart_rate": latest_reading.heart_rate if latest_reading else None,
            "latest_activity": latest_reading.activity_level if latest_reading else None,
            "risk_score": latest_pred.risk_score if latest_pred else 12.0,
            "active_alerts_count": active_alerts
        })
    return summaries

@router.post("", response_model=CattleResponse, status_code=status.HTTP_201_CREATED)
def add_cattle(cattle_in: CattleCreate, db: Session = Depends(get_db)):
    existing = cattle_service.get_cattle_by_tag(db, cattle_in.tag_id)
    if existing:
        raise HTTPException(status_code=400, detail=f"Cattle with tag {cattle_in.tag_id} already exists")
    return cattle_service.create_cattle(db, cattle_in)

@router.get("/{cattle_id}")
def get_cattle_profile(cattle_id: str, db: Session = Depends(get_db)):
    data = cattle_service.get_cattle_profile_summary(db, cattle_id)
    if not data or not data.get("cattle"):
        raise HTTPException(status_code=404, detail="Cattle record not found")
    c = data["cattle"]
    lr = data["latest_reading"]
    lp = data["latest_prediction"]

    return {
        "id": c.id,
        "cattle_id": getattr(c, "cattle_id", c.tag_id) or c.tag_id,
        "tag_id": c.tag_id,
        "name": c.name,
        "breed": c.breed,
        "age": c.age,
        "sex": c.sex,
        "weight": c.weight,
        "farm_id": c.farm_id,
        "farm": getattr(c, "farm_id", "FARM-01"),
        "location": getattr(c, "location", "Pasture Grid Alpha") or "Pasture Grid Alpha",
        "status": c.status,
        "registration_date": getattr(c, "registration_date", c.created_at) or c.created_at,
        "created_at": c.created_at,
        "updated_at": c.updated_at,
        "latest_vitals": {
            "temperature": lr.temperature if lr else None,
            "heart_rate": lr.heart_rate if lr else None,
            "respiratory_rate": lr.respiratory_rate if lr else None,
            "activity_level": getattr(lr, "activity", None) or getattr(lr, "activity_level", None) if lr else None,
            "feed_intake": lr.feed_intake if lr else None,
            "water_intake": lr.water_intake if lr else None,
            "timestamp": lr.timestamp if lr else None
        },
        "latest_prediction": {
            "health_status": lp.health_status if lp else c.status,
            "risk_score": lp.risk_score if lp else 15.0,
            "reason": lp.prediction_reason if lp else "Normal bovine physiology",
            "model": lp.model_name if lp else "VitalRiskEngine-v1",
            "confidence": lp.confidence if lp else 0.95
        },
        "active_alerts_count": data["active_alerts_count"]
    }

@router.put("/{cattle_id}", response_model=CattleResponse)
def update_cattle(cattle_id: str, cattle_in: CattleUpdate, db: Session = Depends(get_db)):
    updated = cattle_service.update_cattle(db, cattle_id, cattle_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Cattle record not found")
    return updated

@router.delete("/{cattle_id}")
def remove_cattle(cattle_id: str, db: Session = Depends(get_db)):
    success = cattle_service.delete_cattle(db, cattle_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cattle record not found")
    return {"status": "deleted", "cattle_id": cattle_id}
