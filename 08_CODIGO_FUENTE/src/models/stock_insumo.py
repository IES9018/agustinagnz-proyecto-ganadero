from sqlalchemy import CheckConstraint, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class StockInsumo(Base):
    __tablename__ = "stock_insumos"

    __table_args__ = (
        CheckConstraint(
            "cantidad >= 0",
            name="ck_stock_insumos_cantidad_no_negativa"
        ),
    )

    id_stock: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    tipo_insumo: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    cantidad: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0
    )

    unidad: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    ubicacion: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    id_establecimiento: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("establecimientos.id_establecimiento"),
        nullable=False,
        index=True
    )
