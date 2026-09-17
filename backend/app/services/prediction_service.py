import json
import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.models.prediction import HealthPrediction, DiseasePrediction
from app.schemas.prediction import HealthPredictionRequest, DiseasePredictionRequest
from app.ml.predict import predict_disease, predict_health_risk

import uuid
from app.db.models.cattle import Cattle
from app.services.ml_service import ml_service

def create_disease_prediction(db: Session, request: DiseasePredictionRequest):
    # Resolve cattle ID (integer or string tag like COW001 / CATTLE-001)
    cattle_db_id = 1
    if isinstance(request.cattle_id, int):
        cattle_db_id = request.cattle_id
    elif isinstance(request.cattle_id, str):
        c = db.query(Cattle).filter(
            (Cattle.tag_id == request.cattle_id) | 
            (Cattle.name == request.cattle_id)
        ).first()
        if c:
            cattle_db_id = c.id
        elif request.cattle_id.isdigit():
            cattle_db_id = int(request.cattle_id)

    # Use validated CATTLEX-RF-v1 Random Forest service
    try:
        rf_res = ml_service.predict(request.symptoms)
        predicted_disease = rf_res["predicted_disease"]
        confidence = rf_res["confidence"]
        confidence_band = rf_res["confidence_band"]
        top_3 = rf_res["top_3"]
        model_version = rf_res.get("model", "CATTLEX-RF-v1")
        display_name = rf_res["display_name"]
        recommendation = rf_res["recommendation"]
        
        # Format top predictions
        top_predictions = [
            {"disease": t["disease"], "display_name": t["display_name"], "probability": t["probability"]}
            for t in top_3
        ]
        
        # Pull top learned importance features
        top_feats = ml_service.get_feature_importance(top_n=5)
        important_features = [
            {
                "feature": f["feature"],
                "display_name": f["display_name"],
                "importance": f["importance"],
                "present": bool(request.symptoms.get(f["feature"], False))
            }
            for f in top_feats
        ]
    except Exception as e:
        # Fallback to legacy predictor if necessary
        res = predict_disease(request.symptoms, model_name=request.model_name or "Random Forest")
        predicted_disease = res["predicted_disease"]
        confidence = res["confidence"]
        confidence_band = "HIGH" if confidence >= 0.80 else ("MODERATE" if confidence >= 0.50 else "LOW")
        top_predictions = res.get("top_predictions", [])
        top_3 = [{"disease": p["disease"], "display_name": p.get("display_name", p["disease"]), "probability": p["probability"]} for p in top_predictions[:3]]
        model_version = "CATTLEX-RF-v1"
        display_name = res.get("display_name", predicted_disease.replace("_", " ").title())
        important_features = res.get("important_features", [])
        recommendation = res.get("recommendation", f"Assessment for {display_name}")

    pred_uuid = str(uuid.uuid4())
    record = DiseasePrediction(
        prediction_id=pred_uuid,
        cattle_id=cattle_db_id,
        predicted_disease=predicted_disease,
        confidence=confidence,
        confidence_band=confidence_band,
        model_name="Random Forest",
        model_version=model_version,
        input_symptoms=json.dumps(request.symptoms),
        top_3=json.dumps(top_3),
        top_predictions=json.dumps(top_predictions),
        important_features=json.dumps(important_features),
        recommendation=recommendation,
        timestamp=datetime.datetime.utcnow(),
        created_at=datetime.datetime.utcnow()
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    output_res = {
        "prediction_id": pred_uuid,
        "cattle_id": request.cattle_id,
        "predicted_disease": predicted_disease,
        "display_name": display_name,
        "confidence": confidence,
        "confidence_band": confidence_band,
        "top_3": top_3,
        "top_predictions": top_predictions,
        "model_version": model_version,
        "model_name": "Random Forest",
        "important_features": important_features,
        "recommendation": recommendation,
        "disclaimer": "AI decision-support prediction — veterinary assessment required.",
        "created_at": record.created_at,
        "timestamp": record.timestamp
    }
    return record, output_res

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
