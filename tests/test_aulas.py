from contextlib import contextmanager

from fastapi.testclient import TestClient

from database.almacen import get_db
from main import app
from modulos.aulas.tablas import Aula


def test_obtener_aulas_vacio():
    cliente = TestClient(app)
    respuesta = cliente.get("/aulas/")
    assert respuesta.status_code == 200
    assert respuesta.json() == []


def test_obtener_aulas_guardadas():
    obtener_db = app.dependency_overrides[get_db]
    with contextmanager(obtener_db)() as db:
        aula = Aula(nombre="Aula 101", capacidad=30)
        db.add(aula)
        db.commit()
        db.refresh(aula)
        aula_id = aula.id

    cliente = TestClient(app)
    respuesta = cliente.get("/aulas/")
    assert respuesta.status_code == 200
    assert respuesta.json() == [
        {"id": aula_id, "nombre": "Aula 101", "capacidad": 30}
    ]
