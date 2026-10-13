from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.evento_sanitario import EventoSanitario


class SanidadRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear_evento(self, animal_id: int, data: dict):
        evento = EventoSanitario(
            id_animal=animal_id,
            tipo_evento=data["tipo_evento"],
            descripcion=data["descripcion"],
            fecha=data["fecha"],
            estado="vigente"
        )

        self.db.add(evento)
        self.db.commit()
        self.db.refresh(evento)

        return self._to_dict(evento)

    def listar_por_animal(self, animal_id: int):
        statement = (
            select(EventoSanitario)
            .where(EventoSanitario.id_animal == animal_id)
            .order_by(
                EventoSanitario.fecha.desc(),
                EventoSanitario.id_evento.desc()
            )
        )

        eventos = self.db.scalars(statement).all()

        return [self._to_dict(evento) for evento in eventos]

    def anular_evento(self, evento_id: int, motivo: str):
        evento = self.db.get(EventoSanitario, evento_id)

        if evento is None:
            return None

        if evento.estado != "anulado":
            evento.estado = "anulado"
            evento.motivo_anulacion = motivo
            evento.fecha_anulacion = datetime.now(timezone.utc)

            self.db.commit()
            self.db.refresh(evento)

        return self._to_dict(evento)

    @staticmethod
    def _to_dict(evento: EventoSanitario):
        return {
            "id_evento": evento.id_evento,
            "id_animal": evento.id_animal,
            "tipo_evento": evento.tipo_evento,
            "descripcion": evento.descripcion,
            "fecha": evento.fecha.isoformat(),
            "estado": evento.estado,
            "motivo_anulacion": evento.motivo_anulacion,
            "fecha_anulacion": (
                evento.fecha_anulacion.isoformat()
                if evento.fecha_anulacion
                else None
            )
        }
