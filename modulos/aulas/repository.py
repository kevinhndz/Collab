from sqlalchemy.orm import Session

from modulos.aulas.tablas import Aula


def obtener_todos(db: Session) -> list[Aula]:
    return db.query(Aula).all()
