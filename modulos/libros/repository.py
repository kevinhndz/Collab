from sqlalchemy.orm import Session

from modulos.libros.schema import LibroCrear
from modulos.libros.tablas import Libro


def crear(db: Session, libro: Libro) -> Libro:
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro


def validar(db: Session, json: LibroCrear) -> Libro | None:
    return db.query(Libro).filter(Libro.titulo == json.titulo).first()
