# CATTLEX REST API Specification

The CATTLEX backend exposes a fully documented RESTful API conforming to OpenAPI 3.1. Interactive Swagger UI documentation is accessible at `/docs`, and ReDoc is at `/redoc`.

## 1. Core Endpoints

### Authentication (`/api/auth`)
- `POST /api/auth/register`: Register new user (`FARMER`, `VETERINARIAN`, `ADMIN`).
- `POST /api/auth/login`: Authenticate with email/password and receive JWT access token.

### Cattle Fleet Management (`/api/cattle`)
- `GET /api/cattle`: Retrieve all registered cattle with latest vitals, risk scores, and alert counts.
- `POST /api/cattle`: Register a new cattle entity.
- `GET /api/cattle/{id}`: Detailed cattle profile, latest vitals, and prediction summaries.
- `PUT /api/cattle/{id}`: Update cattle metadata.
- `DELETE /api/cattle/{id}`: Unregister cattle record.

### Sensor Telemetry (`/api/sensors`)
- `POST /api/sensors/readings`: Ingest real-time collar telemetry packet. Triggers risk analysis and alert workflows.
- `GET /api/sensors/{cattle_id}`: Retrieve historical telemetry time series.
- `GET /api/sensors/{cattle_id}/latest`: Get current vital readings for cattle.

### Predictive Analytics (`/api/predictions`)
- `POST /api/predictions/disease`: Submit observed symptoms and receive multi-disease inference with top 3 differentials and XAI feature signals.
- `POST /api/predictions/health`: Compute vital health risk and health status classification.
- `GET /api/predictions/{cattle_id}`: Retrieve historical prediction records.

### Alerts & Triage (`/api/alerts`)
- `GET /api/alerts`: List active/resolved health alerts with severity filter.
- `POST /api/alerts/{id}/resolve`: Acknowledge and resolve an alert.

### Veterinary Workflow (`/api/veterinarians`)
- `GET /api/veterinarians`: List accredited veterinarians.
- `GET /api/veterinarians/appointments`: List clinical appointments and priorities.
- `POST /api/veterinarians/appointments`: Schedule consultation.
- `PUT /api/veterinarians/appointments/{id}`: Update appointment triage status.

### Dashboard & Trends (`/api/dashboard`)
- `GET /api/dashboard/summary`: Herd-level KPIs (Total, Healthy, At Risk, Critical, Alerts) and average vitals.
- `GET /api/dashboard/trends`: Aggregate telemetry trend time series.

### Model Benchmarks & Registry (`/api/models`)
- `GET /api/models`: Model registry status and active algorithm versions.
- `GET /api/models/performance`: Complete 6-model benchmark metrics, confusion matrices, and feature importances.

### IoT Simulator (`/api/simulator`)
- `GET /api/simulator/status`: Current simulator running state and cattle states.
- `POST /api/simulator/start`: Start background telemetry generation.
- `POST /api/simulator/stop`: Stop telemetry generation.
- `POST /api/simulator/trigger-abnormal`: Trigger sickness onset in a specific cattle.
- `POST /api/simulator/reset`: Reset cattle vitals to normal baseline.
