#!/bin/bash
set -e

echo "=========================================================="
echo " CATTLEX: Setting up Production-Style Academic System    "
echo "=========================================================="

echo "[1/4] Installing Python Backend Dependencies..."
pip install -r backend/requirements.txt

echo "[2/4] Executing ML Model Training & Benchmarking..."
python ml/scripts/train_models.py

echo "[3/4] Seeding Database with Initial Cattle Fleet..."
python scripts/seed_database.py

echo "[4/4] Running Automated Pytest Validation Suite..."
python -m pytest backend/tests/ -v

echo "=========================================================="
echo " CATTLEX Setup Complete!                                  "
echo " To start backend: uvicorn app.main:app --reload (in backend)"
echo " To start frontend: npm run dev (in frontend)             "
echo "=========================================================="
