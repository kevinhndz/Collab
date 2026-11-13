from sqlalchemy.orm import Session

from modulos.usuarios.schema import UsuarioCrear
from modulos.usuarios.tablas import Usuario


def crear(db: Session, usuario: Usuario) -> Usuario:
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def validar(db: Session, json: UsuarioCrear) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == json.email).first()
