import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.models.alert import Alert

def get_alerts(db: Session, status: Optional[str] = None, limit: int = 100) -> List[Alert]:
    query = db.query(Alert)
    if status:
        query = query.filter(Alert.status == status)
    return query.order_by(desc(Alert.created_at)).limit(limit).all()

def resolve_alert(db: Session, alert_id: int) -> Optional[Alert]:
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        return None
    alert.status = "RESOLVED"
    alert.resolved_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(alert)
    return alert
