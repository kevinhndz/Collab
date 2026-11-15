from sqlalchemy.orm import Session

from modulos.aulas import repository


def obtener_aulas(db: Session):
    return repository.obtener_todos(db)
