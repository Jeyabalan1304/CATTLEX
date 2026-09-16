import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["system"] == "CATTLEX"

def test_dashboard_summary():
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert "kpis" in data
    assert "average_vitals" in data

def test_cattle_endpoints():
    # List cattle
    response = client.get("/api/cattle")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # Get single cattle profile (COW001 has id 1 from seeding)
    resp_single = client.get("/api/cattle/1")
    assert resp_single.status_code == 200
    assert resp_single.json()["tag_id"] == "COW001"

def test_disease_catalog():
    resp_sym = client.get("/api/diseases/symptoms")
    assert resp_sym.status_code == 200
    assert resp_sym.json()["count"] == 93

    resp_dis = client.get("/api/diseases/classes")
    assert resp_dis.status_code == 200
    assert resp_dis.json()["count"] == 26

def test_disease_prediction_endpoint():
    payload = {
        "cattle_id": 1,
        "symptoms": {
            "fever": True,
            "coughing": True,
            "diffculty_breath": True,
            "nasel_discharges": True
        },
        "model_name": "Random Forest"
    }
    response = client.post("/api/predictions/disease", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_disease" in data
    assert "confidence" in data
    assert "top_predictions" in data

def test_models_performance_endpoint():
    response = client.get("/api/models/performance")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) >= 6

def test_alerts_endpoint():
    response = client.get("/api/alerts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_veterinary_appointments():
    response = client.get("/api/veterinarians/appointments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
