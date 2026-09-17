from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.models.cattle import Cattle
from app.db.models.sensor import SensorReading
from app.db.models.prediction import HealthPrediction
from app.db.models.alert import Alert
from app.schemas.cattle import CattleCreate, CattleUpdate

def get_all_cattle(db: Session) -> List[Cattle]:
    return db.query(Cattle).order_by(Cattle.tag_id).all()

def get_cattle_by_identifier(db: Session, identifier: any) -> Optional[Cattle]:
    if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
        c = db.query(Cattle).filter(Cattle.id == int(identifier)).first()
        if c:
            return c
    ident_str = str(identifier)
    return db.query(Cattle).filter(
        (Cattle.tag_id == ident_str) | 
        (Cattle.cattle_id == ident_str) | 
        (Cattle.name == ident_str)
    ).first()

def create_cattle(db: Session, cattle_in: CattleCreate) -> Cattle:
    data = cattle_in.dict()
    if not data.get("cattle_id"):
        data["cattle_id"] = data.get("tag_id")
    cattle = Cattle(**data)
    db.add(cattle)
    db.commit()
    db.refresh(cattle)
    return cattle

def update_cattle(db: Session, cattle_id: any, cattle_in: CattleUpdate) -> Optional[Cattle]:
    cattle = get_cattle_by_identifier(db, cattle_id)
    if not cattle:
        return None
    for field, val in cattle_in.dict(exclude_unset=True).items():
        if val is not None and hasattr(cattle, field):
            setattr(cattle, field, val)
    db.commit()
    db.refresh(cattle)
    return cattle

def delete_cattle(db: Session, cattle_id: any) -> bool:
    cattle = get_cattle_by_identifier(db, cattle_id)
    if not cattle:
        return False
    db.delete(cattle)
    db.commit()
    return True

def get_cattle_profile_summary(db: Session, cattle_id: any) -> dict:
    cattle = get_cattle_by_identifier(db, cattle_id)
    if not cattle:
        return {}

    latest_reading = db.query(SensorReading).filter(
        SensorReading.cattle_id == cattle.id
    ).order_by(desc(SensorReading.timestamp)).first()

    latest_prediction = db.query(HealthPrediction).filter(
        HealthPrediction.cattle_id == cattle.id
    ).order_by(desc(HealthPrediction.timestamp)).first()

    active_alerts = db.query(Alert).filter(
        Alert.cattle_id == cattle.id,
        Alert.status.in_(["ACTIVE", "OPEN"])
    ).count()

    return {
        "cattle": cattle,
        "latest_reading": latest_reading,
        "latest_prediction": latest_prediction,
        "active_alerts_count": active_alerts
    }
