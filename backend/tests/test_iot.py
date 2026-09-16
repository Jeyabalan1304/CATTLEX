import pytest
from app.iot.payload_validator import validate_telemetry_payload
from app.iot.sensor_simulator import CattleSensorSimulator
from app.automation.alert_rules import evaluate_sensor_rules
from app.db.models.sensor import SensorReading

def test_telemetry_payload_validation():
    valid_packet = {
        "cattle_id": 1,
        "temperature": 38.6,
        "heart_rate": 65.0,
        "respiratory_rate": 26.0,
        "activity_level": 0.85,
        "feed_intake": 19.0,
        "water_intake": 65.0
    }
    is_valid, err, model = validate_telemetry_payload(valid_packet)
    assert is_valid is True
    assert err is None
    assert model.temperature == 38.6

    # Test invalid temperature
    invalid_packet = valid_packet.copy()
    invalid_packet["temperature"] = 85.0
    is_valid, err, _ = validate_telemetry_payload(invalid_packet)
    assert is_valid is False

def test_simulator_progression():
    sim = CattleSensorSimulator()
    reading = sim.generate_next_reading("COW001")
    assert reading["tag_id"] == "COW001"
    assert 35.0 <= reading["temperature"] <= 43.0
    assert 30.0 <= reading["heart_rate"] <= 150.0

    # Trigger sickness
    sim.trigger_abnormal_event("COW001")
    assert sim.cattle_states["COW001"]["state"] == "DEVELOPING_FEVER"

def test_sensor_rule_alerts():
    critical_reading = SensorReading(
        cattle_id=1,
        temperature=41.0,
        heart_rate=115.0,
        respiratory_rate=55.0,
        activity_level=0.12,
        feed_intake=4.0,
        water_intake=18.0
    )
    alerts = evaluate_sensor_rules(critical_reading, "COW001")
    assert len(alerts) >= 2
    types = [a["type"] for a in alerts]
    assert "TEMPERATURE" in types
    assert "HEART_RATE" in types
