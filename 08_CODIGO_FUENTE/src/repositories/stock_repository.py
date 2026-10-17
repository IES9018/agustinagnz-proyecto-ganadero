
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.stock_insumo import StockInsumo


class StockRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        statement = (
            select(StockInsumo)
            .order_by(
                StockInsumo.categoria,
                StockInsumo.tipo_insumo,
                StockInsumo.id_stock,
            )
        )
        return [
            self._to_dict(item)
            for item in self.db.scalars(statement).all()
        ]

    def obtener(self, stock_id: int):
        return self.db.get(StockInsumo, stock_id)

    def crear(self, data: dict):
        item = StockInsumo(**data)
        self.db.add(item)

        try:
            self.db.commit()
            self.db.refresh(item)
        except Exception:
            self.db.rollback()
            raise

        return self._to_dict(item)

    def actualizar(self, item: StockInsumo, data: dict):
        for campo, valor in data.items():
            setattr(item, campo, valor)

        try:
            self.db.commit()
            self.db.refresh(item)
        except Exception:
            self.db.rollback()
            raise

        return self._to_dict(item)

    def ajustar_cantidad(self, item: StockInsumo, nueva_cantidad: float):
        item.cantidad = nueva_cantidad

        try:
            self.db.commit()
            self.db.refresh(item)
        except Exception:
            self.db.rollback()
            raise

        return self._to_dict(item)

    @staticmethod
    def _to_dict(item: StockInsumo):
        return {
            "id_stock": item.id_stock,
            "tipo_insumo": item.tipo_insumo,
            "categoria": item.categoria,
            "cantidad": float(item.cantidad),
            "stock_minimo": float(item.stock_minimo),
            "stock_critico": float(item.stock_critico),
            "unidad": item.unidad,
            "ubicacion": item.ubicacion,
            "id_establecimiento": item.id_establecimiento,
        }
