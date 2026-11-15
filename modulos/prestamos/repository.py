from sqlalchemy.orm import Session

from modulos.prestamos.schema import PrestamoCrear
from modulos.prestamos.tablas import Prestamo


def crear(db: Session, prestamo: Prestamo) -> Prestamo:
    db.add(prestamo)
    db.commit()
    db.refresh(prestamo)
    return prestamo


def validar(db: Session, json: PrestamoCrear) -> Prestamo | None:
    return (
        db.query(Prestamo)
        .filter(
            Prestamo.usuario_id == json.usuario_id,
            Prestamo.libro_id == json.libro_id,
        )
        .first()
    )


def obtener_por_id(db: Session, prestamo_id: int) -> Prestamo | None:
    return db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()


def eliminar(db: Session, prestamo: Prestamo) -> None:
    db.delete(prestamo)
    db.commit()


def actualizar(db: Session, prestamo: Prestamo) -> Prestamo:
    db.commit()
    db.refresh(prestamo)
    return prestamo