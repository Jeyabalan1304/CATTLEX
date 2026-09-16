from app.schemas.auth import UserCreate, UserResponse, Token, LoginRequest
from app.schemas.cattle import CattleCreate, CattleUpdate, CattleResponse, CattleSummary
from app.schemas.sensor import SensorReadingCreate, SensorReadingResponse, SensorTelemetryBatch
from app.schemas.prediction import (
    HealthPredictionRequest, HealthPredictionResponse,
    DiseasePredictionRequest, DiseasePredictionResponse,
    DiseaseProbability, ImportantFeature
)
from app.schemas.alert import AlertCreate, AlertResponse
from app.schemas.veterinary import AppointmentCreate, AppointmentUpdate, AppointmentResponse
