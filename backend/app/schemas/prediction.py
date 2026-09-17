from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
import datetime

class HealthPredictionRequest(BaseModel):
    cattle_id: Union[int, str]
    temperature: float
    heart_rate: float
    respiratory_rate: float
    activity_level: Optional[float] = None
    activity: Optional[float] = None
    feed_intake: float
    water_intake: float
    ambient_temperature: Optional[float] = 25.0
    humidity: Optional[float] = 60.0

class HealthPredictionResponse(BaseModel):
    cattle_id: Any
    health_status: str          # HEALTHY, AT_RISK, CRITICAL
    risk_score: float           # 0.0 to 100.0
    model_name: str
    confidence: float
    prediction_reason: str
    timestamp: datetime.datetime

class DiseasePredictionRequest(BaseModel):
    cattle_id: Union[int, str]
    symptoms: Dict[str, Any]
    model_name: Optional[str] = "Random Forest"

class DiseaseProbability(BaseModel):
    disease: str
    display_name: Optional[str] = None
    probability: float

class ImportantFeature(BaseModel):
    feature: str
    display_name: str
    importance: float
    present: bool

class DiseasePredictionResponse(BaseModel):
    prediction_id: Optional[str] = None
    cattle_id: Any
    predicted_disease: str
    display_name: Optional[str] = None
    confidence: float
    confidence_band: Optional[str] = "HIGH"
    top_3: Optional[List[Dict[str, Any]]] = None
    top_predictions: Optional[List[DiseaseProbability]] = None
    model_version: Optional[str] = "CATTLEX-RF-v1"
    model_name: Optional[str] = "CATTLEX-RF-v1"
    important_features: Optional[List[ImportantFeature]] = []
    recommendation: Optional[str] = None
    disclaimer: str = "AI decision-support prediction — veterinary assessment required."
    created_at: Optional[datetime.datetime] = None
    timestamp: Optional[datetime.datetime] = None
