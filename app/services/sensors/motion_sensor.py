import asyncio
import time
from typing import Dict, Any
from datetime import datetime
from app.services.monitoring.metrics import EVENT_COUNTER, EVENT_LATENCY

class MotionSensor:

    async def process_event(self, data: Dict[str, Any]) -> Dict[str, Any]:
        
        start_time = time.time()
        
        await asyncio.sleep(0.5) 

        movement = bool(data.get("movement", False))
        zone = data.get("zone", "unknown")
        authorized = data.get("authorized")
        ts = data.get("timestamp") or datetime.utcnow().isoformat()

        if not movement:
            return {"alert": False, "message": "No hay movimiento", "metadata": {"zone": zone, "timestamp": ts}}

        if authorized is False:
            return {
                "alert": True,
                "severity": "high",
                "message": f"Movimiento no autorizado en zona {zone}",
                "metadata": {"timestamp": ts, "zone": zone}
            }
            
        EVENT_COUNTER.labels(sensor_type="motion").inc()
        EVENT_LATENCY.labels(sensor_type="motion").observe(time.time() - start_time)

        return {
            "alert": True,
            "severity": "medium",
            "message": f"Movimiento detectado en zona {zone}",
            "metadata": {"timestamp": ts, "zone": zone}
        }
