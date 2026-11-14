from fastapi.testclient import TestClient
from uuid import uuid4

from main import app


def test_crear_libro():
    cliente = TestClient(app)
    titulo = f"Libro de prueba {uuid4()}"

    respuesta = cliente.post(
        "/libros/",
        json={"titulo": titulo, "autor": "Antoine de Saint-Exupéry"},
    )

    assert respuesta.status_code == 201


def test_ver_lista_de_libros():
    cliente = TestClient(app)

    respuesta = cliente.get("/libros/")

    assert respuesta.status_code == 200


def test_ver_un_libro():
    cliente = TestClient(app)
    titulo = f"Libro para buscar {uuid4()}"

    respuesta_crear = cliente.post(
        "/libros/",
        json={"titulo": titulo, "autor": "Autor de prueba"},
    )
    libro_id = respuesta_crear.json()["id"]

    respuesta = cliente.get(f"/libros/{libro_id}")

    assert respuesta.status_code == 200


def test_borrar_libro():
    cliente = TestClient(app)

    respuesta = cliente.post(
        "/libros/",
        json={"titulo": "Libro para borrar", "autor": "Autor de prueba"},
    )
    libro_id = respuesta.json()["id"]

    respuesta = cliente.delete(f"/libros/{libro_id}")

    assert respuesta.status_code == 204

    respuesta = cliente.get(f"/libros/{libro_id}")

    assert respuesta.status_code == 404


def test_crear_usuario():
    cliente = TestClient(app)
    email = f"{uuid4()}@example.com"

    respuesta = cliente.post(
        "/usuarios/",
        json={"nombre": "Ana Prueba", "email": email},
    )

    assert respuesta.status_code == 201


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
