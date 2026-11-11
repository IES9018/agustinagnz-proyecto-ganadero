import math

from src.models.establecimiento import Establecimiento
from src.repositories.stock_repository import StockRepository


class StockService:

    CATEGORIAS_VALIDAS = (
        "Alimentos",
        "Medicamentos",
        "Insumos generales",
    )

    LIMITES_TEXTO = {
        "tipo_insumo": 150,
        "unidad": 30,
        "ubicacion": 200,
    }

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
            raise ValueError("La operación debe ser 'ingreso' o 'salida'.")

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
            raise LookupError("El establecimiento indicado no existe.")

    @classmethod
    def _validar_datos(cls, data: dict, incluir_cantidad: bool) -> dict:
        if not isinstance(data, dict):
            raise ValueError("Los datos del insumo no son válidos.")

        datos = {}

        for campo, limite in cls.LIMITES_TEXTO.items():
            valor = data.get(campo)

            if not isinstance(valor, str) or not valor.strip():
                raise ValueError(f"El campo '{campo}' es obligatorio.")

            valor = valor.strip()

            if len(valor) > limite:
                raise ValueError(
                    f"El campo '{campo}' no puede superar los "
                    f"{limite} caracteres."
                )

            datos[campo] = valor

        categoria = data.get("categoria", "Insumos generales")

        if not isinstance(categoria, str):
            raise ValueError(
                "La categoría debe ser Alimentos, Medicamentos o Insumos generales."
            )

        categoria = categoria.strip()

        if len(categoria) > 40 or categoria not in cls.CATEGORIAS_VALIDAS:
            raise ValueError(
                "La categoría debe ser Alimentos, Medicamentos o Insumos generales."
            )

        datos["categoria"] = categoria

        stock_minimo = cls._validar_cantidad(data.get("stock_minimo", 10))
        stock_critico = cls._validar_cantidad(data.get("stock_critico", 5))

        if stock_minimo < 0 or stock_critico < 0:
            raise ValueError("Los umbrales de stock no pueden ser negativos.")

        if stock_critico > stock_minimo:
            raise ValueError(
                "El umbral crítico no puede superar el stock mínimo."
            )

        datos["stock_minimo"] = stock_minimo
        datos["stock_critico"] = stock_critico

        establecimiento_id = cls._validar_id_establecimiento(
            data.get("id_establecimiento")
        )

        datos["id_establecimiento"] = establecimiento_id

        if incluir_cantidad:
            cantidad = cls._validar_cantidad(data.get("cantidad"))

            if cantidad < 0:
                raise ValueError("La cantidad inicial no puede ser negativa.")

            datos["cantidad"] = cantidad

        return datos

    @staticmethod
    def _validar_id_establecimiento(valor):
        if isinstance(valor, bool):
            raise ValueError("Debe indicar un establecimiento válido.")

        try:
            establecimiento_id = int(valor)
        except (TypeError, ValueError):
            raise ValueError("Debe indicar un establecimiento válido.")

        if isinstance(valor, float) and not valor.is_integer():
            raise ValueError("Debe indicar un establecimiento válido.")

        if isinstance(valor, str) and str(establecimiento_id) != valor.strip():
            raise ValueError("Debe indicar un establecimiento válido.")

        if not 1 <= establecimiento_id <= 2147483647:
            raise ValueError("Debe indicar un establecimiento válido.")

        return establecimiento_id

    @staticmethod
    def _validar_cantidad(valor) -> float:
        if isinstance(valor, bool) or valor is None:
            raise ValueError("La cantidad debe ser un número válido.")

        try:
            cantidad = float(valor)
        except (TypeError, ValueError):
            raise ValueError("La cantidad debe ser un número válido.")

        if not math.isfinite(cantidad):
            raise ValueError("La cantidad debe ser un número finito.")

        return cantidad