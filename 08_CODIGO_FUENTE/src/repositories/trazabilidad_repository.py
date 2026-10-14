from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.animal import Animal
from src.models.evento_sanitario import EventoSanitario
from src.models.historial_animal import HistorialAnimal


class TrazabilidadRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar_por_animal(self, animal_id: int):
        animal = self.db.get(Animal, animal_id)

        if animal is None:
            return None

        historial = self.db.scalars(
            select(HistorialAnimal)
            .where(HistorialAnimal.id_animal == animal_id)
        ).all()

        eventos_sanitarios = self.db.scalars(
            select(EventoSanitario)
            .where(EventoSanitario.id_animal == animal_id)
        ).all()

        resultado = []

        for registro in historial:
            resultado.append({
                "id": registro.id_historial,
                "fecha": registro.fecha_evento.isoformat(),
                "tipo": registro.tipo_evento,
                "origen": "animal",
                "descripcion": registro.descripcion
            })

        for evento in eventos_sanitarios:
            descripcion = evento.descripcion

            if evento.estado == "anulado":
                descripcion += (
                    f" [ANULADO. Motivo: "
                    f"{evento.motivo_anulacion or 'No informado'}]"
                )

            resultado.append({
                "id": evento.id_evento,
                "fecha": evento.fecha.isoformat(),
                "tipo": evento.tipo_evento,
                "origen": "sanidad",
                "descripcion": descripcion,
                "estado": evento.estado,
                "motivo_anulacion": evento.motivo_anulacion,
                "fecha_anulacion": (
                    evento.fecha_anulacion.isoformat()
                    if evento.fecha_anulacion
                    else None
                )
            })

        resultado.sort(
            key=lambda item: item["fecha"],
            reverse=True
        )

        return {
            "id_animal": animal.id_animal,
            "identificador": animal.identificador,
            "total_eventos": len(resultado),
            "eventos": resultado
        }
