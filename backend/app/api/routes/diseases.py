from fastapi import APIRouter
from app.ml.preprocessing import (
    SYMPTOM_FEATURES, SYMPTOM_DISPLAY_NAMES,
    DISEASE_CLASSES, DISEASE_DISPLAY_NAMES
)

router = APIRouter(prefix="/diseases", tags=["Disease Knowledge Base"])

@router.get("/symptoms")
def list_symptoms():
    """
    Returns the comprehensive list of 93 symptoms available in the CATTLEX ML model.
    """
    symptoms = []
    for feat in SYMPTOM_FEATURES:
        symptoms.append({
            "key": feat,
            "display_name": SYMPTOM_DISPLAY_NAMES.get(feat, feat.replace('_', ' ').title())
        })
    return {
        "count": len(symptoms),
        "symptoms": symptoms
    }

@router.get("/classes")
def list_disease_classes():
    """
    Returns the 26 supported cattle disease categories.
    """
    diseases = []
    for d in DISEASE_CLASSES:
        diseases.append({
            "key": d,
            "display_name": DISEASE_DISPLAY_NAMES.get(d, d.replace('_', ' ').title())
        })
    return {
        "count": len(diseases),
        "source": "Trained on real GitHub reference dataset (2,044 cattle symptom samples)",
        "diseases": diseases
    }
