from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from modulos.prestamos import repository
from modulos.prestamos.schema import PrestamoCrear
from modulos.prestamos.tablas import Prestamo


def crear_prestamo(db: Session, json: PrestamoCrear):
    look_up = repository.validar(db, json)
    if look_up is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un prestamo con ese usuario y ese libro.",
        )
    prestamo = Prestamo(usuario_id=json.usuario_id, libro_id=json.libro_id)
    return repository.crear(db, prestamo)


def eliminar_prestamo(db: Session, prestamo_id: int):
    prestamo = repository.obtener_por_id(db, prestamo_id)
    if prestamo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prestamo no encontrado.",
        )
    repository.eliminar(db, prestamo)


def obtener_prestamos(db: Session):
    return repository.obtener_todos(db)
