from pydantic import BaseModel, ConfigDict, Field
from pydantic import field_validator



class PrestamoCrear(BaseModel):
    usuario_id: int = Field(..., gt=0)
    libro_id: int = Field(..., gt=0)


class PrestamoRespuesta(PrestamoCrear):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PrestamoActualizar(BaseModel):
    usuario_id: int | None = Field(default=None, gt=0)
    libro_id: int | None = Field(default=None, gt=0)

    @field_validator("usuario_id", "libro_id")
    @classmethod
    def validar_campo(cls, valor):
        if valor is None:
            raise ValueError("El campo no puede ser nulo.")
        return valor