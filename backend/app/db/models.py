"""
CATTLEX - Normalized SQLAlchemy Database Entities
Includes users, farms, cattle, sensor_devices, sensor_readings, health_risk_records,
disease_predictions, prediction_probabilities, alerts, alert_events, audit_logs, and veterinary appointments.
"""

from __future__ import annotations
import datetime
import uuid
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Index
)
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="FARM_MANAGER", nullable=False)  # ADMIN, VETERINARIAN, FARM_MANAGER, VIEWER
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    appointments = relationship("VeterinaryAppointment", back_populates="veterinarian")


class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    location = Column(String(200), default="Pasture Grid Alpha")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    cattle = relationship("Cattle", back_populates="farm")


class Cattle(Base):
    __tablename__ = "cattle"

    id = Column(Integer, primary_key=True, index=True)
    cattle_id = Column(String(50), unique=True, index=True, nullable=False) # e.g. CATTLE-001
    tag_id = Column(String(50), unique=True, index=True, nullable=False)    # e.g. COW001 / RFID-001
    name = Column(String(100), nullable=False)
    breed = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)                                   # in months
    sex = Column(String(20), default="Female", nullable=False)
    weight = Column(Float, nullable=False)                                  # in kg
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=True)
    location = Column(String(100), default="North Meadow")
    status = Column(String(50), default="HEALTHY", nullable=False, index=True) # HEALTHY, AT_RISK, CRITICAL
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    farm = relationship("Farm", back_populates="cattle")
    devices = relationship("SensorDevice", back_populates="cattle", cascade="all, delete-orphan")
    sensor_readings = relationship("SensorReading", back_populates="cattle", cascade="all, delete-orphan")
    health_risks = relationship("HealthRiskRecord", back_populates="cattle", cascade="all, delete-orphan")
    disease_predictions = relationship("DiseasePrediction", back_populates="cattle", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="cattle", cascade="all, delete-orphan")
    appointments = relationship("VeterinaryAppointment", back_populates="cattle", cascade="all, delete-orphan")


class SensorDevice(Base):
    __tablename__ = "sensor_devices"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(100), unique=True, index=True, nullable=False) # e.g. COLLAR-COW001
    cattle_id = Column(Integer, ForeignKey("cattle.id"), nullable=True)
    device_type = Column(String(50), default="SOLAR_COLLAR")                 # SOLAR_COLLAR, TROUGH_FEED_RFID, TROUGH_WATER_FLOW
    battery_level = Column(Float, default=98.0)                              # percentage
    status = Column(String(30), default="ONLINE")                            # ONLINE, OFFLINE, LOW_BATTERY
    registered_at = Column(DateTime, default=datetime.datetime.utcnow)

    cattle = relationship("Cattle", back_populates="devices")


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    cattle_id = Column(Integer, ForeignKey("cattle.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    
    # Vital measurements
    temperature = Column(Float, nullable=False)          # °C (MLX90614)
    heart_rate = Column(Float, nullable=False)           # bpm (MAX30102)
    respiratory_rate = Column(Float, nullable=False)     # breaths/min (Acoustic / IMU)
    activity = Column(Float, nullable=False)             # 0.0 - 1.0 (MPU6050)
    feed_intake = Column(Float, nullable=False)          # kg/day (Load Cell + HX711)
    water_intake = Column(Float, nullable=False)         # L/day (YF-S201 Flow)
    
    # Environmental telemetry
    ambient_temperature = Column(Float, default=24.0)    # °C
    humidity = Column(Float, default=60.0)               # %
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    cattle = relationship("Cattle", back_populates="sensor_readings")

Index("idx_sensor_cattle_timestamp", SensorReading.cattle_id, SensorReading.timestamp)


class HealthRiskRecord(Base):
    __tablename__ = "health_risk_records"

    id = Column(Integer, primary_key=True, index=True)
    cattle_id = Column(Integer, ForeignKey("cattle.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    risk_score = Column(Float, nullable=False)           # 0.0 to 100.0
    risk_level = Column(String(30), nullable=False, index=True) # HEALTHY, AT_RISK, CRITICAL
    factors = Column(Text, nullable=False)               # JSON array of factor contributions
    explanation = Column(Text, nullable=False)

    cattle = relationship("Cattle", back_populates="health_risks")

Index("idx_risk_cattle_timestamp", HealthRiskRecord.cattle_id, HealthRiskRecord.timestamp)


class DiseasePrediction(Base):
    __tablename__ = "disease_predictions"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(String(50), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    cattle_id = Column(Integer, ForeignKey("cattle.id"), nullable=False, index=True)
    predicted_disease = Column(String(100), nullable=False, index=True)
    confidence = Column(Float, nullable=False)
    confidence_band = Column(String(20), nullable=False) # HIGH, MODERATE, LOW
    model_version = Column(String(50), default="CATTLEX-RF-v1", nullable=False)
    input_symptoms = Column(Text, nullable=False)        # JSON string of active symptoms
    top_3 = Column(Text, nullable=False)                 # JSON string of top 3 predictions
    recommendation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    cattle = relationship("Cattle", back_populates="disease_predictions")
    probabilities = relationship("PredictionProbability", back_populates="prediction", cascade="all, delete-orphan")


class PredictionProbability(Base):
    __tablename__ = "prediction_probabilities"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(String(50), ForeignKey("disease_predictions.prediction_id"), nullable=False, index=True)
    disease = Column(String(100), nullable=False)
    probability = Column(Float, nullable=False)

    prediction = relationship("DiseasePrediction", back_populates="probabilities")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    cattle_id = Column(Integer, ForeignKey("cattle.id"), nullable=False, index=True)
    alert_type = Column(String(50), nullable=False)      # CRITICAL_HEALTH_RISK, TEMPERATURE_ABNORMALITY, etc.
    severity = Column(String(20), nullable=False)        # INFO, WARNING, CRITICAL
    message = Column(Text, nullable=False)
    status = Column(String(20), default="OPEN", nullable=False, index=True) # OPEN, ACKNOWLEDGED, RESOLVED
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    acknowledged_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)

    cattle = relationship("Cattle", back_populates="alerts")
    events = relationship("AlertEvent", back_populates="alert", cascade="all, delete-orphan")

Index("idx_alert_cattle_status", Alert.cattle_id, Alert.status)


class AlertEvent(Base):
    __tablename__ = "alert_events"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=False, index=True)
    action = Column(String(50), nullable=False)          # CREATED, ACKNOWLEDGED, RESOLVED
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    performed_by = Column(String(100), default="SYSTEM_AUTOMATION")

    alert = relationship("Alert", back_populates="events")


class VeterinaryAppointment(Base):
    __tablename__ = "veterinary_appointments"

    id = Column(Integer, primary_key=True, index=True)
    cattle_id = Column(Integer, ForeignKey("cattle.id"), nullable=False, index=True)
    veterinarian_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    veterinarian_name = Column(String(100), default="Dr. Sarah Jenkins, DVM")
    reason = Column(Text, nullable=False)
    priority = Column(String(20), default="MEDIUM", nullable=False) # LOW, MEDIUM, HIGH, URGENT
    scheduled_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(30), default="PENDING", nullable=False)  # PENDING, SCHEDULED, IN_PROGRESS, COMPLETED, CANCELLED
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    cattle = relationship("Cattle", back_populates="appointments")
    veterinarian = relationship("User", back_populates="appointments")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    details = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    user_id = Column(Integer, nullable=True)
