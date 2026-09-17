import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base

class Cattle(Base):
    __tablename__ = "cattle"

    id = Column(Integer, primary_key=True, index=True)
    cattle_id = Column(String(50), nullable=True, index=True)
    tag_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    breed = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)  # in months
    sex = Column(String(20), default="Female", nullable=False)
    weight = Column(Float, nullable=False)  # in kg
    farm_id = Column(String(50), default="FARM-01", nullable=False)
    location = Column(String(100), default="Pasture Grid Alpha", nullable=True)
    status = Column(String(50), default="HEALTHY", nullable=False)  # HEALTHY, AT_RISK, CRITICAL
    registration_date = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    sensor_readings = relationship("SensorReading", back_populates="cattle", cascade="all, delete-orphan")
    health_predictions = relationship("HealthPrediction", back_populates="cattle", cascade="all, delete-orphan")
    disease_predictions = relationship("DiseasePrediction", back_populates="cattle", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="cattle", cascade="all, delete-orphan")
    appointments = relationship("VeterinaryAppointment", back_populates="cattle", cascade="all, delete-orphan")
