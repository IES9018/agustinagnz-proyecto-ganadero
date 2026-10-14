from src.repositories.trazabilidad_repository import (
    TrazabilidadRepository
)


class TrazabilidadService:

    def __init__(self, db):
        self.repo = TrazabilidadRepository(db)

    def listar_por_animal(self, animal_id: int):
        resultado = self.repo.listar_por_animal(animal_id)

        if resultado is None:
            raise LookupError("Animal no encontrado.")

        return resultado
