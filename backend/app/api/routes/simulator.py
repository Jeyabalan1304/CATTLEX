from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.iot.sensor_simulator import simulator

router = APIRouter(prefix="/simulator", tags=["IoT Sensor Simulator"])

class TriggerAbnormalRequest(BaseModel):
    tag_id: str = "COW001"

class SimulatorStatusResponse(BaseModel):
    running: bool
    simulated_cattle: list
    message: str

@router.get("/status")
def get_simulator_status():
    return {
        "running": simulator.running,
        "cattle": list(simulator.cattle_states.values())
    }

@router.post("/start")
def start_simulator():
    simulator.start()
    return {"status": "started", "running": simulator.running}

@router.post("/stop")
def stop_simulator():
    simulator.stop()
    return {"status": "stopped", "running": simulator.running}

@router.post("/trigger-abnormal")
def trigger_abnormal(req: TriggerAbnormalRequest):
    success = simulator.trigger_abnormal_event(req.tag_id)
    if not success:
        return {"status": "error", "message": f"Cattle tag {req.tag_id} not found in simulator"}
    return {
        "status": "triggered",
        "tag_id": req.tag_id,
        "message": f"Gradual sickness progression triggered for {req.tag_id}. Temperature and heart rate will climb, activity and feed intake will decline over consecutive telemetry cycles."
    }

@router.post("/reset")
def reset_simulator(tag_id: Optional[str] = None):
    simulator.reset_cattle(tag_id)
    return {"status": "reset", "message": "All cattle vitals reset to baseline physiological range."}
