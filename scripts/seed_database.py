import os
import sys
import datetime
import random

# Add backend directory to sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
BACKEND_DIR = os.path.join(PROJECT_ROOT, 'backend')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.db.database import SessionLocal, engine, Base
from app.db.models import User, Cattle, SensorReading, HealthPrediction, DiseasePrediction, Alert, VeterinaryAppointment
from app.core.security import get_password_hash
from app.ml.predict import predict_health_risk

def seed_db():
    print("=" * 60)
    print("CATTLEX: Seeding Database with Realistic Academic Demo Data")
    print("=" * 60)

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Users
        users = [
            ("Farmer John Doe", "farmer@cattlex.io", "farmer123", "FARMER"),
            ("Dr. Sarah Jenkins, DVM", "vet@cattlex.io", "vet123", "VETERINARIAN"),
            ("System Admin", "admin@cattlex.io", "admin123", "ADMIN")
        ]
        for name, email, pwd, role in users:
            existing = db.query(User).filter(User.email == email).first()
            if not existing:
                u = User(name=name, email=email, password_hash=get_password_hash(pwd), role=role)
                db.add(u)
        db.commit()
        print("-> Users seeded (farmer@cattlex.io, vet@cattlex.io, admin@cattlex.io)")

        # 2. Cattle Fleet (COW001 - COW005 with distinct physiological profiles)
        cattle_data = [
            ("COW001", "Bella", "Holstein Friesian", 36, "Female", 580.0, "FARM-01", "HEALTHY"),
            ("COW002", "Daisy", "Jersey", 28, "Female", 440.0, "FARM-01", "AT_RISK"),
            ("COW003", "Luna", "Brown Swiss", 42, "Female", 610.0, "FARM-01", "HEALTHY"),
            ("COW004", "Rosie", "Simmental", 30, "Female", 650.0, "FARM-01", "CRITICAL"),
            ("COW005", "Molly", "Angus", 24, "Female", 520.0, "FARM-01", "AT_RISK")
        ]

        cattle_objects = {}
        for tag_id, name, breed, age, sex, weight, farm_id, status in cattle_data:
            c = db.query(Cattle).filter(Cattle.tag_id == tag_id).first()
            if not c:
                c = Cattle(tag_id=tag_id, name=name, breed=breed, age=age, sex=sex, weight=weight, farm_id=farm_id, status=status)
                db.add(c)
                db.commit()
                db.refresh(c)
            cattle_objects[tag_id] = c
        print(f"-> Cattle seeded ({len(cattle_objects)} registered heads)")

        # 3. Historical Sensor Readings (Last 24 hours in 2-hour increments)
        now = datetime.datetime.utcnow()
        for tag_id, c in cattle_objects.items():
            # Check existing readings count
            existing_count = db.query(SensorReading).filter(SensorReading.cattle_id == c.id).count()
            if existing_count > 0:
                continue

            for step in range(12, -1, -1):
                timestamp = now - datetime.timedelta(hours=step * 2)
                
                if c.status == "HEALTHY":
                    temp = 38.5 + random.uniform(-0.15, 0.2)
                    hr = 64.0 + random.uniform(-4, 4)
                    rr = 26.0 + random.uniform(-2, 2)
                    act = 0.82 + random.uniform(-0.05, 0.05)
                    feed = 19.5 + random.uniform(-1, 1)
                    water = 65.0 + random.uniform(-3, 3)
                elif c.status == "AT_RISK":
                    # Elevated temp & heart rate
                    temp = 39.5 + random.uniform(-0.2, 0.3)
                    hr = 86.0 + random.uniform(-4, 5)
                    rr = 37.0 + random.uniform(-3, 3)
                    act = 0.48 + random.uniform(-0.04, 0.04)
                    feed = 11.5 + random.uniform(-0.8, 0.8)
                    water = 36.0 + random.uniform(-2, 2)
                else:  # CRITICAL
                    temp = 40.7 + random.uniform(-0.2, 0.3)
                    hr = 106.0 + random.uniform(-5, 6)
                    rr = 52.0 + random.uniform(-4, 4)
                    act = 0.18 + random.uniform(-0.03, 0.03)
                    feed = 4.8 + random.uniform(-0.5, 0.5)
                    water = 17.0 + random.uniform(-1.5, 1.5)

                reading = SensorReading(
                    cattle_id=c.id,
                    timestamp=timestamp,
                    temperature=round(temp, 2),
                    heart_rate=round(hr, 1),
                    respiratory_rate=round(rr, 1),
                    activity_level=round(act, 2),
                    feed_intake=round(feed, 1),
                    water_intake=round(water, 1),
                    ambient_temperature=24.5,
                    humidity=62.0
                )
                db.add(reading)

                # Add Health Prediction
                risk_res = predict_health_risk({
                    "temperature": temp,
                    "heart_rate": hr,
                    "respiratory_rate": rr,
                    "activity_level": act,
                    "feed_intake": feed,
                    "water_intake": water
                })
                pred = HealthPrediction(
                    cattle_id=c.id,
                    timestamp=timestamp,
                    health_status=risk_res["health_status"],
                    risk_score=risk_res["risk_score"],
                    model_name="VitalRiskEngine-v1",
                    confidence=risk_res["confidence"],
                    prediction_reason=risk_res["prediction_reason"]
                )
                db.add(pred)

        db.commit()
        print("-> Historical sensor telemetry and vital risk predictions seeded")

        # 4. Alerts
        cow4 = cattle_objects.get("COW004")
        if cow4:
            existing_alert = db.query(Alert).filter(Alert.cattle_id == cow4.id).first()
            if not existing_alert:
                alert1 = Alert(
                    cattle_id=cow4.id,
                    type="MULTI_VITAL",
                    severity="CRITICAL",
                    message="Critical pyrexia (40.8°C) and severe lethargy detected in COW004 (Rosie). High risk of acute bovine pneumonia or mastitis.",
                    status="ACTIVE",
                    created_at=now - datetime.timedelta(hours=2)
                )
                db.add(alert1)

        cow2 = cattle_objects.get("COW002")
        if cow2:
            existing_alert2 = db.query(Alert).filter(Alert.cattle_id == cow2.id).first()
            if not existing_alert2:
                alert2 = Alert(
                    cattle_id=cow2.id,
                    type="TEMPERATURE",
                    severity="WARNING",
                    message="Elevated body temperature (39.5°C) and reduced feed consumption in COW002 (Daisy).",
                    status="ACTIVE",
                    created_at=now - datetime.timedelta(hours=4)
                )
                db.add(alert2)

        # 5. Veterinary Appointments
        if cow4:
            existing_apt = db.query(VeterinaryAppointment).filter(VeterinaryAppointment.cattle_id == cow4.id).first()
            if not existing_apt:
                apt = VeterinaryAppointment(
                    cattle_id=cow4.id,
                    veterinarian_name="Dr. Sarah Jenkins, DVM",
                    reason="URGENT Automated RPA Triage: Critical fever (40.8°C), tachycardia (108 bpm) and recumbency.",
                    priority="URGENT",
                    scheduled_at=now + datetime.timedelta(hours=3),
                    status="SCHEDULED",
                    notes="Prepared emergency antibiotic therapy and IV fluid hydration."
                )
                db.add(apt)

        db.commit()
        print("-> Initial alerts and veterinary appointments seeded successfully!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
