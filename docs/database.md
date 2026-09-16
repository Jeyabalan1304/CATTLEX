# CATTLEX Database Architecture

## 1. Overview
CATTLEX uses SQLAlchemy ORM with support for both PostgreSQL (production and containerized deployments) and SQLite (instant zero-configuration local runs).

---

## 2. Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    USERS ||--o{ VETERINARY_APPOINTMENTS : handles
    CATTLE ||--o{ SENSOR_READINGS : emits
    CATTLE ||--o{ HEALTH_PREDICTIONS : receives
    CATTLE ||--o{ DISEASE_PREDICTIONS : diagnosed_with
    CATTLE ||--o{ ALERTS : triggers
    CATTLE ||--o{ VETERINARY_APPOINTMENTS : assigned_to

    USERS {
        int id PK
        string name
        string email UK
        string password_hash
        string role
        datetime created_at
    }

    CATTLE {
        int id PK
        string tag_id UK
        string name
        string breed
        int age
        string sex
        float weight
        string farm_id
        string status
        datetime created_at
        datetime updated_at
    }

    SENSOR_READINGS {
        int id PK
        int cattle_id FK
        datetime timestamp
        float temperature
        float heart_rate
        float respiratory_rate
        float activity_level
        float feed_intake
        float water_intake
        float ambient_temperature
        float humidity
    }

    HEALTH_PREDICTIONS {
        int id PK
        int cattle_id FK
        datetime timestamp
        string health_status
        float risk_score
        string model_name
        float confidence
        text prediction_reason
    }

    DISEASE_PREDICTIONS {
        int id PK
        int cattle_id FK
        datetime timestamp
        string predicted_disease
        float confidence
        string model_name
        text input_symptoms
        text top_predictions
        text important_features
        text recommendation
    }

    ALERTS {
        int id PK
        int cattle_id FK
        string type
        string severity
        text message
        string status
        datetime created_at
        datetime resolved_at
    }

    VETERINARY_APPOINTMENTS {
        int id PK
        int cattle_id FK
        int veterinarian_id FK
        string veterinarian_name
        text reason
        string priority
        datetime scheduled_at
        string status
        text notes
    }
```
