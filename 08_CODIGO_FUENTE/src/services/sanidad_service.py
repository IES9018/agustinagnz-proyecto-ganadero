from datetime import date

from src.models.animal import Animal
from src.repositories.sanidad_repository import SanidadRepository


class SanidadService:

    def __init__(self, db):
        self.db = db
        self.repo = SanidadRepository(db)

    def crear_evento(self, animal_id: int, data: dict):
        if not isinstance(data, dict):
            raise ValueError("Los datos del evento sanitario no son válidos.")

        animal = self.db.get(Animal, animal_id)

        if animal is None:
            raise LookupError("Animal no encontrado.")

        datos_texto = {}

        for campo in ("tipo_evento", "descripcion"):
            valor = data.get(campo)

            if not isinstance(valor, str) or not valor.strip():
                raise ValueError(f"El campo '{campo}' es obligatorio.")

            valor = valor.strip()

            if campo == "tipo_evento" and len(valor) > 100:
                raise ValueError(
                    "El tipo de evento no puede superar los 100 caracteres."
                )

            datos_texto[campo] = valor

        fecha_evento = self._validar_fecha(data.get("fecha"), "fecha del evento")

        if fecha_evento > date.today():
            raise ValueError("La fecha del evento no puede ser futura.")

        fecha_proxima = None
        valor_fecha_proxima = data.get("fecha_proxima")

        if valor_fecha_proxima not in (None, ""):
            fecha_proxima = self._validar_fecha(
                valor_fecha_proxima,
                "fecha próxima"
            )

            if fecha_proxima < fecha_evento:
                raise ValueError(
                    "La fecha próxima no puede ser anterior "
                    "a la fecha del evento."
                )

        datos = {
            "tipo_evento": datos_texto["tipo_evento"],
            "descripcion": datos_texto["descripcion"],
            "fecha": fecha_evento,
            "fecha_proxima": fecha_proxima,
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
        if not isinstance(motivo, str) or not motivo.strip():
            raise ValueError("El motivo de anulación es obligatorio.")

        evento = self.repo.anular_evento(evento_id, motivo.strip())

        if evento is None:
            raise LookupError("Evento sanitario no encontrado.")

        return evento

    def listar_alertas(self):
        return self.repo.listar_alertas()

    @staticmethod
    def _validar_fecha(valor, nombre):
        if not isinstance(valor, str):
            raise ValueError(f"La {nombre} no tiene un formato válido.")

        try:
            fecha = date.fromisoformat(valor)
        except ValueError:
            raise ValueError(f"La {nombre} no tiene un formato válido.")

        if fecha.isoformat() != valor:
            raise ValueError(f"La {nombre} no tiene un formato válido.")

        return fecha