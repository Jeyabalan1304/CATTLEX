import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.models.alert import Alert

def get_alerts(
    db: Session, 
    status: Optional[str] = None, 
    severity: Optional[str] = None,
    cattle_id: Optional[int] = None,
    limit: int = 100
) -> List[Alert]:
    query = db.query(Alert)
    if status:
        if status.upper() in ["OPEN", "ACTIVE"]:
            query = query.filter(Alert.status.in_(["OPEN", "ACTIVE"]))
        else:
            query = query.filter(Alert.status == status.upper())
    if severity:
        query = query.filter(Alert.severity == severity.upper())
    if cattle_id:
        query = query.filter(Alert.cattle_id == cattle_id)
    return query.order_by(desc(Alert.created_at)).limit(limit).all()

def acknowledge_alert(db: Session, alert_id: int) -> Optional[Alert]:
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        return None
    alert.status = "ACKNOWLEDGED"
    alert.acknowledged_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(alert)
    return alert

def resolve_alert(db: Session, alert_id: int) -> Optional[Alert]:
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        return None
    alert.status = "RESOLVED"
    alert.resolved_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(alert)
    return alert
