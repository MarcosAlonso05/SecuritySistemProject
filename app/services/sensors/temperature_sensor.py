import asyncio
import time
from typing import Dict, Any
from datetime import datetime
from app.services.monitoring.metrics import EVENT_COUNTER, EVENT_LATENCY
from app.services.store import add_event

class TemperatureSensor:

    def __init__(self, low_threshold: float = 0.0, high_threshold: float = 35.0):
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
    
    async def process_event(self, data: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.time()
        await asyncio.sleep(0.5)

        temp = data.get("temperature")
        unit = data.get("unit", "C")
        sensor_id = data.get("sensor_id", "unknown")
        ts = data.get("timestamp") or datetime.utcnow().isoformat()

        EVENT_COUNTER.labels(sensor_type="temperature").inc()

        try:
            if temp is None:
                result = {
                    "alert": False,
                    "message": "Temperatura no proporcionada",
                    "metadata": {"sensor_id": sensor_id}
                }
                latency = time.time() - start_time
                add_event("temperature", result, latency)
                return result

            temp_val = float(temp)
        except (ValueError, TypeError):
            result = {
                "alert": False,
                "message": "Valor de temperatura inválido",
                "metadata": {"sensor_id": sensor_id}
            }
            latency = time.time() - start_time
            add_event("temperature", result, latency)
            return result

        if unit.upper() == "F":
            temp_c = (temp_val - 32) * 5.0 / 9.0
        else:
            temp_c = temp_val

        if temp_c >= self.high_threshold:
            result = {
                "alert": True,
                "severity": "high",
                "message": f"Temperatura extremadamente alta: {temp_c:.1f}°C (sensor {sensor_id})",
                "metadata": {"temperature_c": temp_c, "sensor_id": sensor_id, "timestamp": ts}
            }
        elif temp_c <= self.low_threshold:
            result = {
                "alert": True,
                "severity": "high",
                "message": f"Temperatura extremadamente baja: {temp_c:.1f}°C (sensor {sensor_id})",
                "metadata": {"temperature_c": temp_c, "sensor_id": sensor_id, "timestamp": ts}
            }
        elif temp_c >= (self.high_threshold - 5.0):
            result = {
                "alert": True,
                "severity": "medium",
                "message": f"Temperatura alta cercana al umbral: {temp_c:.1f}°C (sensor {sensor_id})",
                "metadata": {"temperature_c": temp_c, "sensor_id": sensor_id, "timestamp": ts}
            }
        else:
            result = {
                "alert": False,
                "message": "Temperatura normal",
                "metadata": {"temperature_c": temp_c, "sensor_id": sensor_id}
            }

        latency = time.time() - start_time
        EVENT_LATENCY.labels(sensor_type="temperature").observe(latency)
        add_event("temperature", result, latency)

        return result
