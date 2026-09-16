import json
import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.models.prediction import HealthPrediction, DiseasePrediction
from app.schemas.prediction import HealthPredictionRequest, DiseasePredictionRequest
from app.ml.predict import predict_disease, predict_health_risk

def create_disease_prediction(db: Session, request: DiseasePredictionRequest) -> DiseasePrediction:
    # Run ML prediction
    res = predict_disease(request.symptoms, model_name=request.model_name or "Random Forest")

    # Store in database
    record = DiseasePrediction(
        cattle_id=request.cattle_id,
        predicted_disease=res["predicted_disease"],
        confidence=res["confidence"],
        model_name=res["model_name"],
        model_version="1.0.0",
        input_symptoms=json.dumps(request.symptoms),
        top_predictions=json.dumps(res["top_predictions"]),
        important_features=json.dumps(res["important_features"]),
        recommendation=res["recommendation"],
        timestamp=datetime.datetime.utcnow()
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record, res

def create_health_prediction(db: Session, request: HealthPredictionRequest) -> HealthPrediction:
    res = predict_health_risk({
        "temperature": request.temperature,
        "heart_rate": request.heart_rate,
        "respiratory_rate": request.respiratory_rate,
        "activity_level": request.activity_level,
        "feed_intake": request.feed_intake,
        "water_intake": request.water_intake
    })

    record = HealthPrediction(
        cattle_id=request.cattle_id,
        health_status=res["health_status"],
        risk_score=res["risk_score"],
        model_name=res["model_name"],
        model_version="1.0.0",
        confidence=res["confidence"],
        prediction_reason=res["prediction_reason"],
        timestamp=datetime.datetime.utcnow()
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record, res

def get_disease_predictions_for_cattle(db: Session, cattle_id: int, limit: int = 20) -> List[DiseasePrediction]:
    return db.query(DiseasePrediction).filter(
        DiseasePrediction.cattle_id == cattle_id
    ).order_by(desc(DiseasePrediction.timestamp)).limit(limit).all()

def get_health_predictions_for_cattle(db: Session, cattle_id: int, limit: int = 50) -> List[HealthPrediction]:
    return db.query(HealthPrediction).filter(
        HealthPrediction.cattle_id == cattle_id
    ).order_by(desc(HealthPrediction.timestamp)).limit(limit).all()
