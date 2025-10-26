from typing import Dict, Any, Iterable
import asyncio
from datetime import datetime

class AccessSensor:

    async def process_event(self, data: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0)

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

        return {
            "alert": False,
            "message": "Acceso autorizado",
            "metadata": {"badge_id": badge, "door": door, "timestamp": ts}
        }
