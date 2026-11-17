from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class Productor(Base):
    __tablename__ = "productores"

    id_productor: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    documento: Mapped[str | None] = mapped_column(
        String(30),
        unique=True,
        nullable=True,
    )

    telefono: Mapped[str | None] = mapped_column(
        String(40),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    localidad: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
    )

    domicilio: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    observaciones: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    estado: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="activo",
        server_default="activo",
    )