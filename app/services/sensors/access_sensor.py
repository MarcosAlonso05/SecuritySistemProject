import asyncio
import time
from typing import Dict, Any, Iterable
from datetime import datetime
from app.services.monitoring.metrics import EVENT_COUNTER, EVENT_LATENCY
from app.services.store import add_event
from app.services import alerting

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
        
        result = None

        if explicit_unauth is True:
            result = {
                "alert": True,
                "severity": "high",
                "message": f"Intento de acceso no autorizado detectado en puerta {door}",
                "metadata": {"badge_id": badge, "door": door, "timestamp": ts}
            }
            latency = time.time() - start_time
            add_event("access", result, latency)
            return result

        elif badge is None:
            result = {
                "alert": True,
                "severity": "high",
                "message": "Evento de acceso sin badge_id",
                "metadata": {"door": door, "timestamp": ts}
            }
            latency = time.time() - start_time
            add_event("access", result, latency)
            return result

        elif badge not in self.authorized_ids:
            result = {
                "alert": True,
                "severity": "high",
                "message": f"Badge desconocido o no autorizado: {badge} en puerta {door}",
                "metadata": {"badge_id": badge, "door": door, "timestamp": ts}
            }
            latency = time.time() - start_time
            add_event("access", result, latency)
            return result

        if result is None:
            EVENT_COUNTER.labels(sensor_type="access").inc()
            latency = time.time() - start_time
            EVENT_LATENCY.labels(sensor_type="access").observe(latency)

            result = {
                "alert": False,
                "message": "Acceso autorizado",
                "metadata": {"badge_id": badge, "door": door, "timestamp": ts}
            }
            add_event("access", result, latency)
            return result

        latency = time.time() - start_time
        add_event("access", result, latency)
        
        await alerting.dispatch_alert(result) 
        
        return result
