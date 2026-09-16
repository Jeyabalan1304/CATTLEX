from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.alert import AlertResponse
from app.services import alert_service

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("", response_model=List[AlertResponse])
def get_all_alerts(status: Optional[str] = None, limit: int = 100, db: Session = Depends(get_db)):
    return alert_service.get_alerts(db, status=status, limit=limit)

@router.post("/{alert_id}/resolve", response_model=AlertResponse)
def resolve_an_alert(alert_id: int, db: Session = Depends(get_db)):
    resolved = alert_service.resolve_alert(db, alert_id)
    if not resolved:
        raise HTTPException(status_code=404, detail="Alert not found")
    return resolved
