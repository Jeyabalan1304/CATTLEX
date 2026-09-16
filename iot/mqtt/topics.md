# CATTLEX MQTT Architecture & Topic Directory

## 1. Topic Hierarchy
The CATTLEX system employs an organized topic schema following the format:
`cattlex/cattle/{tag_id}/{channel}`

### Core Topics:

| Topic Pattern | Direction | Description | QoS |
| :--- | :--- | :--- | :--- |
| `cattlex/cattle/{tag_id}/telemetry` | Collar -> Broker -> Backend | Real-time vital signs and environmental readings | 1 |
| `cattlex/cattle/{tag_id}/health` | Backend -> Broker -> Subscribers | Computed health status (`HEALTHY`, `AT_RISK`, `CRITICAL`) and risk score (0-100) | 1 |
| `cattlex/cattle/{tag_id}/alerts` | Backend -> Broker -> Dashboard | High-priority safety and physiological threshold violations | 2 |
| `cattlex/cattle/{tag_id}/commands` | Dashboard -> Broker -> Collar | Collar remote configuration (sampling rate, sleep interval) | 1 |

---

## 2. Topic Data Payloads

### Telemetry Packet (`cattlex/cattle/COW001/telemetry`)
```json
{
  "cattle_id": 1,
  "tag_id": "COW001",
  "temperature": 38.65,
  "heart_rate": 66.0,
  "respiratory_rate": 26.0,
  "activity_level": 0.84,
  "feed_intake": 19.5,
  "water_intake": 65.0,
  "ambient_temperature": 24.5,
  "humidity": 61.2,
  "battery_v": 4.15,
  "timestamp": "2026-09-16T08:30:00Z"
}
```

### Health Risk Update (`cattlex/cattle/COW001/health`)
```json
{
  "status": "HEALTHY",
  "risk_score": 12.5,
  "reason": "All physiological vitals within normal bovine reference ranges."
}
```

### Alert Broadcast (`cattlex/cattle/COW001/alerts`)
```json
{
  "type": "TEMPERATURE",
  "severity": "CRITICAL",
  "message": "Critical pyrexia detected in COW001: Body temperature is 40.8°C. Immediate veterinary evaluation recommended."
}
```
