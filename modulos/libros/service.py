from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from modulos.libros import repository
from modulos.libros.schema import LibroCrear
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
