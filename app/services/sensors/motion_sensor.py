import time
import asyncio
from datetime import datetime
from typing import Dict, Any
from app.services.monitoring.metrics import EVENT_COUNTER, EVENT_LATENCY
from app.services.store import add_event  # <-- nuevo import

class MotionSensor:

    async def process_event(self, data: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.time()
        await asyncio.sleep(0.5)

        movement = bool(data.get("movement", False))
        zone = data.get("zone", "unknown")
        authorized = data.get("authorized")
        ts = data.get("timestamp") or datetime.utcnow().isoformat()

        if not movement:
            result = {"alert": False, "message": "No hay movimiento", "metadata": {"zone": zone, "timestamp": ts}}
            latency = time.time() - start_time
            add_event("motion", result, latency)
            return result

        if authorized is False:
            result = {
                "alert": True,
                "severity": "high",
                "message": f"Movimiento no autorizado en zona {zone}",
                "metadata": {"timestamp": ts, "zone": zone}
            }
            latency = time.time() - start_time
            add_event("motion", result, latency)
            return result

        EVENT_COUNTER.labels(sensor_type="motion").inc()
        latency = time.time() - start_time
        EVENT_LATENCY.labels(sensor_type="motion").observe(latency)

        result = {
            "alert": True,
            "severity": "medium",
            "message": f"Movimiento detectado en zona {zone}",
            "metadata": {"timestamp": ts, "zone": zone}
        }
        add_event("motion", result, latency)
        return result
