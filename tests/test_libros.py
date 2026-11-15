from fastapi.testclient import TestClient
from uuid import uuid4
import pytest

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
    titulo = f"Libro para borrar {uuid4()}"

    respuesta = cliente.post(
        "/libros/",
        json={"titulo": titulo, "autor": "Autor de prueba"},
    )
    libro_id = respuesta.json()["id"]

    respuesta = cliente.delete(f"/libros/{libro_id}")

    assert respuesta.status_code == 204

    respuesta = cliente.get(f"/libros/{libro_id}")

    assert respuesta.status_code == 404


def test_reemplazar_libro_put():
    cliente = TestClient(app)
    creado = cliente.post(
        "/libros/",
        json={"titulo": "Libro PUT", "autor": "Autor"},
    )
    libro_id = creado.json()["id"]
    respuesta = cliente.put(
        f"/libros/{libro_id}",
        json={"titulo": "Libro cambiado", "autor": "Autor cambiado"},
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["titulo"] == "Libro cambiado"
    assert respuesta.json()["autor"] == "Autor cambiado"
    assert cliente.get(f"/libros/{libro_id}").json()["autor"] == "Autor cambiado"


def test_actualizar_libro_patch():
    cliente = TestClient(app)
    creado = cliente.post(
        "/libros/", json={"titulo": "Libro PATCH", "autor": "Autor original"}
    )
    assert creado.status_code == 201
    libro_id = creado.json()["id"]
    respuesta = cliente.patch(f"/libros/{libro_id}", json={"autor": "Autor nuevo"})
    assert respuesta.status_code == 200
    assert respuesta.json()["titulo"] == "Libro PATCH"
    assert respuesta.json()["autor"] == "Autor nuevo"
    assert cliente.get(f"/libros/{libro_id}").json()["autor"] == "Autor nuevo"


def test_patch_libro_inexistente():
    cliente = TestClient(app)
    assert cliente.patch("/libros/999999", json={"autor": "Otro"}).status_code == 404


@pytest.mark.parametrize("datos", [{"titulo": None}, {"autor": None}, {"titulo": ""}])
def test_patch_libro_datos_invalidos(datos):
    cliente = TestClient(app)
    assert cliente.patch("/libros/1", json=datos).status_code == 422


def test_patch_libro_titulo_duplicado():
    cliente = TestClient(app)
    cliente.post("/libros/", json={"titulo": "Ocupado", "autor": "Autor"})
    creado = cliente.post("/libros/", json={"titulo": "Otro", "autor": "Autor"})
    libro_id = creado.json()["id"]
    respuesta = cliente.patch(f"/libros/{libro_id}", json={"titulo": "Ocupado"})
    assert respuesta.status_code == 409
    assert cliente.get(f"/libros/{libro_id}").json()["titulo"] == "Otro"


def test_put_libro_inexistente():
    cliente = TestClient(app)
    respuesta = cliente.put("/libros/999999", json={"titulo": "Nuevo", "autor": "Autor"})
    assert respuesta.status_code == 404


def test_put_libro_requiere_todos_los_campos():
    cliente = TestClient(app)
    assert cliente.put("/libros/1", json={"autor": "Otro"}).status_code == 422


def test_put_libro_titulo_duplicado():
    cliente = TestClient(app)
    cliente.post("/libros/", json={"titulo": "Ocupado", "autor": "Autor"})
    creado = cliente.post("/libros/", json={"titulo": "Otro", "autor": "Autor"})
    libro_id = creado.json()["id"]
    respuesta = cliente.put(
        f"/libros/{libro_id}", json={"titulo": "Ocupado", "autor": "Reemplazo"}
    )
    assert respuesta.status_code == 409
    assert cliente.get(f"/libros/{libro_id}").json()["titulo"] == "Otro"
