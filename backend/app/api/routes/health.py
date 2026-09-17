from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db
from app.services.ml_service import ml_service
from app.iot.sensor_simulator import simulator

router = APIRouter(tags=["Health & Readiness"])

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    # Check database
    db_status = "HEALTHY"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "UNREACHABLE"

    # Check ML model
    ml_status = "LOADED" if ml_service.model is not None else "UNINITIALIZED"

    return {
        "status": "UP" if (db_status == "HEALTHY" and ml_status == "LOADED") else "DEGRADED",
        "api": "RUNNING",
        "database": db_status,
        "ml_model": ml_status,
        "model_version": ml_service.version,
        "simulator_running": simulator.running
    }

@router.get("/health/readiness")
def readiness_check(db: Session = Depends(get_db)):
    db_ready = True
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_ready = False

    ml_ready = (ml_service.model is not None and len(ml_service.features) == 93)

    ready = db_ready and ml_ready
    return {
        "ready": ready,
        "database_connected": db_ready,
        "ml_model_loaded": ml_ready,
        "features_loaded": len(ml_service.features),
        "classes_loaded": len(ml_service.classes)
    }
