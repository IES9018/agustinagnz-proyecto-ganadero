from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class EventoSanitario(Base):
    __tablename__ = "eventos_sanitarios"

    id_evento: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_animal: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("animales.id_animal"),
        nullable=False,
        index=True
    )

    tipo_evento: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    descripcion: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    fecha: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    fecha_proxima: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        index=True
    )

    estado: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="vigente"
    )

    motivo_anulacion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    fecha_anulacion: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
