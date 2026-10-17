
import math

from src.models.establecimiento import Establecimiento
from src.repositories.stock_repository import StockRepository


class StockService:
    CATEGORIAS_VALIDAS = (
        "Alimentos",
        "Medicamentos",
        "Insumos generales",
    )

    def __init__(self, db):
        self.db = db
        self.repo = StockRepository(db)

    def listar(self):
        return self.repo.listar()

    def crear(self, data: dict):
        datos = self._validar_datos(data, incluir_cantidad=True)
        self._validar_establecimiento(datos["id_establecimiento"])
        return self.repo.crear(datos)

    def actualizar(self, stock_id: int, data: dict):
        item = self.repo.obtener(stock_id)

        if item is None:
            raise LookupError("Insumo no encontrado.")

        datos = self._validar_datos(data, incluir_cantidad=True)
        self._validar_establecimiento(datos["id_establecimiento"])
        return self.repo.actualizar(item, datos)

    def ajustar_cantidad(
        self,
        stock_id: int,
        tipo_operacion: str,
        cantidad: float
    ):
        item = self.repo.obtener(stock_id)

        if item is None:
            raise LookupError("Insumo no encontrado.")

        if tipo_operacion not in ("ingreso", "salida"):
            raise ValueError(
                "La operación debe ser 'ingreso' o 'salida'."
            )

        cantidad = self._validar_cantidad(cantidad)

        if cantidad <= 0:
            raise ValueError(
                "La cantidad de la operación debe ser mayor que cero."
            )

        if tipo_operacion == "ingreso":
            nueva_cantidad = item.cantidad + cantidad
        else:
            nueva_cantidad = item.cantidad - cantidad

        if nueva_cantidad < 0:
            raise ValueError(
                "La cantidad no puede resultar negativa. "
                "El stock disponible es insuficiente."
            )

        return self.repo.ajustar_cantidad(item, nueva_cantidad)

    def _validar_establecimiento(self, establecimiento_id: int):
        establecimiento = self.db.get(
            Establecimiento,
            establecimiento_id
        )

        if establecimiento is None:
            raise ValueError("El establecimiento indicado no existe.")

    @classmethod
    def _validar_datos(
        cls,
        data: dict,
        incluir_cantidad: bool
    ) -> dict:
        campos_texto = ("tipo_insumo", "unidad", "ubicacion")
        datos = {}

        for campo in campos_texto:
            valor = data.get(campo)

            if valor is None or not str(valor).strip():
                raise ValueError(
                    f"El campo '{campo}' es obligatorio."
                )

            datos[campo] = str(valor).strip()

        categoria = str(
            data.get("categoria", "Insumos generales")
        ).strip()

        if categoria not in cls.CATEGORIAS_VALIDAS:
            raise ValueError(
                "La categoría debe ser Alimentos, Medicamentos "
                "o Insumos generales."
            )

        datos["categoria"] = categoria


        stock_minimo = cls._validar_cantidad(
            data.get("stock_minimo", 10)
        )
        stock_critico = cls._validar_cantidad(
            data.get("stock_critico", 5)
        )

        if stock_minimo < 0 or stock_critico < 0:
            raise ValueError(
                "Los umbrales de stock no pueden ser negativos."
            )

        if stock_critico > stock_minimo:
            raise ValueError(
                "El umbral crítico no puede superar el stock mínimo."
            )

        datos["stock_minimo"] = stock_minimo
        datos["stock_critico"] = stock_critico

        try:
            establecimiento_id = int(data["id_establecimiento"])
        except (KeyError, TypeError, ValueError):
            raise ValueError(
                "Debe indicar un establecimiento válido."
            )

        if establecimiento_id <= 0:
            raise ValueError(
                "Debe indicar un establecimiento válido."
            )

        datos["id_establecimiento"] = establecimiento_id

        if incluir_cantidad:
            cantidad = cls._validar_cantidad(data.get("cantidad"))

            if cantidad < 0:
                raise ValueError(
                    "La cantidad inicial no puede ser negativa."
                )

            datos["cantidad"] = cantidad

        return datos

    @staticmethod
    def _validar_cantidad(valor) -> float:
        try:
            cantidad = float(valor)
        except (TypeError, ValueError):
            raise ValueError("La cantidad debe ser un número válido.")

        if not math.isfinite(cantidad):
            raise ValueError("La cantidad debe ser un número finito.")

        return cantidad
