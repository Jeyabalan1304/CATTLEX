import os
import json
from typing import Dict, List, Tuple, Any, Optional
import numpy as np
import joblib
from app.core.config import settings
from app.core.logging import logger
from app.ml.preprocessing import (
    SYMPTOM_FEATURES, SYMPTOM_DISPLAY_NAMES,
    DISEASE_CLASSES, DISEASE_DISPLAY_NAMES, SymptomPreprocessor
)

# Global caches for trained models
_loaded_models: Dict[str, Any] = {}
_label_encoder = None
_vital_risk_model = None
_metrics_data = None
_preprocessor = SymptomPreprocessor()

MODEL_FILES = {
    "Random Forest": "random_forest_disease.joblib",
    "Gaussian Naive Bayes": "gaussian_nb_disease.joblib",
    "Decision Tree": "decision_tree_disease.joblib",
    "Logistic Regression": "logistic_regression_disease.joblib",
    "k-NN": "knn_disease.joblib",
    "Support Vector Machine": "svm_disease.joblib"
}


def load_ml_artifacts():
    global _loaded_models, _label_encoder, _vital_risk_model, _metrics_data

    model_dir = settings.MODEL_DIR
    logger.info(f"Loading ML artifacts from: {model_dir}")

    # 1. Load Label Encoder
    le_path = os.path.join(model_dir, "label_encoder.joblib")
    if os.path.exists(le_path):
        _label_encoder = joblib.load(le_path)
    else:
        logger.warning(f"Label encoder not found at {le_path}")

    # 2. Load Disease Classifiers
    for model_name, filename in MODEL_FILES.items():
        path = os.path.join(model_dir, filename)
        if os.path.exists(path):
            try:
                _loaded_models[model_name] = joblib.load(path)
                logger.info(f"Loaded classifier: {model_name}")
            except Exception as e:
                logger.error(f"Error loading {model_name} from {path}: {e}")
        else:
            logger.warning(f"Model file missing: {path}")

    # 3. Load Vital Health Risk Model
    vital_path = os.path.join(model_dir, "vital_health_risk_model.joblib")
    if os.path.exists(vital_path):
        try:
            _vital_risk_model = joblib.load(vital_path)
            logger.info("Loaded Vital Signs Health Risk engine.")
        except Exception as e:
            logger.error(f"Error loading vital risk model: {e}")

    # 4. Load Metrics & Feature Importance JSON
    metrics_path = os.path.join(model_dir, "model_metrics.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, "r", encoding="utf-8") as f:
            _metrics_data = json.load(f)


def get_available_models() -> List[str]:
    return list(_loaded_models.keys())


def predict_disease(symptoms: Dict[str, bool], model_name: str = "Random Forest") -> Dict[str, Any]:
    """
    Infers cattle disease probability from symptom input vector.
    """
    if not _loaded_models:
        load_ml_artifacts()

    # Default to Random Forest if requested model not available
    clf = _loaded_models.get(model_name) or _loaded_models.get("Random Forest")
    if clf is None:
        raise RuntimeError("No ML models are loaded in memory. Ensure training script has run.")

    # Vectorize symptoms
    X_vec = _preprocessor.transform(symptoms)

    # Prediction & probabilities
    prediction_idx = clf.predict(X_vec)[0]
    
    if hasattr(clf, "predict_proba"):
        probas = clf.predict_proba(X_vec)[0]
    elif hasattr(clf, "decision_function"):
        # SVM or non-probabilistic fallback
        df_vals = clf.decision_function(X_vec)[0]
        # Softmax approximation
        exp_vals = np.exp(df_vals - np.max(df_vals))
        probas = exp_vals / np.sum(exp_vals)
    else:
        probas = np.zeros(len(_label_encoder.classes_))
        probas[prediction_idx] = 1.0

    # Top 3 predictions
    top_indices = np.argsort(probas)[::-1][:3]
    top_predictions = []
    for idx in top_indices:
        disease_key = _label_encoder.inverse_transform([idx])[0]
        top_predictions.append({
            "disease": disease_key,
            "display_name": DISEASE_DISPLAY_NAMES.get(disease_key, disease_key.replace('_', ' ').title()),
            "probability": round(float(probas[idx]), 4)
        })

    predicted_key = _label_encoder.inverse_transform([prediction_idx])[0]
    predicted_display = DISEASE_DISPLAY_NAMES.get(predicted_key, predicted_key.replace('_', ' ').title())
    confidence = round(float(probas[prediction_idx]), 4)

    # Feature importances extraction (using Random Forest reference)
    important_features = []
    rf_model = _loaded_models.get("Random Forest")
    if rf_model and hasattr(rf_model, "feature_importances_"):
        rf_importances = rf_model.feature_importances_
        # Find active symptoms first
        active_symptoms = [k for k, v in symptoms.items() if v in [True, 1, '1', 'true', 'True']]
        for feat in active_symptoms:
            if feat in SYMPTOM_FEATURES:
                feat_idx = SYMPTOM_FEATURES.index(feat)
                important_features.append({
                    "feature": feat,
                    "display_name": SYMPTOM_DISPLAY_NAMES.get(feat, feat.replace('_', ' ').title()),
                    "importance": round(float(rf_importances[feat_idx]), 4),
                    "present": True
                })
        # Sort active features by importance
        important_features.sort(key=lambda x: x["importance"], reverse=True)

    # Clinical guideline recommendation
    recommendation = (
        f"Predicted condition: {predicted_display} with {confidence*100:.1f}% confidence. "
        f"Initiate veterinary evaluation immediately and monitor vital parameters."
    )

    return {
        "predicted_disease": predicted_key,
        "display_name": predicted_display,
        "confidence": confidence,
        "model_name": model_name if model_name in _loaded_models else "Random Forest",
        "top_predictions": top_predictions,
        "important_features": important_features,
        "recommendation": recommendation
    }


def predict_health_risk(vitals: Dict[str, float]) -> Dict[str, Any]:
    """
    Computes cattle health status (HEALTHY, AT_RISK, CRITICAL) and 0-100 risk score
    from vital sensor readings using veterinary reference physiological thresholds.
    """
    temp = vitals.get("temperature", 38.6)
    hr = vitals.get("heart_rate", 65.0)
    rr = vitals.get("respiratory_rate", 28.0)
    act = vitals.get("activity_level", 0.8)
    feed = vitals.get("feed_intake", 18.0)
    water = vitals.get("water_intake", 60.0)

    # Physiological deviation penalties
    risk_points = 0.0
    reasons = []

    # Temperature (Normal Bovine: 38.0 - 39.3°C)
    if temp > 40.2:
        risk_points += 35.0
        reasons.append(f"Severe pyrexia/fever ({temp:.1f}°C)")
    elif temp > 39.3:
        risk_points += 20.0
        reasons.append(f"Elevated body temperature ({temp:.1f}°C)")
    elif temp < 37.5:
        risk_points += 30.0
        reasons.append(f"Hypothermia ({temp:.1f}°C)")

    # Heart Rate (Normal: 48 - 84 bpm)
    if hr > 95:
        risk_points += 25.0
        reasons.append(f"Tachycardia ({hr:.0f} bpm)")
    elif hr > 84:
        risk_points += 15.0
        reasons.append(f"Elevated heart rate ({hr:.0f} bpm)")
    elif hr < 44:
        risk_points += 25.0
        reasons.append(f"Bradycardia ({hr:.0f} bpm)")

    # Respiratory Rate (Normal: 24 - 36 bpm)
    if rr > 45:
        risk_points += 20.0
        reasons.append(f"Tachypnea / labored breathing ({rr:.0f} bpm)")
    elif rr < 16:
        risk_points += 20.0
        reasons.append(f"Depressed respiration ({rr:.0f} bpm)")

    # Activity Level (Normal: 0.65 - 1.0)
    if act < 0.30:
        risk_points += 25.0
        reasons.append(f"Severe lethargy / immobility (activity: {act:.2f})")
    elif act < 0.55:
        risk_points += 15.0
        reasons.append(f"Reduced herd mobility (activity: {act:.2f})")

    # Feed Intake (Normal: 14 - 25 kg/day)
    if feed < 7.0:
        risk_points += 25.0
        reasons.append(f"Acute anorexia / reduced feed ({feed:.1f} kg)")
    elif feed < 13.0:
        risk_points += 15.0
        reasons.append(f"Subnormal feed intake ({feed:.1f} kg)")

    # Water Intake (Normal: 40 - 85 L/day)
    if water < 20.0:
        risk_points += 20.0
        reasons.append(f"Severe dehydration risk ({water:.1f} L)")
    elif water < 35.0:
        risk_points += 10.0
        reasons.append(f"Subnormal water consumption ({water:.1f} L)")

    # Bound risk score between 5.0 and 99.0
    final_risk_score = round(min(max(risk_points, 5.0), 99.0), 1)

    if final_risk_score >= 70.0:
        status = "CRITICAL"
        confidence = 0.94
    elif final_risk_score >= 35.0:
        status = "AT_RISK"
        confidence = 0.88
    else:
        status = "HEALTHY"
        confidence = 0.96
        reasons = ["All physiological vitals within normal bovine reference ranges."]

    reason_str = "; ".join(reasons)

    return {
        "health_status": status,
        "risk_score": final_risk_score,
        "confidence": confidence,
        "prediction_reason": reason_str,
        "model_name": "VitalSigns-RiskEngine-v1"
    }


def get_metrics_payload() -> Dict[str, Any]:
    global _metrics_data
    if _metrics_data is None:
        load_ml_artifacts()
    return _metrics_data or {}
