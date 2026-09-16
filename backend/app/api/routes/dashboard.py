from typing import Dict, Any, List
import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.db.database import get_db
from app.db.models.cattle import Cattle
from app.db.models.sensor import SensorReading
from app.db.models.alert import Alert
from app.db.models.prediction import HealthPrediction, DiseasePrediction

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_cattle = db.query(Cattle).count()
    healthy_cattle = db.query(Cattle).filter(Cattle.status == "HEALTHY").count()
    at_risk_cattle = db.query(Cattle).filter(Cattle.status == "AT_RISK").count()
    critical_cattle = db.query(Cattle).filter(Cattle.status == "CRITICAL").count()
    active_alerts = db.query(Alert).filter(Alert.status == "ACTIVE").count()

    recent_alerts = db.query(Alert).order_by(desc(Alert.created_at)).limit(5).all()
    recent_health_predictions = db.query(HealthPrediction).order_by(desc(HealthPrediction.timestamp)).limit(5).all()

    # Calculate average latest vitals
    avg_vitals = db.query(
        func.avg(SensorReading.temperature).label("avg_temp"),
        func.avg(SensorReading.heart_rate).label("avg_hr"),
        func.avg(SensorReading.respiratory_rate).label("avg_rr"),
        func.avg(SensorReading.activity_level).label("avg_act"),
        func.avg(SensorReading.feed_intake).label("avg_feed"),
        func.avg(SensorReading.water_intake).label("avg_water")
    ).first()

    return {
        "kpis": {
            "total_cattle": total_cattle,
            "healthy": healthy_cattle,
            "at_risk": at_risk_cattle,
            "critical": critical_cattle,
            "active_alerts": active_alerts
        },
        "average_vitals": {
            "temperature": round(float(avg_vitals.avg_temp or 38.6), 1),
            "heart_rate": round(float(avg_vitals.avg_hr or 66.0), 0),
            "respiratory_rate": round(float(avg_vitals.avg_rr or 27.0), 0),
            "activity_level": round(float(avg_vitals.avg_act or 0.81), 2),
            "feed_intake": round(float(avg_vitals.avg_feed or 18.2), 1),
            "water_intake": round(float(avg_vitals.avg_water or 62.5), 1)
        },
        "recent_alerts": recent_alerts,
        "recent_predictions": recent_health_predictions
    }

@router.get("/trends")
def get_herd_trends(cattle_id: int = None, limit: int = 24, db: Session = Depends(get_db)):
    query = db.query(SensorReading)
    if cattle_id:
        query = query.filter(SensorReading.cattle_id == cattle_id)
    readings = query.order_by(desc(SensorReading.timestamp)).limit(limit).all()
    readings.reverse()

    return [
        {
            "id": r.id,
            "timestamp": r.timestamp.strftime("%H:%M:%S"),
            "cattle_id": r.cattle_id,
            "temperature": r.temperature,
            "heart_rate": r.heart_rate,
            "respiratory_rate": r.respiratory_rate,
            "activity_level": r.activity_level,
            "feed_intake": r.feed_intake,
            "water_intake": r.water_intake
        }
        for r in readings
    ]
