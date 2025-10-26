import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MotionSensor:
    def process_event(self, data: dict) -> dict:
        motion_detected = data.get("motion_detected", False)
        area = data.get("area", "unknown")
        
        if motion_detected:
            logger.warning(f"ALERTA: Movimiento detectado en el área {area}")
            return {
                "alert": True,
                "type": "motion",
                "message": f"Movimiento no autorizado detectado en {area}."
            }
        return {"alert": False}

class TemperatureSensor:
    MAX_TEMP = 90.0

    def process_event(self, data: dict) -> dict:
        temperature = data.get("temperature", 20.0)
        location = data.get("location", "server_room")
        
        if temperature > self.MAX_TEMP:
            logger.critical(f"ALERTA: Temperatura extrema en {location}: {temperature}°C")
            return {
                "alert": True,
                "type": "temperature",
                "message": f"Peligro de incendio: Temperatura de {temperature}°C en {location}."
            }
        return {"alert": False}

class AccessSensor:
    AUTHORIZED_PERSONNEL = ["admin_user"]

    def process_event(self, data: dict) -> dict:
        user_id = data.get("user_id")
        door_id = data.get("door_id", "main_lab")
        
        if user_id not in self.AUTHORIZED_PERSONNEL:
            logger.warning(f"ALERTA: Intento de acceso denegado en {door_id} por {user_id}")
            return {
                "alert": True,
                "type": "access",
                "message": f"Acceso no autorizado intentado en {door_id} por usuario '{user_id}'."
            }
        return {"alert": False, "message": f"Acceso concedido a {user_id} en {door_id}."}


SENSOR_REGISTRY = {
    "motion": MotionSensor(),
    "temperature": TemperatureSensor(),
    "access": AccessSensor(),
}

def get_sensor(sensor_type: str):
    """Devuelve una instancia del sensor solicitado."""
    sensor = SENSOR_REGISTRY.get(sensor_type)
    if not sensor:
        raise ValueError(f"Tipo de sensor desconocido: {sensor_type}")
    return sensor