# CATTLEX Deployment & Operations Guide

## 1. Quick Local Startup (Zero Dependency)
The system is designed to run directly on Windows, macOS, or Linux using Python and Node.js:

```bash
# 1. Setup virtual environment & dependencies
cd cattlex/backend
pip install -r requirements.txt

# 2. Train and serialize ML models
python ../ml/scripts/train_models.py

# 3. Seed demo cattle and historical readings
python ../scripts/seed_database.py

# 4. Start FastAPI backend server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# 5. Start React Vite frontend (in separate terminal)
cd ../frontend
npm install
npm run dev
```

---

## 2. Docker Compose Deployment
To run with PostgreSQL, Mosquitto MQTT broker, FastAPI backend, and React frontend in isolated containers:

```bash
docker compose up --build -d
```

### Services Started:
- `cattlex-frontend`: Port 5173 / 80
- `cattlex-backend`: Port 8000
- `cattlex-postgres`: Port 5432
- `cattlex-mqtt`: Port 1883 & 9001 (WebSockets)
