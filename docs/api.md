# CATTLEX API Specification (v1 & Legacy Endpoints)

Interactive OpenAPI / Swagger UI is available at `/docs`, and ReDoc documentation is at `/redoc`.

Base URL Prefix: `/api/v1` (with `/api` legacy aliases supported).

---

## 1. System Health & Readiness

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Service health status, database connectivity, ML model state, and simulator status. |
| `GET` | `/api/v1/health/readiness` | Readiness check verifying all 93 features and 26 classes are loaded. |

---

## 2. Machine Learning Model Management & Explainability

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/ml/model-info` | Production Random Forest specifications, independent test accuracy (98.85%), Macro-F1 (94.87%), and latency (0.669 ms). |
| `GET` | `/api/v1/analytics/feature-importance` | Top learned Gini feature importances labeled scientifically as model feature importance. |

---

## 3. Disease Prediction API

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/predictions/features` | Returns the list of 93 validated symptom features. |
| `POST` | `/api/v1/predictions/disease` | Submits observed symptoms dictionary and returns predicted disease, confidence, confidence band (`HIGH`, `MODERATE`, `LOW`), top 3 differentials with probabilities, and model version. |
| `GET` | `/api/v1/predictions/{cattle_id}` | Retrieves historical predictions for specific cattle. |

### Sample Request: `POST /api/v1/predictions/disease`
```json
{
  "cattle_id": "COW001",
  "symptoms": {
    "fever": 1,
    "depression": 1,
    "anorexia": 1,
    "udder_swelling": 1,
    "milk_flakes": 1
  }
}
```

### Sample Response:
```json
{
  "prediction_id": "8f031201-90a4-4444-8461-ca31d4e74880",
  "cattle_id": "COW001",
  "predicted_disease": "mastitis",
  "display_name": "Mastitis",
  "confidence": 0.942,
  "confidence_band": "HIGH",
  "top_3": [
    {"disease": "mastitis", "display_name": "Mastitis", "probability": 0.942},
    {"disease": "foot_rot", "display_name": "Foot Rot", "probability": 0.024},
    {"disease": "blackleg", "display_name": "Blackleg", "probability": 0.011}
  ],
  "model_version": "CATTLEX-RF-v1",
  "disclaimer": "AI decision-support prediction — veterinary assessment required."
}
```

---

## 4. Cattle Management

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/cattle` | Retrieve all cattle with status, latest vitals, and alert counts. |
| `GET` | `/api/v1/cattle/{id}` | Detailed cattle profile by integer ID or tag string (`COW001`). |
| `POST` | `/api/v1/cattle` | Register new cattle entity. |
| `PUT` | `/api/v1/cattle/{id}` | Update cattle record. |
| `DELETE` | `/api/v1/cattle/{id}` | Remove cattle record. |

---

## 5. IoT Sensor Telemetry

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/sensors/readings` | Ingest sensor telemetry packet, runs physiological risk scoring, triggers alerts, and broadcasts to dashboard. |
| `GET` | `/api/v1/sensors/{cattle_id}` | Retrieve historical telemetry series. |
| `GET` | `/api/v1/sensors/{cattle_id}/latest`| Get current vital readings. |

---

## 6. Alerts & Triage

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/alerts` | List alerts (supports `status`, `severity`, `cattle_id` filtering). |
| `POST` | `/api/v1/alerts/{id}/acknowledge` | Mark alert as acknowledged. |
| `POST` | `/api/v1/alerts/{id}/resolve` | Resolve an active alert. |

---

## 7. IoT Simulation Engine

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/simulation/status` | Current simulator state, cattle count, and interval. |
| `POST` | `/api/v1/simulation/start` | Start simulator with scenario (`NORMAL`, `AT_RISK`, `CRITICAL`, `DISEASE_EVENT`). |
| `POST` | `/api/v1/simulation/stop` | Stop simulator. |
| `POST` | `/api/v1/simulation/trigger-abnormal` | Trigger gradual onset of acute illness for specific animal. |
| `POST` | `/api/v1/simulation/reset` | Reset all simulated cattle to normal physiological range. |

---

## 8. Real-Time WebSockets

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `WS` | `/api/v1/ws/dashboard` | Live telemetry stream, risk updates, prediction events, and alerts. |
| `WS` | `/ws` | Root WebSocket connection alias. |

---

## 9. Analytics & Reporting

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/analytics/overview` | Herd health KPIs and vitals averages with date filtering. |
| `GET` | `/api/v1/analytics/diseases` | Frequency distribution of detected diseases. |
| `GET` | `/api/v1/analytics/health` | Physiological risk level distribution (`HEALTHY`, `AT_RISK`, `CRITICAL`). |
| `GET` | `/api/v1/analytics/sensors` | Multi-vital historical time series trends. |
