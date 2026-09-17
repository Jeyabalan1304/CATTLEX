import asyncio
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.db.database import engine, Base
from app.db import models
from app.ml.predict import load_ml_artifacts
from app.iot.mqtt_client import mqtt_manager
from app.iot.sensor_simulator import simulator

# Import routes
from app.api.routes.auth import router as auth_router
from app.api.routes.cattle import router as cattle_router
from app.api.routes.sensors import router as sensor_router
from app.api.routes.predictions import router as prediction_router
from app.api.routes.diseases import router as disease_router
from app.api.routes.alerts import router as alert_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.veterinarians import router as vet_router
from app.api.routes.models_info import router as models_router
from app.api.routes.simulator import router as simulator_router

# Setup structured logging
setup_logging()

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for modern frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket Connection Manager for live dashboard telemetry
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    def broadcast_sync(self, message: dict):
        """Dispatches message synchronously across all active WebSocket clients"""
        for connection in list(self.active_connections):
            try:
                # Use current running event loop to schedule send
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(connection.send_json(message))
            except Exception:
                pass

from app.api.routes.health import router as health_router
from app.api.routes.ml import router as ml_router
from app.api.routes.analytics import router as analytics_router

ws_manager = ConnectionManager()

@app.websocket("/ws")
@app.websocket("/api/v1/ws/dashboard")
@app.websocket("/api/ws/dashboard")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep connection open, receive ping or client commands
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception:
        ws_manager.disconnect(websocket)

@app.on_event("startup")
def on_startup():
    logger.info("Initializing CATTLEX Database Tables...")
    Base.metadata.create_all(bind=engine)

    logger.info("Pre-loading CATTLEX ML Classifiers & Artifacts...")
    try:
        load_ml_artifacts()
    except Exception as e:
        logger.error(f"Error loading ML artifacts: {e}")

    logger.info("Wiring Real-Time Telemetry Callbacks...")
    # Link MQTT manager broadcast to WebSockets
    mqtt_manager.set_ws_broadcast(ws_manager.broadcast_sync)
    mqtt_manager.start()

    # Link Simulator output to the telemetry ingestion pipeline
    simulator.set_callback(mqtt_manager.process_telemetry)

    logger.info("CATTLEX Backend Engine is fully initialized and operational.")

@app.get("/")
def root():
    return {
        "system": "CATTLEX",
        "title": "An AI-Integrated, Solar-Powered IoT System Enhanced with Predictive Analytics for Multi-Disease Management in Livestock",
        "version": settings.PROJECT_VERSION,
        "status": "online",
        "docs_url": "/docs"
    }

from app.api.routes.simulation import router as simulation_router

# Register all Routers under /api/v1 (primary) and /api (legacy)
for prefix in [settings.API_V1_STR, settings.API_LEGACY_STR]:
    app.include_router(health_router, prefix=prefix)
    app.include_router(ml_router, prefix=prefix)
    app.include_router(analytics_router, prefix=prefix)
    app.include_router(auth_router, prefix=prefix)
    app.include_router(cattle_router, prefix=prefix)
    app.include_router(sensor_router, prefix=prefix)
    app.include_router(prediction_router, prefix=prefix)
    app.include_router(disease_router, prefix=prefix)
    app.include_router(alert_router, prefix=prefix)
    app.include_router(dashboard_router, prefix=prefix)
    app.include_router(vet_router, prefix=prefix)
    app.include_router(models_router, prefix=prefix)
    app.include_router(simulator_router, prefix=prefix)
    app.include_router(simulation_router, prefix=prefix)
