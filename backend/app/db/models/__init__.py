from app.db.models.user import User
from app.db.models.cattle import Cattle
from app.db.models.sensor import SensorReading
from app.db.models.prediction import HealthPrediction, DiseasePrediction
from app.db.models.alert import Alert
from app.db.models.veterinary import VeterinaryAppointment

__all__ = [
    "User",
    "Cattle",
    "SensorReading",
    "HealthPrediction",
    "DiseasePrediction",
    "Alert",
    "VeterinaryAppointment"
]
