from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class Animal(Base):
    __tablename__ = "animales"

    id_animal: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    identificador: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    especie: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    raza: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    fecha_nacimiento: Mapped[date | None] = mapped_column(
        Date,
        nullable=False
    )

    estado_sanitario: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    id_establecimiento: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("establecimientos.id_establecimiento"),
        nullable=False
    )