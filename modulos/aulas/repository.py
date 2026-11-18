from sqlalchemy.orm import Session

from modulos.aulas.tablas import Aula


def obtener_todos(db: Session) -> list[Aula]:
    return db.query(Aula).all()


def obtener_por_id(db: Session, aula_id: int) -> Aula | None:
    return db.query(Aula).filter(Aula.id == aula_id).first()


def actualizar(db: Session, aula: Aula) -> Aula:
    db.commit()
    db.refresh(aula)
    return aula


