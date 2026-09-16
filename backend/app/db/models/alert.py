import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    cattle_id = Column(Integer, ForeignKey("cattle.id"), nullable=False, index=True)
    type = Column(String(50), nullable=False)            # TEMPERATURE, HEART_RATE, ACTIVITY, FEED_WATER, MULTI_VITAL, DISEASE_RISK
    severity = Column(String(20), nullable=False)        # INFO, WARNING, CRITICAL
    message = Column(Text, nullable=False)
    status = Column(String(20), default="ACTIVE", nullable=False)  # ACTIVE, RESOLVED, DISMISSED
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    resolved_at = Column(DateTime, nullable=True)

    cattle = relationship("Cattle", back_populates="alerts")
