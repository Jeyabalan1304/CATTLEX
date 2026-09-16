from typing import List, Dict, Any
from app.ml.preprocessing import SYMPTOM_FEATURES, SYMPTOM_DISPLAY_NAMES
from app.ml.predict import _loaded_models

def explain_prediction(symptoms: Dict[str, bool]) -> List[Dict[str, Any]]:
    """
    Computes explainable AI contribution scores for the active symptoms.
    Uses Random Forest Gini impurity reduction (feature_importances_) as the baseline metric.
    """
    rf_model = _loaded_models.get("Random Forest")
    if rf_model is None or not hasattr(rf_model, "feature_importances_"):
        return []

    importances = rf_model.feature_importances_
    results = []

    for idx, feature_name in enumerate(SYMPTOM_FEATURES):
        is_active = symptoms.get(feature_name, False) in [True, 1, '1', 'true', 'True']
        if is_active:
            results.append({
                "feature": feature_name,
                "display_name": SYMPTOM_DISPLAY_NAMES.get(feature_name, feature_name.replace('_', ' ').title()),
                "importance_score": round(float(importances[idx]), 4),
                "is_present": True,
                "clinical_impact": "High Risk Factor" if importances[idx] > 0.02 else "Secondary Symptom"
            })

    results.sort(key=lambda x: x["importance_score"], reverse=True)
    return results
