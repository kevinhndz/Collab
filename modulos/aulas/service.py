from fastapi import HTTPException
from sqlalchemy.orm import Session

from modulos.aulas import repository
from modulos.aulas.schema import AulaActualizar, AulaCrear


def obtener_aulas(db: Session):
    return repository.obtener_todos(db)


def reemplazar_aula(db: Session, aula_id: int, datos: AulaCrear):
    aula = repository.obtener_por_id(db, aula_id)
    if aula is None:
        raise HTTPException(status_code=404, detail="Aula no encontrada.")
    aula.nombre = datos.nombre
    aula.capacidad = datos.capacidad
    return repository.actualizar(db, aula)


def actualizar_aula(db: Session, aula_id: int, datos: AulaActualizar):
    aula = repository.obtener_por_id(db, aula_id)

    if aula is None:
        raise HTTPException(status_code=404, detail="Aula no encontrada.")

    if datos.nombre is not None:
        aula.nombre = datos.nombre

    if datos.capacidad is not None:
        aula.capacidad = datos.capacidad

    return repository.actualizar(db, aula)
