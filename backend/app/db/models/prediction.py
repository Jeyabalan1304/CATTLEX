import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class HealthPrediction(Base):
    __tablename__ = "health_predictions"

    id = Column(Integer, primary_key=True, index=True)
    cattle_id = Column(Integer, ForeignKey("cattle.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    health_status = Column(String(50), nullable=False)   # HEALTHY, AT_RISK, CRITICAL
    risk_score = Column(Float, nullable=False)           # 0.0 to 100.0
    model_name = Column(String(100), default="VitalRiskEngine-RF", nullable=False)
    model_version = Column(String(50), default="1.0.0", nullable=False)
    confidence = Column(Float, nullable=False)
    prediction_reason = Column(Text, nullable=True)

    cattle = relationship("Cattle", back_populates="health_predictions")


import uuid

class DiseasePrediction(Base):
    __tablename__ = "disease_predictions"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(String(50), default=lambda: str(uuid.uuid4()), index=True)
    cattle_id = Column(Integer, ForeignKey("cattle.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    predicted_disease = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    confidence_band = Column(String(20), default="HIGH", nullable=False)
    model_name = Column(String(100), default="CATTLEX-RF-v1", nullable=False)
    model_version = Column(String(50), default="CATTLEX-RF-v1", nullable=False)
    input_symptoms = Column(Text, nullable=False)        # JSON string of active symptoms
    top_3 = Column(Text, nullable=True)                 # JSON string of top 3 predictions
    top_predictions = Column(Text, nullable=True)        # JSON string of top 3 predictions
    important_features = Column(Text, nullable=True)     # JSON string of key feature weights
    recommendation = Column(Text, nullable=False)

    cattle = relationship("Cattle", back_populates="disease_predictions")
