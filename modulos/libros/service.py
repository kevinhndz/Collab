from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from modulos.libros import repository
from modulos.libros.schema import LibroActualizar, LibroCrear
from modulos.libros.tablas import Libro


def crear_libro(db: Session, json: LibroCrear):
    look_up = repository.validar(db, json)
    if look_up is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un libro con ese titulo.",
        )
    libro = Libro(titulo=json.titulo, autor=json.autor)
    return repository.crear(db, libro)


def obtener_libros(db: Session):
    return repository.obtener_todos(db)


def obtener_libro(db: Session, libro_id: int):
    libro = repository.obtener_por_id(db, libro_id)
    if libro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Libro no encontrado.",
        )
    return libro


def eliminar_libro(db: Session, libro_id: int):
    libro = repository.obtener_por_id(db, libro_id)
    if libro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Libro no encontrado.",
        )
    repository.eliminar(db, libro)


def actualizar_libro(db: Session, libro_id: int, json: LibroActualizar):
    libro = obtener_libro(db, libro_id)
    datos = json.model_dump(exclude_unset=True)
    if "titulo" in datos:
        look_up = repository.validar(db, json)
        if look_up is not None and look_up.id != libro_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un libro con ese titulo.",
            )
    for campo, valor in datos.items():
        setattr(libro, campo, valor)
    return repository.actualizar(db, libro)
