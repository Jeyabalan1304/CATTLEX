import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    cattle_id = Column(Integer, ForeignKey("cattle.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    
    # Vital measurements
    temperature = Column(Float, nullable=False)          # °C (MLX90614)
    heart_rate = Column(Float, nullable=False)           # bpm (MAX30102)
    respiratory_rate = Column(Float, nullable=False)     # bpm (Acoustic / Accelerometer)
    activity_level = Column(Float, nullable=False)       # 0.0 - 1.0 (MPU6050)
    feed_intake = Column(Float, nullable=False)          # kg / day (Load cell)
    water_intake = Column(Float, nullable=False)         # L / day (YF-S201 flow)
    
    # Environmental telemetry
    ambient_temperature = Column(Float, nullable=True)   # °C
    humidity = Column(Float, nullable=True)              # %
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    cattle = relationship("Cattle", back_populates="sensor_readings")
