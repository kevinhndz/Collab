from fastapi import APIRouter, Depends, HTTPException  
from sqlalchemy.orm import Session

from database.almacen import get_db
from modulos.libros import service
from modulos.libros.schema import LibroCrear, LibroRespuesta

router = APIRouter(prefix="/libros", tags=["Libros"])


@router.post("/", response_model=LibroRespuesta, status_code=201)
def crear_libro(json: LibroCrear, db: Session = Depends(get_db)):
    return service.crear_libro(db, json)


@router.delete("/{libro_id}", status_code=204)
def eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    service.eliminar_libro(db, libro_id)