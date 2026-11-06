from datetime import date

from src.models.establecimiento import Establecimiento
from src.repositories.animal_repository import AnimalRepository


class AnimalService:

    CAMPOS_TEXTO = {
        "identificador": 100,
        "especie": 100,
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
            raise ValueError("Los datos del animal no son válidos.")

        datos = {}

        for campo, limite in self.CAMPOS_TEXTO.items():
            valor = data.get(campo)

            if not isinstance(valor, str) or not valor.strip():
                raise ValueError(f"El campo '{campo}' es obligatorio.")

            valor = valor.strip()

            if len(valor) > limite:
                raise ValueError(
                    f"El campo '{campo}' no puede superar los {limite} caracteres."
                )

            datos[campo] = valor

        valor_fecha = data.get("fecha_nacimiento")

        if not isinstance(valor_fecha, str):
            raise ValueError("La fecha de nacimiento no tiene un formato válido.")

        try:
            fecha_nacimiento = date.fromisoformat(valor_fecha)
        except ValueError:
            raise ValueError("La fecha de nacimiento no tiene un formato válido.")

        if fecha_nacimiento.isoformat() != valor_fecha:
            raise ValueError("La fecha de nacimiento no tiene un formato válido.")

        if fecha_nacimiento > date.today():
            raise ValueError("La fecha de nacimiento no puede ser futura.")

        datos["fecha_nacimiento"] = fecha_nacimiento

        establecimiento_id = self._validar_id_establecimiento(
            data.get("id_establecimiento")
        )

        establecimiento = self.db.get(Establecimiento, establecimiento_id)

        if establecimiento is None:
            raise ValueError("El establecimiento indicado no existe.")

        datos["id_establecimiento"] = establecimiento_id

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

        if establecimiento_id <= 0:
            raise ValueError("Debe indicar un establecimiento válido.")

        return establecimiento_id