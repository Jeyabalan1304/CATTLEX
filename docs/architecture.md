# CATTLEX System Architecture

## 1. Overview
CATTLEX ("An AI-Integrated, Solar-Powered IoT System Enhanced with Predictive Analytics for Multi-Disease Management in Livestock") is an autonomous, end-to-end cattle health and disease intelligence platform. It bridges edge-computing solar collars, real-time MQTT message brokers, a reactive FastAPI analytical backend, and a modern React dashboard.

---

## 2. End-to-End Architecture Diagram

```mermaid
graph TD
    subgraph "Pasture Edge IoT"
        Solar["Solar Panel (5V 2W) + LiFePO4 Battery"]
        Collar["Smart Cattle Collar (ESP32)"]
        S_MLX["MLX90614 (Body Temp)"] --> Collar
        S_MAX["MAX30102 (Heart Rate & SpO2)"] --> Collar
        S_MPU["MPU6050 (Activity & Rumination)"] --> Collar
        Solar --> Collar
        
        Station["Feed & Water Pasture Station"]
        S_RFID["RC522 RFID Tag Reader"] --> Station
        S_HX["Load Cell + HX711 (Feed Intake)"] --> Station
        S_YF["YF-S201 (Water Flow Meter)"] --> Station
    end

    subgraph "Connectivity Layer"
        Collar -->|Wi-Fi / LoRaWAN| MQTT["Mosquitto MQTT Broker (1883)"]
        Station -->|Wi-Fi / LoRaWAN| MQTT
    end

    subgraph "CATTLEX Backend Engine (FastAPI)"
        MQTT --> Ingestion["MQTT Ingestion & Telemetry Validator"]
        Ingestion --> DB[(PostgreSQL / SQLite)]
        Ingestion --> RiskEngine["Vital Signs Health Risk Engine"]
        RiskEngine --> Workflow["CATTLEX Automated Health Workflow (RPA)"]
        Workflow --> Alerts["Alert Dispatcher"]
        Workflow --> Triage["Veterinary Triage Engine"]
        
        ML["Multi-Disease ML Inference Engine\n(Random Forest, GNB, DT, LR, k-NN, SVM)"]
        XAI["Explainable AI (Feature Importance)"]
        ML --- XAI
        
        REST["FastAPI REST Endpoints (/api/v1)"]
        WS["WebSocket Broadcaster (/ws)"]
    end

    subgraph "Client Applications"
        REST <--> ReactUI["Modern React Dashboard"]
        WS --> ReactUI
        ReactUI --> Farmer["Farmer Portal (Monitoring & Predictions)"]
        ReactUI --> Vet["Veterinarian Portal (Triage & Appointments)"]
    end
```

---

## 3. Subsystem Breakdown

1. **Smart Solar Collar**:
   - Gathers high-frequency physiological parameters (temperature, pulse, movement).
   - Operates on energy-harvested solar power with deep sleep power management.
2. **Telemetry Ingestion & Message Broker**:
   - MQTT topic hierarchy isolates telemetry streams (`cattlex/cattle/{tag_id}/telemetry`).
   - Validates JSON payload structures and handles network reconnectivity.
3. **Reactive Predictive Analytics**:
   - Continuous Vital Signs Risk Engine computes health status (`HEALTHY`, `AT_RISK`, `CRITICAL`) and risk score (0-100).
   - Event-driven RPA workflow transitions cattle states, triggers triage alerts, and schedules veterinary visits.
   - On-demand Multiclass Disease Classifier predicts top differentials across 26 cattle diseases from observed symptoms.
4. **Operations Dashboard**:
   - Live gauge meters, herd health KPI distribution, historical time-series analytics, interactive disease diagnosis simulator.
