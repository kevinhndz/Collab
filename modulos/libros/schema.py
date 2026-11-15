from pydantic import BaseModel, ConfigDict, Field, field_validator


class LibroCrear(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=255)
    autor: str = Field(..., min_length=1, max_length=255)


class LibroRespuesta(LibroCrear):
    id: int
    model_config = ConfigDict(from_attributes=True)


class LibroActualizar(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=255)
    autor: str | None = Field(default=None, min_length=1, max_length=255)

    @field_validator("titulo", "autor")
    @classmethod
    def validar_campo(cls, valor):
        if valor is None:
            raise ValueError("El campo no puede ser nulo.")
        return valor
