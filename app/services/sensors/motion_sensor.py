from typing import Dict, Any
import asyncio
from datetime import datetime

class MotionSensor:

    async def process_event(self, data: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0) 

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

        return {
            "alert": True,
            "severity": "medium",
            "message": f"Movimiento detectado en zona {zone}",
            "metadata": {"timestamp": ts, "zone": zone}
        }
