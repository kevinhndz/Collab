from fastapi import APIRouter, Depends, HTTPException  # HTTPException lo usan las tareas de GET y DELETE
from sqlalchemy.orm import Session
from modulos.prestamos.schema import PrestamoActualizar


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


@router.patch("/{prestamo_id}", response_model=PrestamoRespuesta)
def actualizar_prestamo(
    prestamo_id: int,
    json: PrestamoActualizar,
    db: Session = Depends(get_db),
):
    return service.actualizar_prestamo(db, prestamo_id, json)