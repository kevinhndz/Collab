from fastapi import APIRouter, Depends, HTTPException  # HTTPException lo usan las tareas de GET y DELETE
from sqlalchemy.orm import Session

from database.almacen import get_db
from modulos.prestamos import service
from modulos.prestamos.schema import PrestamoCrear, PrestamoRespuesta

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])


@router.post("/", response_model=PrestamoRespuesta, status_code=201)
def crear_prestamo(json: PrestamoCrear, db: Session = Depends(get_db)):
    return service.crear_prestamo(db, json)
