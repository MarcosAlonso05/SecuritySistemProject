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


@pytest.fixture(autouse=True)
def mock_external_services(mocker):
    
    mocker.patch("app.services.sensors.access_sensor.add_event", return_value=None)
    mocker.patch("app.services.sensors.access_sensor.EVENT_COUNTER", MagicMock())
    mocker.patch("app.services.sensors.access_sensor.EVENT_LATENCY", MagicMock())
    
    mocker.patch("app.services.sensors.motion_sensor.add_event", return_value=None)
    mocker.patch("app.services.sensors.motion_sensor.EVENT_COUNTER", MagicMock())
    mocker.patch("app.services.sensors.motion_sensor.EVENT_LATENCY", MagicMock())

    mocker.patch("app.services.sensors.temperature_sensor.add_event", return_value=None)
    mocker.patch("app.services.sensors.temperature_sensor.EVENT_COUNTER", MagicMock())
    mocker.patch("app.services.sensors.temperature_sensor.EVENT_LATENCY", MagicMock())

def test_access_sensor_authorized():
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

def test_motion_sensor_authorized_movement():
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


def test_temperature_sensor_normal():
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
