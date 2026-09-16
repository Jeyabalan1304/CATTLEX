from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.models.veterinary import VeterinaryAppointment
from app.schemas.veterinary import AppointmentCreate, AppointmentUpdate

def get_appointments(db: Session, status: Optional[str] = None) -> List[VeterinaryAppointment]:
    query = db.query(VeterinaryAppointment)
    if status:
        query = query.filter(VeterinaryAppointment.status == status)
    return query.order_by(desc(VeterinaryAppointment.created_at)).all()

def create_appointment(db: Session, appt_in: AppointmentCreate) -> VeterinaryAppointment:
    appt = VeterinaryAppointment(**appt_in.dict())
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt

def update_appointment(db: Session, appt_id: int, appt_in: AppointmentUpdate) -> Optional[VeterinaryAppointment]:
    appt = db.query(VeterinaryAppointment).filter(VeterinaryAppointment.id == appt_id).first()
    if not appt:
        return None
    for field, val in appt_in.dict(exclude_unset=True).items():
        setattr(appt, field, val)
    db.commit()
    db.refresh(appt)
    return appt
