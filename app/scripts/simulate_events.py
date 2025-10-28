import asyncio
import httpx
import random
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"


events_to_send = [
    {
        "name": "Acceso: Autorizado (ID001)",
        "url": "/sensor/access",
        "payload": {"badge_id": "ID001", "door": "Entrada Principal"}
    },
    {
        "name": "Acceso: No Autorizado (ID999)",
        "url": "/sensor/access",
        "payload": {"badge_id": "ID999", "door": "Sala de Servidores", "timestamp": datetime.utcnow().isoformat()}
    },
    {
        "name": "Acceso: Alerta (Sin Badge)",
        "url": "/sensor/access",
        "payload": {"badge_id": None, "door": "Puerta Trasera"}
    },
    {
        "name": "Acceso: Alerta (Forzado)",
        "url": "/sensor/access",
        "payload": {"unauthorized_access": True, "door": "Ventana Oficina"}
    },
    
    {
        "name": "Movimiento: Alerta (No Autorizado)",
        "url": "/sensor/motion",
        "payload": {"movement": True, "zone": "Área Restringida", "authorized": False}
    },
    {
        "name": "Movimiento: Normal (Autorizado)",
        "url": "/sensor/motion",
        "payload": {"movement": True, "zone": "Lobby", "authorized": True, "timestamp": datetime.utcnow().isoformat()}
    },
    {
        "name": "Movimiento: Normal (Sin Movimiento)",
        "url": "/sensor/motion",
        "payload": {"movement": False, "zone": "Pasillo 1"}
    },

    {
        "name": "Temp: Alerta (MUY ALTA)",
        "url": "/sensor/temperature",
        "payload": {"temperature": 41.5, "unit": "C", "sensor_id": "SENSOR-SALA-01"}
    },
    {
        "name": "Temp: Alerta (MUY BAJA)",
        "url": "/sensor/temperature",
        "payload": {"temperature": -5.0, "unit": "C", "sensor_id": "SENSOR-CONGELADOR"}
    },
    {
        "name": "Temp: Normal (Oficina)",
        "url": "/sensor/temperature",
        "payload": {"temperature": 22.0, "unit": "C", "sensor_id": "SENSOR-OFICINA", "timestamp": datetime.utcnow().isoformat()}
    },
    {
        "name": "Temp: Normal (Fahrenheit)",
        "url": "/sensor/temperature",
        "payload": {"temperature": 85.0, "unit": "F", "sensor_id": "SENSOR-SALA-EEUU"} # Se convertirá a ~29.4C
    }
]

async def send_request(client: httpx.AsyncClient, event_data: dict):
    url = f"{BASE_URL}{event_data['url']}"
    payload = event_data['payload']
    name = event_data['name']
    
    try:
        await asyncio.sleep(random.uniform(0.1, 0.3))
        
        response = await client.post(url, json=payload)
        response.raise_for_status()
        
        print(f"  > ÉXITO [{name}]: {response.json().get('message')}")
        return response.json()
        
    except httpx.HTTPStatusError as e:
        print(f"  > ERROR de HTTP [{name}]: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"  > ERROR de Conexión [{name}]: {e}")
    except Exception as e:
        print(f"  > ERROR Inesperado [{name}]: {e}")

def show_menu():
    print("\n--- Simulador Interactivo de Eventos ---")
    print("Elige un evento para lanzar:")
    for i, event in enumerate(events_to_send):
        print(f"  {i+1}. {event['name']}")
    print("-" * 40)
    print("  a. Lanzar TODOS los eventos (concurrente)")
    print("  q. Salir")

async def run_all_events(client: httpx.AsyncClient):
    print(f"\nLanzando {len(events_to_send)} eventos concurrentemente...")
    
    tasks = []
    for event_data in events_to_send:
        tasks.append(send_request(client, event_data))
    
    results = await asyncio.gather(*tasks)
    
    alerts = [r for r in results if r and r.get('alert')]
    print("\n--- Simulación Completa ---")
    print(f"Total de peticiones enviadas: {len(tasks)}")
    print(f"Total de alertas generadas: {len(alerts)}")

async def main():
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        
        while True:
            show_menu()
            choice = input("Opción: ").strip().lower()

            if choice == 'q':
                print("Saliendo...")
                break
            
            if choice == 'a':
                await run_all_events(client)
                continue

            try:
                event_index = int(choice) - 1
                
                if 0 <= event_index < len(events_to_send):
                    event_to_run = events_to_send[event_index]
                    print(f"\nLanzando evento: {event_to_run['name']}...")
                    await send_request(client, event_to_run)
                else:
                    print(f"Error: El número debe estar entre 1 y {len(events_to_send)}.")
            
            except ValueError:
                print(f"Error: Opción '{choice}' no reconocida. Inténtalo de nuevo.")
            except Exception as e:
                print(f"Error inesperado en el bucle principal: {e}")

if __name__ == "__main__":
    
    print(f"Conectando al servidor en {BASE_URL}...")
    print("Asegúrate de que tu servidor FastAPI (uvicorn) esté funcionando.")
    asyncio.run(main())