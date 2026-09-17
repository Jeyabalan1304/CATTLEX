from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.iot.sensor_simulator import simulator

router = APIRouter(prefix="/simulator", tags=["IoT Sensor Simulator"])

class SimulationStartRequest(BaseModel):
    scenario: Optional[str] = "NORMAL"  # NORMAL, AT_RISK, CRITICAL, DISEASE_EVENT
    cattle_count: Optional[int] = 5
    interval_seconds: Optional[float] = 4.0
    selected_cattle: Optional[list] = None

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
        "interval_seconds": simulator._interval_seconds,
        "cattle_count": len(simulator.cattle_states),
        "cattle": list(simulator.cattle_states.values())
    }

@router.post("/start")
def start_simulator(req: Optional[SimulationStartRequest] = None):
    if req:
        if req.interval_seconds:
            simulator._interval_seconds = max(1.0, float(req.interval_seconds))
        if req.scenario:
            scen = req.scenario.upper()
            if scen == "CRITICAL":
                for tag in simulator.cattle_states:
                    simulator.cattle_states[tag]["state"] = "CRITICAL"
            elif scen == "AT_RISK":
                for tag in simulator.cattle_states:
                    simulator.cattle_states[tag]["state"] = "AT_RISK"
            elif scen == "DISEASE_EVENT":
                target = (req.selected_cattle[0] if req.selected_cattle else "COW001")
                simulator.trigger_abnormal_event(target)
            elif scen == "NORMAL":
                simulator.reset_cattle()

    simulator.start()
    return {
        "status": "started",
        "running": simulator.running,
        "scenario": req.scenario if req else "NORMAL",
        "interval_seconds": simulator._interval_seconds
    }

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
