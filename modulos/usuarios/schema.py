from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UsuarioCrear(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=255)
    email: EmailStr


class UsuarioRespuesta(UsuarioCrear):
    id: int
    model_config = ConfigDict(from_attributes=True)
