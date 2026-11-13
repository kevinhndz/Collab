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
