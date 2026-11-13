from fastapi import APIRouter, Depends, HTTPException  # HTTPException lo usan las tareas de GET y DELETE
from sqlalchemy.orm import Session

from database.almacen import get_db
from modulos.usuarios import service
from modulos.usuarios.schema import UsuarioCrear, UsuarioRespuesta

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioRespuesta, status_code=201)
def crear_usuario(json: UsuarioCrear, db: Session = Depends(get_db)):
    return service.crear_usuario(db, json)
