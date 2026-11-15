from fastapi.testclient import TestClient
from uuid import uuid4

from main import app


def test_crear_prestamo():
    cliente = TestClient(app)
    email = f"{uuid4()}@example.com"
    titulo = f"Libro prestado {uuid4()}"

    respuesta_usuario = cliente.post(
        "/usuarios/",
        json={"nombre": "Luis Prueba", "email": email},
    )
    usuario_id = respuesta_usuario.json()["id"]

    respuesta_libro = cliente.post(
        "/libros/",
        json={"titulo": titulo, "autor": "Autor de prueba"},
    )
    libro_id = respuesta_libro.json()["id"]

    respuesta = cliente.post(
        "/prestamos/",
        json={"usuario_id": usuario_id, "libro_id": libro_id},
    )

    assert respuesta.status_code == 201


def test_obtener_prestamos():
    cliente = TestClient(app)
    respuesta = cliente.get("/prestamos/")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)
