from .motion_sensor import MotionSensor
from .temperature_sensor import TemperatureSensor
from .access_sensor import AccessSensor

SENSOR_REGISTRY = {
    "motion": MotionSensor(),
    "temperature": TemperatureSensor(),
    "access": AccessSensor(),
}

__all__ = ["SENSOR_REGISTRY"]
