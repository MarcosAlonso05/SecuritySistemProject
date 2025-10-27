import asyncio
import time
from typing import Dict, Any
from datetime import datetime
from app.services.monitoring.metrics import EVENT_COUNTER, EVENT_LATENCY

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
        EVENT_LATENCY.labels(sensor_type="temperature").observe(time.time() - start_time)

        if temp is None:
            return {"alert": False, "message": "Temperatura no proporcionada", "metadata": {"sensor_id": sensor_id}}

        try:
            temp_val = float(temp)
        except (ValueError, TypeError):
            return {"alert": False, "message": "Valor de temperatura inválido", "metadata": {"sensor_id": sensor_id}}

        if unit.upper() == "F":
            temp_c = (temp_val - 32) * 5.0/9.0
        else:
            temp_c = temp_val

        if temp_c >= self.high_threshold:
            return {
                "alert": True,
                "severity": "high",
                "message": f"Temperatura extremadamente alta: {temp_c:.1f}°C (sensor {sensor_id})",
                "metadata": {"temperature_c": temp_c, "sensor_id": sensor_id, "timestamp": ts}
            }

        if temp_c <= self.low_threshold:
            return {
                "alert": True,
                "severity": "high",
                "message": f"Temperatura extremadamente baja: {temp_c:.1f}°C (sensor {sensor_id})",
                "metadata": {"temperature_c": temp_c, "sensor_id": sensor_id, "timestamp": ts}
            }

        warning_margin = 5.0
        if temp_c >= (self.high_threshold - warning_margin):
            return {
                "alert": True,
                "severity": "medium",
                "message": f"Temperatura alta cercana al umbral: {temp_c:.1f}°C (sensor {sensor_id})",
                "metadata": {"temperature_c": temp_c, "sensor_id": sensor_id, "timestamp": ts}
            }

        return {"alert": False, "message": "Temperatura normal", "metadata": {"temperature_c": temp_c, "sensor_id": sensor_id}}
