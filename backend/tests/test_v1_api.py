import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_v1_health_and_readiness():
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["api"] == "RUNNING"
    assert data["database"] == "HEALTHY"
    assert data["ml_model"] == "LOADED"

    resp_ready = client.get("/api/v1/health/readiness")
    assert resp_ready.status_code == 200
    assert resp_ready.json()["ready"] is True
    assert resp_ready.json()["features_loaded"] == 93
    assert resp_ready.json()["classes_loaded"] == 26

def test_v1_ml_model_info():
    resp = client.get("/api/v1/ml/model-info")
    assert resp.status_code == 200
    data = resp.json()
    assert data["model"] == "Random Forest"
    assert data["version"] == "CATTLEX-RF-v1"
    assert data["features"] == 93
    assert data["classes"] == 26
    assert data["independent_test_accuracy"] == 0.9885
    assert data["independent_test_macro_f1"] == 0.9487
    assert data["balanced_accuracy"] == 0.9615

def test_v1_prediction_features():
    resp = client.get("/api/v1/predictions/features")
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] == 93
    assert len(data["features"]) == 93
    assert "fever" in data["features"]
    assert "depression" in data["features"]

def test_v1_disease_prediction_endpoint():
    payload = {
        "cattle_id": "COW001",
        "symptoms": {
            "fever": 1,
            "loss_of_appetite": 1,
            "depression": 1,
            "udder_swelling": 1,
            "udder_heat": 1,
            "milk_flakes": 1
        }
    }
    resp = client.post("/api/v1/predictions/disease", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "prediction_id" in data
    assert "predicted_disease" in data
    assert "confidence" in data
    assert data["confidence_band"] in ["HIGH", "MODERATE", "LOW"]
    assert "top_3" in data
    assert len(data["top_3"]) <= 3
    assert data["model_version"] == "CATTLEX-RF-v1"

def test_v1_sensor_readings_ingestion():
    payload = {
        "cattle_id": 1,
        "temperature": 39.4,
        "heart_rate": 82.0,
        "respiratory_rate": 31.0,
        "activity": 0.65,
        "feed_intake": 16.0,
        "water_intake": 55.0,
        "ambient_temperature": 28.0,
        "humidity": 65.0
    }
    resp = client.post("/api/v1/sensors/readings", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"

def test_v1_alerts_lifecycle():
    # Fetch alerts
    resp = client.get("/api/v1/alerts")
    assert resp.status_code == 200
    alerts = resp.json()
    assert isinstance(alerts, list)

    if alerts:
        alert_id = alerts[0]["id"]
        # Acknowledge
        resp_ack = client.post(f"/api/v1/alerts/{alert_id}/acknowledge")
        assert resp_ack.status_code == 200
        assert resp_ack.json()["status"] == "ACKNOWLEDGED"

        # Resolve
        resp_res = client.post(f"/api/v1/alerts/{alert_id}/resolve")
        assert resp_res.status_code == 200
        assert resp_res.json()["status"] == "RESOLVED"

def test_v1_analytics_endpoints():
    # Overview
    resp_overview = client.get("/api/v1/analytics/overview?days=30")
    assert resp_overview.status_code == 200
    assert "kpis" in resp_overview.json()

    # Feature importance
    resp_feat = client.get("/api/v1/analytics/feature-importance?top_n=10")
    assert resp_feat.status_code == 200
    data_feat = resp_feat.json()
    assert "Model Feature Importance" in data_feat["title"]
    assert len(data_feat["features"]) > 0

def test_v1_simulation_controls():
    # Status
    resp_stat = client.get("/api/v1/simulation/status")
    assert resp_stat.status_code == 200
    assert "running" in resp_stat.json()

    # Start with scenario
    resp_start = client.post("/api/v1/simulation/start", json={"scenario": "AT_RISK", "interval_seconds": 3.0})
    assert resp_start.status_code == 200
    assert resp_start.json()["status"] == "started"

    # Stop
    resp_stop = client.post("/api/v1/simulation/stop")
    assert resp_stop.status_code == 200
    assert resp_stop.json()["status"] == "stopped"
