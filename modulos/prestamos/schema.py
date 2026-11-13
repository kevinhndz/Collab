from pydantic import BaseModel, ConfigDict, Field


class PrestamoCrear(BaseModel):
    usuario_id: int = Field(..., gt=0)
    libro_id: int = Field(..., gt=0)


class PrestamoRespuesta(PrestamoCrear):
    id: int
    model_config = ConfigDict(from_attributes=True)
