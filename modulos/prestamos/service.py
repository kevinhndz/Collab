from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from modulos.prestamos.schema import PrestamoActualizar
from modulos.usuarios import repository as usuarios_repository
from modulos.libros import repository as libros_repository

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


def actualizar_prestamo(db: Session, prestamo_id: int, json: PrestamoActualizar):
    prestamo = repository.obtener_por_id(db, prestamo_id)
    if prestamo is None:
        raise HTTPException(status_code=404, detail="Prestamo no encontrado.")

    datos = json.model_dump(exclude_unset=True)
    usuario_id = datos.get("usuario_id", prestamo.usuario_id)
    libro_id = datos.get("libro_id", prestamo.libro_id)

    if usuarios_repository.obtener_por_id(db, usuario_id) is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    if libros_repository.obtener_por_id(db, libro_id) is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado.")

    combinacion = PrestamoCrear(usuario_id=usuario_id, libro_id=libro_id)
    look_up = repository.validar(db, combinacion)
    if look_up is not None and look_up.id != prestamo_id:
        raise HTTPException(status_code=409, detail="El prestamo ya existe.")

    prestamo.usuario_id = usuario_id
    prestamo.libro_id = libro_id
    return repository.actualizar(db, prestamo)