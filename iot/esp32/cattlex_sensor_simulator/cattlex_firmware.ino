/*
 * CATTLEX Smart Solar Collar - ESP32 Conceptual IoT Firmware
 * Research Architecture:
 * - MCU: ESP-WROOM-32 (Ultra Low Power Deep Sleep support + Solar Charging)
 * - MLX90614 (I2C): Infrared Non-contact Body Temperature
 * - MAX30102 (I2C): Photoplethysmogram Heart Rate & SpO2
 * - MPU6050 (I2C): 3-Axis Accelerometer/Gyroscope for Rumination & Head Movement
 * - RC522 RFID + Load Cell (HX711): Pasture/Trough Feed Intake Station
 * - YF-S201: Hall-effect Water Flow Meter
 * - Connectivity: Dual-path LoRaWAN (SX1276) / 2.4GHz Wi-Fi with MQTT telemetry
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Wire.h>

// Required Hardware Sensor Libraries (Refer to docs/iot.md for wiring):
// #include <Adafruit_MLX90614.h>
// #include "MAX30105.h"
// #include "heartRate.h"
// #include <Adafruit_MPU6050.h>

// Wi-Fi & MQTT Configurations
const char* WIFI_SSID = "CATTLEX_RANCH_WIFI";
const char* WIFI_PASS = "PastureIoT2026";
const char* MQTT_BROKER = "192.168.1.100"; // Replace with your CATTLEX MQTT broker IP
const int MQTT_PORT = 1883;
const char* CATTLE_TAG_ID = "COW001";
const int CATTLE_DB_ID = 1;

WiFiClient espClient;
PubSubClient mqttClient(espClient);

// Timing configurations
unsigned long lastTelemetryMillis = 0;
const unsigned long TELEMETRY_INTERVAL_MS = 5000; // 5-second sampling cycle

void setupWiFi() {
  Serial.print("Connecting to Wi-Fi: ");
  Serial.println(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi Connected. IP: " + WiFi.localIP().toString());
}

void reconnectMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("Attempting MQTT broker connection...");
    String clientId = "CATTLEX_Collar_" + String(CATTLE_TAG_ID);
    if (mqttClient.connect(clientId.c_str())) {
      Serial.println("Connected to CATTLEX Broker.");
      // Subscribe to remote collar configuration commands
      String commandTopic = "cattlex/cattle/" + String(CATTLE_TAG_ID) + "/commands";
      mqttClient.subscribe(commandTopic.c_str());
    } else {
      Serial.print("Failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println("; retrying in 3 seconds...");
      delay(3000);
    }
  }
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Collar command received [");
  Serial.print(topic);
  Serial.print("]: ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22); // I2C SDA=GPIO21, SCL=GPIO22

  Serial.println("==================================================");
  Serial.println(" CATTLEX Smart Solar Collar Firmware Initializing ");
  Serial.println(" Tag ID: " + String(CATTLE_TAG_ID));
  Serial.println("==================================================");

  // Initialize sensors here:
  // mlx.begin();
  // particleSensor.begin(Wire, I2C_SPEED_FAST);
  // mpu.begin();

  setupWiFi();
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setCallback(mqttCallback);
}

void loop() {
  if (!mqttClient.connected()) {
    reconnectMQTT();
  }
  mqttClient.loop();

  unsigned long currentMillis = millis();
  if (currentMillis - lastTelemetryMillis >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryMillis = currentMillis;

    // Read physical hardware sensors:
    // float bodyTemp = mlx.readObjectTempC();
    // float heartRate = getHeartRateBpm();
    // float activity = computeMotionMagnitude();

    // Baseline mock values for demonstration testing without bench hardware:
    float bodyTemp = 38.6;
    float heartRate = 65.0;
    float respirationRate = 26.0;
    float activityLevel = 0.85;
    float feedIntake = 19.2;
    float waterIntake = 64.0;
    float ambientTemp = 24.5;
    float humidity = 60.0;

    // Serialize JSON Telemetry Packet
    StaticJsonDocument<512> doc;
    doc["cattle_id"] = CATTLE_DB_ID;
    doc["tag_id"] = CATTLE_TAG_ID;
    doc["temperature"] = round(bodyTemp * 100.0) / 100.0;
    doc["heart_rate"] = round(heartRate * 10.0) / 10.0;
    doc["respiratory_rate"] = round(respirationRate * 10.0) / 10.0;
    doc["activity_level"] = round(activityLevel * 100.0) / 100.0;
    doc["feed_intake"] = feedIntake;
    doc["water_intake"] = waterIntake;
    doc["ambient_temperature"] = ambientTemp;
    doc["humidity"] = humidity;
    doc["battery_v"] = 4.12; // Solar lithium cell voltage
    doc["solar_charging"] = true;

    char buffer[512];
    size_t n = serializeJson(doc, buffer);

    String topic = "cattlex/cattle/" + String(CATTLE_TAG_ID) + "/telemetry";
    boolean published = mqttClient.publish(topic.c_str(), buffer, n);

    if (published) {
      Serial.print("Telemetry published -> ");
      Serial.println(buffer);
    } else {
      Serial.println("Telemetry publish failed.");
    }
  }
}
