from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class Establecimiento(Base):
    __tablename__ = "establecimientos"

    id_establecimiento: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    ubicacion: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    capacidad: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    estado: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="activo"
    )