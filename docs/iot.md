# CATTLEX IoT Hardware Architecture & Sensor Integration Guide

## 1. Hardware Architecture Overview
The CATTLEX system is designed to interface with solar-powered smart collars deployed on grazing livestock. The edge node integrates low-power sensing, signal filtering, power harvesting, and wireless telemetry transmission via Wi-Fi or LoRaWAN to an MQTT message broker.

---

## 2. Sensor Specifications & Physiological Mapping

### 1. MLX90614 (Infrared Non-Contact Temperature Sensor)
- **Target Parameter**: Core Body Surface / Ear Canal Temperature (°C).
- **Measurement Range**: -70°C to +382.2°C (Object), accurate to ±0.5°C in bovine physiological range (35°C - 43°C).
- **Interface**: I2C bus (default address 0x5A).
- **Sampling Frequency**: 0.2 Hz (every 5 seconds).
- **Calibration Considerations**: Skin emissivity offset (typically 0.98 for bovine epidermis) with hair-free acoustic placement inside the inner ear conch or ventral tail base.

### 2. MAX30102 (Pulse Oximetry & Photoplethysmography Sensor)
- **Target Parameter**: Heart Rate (bpm) and Peripheral Capillary Oxygen Saturation (SpO2).
- **Principle**: Dual-wavelength (Red 660 nm and IR 880 nm) optical absorption during pulsatile arterial blood flow.
- **Normal Bovine Range**: 48 to 84 bpm.
- **Interface**: I2C bus (address 0x57).
- **Motion Artifact Mitigation**: Digital band-pass filtering (0.5 Hz - 4.0 Hz) coupled with 3-axis accelerometer cross-referencing.

### 3. MPU6050 (6-Axis Inertial Measurement Unit)
- **Target Parameter**: Neck/Head Movement, Rumination Chewing Frequency, and Grazing Activity.
- **Sensors**: 3-axis MEMS accelerometer (±2g range) + 3-axis gyroscope (±250°/s range).
- **Derived Feature**: Vector Magnitude Area (VMA) computed on collar edge to determine whether cattle is active (0.70-0.95), resting, or recumbent/lethargic (<0.30).

### 4. RC522 RFID Reader + Load Cell (HX711)
- **Target Parameter**: Cattle Identity and Daily Feed Ingestion (kg/day).
- **Station Deployment**: Feed bunk automated gateway. When RFID ear tag is read within 10 cm, load cell differential calculates weight before and after feeding bout.

### 5. YF-S201 (Water Flow Hall-Effect Sensor)
- **Target Parameter**: Water Consumption (Liters/day).
- **Station Deployment**: Trough inlet pipe. Produces 450 pulses per liter of water flowing through the drinking bowl.

---

## 3. Power Supply Subsystem
- **Solar Harvesting**: 5V, 2W monocrystalline solar cell with ETFE encapsulation for weather resistance.
- **Battery Storage**: 3.7V 2500mAh LiFePO4 cell (chosen for safety over broad thermal operating ranges: -20°C to +60°C).
- **Power Budget**:
  - Active Transmission: ~120 mA for 150 ms.
  - Sensing Cycle: ~15 mA for 300 ms.
  - Deep Sleep: ~15 µA.
  - Average Hourly Energy Draw: < 8 mAh, guaranteeing perpetual autonomous operation under ambient solar irradiance.

---

## 4. Software Simulator vs Physical Hardware
For academic demonstrations and local development without bench electronics, CATTLEX provides the `CattleSensorSimulator` module (`app/iot/sensor_simulator.py`), which reproduces correlated multi-variable shifts over time without requiring physical hardware.
