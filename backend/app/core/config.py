import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "CATTLEX"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    DESCRIPTION: str = "An AI-Integrated, Solar-Powered IoT System Enhanced with Predictive Analytics for Multi-Disease Management in Livestock"
    
    # Environment & Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_DIR: str = os.path.join(BASE_DIR, "ml", "saved_models")
    
    # Database - Default to local SQLite for instant zero-dependency local running, or PostgreSQL when configured
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'cattlex.db')}")
    
    # JWT Security
    SECRET_KEY: str = os.getenv("JWT_SECRET", "cattlex-super-secret-key-2026-ieee-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # MQTT Broker Configuration
    MQTT_BROKER_HOST: str = os.getenv("MQTT_HOST", "localhost")
    MQTT_BROKER_PORT: int = int(os.getenv("MQTT_PORT", 1883))
    MQTT_TOPIC_PREFIX: str = "cattlex/cattle"
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "*"]

settings = Settings()
