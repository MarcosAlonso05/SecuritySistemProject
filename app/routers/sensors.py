import asyncio
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query

from app.services.sensors import SENSOR_REGISTRY

router = APIRouter(prefix="/sensor", tags=["sensors"])

@router.get("/")
async def list_sensors() -> Dict[str, Any]:    
    return {
        "available_sensors": list(SENSOR_REGISTRY.keys()),
        "count": len(SENSOR_REGISTRY)
    }

@router.post("/{sensor_type}")
async def receive_sensor_event(
    sensor_type: str,
    event: Dict[str, Any],
    wait: Optional[bool] = Query(False, description="Si True, espera al resultado del procesamiento")) -> Dict[str, Any]:    
    sensor = SENSOR_REGISTRY.get(sensor_type)
    if sensor is None:
        raise HTTPException(status_code=404, detail=f"Sensor '{sensor_type}' no registrado")

    if wait:
        result = await sensor.process_event(event)
        return {"status": "processed", "result": result}

    asyncio.create_task(sensor.process_event(event))
    return {"status": "accepted", "detail": "Evento encolado para procesamiento"}

@router.post("/motion")
async def receive_motion(event: Dict[str, Any], wait: Optional[bool] = Query(False)):
    return await receive_sensor_event("motion", event, wait)

@router.post("/temperature")
async def receive_temperature(event: Dict[str, Any], wait: Optional[bool] = Query(False)):
    return await receive_sensor_event("temperature", event, wait)

@router.post("/access")
async def receive_access(event: Dict[str, Any], wait: Optional[bool] = Query(False)):
    return await receive_sensor_event("access", event, wait)