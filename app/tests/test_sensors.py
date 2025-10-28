import pytest
import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

try:
    from app.main import app
except ImportError:
    raise ImportError("No se pudo importar 'app.main'. Asegúrate de que 'app/main.py' existe y que la estructura de tu proyecto es correcta.")

client = TestClient(app)


# --- Mock de Dependencias ---
@pytest.fixture(autouse=True)
def mock_external_services(mocker):
    """
    Fixture de Pytest que automáticamente "mockea" (simula) las dependencias
    externas (métricas y store) antes de cada test.
    Esto evita que los tests intenten conectarse a servicios reales.
    """
    
    # Mock de los servicios para AccessSensor
    mocker.patch("app.services.sensors.access_sensor.add_event", return_value=None)
    mocker.patch("app.services.sensors.access_sensor.EVENT_COUNTER", MagicMock())
    mocker.patch("app.services.sensors.access_sensor.EVENT_LATENCY", MagicMock())
    
    # Mock de los servicios para MotionSensor
    mocker.patch("app.services.sensors.motion_sensor.add_event", return_value=None)
    mocker.patch("app.services.sensors.motion_sensor.EVENT_COUNTER", MagicMock())
    mocker.patch("app.services.sensors.motion_sensor.EVENT_LATENCY", MagicMock())

    # Mock de los servicios para TemperatureSensor
    mocker.patch("app.services.sensors.temperature_sensor.add_event", return_value=None)
    mocker.patch("app.services.sensors.temperature_sensor.EVENT_COUNTER", MagicMock())
    mocker.patch("app.services.sensors.temperature_sensor.EVENT_LATENCY", MagicMock())


# --- Tests para Access Sensor ---

def test_access_sensor_authorized():
    """
    Prueba un evento de acceso autorizado.
    El badge "ID001" está hardcodeado como autorizado en tu router.
    """
    payload = {
        "badge_id": "ID001",
        "door": "Entrada Principal"
    }
    response = client.post("/sensor/access", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["alert"] is False
    assert data["message"] == "Acceso autorizado"
    assert data["metadata"]["badge_id"] == "ID001"

def test_access_sensor_unauthorized():
    """
    Prueba un evento de acceso no autorizado con un badge desconocido.
    """
    payload = {
        "badge_id": "ID999",
        "door": "Sala de Servidores"
    }
    response = client.post("/sensor/access", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["alert"] is True
    assert data["severity"] == "high"
    assert "Badge desconocido o no autorizado" in data["message"]
    assert data["metadata"]["badge_id"] == "ID999"

# --- Tests para Motion Sensor ---

def test_motion_sensor_authorized_movement():
    """
    Prueba un evento de movimiento detectado que está autorizado.
    Debería generar una alerta de severidad "medium".
    """
    payload = {
        "movement": True,
        "zone": "Lobby",
        "authorized": True
    }
    response = client.post("/sensor/motion", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["alert"] is True
    assert data["severity"] == "medium"
    assert "Movimiento detectado" in data["message"]

def test_motion_sensor_unauthorized_movement():
    """
    Prueba un evento de movimiento detectado que NO está autorizado.
    Debería generar una alerta de severidad "high".
    """
    payload = {
        "movement": True,
        "zone": "Área Restringida",
        "authorized": False
    }
    response = client.post("/sensor/motion", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["alert"] is True
    assert data["severity"] == "high"
    assert "Movimiento no autorizado" in data["message"]

# --- Tests para Temperature Sensor ---

def test_temperature_sensor_normal():
    """
    Prueba un evento de temperatura normal.
    El rango normal está hardcodeado entre 0 y 35 en tu router.
    """
    payload = {
        "temperature": 24.5,
        "unit": "C",
        "sensor_id": "SENSOR-SALA-01"
    }
    response = client.post("/sensor/temperature", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["alert"] is False
    assert data["message"] == "Temperatura normal"
    assert data["metadata"]["temperature_c"] == 24.5

def test_temperature_sensor_high_alert():
    """
    Prueba un evento de temperatura alta que dispara una alerta.
    """
    payload = {
        "temperature": 40.0,
        "unit": "C",
        "sensor_id": "SENSOR-SALA-02"
    }
    response = client.post("/sensor/temperature", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["alert"] is True
    assert data["severity"] == "high"
    assert "Temperatura extremadamente alta" in data["message"]
    assert data["metadata"]["temperature_c"] == 40.0
