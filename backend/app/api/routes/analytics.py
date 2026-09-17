from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.db.database import get_db
from app.db.models.cattle import Cattle
from app.db.models.sensor import SensorReading
from app.db.models.alert import Alert
from app.db.models.prediction import HealthPrediction, DiseasePrediction
from app.services.ml_service import ml_service

router = APIRouter(prefix="/analytics", tags=["Analytics & Explainability"])

@router.get("/overview")
def get_analytics_overview(
    days: Optional[int] = Query(default=30, description="Time window in days: 1 (today), 7, 30, etc."),
    db: Session = Depends(get_db)
):
    cutoff = datetime.utcnow() - timedelta(days=days)

    total_cattle = db.query(Cattle).count()
    healthy_cattle = db.query(Cattle).filter(Cattle.status == "HEALTHY").count()
    at_risk_cattle = db.query(Cattle).filter(Cattle.status == "AT_RISK").count()
    critical_cattle = db.query(Cattle).filter(Cattle.status == "CRITICAL").count()

    active_alerts = db.query(Alert).filter(Alert.status.in_(["ACTIVE", "OPEN"])).count()
    resolved_alerts = db.query(Alert).filter(Alert.status == "RESOLVED").count()

    total_predictions = db.query(DiseasePrediction).filter(DiseasePrediction.timestamp >= cutoff).count()
    total_readings = db.query(SensorReading).filter(SensorReading.timestamp >= cutoff).count()

    # Vitals average
    avg_vitals = db.query(
        func.avg(SensorReading.temperature).label("avg_temp"),
        func.avg(SensorReading.heart_rate).label("avg_hr"),
        func.avg(SensorReading.respiratory_rate).label("avg_rr"),
        func.avg(SensorReading.feed_intake).label("avg_feed"),
        func.avg(SensorReading.water_intake).label("avg_water")
    ).filter(SensorReading.timestamp >= cutoff).first()

    return {
        "timeframe_days": days,
        "kpis": {
            "total_cattle": total_cattle,
            "healthy": healthy_cattle,
            "at_risk": at_risk_cattle,
            "critical": critical_cattle,
            "active_alerts": active_alerts,
            "resolved_alerts": resolved_alerts,
            "total_predictions": total_predictions,
            "total_readings": total_readings
        },
        "health_distribution": {
            "HEALTHY": healthy_cattle,
            "AT_RISK": at_risk_cattle,
            "CRITICAL": critical_cattle
        },
        "average_vitals": {
            "temperature": round(float(avg_vitals.avg_temp or 38.6), 1),
            "heart_rate": round(float(avg_vitals.avg_hr or 65.0), 0),
            "respiratory_rate": round(float(avg_vitals.avg_rr or 26.0), 0),
            "feed_intake": round(float(avg_vitals.avg_feed or 18.5), 1),
            "water_intake": round(float(avg_vitals.avg_water or 63.0), 1)
        }
    }

@router.get("/diseases")
def get_disease_analytics(
    days: Optional[int] = Query(default=30),
    db: Session = Depends(get_db)
):
    cutoff = datetime.utcnow() - timedelta(days=days)
    records = db.query(
        DiseasePrediction.predicted_disease,
        func.count(DiseasePrediction.id).label("count"),
        func.avg(DiseasePrediction.confidence).label("avg_confidence")
    ).filter(
        DiseasePrediction.timestamp >= cutoff
    ).group_by(DiseasePrediction.predicted_disease).all()

    distribution = [
        {
            "disease": r.predicted_disease,
            "display_name": r.predicted_disease.replace("_", " ").title(),
            "count": r.count,
            "average_confidence": round(float(r.avg_confidence or 0.0), 4)
        }
        for r in records
    ]

    return {
        "timeframe_days": days,
        "total_diseases_detected": len(distribution),
        "distribution": distribution
    }

@router.get("/health")
def get_health_risk_analytics(
    days: Optional[int] = Query(default=7),
    db: Session = Depends(get_db)
):
    cutoff = datetime.utcnow() - timedelta(days=days)
    records = db.query(
        HealthPrediction.health_status,
        func.count(HealthPrediction.id).label("count"),
        func.avg(HealthPrediction.risk_score).label("avg_risk")
    ).filter(
        HealthPrediction.timestamp >= cutoff
    ).group_by(HealthPrediction.health_status).all()

    return {
        "timeframe_days": days,
        "risk_levels": [
            {
                "status": r.health_status,
                "count": r.count,
                "average_risk_score": round(float(r.avg_risk or 0.0), 2)
            }
            for r in records
        ]
    }

@router.get("/sensors")
def get_sensor_analytics(
    cattle_id: Optional[int] = None,
    limit: int = Query(default=50, le=200),
    db: Session = Depends(get_db)
):
    query = db.query(SensorReading)
    if cattle_id:
        query = query.filter(SensorReading.cattle_id == cattle_id)
    readings = query.order_by(desc(SensorReading.timestamp)).limit(limit).all()
    readings.reverse()

    return [
        {
            "id": r.id,
            "cattle_id": r.cattle_id,
            "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": r.temperature,
            "heart_rate": r.heart_rate,
            "respiratory_rate": r.respiratory_rate,
            "activity": getattr(r, "activity", None) or getattr(r, "activity_level", 0.8),
            "feed_intake": r.feed_intake,
            "water_intake": r.water_intake
        }
        for r in readings
    ]

@router.get("/feature-importance")
def get_model_feature_importance(top_n: int = Query(default=20, le=93)):
    """
    Returns the top learned features from Random Forest feature importance.
    Scientifically labeled: Model feature importance (not clinical cause of disease).
    """
    features = ml_service.get_feature_importance(top_n=top_n)
    return {
        "model": ml_service.version,
        "title": "Model Feature Importance",
        "description": "Learned Gini feature importance from CATTLEX-RF-v1 Random Forest classifier.",
        "note": "Model feature importance represents statistical weighting in the trained decision trees and does not constitute proven biological causality.",
        "features": features
    }
