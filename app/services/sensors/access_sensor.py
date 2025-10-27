import asyncio
import time
from typing import Dict, Any, Iterable
from datetime import datetime
from app.services.monitoring.metrics import EVENT_COUNTER, EVENT_LATENCY

class AccessSensor:
    
    def __init__(self, authorized_ids: Iterable[str] = None):
        self.authorized_ids = set(authorized_ids or [])

    async def process_event(self, data: Dict[str, Any]) -> Dict[str, Any]:
        
        start_time = time.time()
        
        await asyncio.sleep(0.5)

        badge = data.get("badge_id")
        explicit_unauth = data.get("unauthorized_access")
        ts = data.get("timestamp") or datetime.utcnow().isoformat()
        door = data.get("door", "unknown")

        if explicit_unauth is True:
            return {
                "alert": True,
                "severity": "high",
                "message": f"Intento de acceso no autorizado detectado en puerta {door}",
                "metadata": {"badge_id": badge, "door": door, "timestamp": ts}
            }

        if badge is None:
            return {
                "alert": True,
                "severity": "high",
                "message": "Evento de acceso sin badge_id",
                "metadata": {"door": door, "timestamp": ts}
            }

        if badge not in self.authorized_ids:
            return {
                "alert": True,
                "severity": "high",
                "message": f"Badge desconocido o no autorizado: {badge} en puerta {door}",
                "metadata": {"badge_id": badge, "door": door, "timestamp": ts}
            }
            
        EVENT_COUNTER.labels(sensor_type="access").inc()
        EVENT_LATENCY.labels(sensor_type="access").observe(time.time() - start_time)

        return {
            "alert": False,
            "message": "Acceso autorizado",
            "metadata": {"badge_id": badge, "door": door, "timestamp": ts}
        }
