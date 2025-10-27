import asyncio
from typing import Dict, Any, Optional
from pydantic import BaseModel
from app.services.sensors.motion_sensor import MotionSensor
from app.services.sensors.access_sensor import AccessSensor
from app.services.sensors.temperature_sensor import TemperatureSensor
from fastapi import APIRouter, HTTPException, Query

from app.services.sensors import SENSOR_REGISTRY

router = APIRouter(prefix="/sensor", tags=["sensors"])

@router.get("/")
async def list_sensors() -> Dict[str, Any]:    
    return {
        "available_sensors": list(SENSOR_REGISTRY.keys()),
        "count": len(SENSOR_REGISTRY)
    }

class MotionEvent(BaseModel):
    movement: bool
    zone: str
    authorized: bool | None = None
    timestamp: str | None = None

class AccessEvent(BaseModel):
    badge_id: str | None = None
    door: str = "unknown"
    unauthorized_access: bool | None = None
    timestamp: str | None = None

class TemperatureEvent(BaseModel):
    temperature: Optional[float] = None
    unit: str = "C"
    sensor_id: str = "unknown"
    timestamp: Optional[str] = None

@router.post("/motion")
async def simulate_motion_event(event: MotionEvent):
    sensor = MotionSensor()
    result = await sensor.process_event(event.dict())
    return result

@router.post("/access")
async def simulate_access_event(event: AccessEvent):
    sensor = AccessSensor(authorized_ids=["ID001", "ID002"])
    result = await sensor.process_event(event.dict())
    return result

@router.post("/temperature")
async def simulate_temperature_event(
    event: TemperatureEvent,
    wait: Optional[bool] = Query(False, description="Esperar medio segundo para simular retardo del sensor")):
        if wait:
            await asyncio.sleep(0.5)

        sensor = TemperatureSensor(low_threshold=0.0, high_threshold=35.0)
        result = await sensor.process_event(event.dict())
        return result