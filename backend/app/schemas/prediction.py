from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import datetime

class HealthPredictionRequest(BaseModel):
    cattle_id: int
    temperature: float
    heart_rate: float
    respiratory_rate: float
    activity_level: float
    feed_intake: float
    water_intake: float
    ambient_temperature: Optional[float] = 25.0
    humidity: Optional[float] = 60.0

class HealthPredictionResponse(BaseModel):
    cattle_id: int
    health_status: str          # HEALTHY, AT_RISK, CRITICAL
    risk_score: float           # 0.0 to 100.0
    model_name: str
    confidence: float
    prediction_reason: str
    timestamp: datetime.datetime

class DiseasePredictionRequest(BaseModel):
    cattle_id: int
    symptoms: Dict[str, bool]
    model_name: Optional[str] = "Random Forest"

class DiseaseProbability(BaseModel):
    disease: str
    display_name: str
    probability: float

class ImportantFeature(BaseModel):
    feature: str
    display_name: str
    importance: float
    present: bool

class DiseasePredictionResponse(BaseModel):
    cattle_id: int
    predicted_disease: str
    display_name: str
    confidence: float
    model_name: str
    top_predictions: List[DiseaseProbability]
    important_features: List[ImportantFeature]
    recommendation: str
    disclaimer: str = "This is a predictive decision-support system and not a definitive veterinary diagnosis. Professional veterinary evaluation is recommended."
    timestamp: datetime.datetime
