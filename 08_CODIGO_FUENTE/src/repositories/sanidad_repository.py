from datetime import date, datetime, timedelta, timezone

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
            fecha_proxima=data.get("fecha_proxima"),
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

    def listar_alertas(self):
        hoy = date.today()
        limite = hoy + timedelta(days=30)

        statement = (
            select(EventoSanitario)
            .where(
                EventoSanitario.estado == "vigente",
                EventoSanitario.fecha_proxima.is_not(None),
                EventoSanitario.fecha_proxima <= limite,
            )
            .order_by(
                EventoSanitario.fecha_proxima.asc(),
                EventoSanitario.id_evento.asc(),
            )
        )

        eventos = self.db.scalars(statement).all()
        alertas = []

        for evento in eventos:
            datos = self._to_dict(evento)

            datos["tipo_alerta"] = (
                "Pendiente vencido"
                if evento.fecha_proxima < hoy
                else "Próximo"
            )

            alertas.append(datos)

        return alertas
    
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
            "fecha_proxima": (
                evento.fecha_proxima.isoformat()
                if evento.fecha_proxima
                else None
            ),
            "estado": evento.estado,
            "motivo_anulacion": evento.motivo_anulacion,
            "fecha_anulacion": (
                evento.fecha_anulacion.isoformat()
                if evento.fecha_anulacion
                else None
            )
        }
