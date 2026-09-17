import json
import threading
from typing import Dict, Any, Optional
import paho.mqtt.client as mqtt
from app.core.config import settings
from app.core.logging import logger
from app.db.database import SessionLocal
from app.db.models.cattle import Cattle
from app.db.models.sensor import SensorReading
from app.schemas.sensor import SensorReadingCreate
from app.ml.predict import predict_health_risk
from app.automation.alert_rules import evaluate_sensor_rules
from app.automation.veterinary_workflow import trigger_automated_health_workflow

class CATTLEXMqttClient:
    def __init__(self):
        self.client: Optional[mqtt.Client] = None
        self.connected = False
        self.ws_broadcast_callback = None

    def set_ws_broadcast(self, callback):
        self.ws_broadcast_callback = callback

    def start(self):
        try:
            # Paho MQTT v2 compatibility
            try:
                self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="cattlex-backend-node")
            except AttributeError:
                self.client = mqtt.Client(client_id="cattlex-backend-node")

            self.client.on_connect = self._on_connect
            self.client.on_message = self._on_message
            self.client.on_disconnect = self._on_disconnect

            # Connect in a background thread to prevent blocking FastAPI startup if broker is offline
            threading.Thread(target=self._connect_thread, daemon=True).start()
        except Exception as e:
            logger.warning(f"MQTT Client initialization failed: {e}. (Proceeding with simulated/HTTP telemetry ingestion)")

    def _connect_thread(self):
        try:
            logger.info(f"Attempting connection to MQTT Broker at {settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT}...")
            self.client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT, keepalive=60)
            self.client.loop_forever()
        except Exception as e:
            logger.info(f"MQTT Broker at {settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT} unreachable: {e}. Local HTTP and SensorSimulator ingestion remain fully functional.")

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.connected = True
            logger.info("Successfully connected to MQTT Broker.")
            telemetry_topic = f"{settings.MQTT_TOPIC_PREFIX}/+/telemetry"
            client.subscribe(telemetry_topic)
            logger.info(f"Subscribed to topic: {telemetry_topic}")
        else:
            logger.warning(f"MQTT connection returned code {rc}")

    def _on_disconnect(self, client, userdata, rc, properties=None):
        self.connected = False
        logger.warning("Disconnected from MQTT Broker.")

    def _on_message(self, client, userdata, msg):
        try:
            payload_str = msg.payload.decode("utf-8")
            data = json.loads(payload_str)
            self.process_telemetry(data)
        except Exception as e:
            logger.error(f"Error processing MQTT message on {msg.topic}: {e}")

    def publish_message(self, topic: str, payload: dict):
        if self.connected and self.client:
            try:
                self.client.publish(topic, json.dumps(payload), qos=1)
            except Exception as e:
                logger.error(f"Failed to publish MQTT message to {topic}: {e}")

    def process_telemetry(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Core ingestion pipeline: Validates telemetry, persists reading, runs health risk model,
        evaluates safety alerts, executes automated RPA workflow, and broadcasts to dashboard.
        """
        db = SessionLocal()
        try:
            cattle_id = data.get("cattle_id")
            tag_id = data.get("tag_id")

            # Lookup cattle
            cattle = None
            if cattle_id:
                cattle = db.query(Cattle).filter(Cattle.id == cattle_id).first()
            elif tag_id:
                cattle = db.query(Cattle).filter(Cattle.tag_id == tag_id).first()

            if not cattle:
                logger.warning(f"Telemetry received for unknown cattle: {data}")
                return {"status": "ignored", "reason": "Cattle not found"}

            # Create and store sensor reading
            act_val = data.get("activity_level") if data.get("activity_level") is not None else data.get("activity", 0.8)
            reading = SensorReading(
                cattle_id=cattle.id,
                temperature=float(data["temperature"]),
                heart_rate=float(data["heart_rate"]),
                respiratory_rate=float(data["respiratory_rate"]),
                activity_level=float(act_val),
                feed_intake=float(data["feed_intake"]),
                water_intake=float(data["water_intake"]),
                ambient_temperature=float(data.get("ambient_temperature") or 24.0),
                humidity=float(data.get("humidity") or 60.0),
                latitude=float(data["latitude"]) if data.get("latitude") is not None else 12.9716,
                longitude=float(data["longitude"]) if data.get("longitude") is not None else 77.5946
            )
            db.add(reading)
            db.commit()
            db.refresh(reading)

            # Compute Health Risk prediction
            risk_result = predict_health_risk({
                "temperature": reading.temperature,
                "heart_rate": reading.heart_rate,
                "respiratory_rate": reading.respiratory_rate,
                "activity_level": reading.activity_level,
                "feed_intake": reading.feed_intake,
                "water_intake": reading.water_intake
            })

            # Evaluate direct physiological rule violations
            rule_alerts = evaluate_sensor_rules(reading, cattle.tag_id)

            # Execute Automated Health Workflow (state transition, alerts, veterinary triage)
            workflow_result = trigger_automated_health_workflow(
                db=db,
                cattle=cattle,
                health_status=risk_result["health_status"],
                risk_score=risk_result["risk_score"],
                reason=risk_result["prediction_reason"],
                confidence=risk_result["confidence"]
            )

            # Construct broadcast payload
            broadcast_data = {
                "type": "TELEMETRY_UPDATE",
                "cattle_id": cattle.id,
                "tag_id": cattle.tag_id,
                "name": cattle.name,
                "reading": {
                    "temperature": reading.temperature,
                    "heart_rate": reading.heart_rate,
                    "respiratory_rate": reading.respiratory_rate,
                    "activity_level": reading.activity_level,
                    "feed_intake": reading.feed_intake,
                    "water_intake": reading.water_intake,
                    "ambient_temperature": reading.ambient_temperature,
                    "humidity": reading.humidity,
                    "timestamp": reading.timestamp.isoformat()
                },
                "health": {
                    "status": cattle.status,
                    "risk_score": risk_result["risk_score"],
                    "reason": risk_result["prediction_reason"]
                },
                "workflow": workflow_result
            }

            # Broadcast to live WebSockets
            if self.ws_broadcast_callback:
                self.ws_broadcast_callback(broadcast_data)

            # Publish to MQTT health status topic
            if self.connected:
                self.publish_message(f"cattlex/cattle/{cattle.tag_id}/health", broadcast_data["health"])

            return broadcast_data
        finally:
            db.close()

# Singleton MQTT Manager
mqtt_manager = CATTLEXMqttClient()
