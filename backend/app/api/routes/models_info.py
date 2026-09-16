from fastapi import APIRouter
from app.ml.predict import get_metrics_payload
from app.ml.model_registry import get_registry_info

router = APIRouter(prefix="/models", tags=["Model Analytics & Registry"])

@router.get("")
def get_model_registry():
    return get_registry_info()

@router.get("/performance")
def get_model_performance():
    payload = get_metrics_payload()
    return payload
