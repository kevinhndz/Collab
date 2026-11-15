from fastapi import APIRouter, Depends, HTTPException  # HTTPException lo usan las tareas de GET y DELETE
from sqlalchemy.orm import Session

from database.almacen import get_db
from modulos.prestamos import service
from modulos.prestamos.schema import PrestamoCrear, PrestamoRespuesta

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])


@router.post("/", response_model=PrestamoRespuesta, status_code=201)
def crear_prestamo(json: PrestamoCrear, db: Session = Depends(get_db)):
    return service.crear_prestamo(db, json)


@router.delete("/{prestamo_id}", status_code=204)
def eliminar_prestamo(prestamo_id: int, db: Session = Depends(get_db)):
    service.eliminar_prestamo(db, prestamo_id)


@router.get("/", response_model=list[PrestamoRespuesta])
def listar_prestamos(db: Session = Depends(get_db)):
    return service.obtener_prestamos(db)



