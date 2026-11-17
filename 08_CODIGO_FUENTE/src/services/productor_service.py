
from src.repositories.productor_repository import ProductorRepository


class ProductorService:

    ESTADOS_VALIDOS = ("activo", "inactivo")

    LIMITES = {
        "nombre": 150,
        "documento": 30,
        "telefono": 40,
        "email": 255,
        "localidad": 120,
        "domicilio": 200,
        "observaciones": 2000,
    }

    def __init__(self, db):
        self.db = db
        self.repo = ProductorRepository(db)

    def listar(self):
        return self.repo.listar()

    def obtener(self, productor_id: int):
        productor = self.repo.obtener(productor_id)

        if productor is None:
            raise LookupError("Productor no encontrado.")

        return self.repo._to_dict(productor)

    def crear(self, data: dict):
        datos = self._validar_productor(data)

        documento = datos.get("documento")

        if documento and self.repo.obtener_por_documento(documento):
            raise ValueError(
                "Ya existe un productor registrado con ese documento."
            )

        return self.repo.crear(datos)

    def actualizar(self, productor_id: int, data: dict):
        productor = self.repo.obtener(productor_id)

        if productor is None:
            raise LookupError("Productor no encontrado.")

        datos = self._validar_productor(data)

        documento = datos.get("documento")

        if documento:
            existente = self.repo.obtener_por_documento(documento)

            if (
                existente is not None
                and existente.id_productor != productor_id
            ):
                raise ValueError(
                    "Ya existe otro productor con ese documento."
                )

        return self.repo.actualizar(productor, datos)

    def cambiar_estado(self, productor_id: int, estado: str):
        productor = self.repo.obtener(productor_id)

        if productor is None:
            raise LookupError("Productor no encontrado.")

        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError("El estado debe ser activo o inactivo.")

        return self.repo.cambiar_estado(productor, estado)

    def listar_establecimientos(self, productor_id: int):
        self._obtener_productor(productor_id)
        return self.repo.listar_establecimientos(productor_id)

    def crear_establecimiento(self, productor_id: int, data: dict):
        productor = self._obtener_productor(productor_id)

        if productor.estado != "activo":
            raise ValueError(
                "No se pueden agregar establecimientos a un productor inactivo."
            )

        datos = self._validar_establecimiento(data)

        return self.repo.crear_establecimiento(
            productor_id,
            datos,
        )

    def actualizar_establecimiento(
        self,
        establecimiento_id: int,
        data: dict,
    ):
        establecimiento = self.repo.obtener_establecimiento(
            establecimiento_id
        )

        if establecimiento is None:
            raise LookupError("Establecimiento no encontrado.")

        datos = self._validar_establecimiento(data)

        return self.repo.actualizar_establecimiento(
            establecimiento,
            datos,
        )

    def cambiar_estado_establecimiento(
        self,
        establecimiento_id: int,
        estado: str,
    ):
        establecimiento = self.repo.obtener_establecimiento(
            establecimiento_id
        )

        if establecimiento is None:
            raise LookupError("Establecimiento no encontrado.")

        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError("El estado debe ser activo o inactivo.")

        return self.repo.cambiar_estado_establecimiento(
            establecimiento,
            estado,
        )

    def _obtener_productor(self, productor_id: int):
        productor = self.repo.obtener(productor_id)

        if productor is None:
            raise LookupError("Productor no encontrado.")

        return productor

    @classmethod
    def _validar_productor(cls, data: dict):
        if not isinstance(data, dict):
            raise ValueError("Los datos del productor no son válidos.")

        datos = {}

        for campo, limite in cls.LIMITES.items():
            valor = data.get(campo)

            if valor is None:
                if campo == "nombre":
                    raise ValueError("El nombre del productor es obligatorio.")

                datos[campo] = None
                continue

            if not isinstance(valor, str):
                raise ValueError(f"El campo {campo} debe ser texto.")

            valor = valor.strip()

            if campo == "nombre" and not valor:
                raise ValueError("El nombre del productor es obligatorio.")

            if len(valor) > limite:
                raise ValueError(
                    f"El campo {campo} no puede superar {limite} caracteres."
                )

            datos[campo] = valor or None

        return datos

    @staticmethod
    def _validar_establecimiento(data: dict):
        if not isinstance(data, dict):
            raise ValueError("Los datos del establecimiento no son válidos.")

        nombre = data.get("nombre")
        ubicacion = data.get("ubicacion")
        capacidad = data.get("capacidad")

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del establecimiento es obligatorio.")

        if len(nombre.strip()) > 150:
            raise ValueError("El nombre no puede superar 150 caracteres.")

        if not isinstance(ubicacion, str) or not ubicacion.strip():
            raise ValueError("La ubicación del establecimiento es obligatoria.")

        if len(ubicacion.strip()) > 200:
            raise ValueError("La ubicación no puede superar 200 caracteres.")

        if capacidad in ("", None):
            capacidad = None
        else:
            if isinstance(capacidad, bool):
                raise ValueError("La capacidad debe ser un entero positivo.")

            try:
                capacidad = int(capacidad)
            except (TypeError, ValueError):
                raise ValueError("La capacidad debe ser un entero positivo.")

            if capacidad < 1:
                raise ValueError("La capacidad debe ser mayor que cero.")

        estado = data.get("estado", "activo")

        if estado not in ("activo", "inactivo"):
            raise ValueError("El estado debe ser activo o inactivo.")

        return {
            "nombre": nombre.strip(),
            "ubicacion": ubicacion.strip(),
            "capacidad": capacidad,
            "estado": estado,
        }
