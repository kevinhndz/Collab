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


def test_actualizar_prestamo_patch():
    cliente = TestClient(app)
    usuario = cliente.post(
        "/usuarios/",
        json={"nombre": "Ana Prueba", "email": f"{uuid4()}@example.com"},
    )
    assert usuario.status_code == 201
    usuario_id = usuario.json()["id"]

    libro = cliente.post(
        "/libros/", json={"titulo": f"Original {uuid4()}", "autor": "Autor"}
    )
    nuevo = cliente.post(
        "/libros/", json={"titulo": f"Nuevo {uuid4()}", "autor": "Autor"}
    )
    assert libro.status_code == 201
    assert nuevo.status_code == 201

    prestamo = cliente.post(
        "/prestamos/",
        json={"usuario_id": usuario_id, "libro_id": libro.json()["id"]},
    )
    assert prestamo.status_code == 201
    prestamo_id = prestamo.json()["id"]

    respuesta = cliente.patch(
        f"/prestamos/{prestamo_id}", json={"libro_id": nuevo.json()["id"]}
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["libro_id"] == nuevo.json()["id"]
    assert respuesta.json()["usuario_id"] == usuario_id
    guardado = cliente.patch(f"/prestamos/{prestamo_id}", json={})
    assert guardado.status_code == 200
    assert guardado.json() == respuesta.json()


def test_obtener_prestamos():
    cliente = TestClient(app)
    respuesta = cliente.get("/prestamos/")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)

