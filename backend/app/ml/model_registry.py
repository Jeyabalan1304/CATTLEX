import os
import json
from typing import Dict, Any
from app.core.config import settings

def get_registry_info() -> Dict[str, Any]:
    registry_path = os.path.join(settings.MODEL_DIR, "model_registry.json")
    if os.path.exists(registry_path):
        with open(registry_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "registry_version": "1.0.0",
        "status": "initialized",
        "primary_model": "Random Forest",
        "models": {}
    }
