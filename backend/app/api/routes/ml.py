from fastapi import APIRouter
from app.services.ml_service import ml_service
from app.ml.predict import get_metrics_payload
from app.ml.model_registry import get_registry_info

router = APIRouter(prefix="/ml", tags=["Model Analytics & Registry"])

@router.get("/model-info")
def get_ml_model_info():
    """
    Returns exact Random Forest model specifications and benchmark results
    sourced from model_metadata.json.
    """
    return ml_service.get_model_info()

@router.get("/registry")
def get_model_registry():
    return get_registry_info()

@router.get("/performance")
def get_model_performance():
    return get_metrics_payload()
