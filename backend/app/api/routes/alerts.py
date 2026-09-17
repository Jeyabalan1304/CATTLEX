from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.alert import AlertResponse
from app.services import alert_service

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("", response_model=List[AlertResponse])
def get_all_alerts(
    status: Optional[str] = None, 
    severity: Optional[str] = None,
    cattle_id: Optional[int] = None,
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    alerts = alert_service.get_alerts(db, status=status, severity=severity, cattle_id=cattle_id, limit=limit)
    res = []
    for a in alerts:
        res.append({
            "id": a.id,
            "cattle_id": a.cattle_id,
            "type": getattr(a, "alert_type", None) or getattr(a, "type", "HEALTH_RISK"),
            "alert_type": getattr(a, "alert_type", None) or getattr(a, "type", "HEALTH_RISK"),
            "severity": a.severity,
            "message": a.message,
            "status": a.status,
            "timestamp": getattr(a, "timestamp", a.created_at) or a.created_at,
            "created_at": a.created_at,
            "acknowledged_at": getattr(a, "acknowledged_at", None),
            "resolved_at": a.resolved_at
        })
    return res

@router.post("/{alert_id}/acknowledge", response_model=AlertResponse)
def acknowledge_an_alert(alert_id: int, db: Session = Depends(get_db)):
    ack = alert_service.acknowledge_alert(db, alert_id)
    if not ack:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {
        "id": ack.id,
        "cattle_id": ack.cattle_id,
        "type": getattr(ack, "alert_type", None) or getattr(ack, "type", "HEALTH_RISK"),
        "alert_type": getattr(ack, "alert_type", None) or getattr(ack, "type", "HEALTH_RISK"),
        "severity": ack.severity,
        "message": ack.message,
        "status": ack.status,
        "timestamp": getattr(ack, "timestamp", ack.created_at) or ack.created_at,
        "created_at": ack.created_at,
        "acknowledged_at": getattr(ack, "acknowledged_at", None),
        "resolved_at": ack.resolved_at
    }

@router.post("/{alert_id}/resolve", response_model=AlertResponse)
def resolve_an_alert(alert_id: int, db: Session = Depends(get_db)):
    resolved = alert_service.resolve_alert(db, alert_id)
    if not resolved:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {
        "id": resolved.id,
        "cattle_id": resolved.cattle_id,
        "type": getattr(resolved, "alert_type", None) or getattr(resolved, "type", "HEALTH_RISK"),
        "alert_type": getattr(resolved, "alert_type", None) or getattr(resolved, "type", "HEALTH_RISK"),
        "severity": resolved.severity,
        "message": resolved.message,
        "status": resolved.status,
        "timestamp": getattr(resolved, "timestamp", resolved.created_at) or resolved.created_at,
        "created_at": resolved.created_at,
        "acknowledged_at": getattr(resolved, "acknowledged_at", None),
        "resolved_at": resolved.resolved_at
    }
