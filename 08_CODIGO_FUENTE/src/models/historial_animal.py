from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class HistorialAnimal(Base):
    __tablename__ = "historial_animales"

    id_historial: Mapped[int] = mapped_column(
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
        String(50),
        nullable=False
    )

    descripcion: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    fecha_evento: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now
    )
