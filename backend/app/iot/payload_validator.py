from typing import Dict, Any, Tuple, Optional
from app.schemas.sensor import SensorReadingCreate

def validate_telemetry_payload(data: Dict[str, Any]) -> Tuple[bool, Optional[str], Optional[SensorReadingCreate]]:
    """
    Validates incoming JSON telemetry packet against cattle sensor schema.
    """
    try:
        validated = SensorReadingCreate(**data)
        return True, None, validated
    except Exception as e:
        return False, str(e), None
