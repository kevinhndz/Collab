from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.almacen import get_db
from modulos.aulas import service
from modulos.aulas.schema import AulaRespuesta

router = APIRouter(prefix="/aulas", tags=["Aulas"])


@router.get("/", response_model=list[AulaRespuesta])
def listar_aulas(db: Session = Depends(get_db)):
    return service.obtener_aulas(db)


@router.patch("/{aula_id}", response_model=AulaRespuesta)
def actualizar_aula(
    aula_id: int,
    datos: AulaActualizar,
    db: Session = Depends(get_db),
):
    return service.actualizar_aula(db, aula_id, datos)
