import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="FARMER", nullable=False)  # FARMER, VETERINARIAN, ADMIN
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
