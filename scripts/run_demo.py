"""
CATTLEX - End-to-End Academic Demonstration Script
Simulates the complete research lifecycle:
1. Verifies Database & ML Model Registry
2. Ingests Baseline Telemetry for COW001 (Healthy)
3. Simulates Correlated Sickness Onset: Temperature rising, activity declining, heart rate accelerating
4. Executes Real-Time Risk Engine: Transitions COW001 from HEALTHY -> AT_RISK -> CRITICAL
5. Dispatches Automated Triage Alert
6. Triggers Veterinary Appointment RPA Recommendation
7. Performs Multiclass Disease Prediction from Symptoms with Explainable AI feature signals
"""

import os
import sys
import time
import json
import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
BACKEND_DIR = os.path.join(PROJECT_ROOT, 'backend')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.db.database import SessionLocal
from app.db.models import Cattle, Alert, VeterinaryAppointment, HealthPrediction, DiseasePrediction
from app.iot.mqtt_client import mqtt_manager
from app.ml.predict import predict_disease
from app.ml.explain import explain_prediction

def run_demonstration():
    print("=" * 75)
    print(" CATTLEX: REAL-TIME IoT & AI MULTI-DISEASE PREDICTION DEMO SCENARIO")
    print("=" * 75)

    db = SessionLocal()
    try:
        # Step 1: Lookup COW001
        cow1 = db.query(Cattle).filter(Cattle.tag_id == "COW001").first()
        if not cow1:
            print("COW001 not found. Please run seed_database.py first.")
            return

        print(f"\n[1] Initial State for Cattle: {cow1.tag_id} ({cow1.name})")
        print(f"    Breed: {cow1.breed} | Age: {cow1.age} mo | Status: {cow1.status}")

        # Step 2: Normal Baseline Ingestion
        print("\n[2] Ingesting IoT Telemetry (Normal Physiological State)...")
        normal_packet = {
            "cattle_id": cow1.id,
            "tag_id": cow1.tag_id,
            "temperature": 38.6,
            "heart_rate": 65.0,
            "respiratory_rate": 26.0,
            "activity_level": 0.86,
            "feed_intake": 19.5,
            "water_intake": 66.0,
            "ambient_temperature": 24.0,
            "humidity": 60.0
        }
        res_normal = mqtt_manager.process_telemetry(normal_packet)
        print(f"    -> Vitals Processed: Temp={normal_packet['temperature']}°C, HR={normal_packet['heart_rate']} bpm, Activity={normal_packet['activity_level']}")
        print(f"    -> Health Risk Engine Output: {res_normal['health']['status']} (Risk Score: {res_normal['health']['risk_score']}/100)")
        print(f"    -> Reason: {res_normal['health']['reason']}")

        time.sleep(1.0)

        # Step 3: Progressive Correlated Sickness Progression (AT_RISK)
        print("\n[3] Sickness Event Detected: Correlated Multivariable Shift (Elevated Temp + Dropping Feed Intake)...")
        at_risk_packet = {
            "cattle_id": cow1.id,
            "tag_id": cow1.tag_id,
            "temperature": 39.7,
            "heart_rate": 90.0,
            "respiratory_rate": 40.0,
            "activity_level": 0.45,
            "feed_intake": 10.5,
            "water_intake": 34.0,
            "ambient_temperature": 24.5,
            "humidity": 62.0
        }
        res_risk = mqtt_manager.process_telemetry(at_risk_packet)
        print(f"    -> Vitals Processed: Temp={at_risk_packet['temperature']}°C, HR={at_risk_packet['heart_rate']} bpm, Activity={at_risk_packet['activity_level']}")
        print(f"    -> Health Status: {res_risk['health']['status']} (Risk Score: {res_risk['health']['risk_score']}/100)")
        print(f"    -> Automated Actions: {res_risk['workflow']['actions_taken']}")

        time.sleep(1.0)

        # Step 4: Acute Critical Deterioration (CRITICAL)
        print("\n[4] Acute Deterioration Event: Pyrexia Spike (40.9°C) + Severe Lethargy (0.16)...")
        critical_packet = {
            "cattle_id": cow1.id,
            "tag_id": cow1.tag_id,
            "temperature": 40.9,
            "heart_rate": 112.0,
            "respiratory_rate": 56.0,
            "activity_level": 0.16,
            "feed_intake": 4.2,
            "water_intake": 15.0,
            "ambient_temperature": 25.0,
            "humidity": 63.0
        }
        res_critical = mqtt_manager.process_telemetry(critical_packet)
        print(f"    -> Vitals Processed: Temp={critical_packet['temperature']}°C, HR={critical_packet['heart_rate']} bpm, Activity={critical_packet['activity_level']}")
        print(f"    -> Health Status: {res_critical['health']['status']} (Risk Score: {res_critical['health']['risk_score']}/100)")
        print(f"    -> Automated Actions Triggered: {res_critical['workflow']['actions_taken']}")

        # Step 5: Symptom-based Multi-Disease Inference
        print("\n[5] Farmer Inputs Observed Clinical Symptoms to Decision-Support Engine:")
        symptoms_input = {
            "fever": True,
            "loss_of_appetite": True,
            "udder_swelling": True,
            "udder_heat": True,
            "udder_pain": True,
            "milk_flakes": True,
            "milk_clots": True,
            "reduction_milk_vields": True
        }
        print(f"    Active Symptoms: {[k.replace('_', ' ').title() for k, v in symptoms_input.items() if v]}")

        disease_pred = predict_disease(symptoms_input, model_name="Random Forest")
        print("\n[6] CATTLEX ML Disease Inference Results:")
        print(f"    Predicted Disease:  {disease_pred['display_name']}")
        print(f"    Model Confidence:   {disease_pred['confidence']*100:.2f}%")
        print(f"    Primary Algorithm:  {disease_pred['model_name']}")
        print(f"    Top 3 Differential Diagnoses:")
        for idx, p in enumerate(disease_pred['top_predictions'], 1):
            print(f"      {idx}. {p['display_name']} ({p['probability']*100:.2f}%)")

        print("\n[7] Explainable AI (XAI) - Top Contributing Feature Signals:")
        for feat in disease_pred['important_features'][:5]:
            print(f"    - {feat['display_name']:28} | Relative Importance: {feat['importance']:.4f}")

        print("\n[8] Automated Veterinary Clinical Recommendation:")
        print(f"    \"{disease_pred['recommendation']}\"")
        print("    Disclaimer: Non-definitive decision-support tool. Certified veterinary consultation advised.")

        print("\n" + "=" * 75)
        print(" DEMONSTRATION COMPLETE: CATTLEX End-to-End Pipeline Verified Successfully!")
        print("=" * 75)

    finally:
        db.close()

if __name__ == '__main__':
    run_demonstration()
