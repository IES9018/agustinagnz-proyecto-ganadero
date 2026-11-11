from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AnimalInput(BaseModel):
    identificador: str = Field(min_length=1, max_length=100)
    especie: str = Field(min_length=1, max_length=100)
    sexo: str = Field(min_length=1, max_length=100)
    raza: str = Field(min_length=1, max_length=100)
    fecha_nacimiento: date
    estado_sanitario: str = Field(min_length=1, max_length=100)
    id_establecimiento: int = Field(ge=1)

    @field_validator(
        "identificador",
        "especie",
        "sexo",
        "raza",
        "estado_sanitario"
    )
    @classmethod
    def validar_texto(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("El campo no puede estar vacío.")

        return value


class AnimalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_animal: int
    identificador: str
    especie: str
    sexo: str
    raza: str
    fecha_nacimiento: date | None
    estado_sanitario: str
    id_establecimiento: int