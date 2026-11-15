from pydantic import BaseModel, ConfigDict, Field


class AulaCrear(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    capacidad: int = Field(..., gt=0)


class AulaRespuesta(AulaCrear):
    id: int
    model_config = ConfigDict(from_attributes=True)
