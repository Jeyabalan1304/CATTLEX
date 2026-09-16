import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class VeterinaryAppointment(Base):
    __tablename__ = "veterinary_appointments"

    id = Column(Integer, primary_key=True, index=True)
    cattle_id = Column(Integer, ForeignKey("cattle.id"), nullable=False, index=True)
    veterinarian_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    veterinarian_name = Column(String(100), default="Dr. Sarah Jenkins, DVM")
    reason = Column(Text, nullable=False)
    priority = Column(String(20), default="MEDIUM", nullable=False)  # LOW, MEDIUM, HIGH, URGENT
    scheduled_at = Column(DateTime, default=lambda: datetime.datetime.utcnow() + datetime.timedelta(days=1))
    status = Column(String(30), default="PENDING", nullable=False)   # PENDING, SCHEDULED, IN_PROGRESS, COMPLETED, CANCELLED
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    cattle = relationship("Cattle", back_populates="appointments")
