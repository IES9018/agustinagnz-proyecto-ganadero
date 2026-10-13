from datetime import date

from src.models.animal import Animal
from src.repositories.sanidad_repository import SanidadRepository


class SanidadService:
    def __init__(self, db):
        self.db = db
        self.repo = SanidadRepository(db)

    def crear_evento(self, animal_id: int, data: dict):
        animal = self.db.get(Animal, animal_id)

        if animal is None:
            raise LookupError("Animal no encontrado.")

        for campo in ("tipo_evento", "descripcion", "fecha"):
            valor = data.get(campo)

            if valor is None or not str(valor).strip():
                raise ValueError(
                    f"El campo '{campo}' es obligatorio."
                )

        try:
            fecha_evento = date.fromisoformat(str(data["fecha"]))
        except ValueError:
            raise ValueError(
                "La fecha del evento no tiene un formato válido."
            )

        if fecha_evento > date.today():
            raise ValueError(
                "La fecha del evento no puede ser futura."
            )

        datos = {
            "tipo_evento": str(data["tipo_evento"]).strip(),
            "descripcion": str(data["descripcion"]).strip(),
            "fecha": fecha_evento
        }

        return self.repo.crear_evento(animal_id, datos)

    def listar_eventos(self, animal_id: int):
        animal = self.db.get(Animal, animal_id)

        if animal is None:
            raise LookupError("Animal no encontrado.")

        return self.repo.listar_por_animal(animal_id)

    def eliminar_evento(
        self,
        evento_id: int,
        motivo: str = "Anulación administrativa"
    ):
        if not motivo or not motivo.strip():
            raise ValueError("El motivo de anulación es obligatorio.")

        evento = self.repo.anular_evento(evento_id, motivo.strip())

        if evento is None:
            raise LookupError("Evento sanitario no encontrado.")

        return evento
