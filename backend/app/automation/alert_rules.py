from typing import List, Dict, Optional, Tuple
from app.db.models.sensor import SensorReading
from app.db.models.alert import Alert

def evaluate_sensor_rules(reading: SensorReading, tag_id: str) -> List[Dict[str, str]]:
    """
    Evaluates physiological sensor readings against veterinary safety thresholds.
    Returns a list of alert dictionaries if conditions are violated.
    """
    alerts = []

    # 1. Temperature Rule (MLX90614)
    if reading.temperature > 40.2:
        alerts.append({
            "type": "TEMPERATURE",
            "severity": "CRITICAL",
            "message": f"Critical pyrexia/fever detected in {tag_id}: Body temperature is {reading.temperature:.1f}°C (Threshold: >40.2°C). Immediate cooling and veterinary intervention required."
        })
    elif reading.temperature > 39.4:
        alerts.append({
            "type": "TEMPERATURE",
            "severity": "WARNING",
            "message": f"Elevated temperature in {tag_id}: Body temperature is {reading.temperature:.1f}°C (Threshold: >39.4°C). Monitor for disease symptoms."
        })
    elif reading.temperature < 37.5:
        alerts.append({
            "type": "TEMPERATURE",
            "severity": "CRITICAL",
            "message": f"Hypothermia alert for {tag_id}: Body temperature dropped to {reading.temperature:.1f}°C (Threshold: <37.5°C)."
        })

    # 2. Heart Rate Rule (MAX30102)
    if reading.heart_rate > 95.0:
        alerts.append({
            "type": "HEART_RATE",
            "severity": "CRITICAL" if reading.heart_rate > 105.0 else "WARNING",
            "message": f"Tachycardia detected in {tag_id}: Heart rate elevated at {reading.heart_rate:.0f} bpm (Normal range: 48-84 bpm)."
        })
    elif reading.heart_rate < 42.0:
        alerts.append({
            "type": "HEART_RATE",
            "severity": "CRITICAL",
            "message": f"Bradycardia detected in {tag_id}: Heart rate depressed at {reading.heart_rate:.0f} bpm (Normal range: 48-84 bpm)."
        })

    # 3. Activity Level Rule (MPU6050)
    if reading.activity_level < 0.25:
        alerts.append({
            "type": "ACTIVITY",
            "severity": "CRITICAL",
            "message": f"Severe lethargy / recumbency detected in {tag_id}: Activity index is {reading.activity_level:.2f} (Normal: >0.65). Animal may be unable to stand."
        })
    elif reading.activity_level < 0.45:
        alerts.append({
            "type": "ACTIVITY",
            "severity": "WARNING",
            "message": f"Subdued movement in {tag_id}: Activity index reduced to {reading.activity_level:.2f}."
        })

    # 4. Feed & Water Intake Rules
    if reading.feed_intake < 6.0 and reading.water_intake < 22.0:
        alerts.append({
            "type": "FEED_WATER",
            "severity": "CRITICAL",
            "message": f"Acute nutritional collapse in {tag_id}: Feed intake is {reading.feed_intake:.1f} kg and water intake is {reading.water_intake:.1f} L. High dehydration/ketosis risk."
        })
    elif reading.feed_intake < 10.0:
        alerts.append({
            "type": "FEED_WATER",
            "severity": "WARNING",
            "message": f"Reduced feed consumption in {tag_id}: Feed intake at {reading.feed_intake:.1f} kg/day (Normal: 14-25 kg)."
        })

    return alerts
