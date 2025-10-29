import asyncio
from collections import deque
from typing import Dict, Any, List
import time

MAX_RECENT_ALERTS = 50
ALERT_ROLES = ["admin", "operator"] 

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_SENDER = "tu-email-de-alertas@gmail.com"
EMAIL_PASSWORD = "tu-password-de-aplicacion"
EMAIL_RECEIVER = "tu-email-de-admin@dominio.com"

alert_queue = asyncio.Queue()
RECENT_ALERTS = deque(maxlen=MAX_RECENT_ALERTS)

def send_alert_email_sync(message: str, metadata: Dict[str, Any]):
    subject = f"ALERTA DE SEGURIDAD CRÍTICA: {message}"
    body = f"""
    (SIMULACIÓN) Email enviado a {EMAIL_RECEIVER}:
    Asunto: {subject}
    Cuerpo:
    Se ha detectado una nueva alerta crítica en el sistema de monitoreo.
    Mensaje: {message}
    Metadatos: {str(metadata)}
    """

    try:
        print(f"[Debug Email] SIMULANDO conexión a {SMTP_SERVER}:{SMTP_PORT}...")
        
        time.sleep(2) 
        
        print(f"[Debug Email] SIMULACIÓN de email enviado a {EMAIL_RECEIVER}:")
        print(body)
        print("[Debug Email] SIMULACIÓN Conexión cerrada.")
        
    except Exception as e:
        print(f"[Debug Email] ERROR durante la simulación de email: {e}")
        raise

async def alert_consumer_task():
    print("[AlertService] Iniciando consumidor de alertas en segundo plano...")
    while True:
        try:
            alert = await alert_queue.get()
            
            print(f"[AlertService] Procesando alerta: {alert.get('message')}")
            
            if alert.get("severity") == "high":
                print(f"[AlertService] Alerta 'high' detectada. Intentando enviar email...")
                try:
                    await asyncio.to_thread(
                        send_alert_email_sync,
                        alert.get('message'),
                        alert.get('metadata', {})
                    )
                    print(f"[AlertService] Email enviado exitosamente por: {alert.get('message')}")
                except Exception as e:
                    print(f"[AlertService] ERROR al enviar email: {e}")

            alert_queue.task_done()
            
        except asyncio.CancelledError:
            print("[AlertService] Tarea de consumidor cancelada.")
            break
        except Exception as e:
            print(f"[AlertService] Error procesando alerta: {e}")
            alert_queue.task_done()

async def dispatch_alert(event: Dict[str, Any]):
    if event.get("alert") == True and event.get("severity") == "high":
        RECENT_ALERTS.appendleft(event) 
        
        await alert_queue.put(event)

def get_recent_alerts(limit: int = 20) -> List[Dict[str, Any]]:
    return list(RECENT_ALERTS)[:limit]

def get_alert_roles() -> List[str]:
    return ALERT_ROLES
