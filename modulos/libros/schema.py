from pydantic import BaseModel, ConfigDict, Field


class LibroCrear(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=255)
    autor: str = Field(..., min_length=1, max_length=255)


class LibroRespuesta(LibroCrear):
    id: int
    model_config = ConfigDict(from_attributes=True)
