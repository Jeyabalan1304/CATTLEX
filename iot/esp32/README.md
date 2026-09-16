# CATTLEX Smart Solar-Powered IoT Collar Firmware (ESP32)

## 1. Overview
The CATTLEX smart collar is an energy-autonomous, solar-harvesting IoT edge device designed for continuous physiological and behavioral tracking of grazing cattle.

## 2. Sensor Integration Matrix
| Sensor Component | Physiological / Environmental Metric | Physical Interface | Power Profile |
| :--- | :--- | :--- | :--- |
| **MLX90614** | Infrared Body Surface / Tympanic Temperature (°C) | I2C (0x5A) | 3.3V / 1.5 mA |
| **MAX30102** | Pulse Oximetry & Heart Rate (bpm) | I2C (0x57) | 1.8V / 3.3V (600 µA) |
| **MPU6050** | 3-Axis Head/Neck Movement & Rumination Index | I2C (0x68) | 3.3V / 3.8 mA |
| **RC522 + HX711** | RFID Cattle Tag ID + Feed Intake Scale (kg) | SPI / 2-wire | Station-based |
| **YF-S201** | Water Flow & Volume Ingestion (Liters) | GPIO Interrupt | Station-based |
| **DHT22 / BME280** | Pasture Ambient Temperature & Relative Humidity | 1-Wire / I2C | 3.3V / 1.0 mA |

## 3. Power Architecture
- **Energy Source**: Monocrystalline solar panel (5V, 2W) mounted on top of collar casing.
- **Storage**: 3.7V 2500mAh 18650 LiFePO4 / Li-ion rechargeable cell with TP4056 charge controller.
- **Power Management**: ESP32 Light Sleep between telemetry bursts reduces average current consumption to under 12 mA, enabling indefinite solar-powered operation in open pasture environments.

## 4. Software Setup & Flashing
1. Install [Arduino IDE](https://www.arduino.cc/en/software) or PlatformIO.
2. Add ESP32 board support: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`.
3. Install required libraries:
   - `PubSubClient` (Nick O'Leary)
   - `ArduinoJson` (Benoît Blanchon)
   - `Adafruit MLX90614 Library`
   - `SparkFun MAX3010x Pulse and Proximity Sensor Library`
4. Configure Wi-Fi SSID, password, and CATTLEX MQTT Broker IP in `cattlex_firmware.ino`.
5. Connect ESP32 via USB and upload at 115200 baud.
