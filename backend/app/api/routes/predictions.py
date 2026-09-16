import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.database import get_db
from app.schemas.prediction import (
    HealthPredictionRequest, HealthPredictionResponse,
    DiseasePredictionRequest, DiseasePredictionResponse
)
from app.services import prediction_service
from app.db.models.prediction import DiseasePrediction, HealthPrediction
from app.db.models.cattle import Cattle
from app.automation.veterinary_workflow import trigger_automated_health_workflow

router = APIRouter(prefix="/predictions", tags=["Predictions"])

@router.post("/disease", response_model=DiseasePredictionResponse)
def predict_cattle_disease(request: DiseasePredictionRequest, db: Session = Depends(get_db)):
    cattle = db.query(Cattle).filter(Cattle.id == request.cattle_id).first()
    if not cattle:
        raise HTTPException(status_code=404, detail="Cattle not found")

    record, ml_res = prediction_service.create_disease_prediction(db, request)

    # If predicted with high confidence and not healthy, ensure alert is flagged
    if ml_res["confidence"] >= 0.70:
        trigger_automated_health_workflow(
            db=db,
            cattle=cattle,
            health_status="AT_RISK" if cattle.status == "HEALTHY" else cattle.status,
            risk_score=75.0 if cattle.status != "CRITICAL" else 90.0,
            reason=f"High-confidence symptom prediction for {ml_res['display_name']} ({ml_res['confidence']*100:.1f}%)",
            confidence=ml_res["confidence"]
        )

    return {
        "cattle_id": request.cattle_id,
        "predicted_disease": ml_res["predicted_disease"],
        "display_name": ml_res["display_name"],
        "confidence": ml_res["confidence"],
        "model_name": ml_res["model_name"],
        "top_predictions": ml_res["top_predictions"],
        "important_features": ml_res["important_features"],
        "recommendation": ml_res["recommendation"],
        "disclaimer": "This is a predictive decision-support system and not a definitive veterinary diagnosis. Professional veterinary evaluation is recommended.",
        "timestamp": record.timestamp
    }

@router.post("/health", response_model=HealthPredictionResponse)
def predict_cattle_health(request: HealthPredictionRequest, db: Session = Depends(get_db)):
    cattle = db.query(Cattle).filter(Cattle.id == request.cattle_id).first()
    if not cattle:
        raise HTTPException(status_code=404, detail="Cattle not found")

    record, res = prediction_service.create_health_prediction(db, request)

    trigger_automated_health_workflow(
        db=db,
        cattle=cattle,
        health_status=res["health_status"],
        risk_score=res["risk_score"],
        reason=res["prediction_reason"],
        confidence=res["confidence"]
    )

    return {
        "cattle_id": record.cattle_id,
        "health_status": record.health_status,
        "risk_score": record.risk_score,
        "model_name": record.model_name,
        "confidence": record.confidence,
        "prediction_reason": record.prediction_reason,
        "timestamp": record.timestamp
    }

@router.get("/{cattle_id}")
def get_prediction_history(cattle_id: int, db: Session = Depends(get_db)):
    health_preds = prediction_service.get_health_predictions_for_cattle(db, cattle_id, limit=30)
    disease_preds = prediction_service.get_disease_predictions_for_cattle(db, cattle_id, limit=20)

    formatted_disease = []
    for d in disease_preds:
        formatted_disease.append({
            "id": d.id,
            "predicted_disease": d.predicted_disease,
            "confidence": d.confidence,
            "model_name": d.model_name,
            "recommendation": d.recommendation,
            "top_predictions": json.loads(d.top_predictions) if d.top_predictions else [],
            "important_features": json.loads(d.important_features) if d.important_features else [],
            "timestamp": d.timestamp
        })

    return {
        "cattle_id": cattle_id,
        "health_predictions": health_preds,
        "disease_predictions": formatted_disease
    }
