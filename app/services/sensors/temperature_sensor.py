from typing import Dict, Any
import asyncio
from datetime import datetime

class TemperatureSensor:

    async def process_event(self, data: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0)

        temp = data.get("temperature")
        unit = data.get("unit", "C")
        sensor_id = data.get("sensor_id", "unknown")
        ts = data.get("timestamp") or datetime.utcnow().isoformat()

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
