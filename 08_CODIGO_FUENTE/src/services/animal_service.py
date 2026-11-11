
from datetime import date, datetime

from src.models.establecimiento import Establecimiento
from src.repositories.animal_repository import AnimalRepository


class AnimalService:

    CAMPOS_TEXTO = {
        "identificador": 100,
        "especie": 100,
        "sexo": 100,
        "raza": 100,
        "estado_sanitario": 100,
    }

    def __init__(self, db):
        self.db = db
        self.repo = AnimalRepository(db)

    def crear_animal(self, data):
        datos = self._validar(data)
        return self.repo.crear(datos)

    def listar_animales(self):
        return self.repo.listar()

    def obtener_animal(self, animal_id):
        animal = self.repo.obtener(animal_id)

        if animal is None:
            return None

        return self.repo._to_dict(animal)

    def actualizar_animal(self, animal_id, data):
        datos = self._validar(data)
        datos["fecha_nacimiento"] = datos["fecha_nacimiento"].isoformat()
        return self.repo.actualizar(animal_id, datos)

    def _validar(self, data):
        if not isinstance(data, dict):
            raise ValueError(
                "Los datos del animal deben enviarse como un diccionario."
            )

        datos = data.copy()

        campos_obligatorios = (
            "identificador",
            "especie",
            "sexo",
            "raza",
            "fecha_nacimiento",
            "estado_sanitario",
            "id_establecimiento",
        )

        for campo in campos_obligatorios:
            valor = datos.get(campo)

            if valor is None or (
                isinstance(valor, str) and not valor.strip()
            ):
                raise ValueError(
                    f"El campo '{campo}' es obligatorio."
                )

        for campo, longitud_maxima in self.CAMPOS_TEXTO.items():
            valor = datos[campo]

            if not isinstance(valor, str):
                raise ValueError(
                    f"El campo '{campo}' debe ser texto."
                )

            valor = valor.strip()

            if len(valor) > longitud_maxima:
                raise ValueError(
                    f"El campo '{campo}' no puede superar "
                    f"los {longitud_maxima} caracteres."
                )

            datos[campo] = valor

        fecha_nacimiento = datos["fecha_nacimiento"]

        if isinstance(fecha_nacimiento, datetime):
            fecha_nacimiento = fecha_nacimiento.date()

        elif isinstance(fecha_nacimiento, date):
            pass

        elif isinstance(fecha_nacimiento, str):
            try:
                fecha_nacimiento = date.fromisoformat(
                    fecha_nacimiento.strip()
                )
            except ValueError:
                raise ValueError(
                    "La fecha de nacimiento tiene un formato inválido."
                )

        else:
            raise ValueError(
                "La fecha de nacimiento tiene un formato inválido."
            )

        if fecha_nacimiento > date.today():
            raise ValueError(
                "La fecha de nacimiento no puede ser futura."
            )

        datos["fecha_nacimiento"] = fecha_nacimiento

        id_establecimiento = self._validar_id_establecimiento(
            datos["id_establecimiento"]
        )

        datos["id_establecimiento"] = id_establecimiento

        if self.db.get(Establecimiento, id_establecimiento) is None:
            raise LookupError(
                "El establecimiento no existe."
            )

        return datos

    @staticmethod
    def _validar_id_establecimiento(valor):
        if isinstance(valor, bool):
            raise ValueError(
                "Debe indicar un establecimiento válido."
            )

        try:
            establecimiento_id = int(valor)
        except (TypeError, ValueError):
            raise ValueError(
                "Debe indicar un establecimiento válido."
            )

        if isinstance(valor, float) and not valor.is_integer():
            raise ValueError(
                "Debe indicar un establecimiento válido."
            )

        if (
            isinstance(valor, str)
            and str(establecimiento_id) != valor.strip()
        ):
            raise ValueError(
                "Debe indicar un establecimiento válido."
            )

        if not 1 <= establecimiento_id <= 2147483647:
            raise ValueError(
                "Debe indicar un establecimiento válido."
            )

        return establecimiento_id
