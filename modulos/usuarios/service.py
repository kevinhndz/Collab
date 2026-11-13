from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from modulos.usuarios import repository
from modulos.usuarios.schema import UsuarioCrear
from modulos.usuarios.tablas import Usuario


def crear_usuario(db: Session, json: UsuarioCrear):
    look_up = repository.validar(db, json)
    if look_up is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese correo electronico.",
        )
    usuario = Usuario(nombre=json.nombre, email=json.email)
    return repository.crear(db, usuario)
