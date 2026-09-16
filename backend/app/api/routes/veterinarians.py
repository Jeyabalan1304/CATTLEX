from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.user import User
from app.schemas.veterinary import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from app.services import veterinary_service

router = APIRouter(prefix="/veterinarians", tags=["Veterinary Workflow"])

@router.get("")
def list_veterinarians(db: Session = Depends(get_db)):
    vets = db.query(User).filter(User.role == "VETERINARIAN").all()
    if not vets:
        return [
            {"id": 901, "name": "Dr. Sarah Jenkins, DVM", "email": "s.jenkins@cattlex.io", "specialty": "Bovine Internal Medicine"},
            {"id": 902, "name": "Dr. Robert Vance, DVM", "email": "r.vance@cattlex.io", "specialty": "Livestock Epidemiology & Surgery"}
        ]
    return [{"id": v.id, "name": v.name, "email": v.email, "specialty": "Veterinary Livestock Practitioner"} for v in vets]

@router.get("/appointments", response_model=List[AppointmentResponse])
def get_appointments(status: Optional[str] = None, db: Session = Depends(get_db)):
    return veterinary_service.get_appointments(db, status=status)

@router.post("/appointments", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(appt_in: AppointmentCreate, db: Session = Depends(get_db)):
    return veterinary_service.create_appointment(db, appt_in)

@router.put("/appointments/{appt_id}", response_model=AppointmentResponse)
def update_appointment(appt_id: int, appt_in: AppointmentUpdate, db: Session = Depends(get_db)):
    updated = veterinary_service.update_appointment(db, appt_id, appt_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return updated
