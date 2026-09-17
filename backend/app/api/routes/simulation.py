from fastapi import APIRouter
from app.api.routes.simulator import (
    get_simulator_status,
    start_simulator,
    stop_simulator,
    trigger_abnormal,
    reset_simulator
)

router = APIRouter(prefix="/simulation", tags=["IoT Simulation Engine"])

router.add_api_route("/status", get_simulator_status, methods=["GET"])
router.add_api_route("/start", start_simulator, methods=["POST"])
router.add_api_route("/stop", stop_simulator, methods=["POST"])
router.add_api_route("/trigger-abnormal", trigger_abnormal, methods=["POST"])
router.add_api_route("/reset", reset_simulator, methods=["POST"])
