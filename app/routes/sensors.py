from fastapi import APIRouter
from pydantic import BaseModel
from app.services.sensors.motion_sensor import MotionSensor
from app.services.sensors.access_sensor import AccessSensor
from app.services.sensors.temperature_sensor import TemperatureSensor

router = APIRouter(prefix="/sensor", tags=["sensors"])

class MotionEvent(BaseModel):
    movement: bool
    zone: str
    authorized: bool | None = None

class AccessEvent(BaseModel):
    badge_id: str | None = None
    door: str = "unknown"
    unauthorized_access: bool | None = None

class TempEvent(BaseModel):
    temperature: float
    unit: str = "C"
    sensor_id: str

@router.post("/motion")
async def simulate_motion(event: MotionEvent):
    sensor = MotionSensor()
    result = await sensor.process_event(event.dict())
    return result

@router.post("/access")
async def simulate_access(event: AccessEvent):
    sensor = AccessSensor(authorized_ids=["ID001", "ID002"])
    result = await sensor.process_event(event.dict())
    return result

@router.post("/temperature")
async def simulate_temperature(event: TempEvent):
    sensor = TemperatureSensor(low_threshold=0, high_threshold=35)
    result = await sensor.process_event(event.dict())
    return result
