import time
import random
import threading
from typing import Dict, Any, List, Optional
from app.core.logging import logger

class CattleSensorSimulator:
    """
    Simulates realistic IoT multi-sensor telemetry for cattle.
    Implements correlated temporal physiological state transitions:
    - MLX90614: Infrared body temperature (°C)
    - MAX30102: Photoplethysmogram heart rate (bpm)
    - Respiration: Breaths/min
    - MPU6050: 3-Axis movement/activity index (0.0 to 1.0)
    - Load Cell + RFID: Daily feed intake (kg)
    - YF-S201: Water flow / intake (L)
    - DHT22: Ambient temp & relative humidity
    """

    def __init__(self):
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self._interval_seconds = 4.0
        self._callback = None

        # Cattle internal physiological state models
        # state: 'HEALTHY' | 'DEVELOPING_FEVER' | 'AT_RISK' | 'CRITICAL'
        self.cattle_states: Dict[str, Dict[str, Any]] = {
            "COW001": {
                "id": 1,
                "tag_id": "COW001",
                "state": "HEALTHY",
                "base_temp": 38.6,
                "temp": 38.6,
                "heart_rate": 64.0,
                "respiratory_rate": 26.0,
                "activity_level": 0.84,
                "feed_intake": 19.5,
                "water_intake": 65.0,
                "step_count": 0
            },
            "COW002": {
                "id": 2,
                "tag_id": "COW002",
                "state": "AT_RISK",
                "base_temp": 39.5,
                "temp": 39.5,
                "heart_rate": 88.0,
                "respiratory_rate": 38.0,
                "activity_level": 0.48,
                "feed_intake": 11.2,
                "water_intake": 36.0,
                "step_count": 0
            },
            "COW003": {
                "id": 3,
                "tag_id": "COW003",
                "state": "HEALTHY",
                "base_temp": 38.5,
                "temp": 38.5,
                "heart_rate": 62.0,
                "respiratory_rate": 25.0,
                "activity_level": 0.88,
                "feed_intake": 21.0,
                "water_intake": 70.0,
                "step_count": 0
            },
            "COW004": {
                "id": 4,
                "tag_id": "COW004",
                "state": "CRITICAL",
                "base_temp": 40.8,
                "temp": 40.8,
                "heart_rate": 108.0,
                "respiratory_rate": 54.0,
                "activity_level": 0.18,
                "feed_intake": 4.5,
                "water_intake": 16.0,
                "step_count": 0
            },
            "COW005": {
                "id": 5,
                "tag_id": "COW005",
                "state": "AT_RISK",
                "base_temp": 39.4,
                "temp": 39.4,
                "heart_rate": 84.0,
                "respiratory_rate": 36.0,
                "activity_level": 0.52,
                "feed_intake": 12.8,
                "water_intake": 39.0,
                "step_count": 0
            }
        }

    def set_callback(self, callback):
        self._callback = callback

    def trigger_abnormal_event(self, tag_id: str = "COW001"):
        """
        Triggers gradual onset of sickness / acute mastitis / respiratory distress
        in the specified cattle. Sensors will transition dynamically over time rather than instant jump.
        """
        if tag_id in self.cattle_states:
            self.cattle_states[tag_id]["state"] = "DEVELOPING_FEVER"
            self.cattle_states[tag_id]["step_count"] = 0
            logger.info(f"Simulator: Triggered correlated sickness onset for {tag_id}.")
            return True
        return False

    def reset_cattle(self, tag_id: Optional[str] = None):
        """
        Resets cattle back to baseline physiological ranges.
        """
        tags = [tag_id] if tag_id and tag_id in self.cattle_states else list(self.cattle_states.keys())
        for tag in tags:
            self.cattle_states[tag]["state"] = "HEALTHY"
            self.cattle_states[tag]["temp"] = 38.5 + random.uniform(-0.2, 0.2)
            self.cattle_states[tag]["heart_rate"] = 62.0 + random.uniform(-4, 4)
            self.cattle_states[tag]["respiratory_rate"] = 26.0 + random.uniform(-2, 2)
            self.cattle_states[tag]["activity_level"] = 0.82 + random.uniform(-0.05, 0.05)
            self.cattle_states[tag]["feed_intake"] = 19.0 + random.uniform(-1, 1)
            self.cattle_states[tag]["water_intake"] = 65.0 + random.uniform(-3, 3)
            self.cattle_states[tag]["step_count"] = 0
        logger.info(f"Simulator: Reset cattle vitals for {tags}")

    def generate_next_reading(self, tag_id: str) -> Dict[str, Any]:
        """
        Advances the cattle's state machine and produces correlated physiological sensor readings.
        """
        c = self.cattle_states[tag_id]
        state = c["state"]
        c["step_count"] += 1

        if state == "HEALTHY":
            # Normal physiological noise
            c["temp"] = round(38.5 + random.uniform(-0.15, 0.2), 2)
            c["heart_rate"] = round(64.0 + random.uniform(-3.0, 3.0), 1)
            c["respiratory_rate"] = round(26.0 + random.uniform(-1.5, 1.5), 1)
            c["activity_level"] = round(min(max(c["activity_level"] + random.uniform(-0.03, 0.03), 0.70), 0.95), 2)
            c["feed_intake"] = round(19.0 + random.uniform(-0.8, 0.8), 1)
            c["water_intake"] = round(65.0 + random.uniform(-2.0, 2.0), 1)

        elif state == "DEVELOPING_FEVER":
            # Correlated temporal progression: gradual fever, tachycardia, tachypnea, reduced appetite & lethargy
            c["temp"] = round(min(c["temp"] + random.uniform(0.18, 0.35), 41.2), 2)
            c["heart_rate"] = round(min(c["heart_rate"] + random.uniform(2.5, 4.5), 112.0), 1)
            c["respiratory_rate"] = round(min(c["respiratory_rate"] + random.uniform(1.8, 3.2), 56.0), 1)
            c["activity_level"] = round(max(c["activity_level"] - random.uniform(0.05, 0.09), 0.15), 2)
            c["feed_intake"] = round(max(c["feed_intake"] - random.uniform(1.2, 2.0), 3.8), 1)
            c["water_intake"] = round(max(c["water_intake"] - random.uniform(3.0, 5.5), 14.0), 1)

            if c["temp"] >= 40.4:
                c["state"] = "CRITICAL"
            elif c["temp"] >= 39.4:
                c["state"] = "AT_RISK"

        elif state == "AT_RISK":
            c["temp"] = round(39.6 + random.uniform(-0.15, 0.25), 2)
            c["heart_rate"] = round(88.0 + random.uniform(-3.0, 3.0), 1)
            c["respiratory_rate"] = round(38.0 + random.uniform(-2.0, 2.0), 1)
            c["activity_level"] = round(max(min(c["activity_level"] + random.uniform(-0.02, 0.02), 0.55), 0.40), 2)
            c["feed_intake"] = round(11.0 + random.uniform(-0.5, 0.5), 1)
            c["water_intake"] = round(35.0 + random.uniform(-1.5, 1.5), 1)

        elif state == "CRITICAL":
            c["temp"] = round(40.8 + random.uniform(-0.2, 0.2), 2)
            c["heart_rate"] = round(108.0 + random.uniform(-3.0, 4.0), 1)
            c["respiratory_rate"] = round(52.0 + random.uniform(-2.5, 2.5), 1)
            c["activity_level"] = round(max(0.18 + random.uniform(-0.03, 0.03), 0.08), 2)
            c["feed_intake"] = round(4.5 + random.uniform(-0.4, 0.4), 1)
            c["water_intake"] = round(16.0 + random.uniform(-1.0, 1.0), 1)

        # Ambient sensor data (solar-powered pasture node)
        amb_temp = round(25.0 + random.uniform(-1.0, 1.5), 1)
        humidity = round(62.0 + random.uniform(-2.0, 3.0), 1)

        return {
            "cattle_id": c["id"],
            "tag_id": c["tag_id"],
            "temperature": c["temp"],
            "heart_rate": c["heart_rate"],
            "respiratory_rate": c["respiratory_rate"],
            "activity_level": c["activity_level"],
            "feed_intake": c["feed_intake"],
            "water_intake": c["water_intake"],
            "ambient_temperature": amb_temp,
            "humidity": humidity,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

    def start(self):
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logger.info("CATTLEX Sensor Simulator started.")

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        logger.info("CATTLEX Sensor Simulator stopped.")

    def _run_loop(self):
        while self.running:
            for tag_id in self.cattle_states.keys():
                reading = self.generate_next_reading(tag_id)
                if self._callback:
                    try:
                        self._callback(reading)
                    except Exception as e:
                        logger.error(f"Simulator callback exception: {e}")
            time.sleep(self._interval_seconds)

# Singleton simulator instance
simulator = CattleSensorSimulator()
