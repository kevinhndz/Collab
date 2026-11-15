from fastapi.testclient import TestClient
from uuid import uuid4

from main import app


def test_crear_usuario():
    cliente = TestClient(app)
    email = f"{uuid4()}@example.com"

    respuesta = cliente.post(
        "/usuarios/",
        json={"nombre": "Ana Prueba", "email": email},
    )

    assert respuesta.status_code == 201
