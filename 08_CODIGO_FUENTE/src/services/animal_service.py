from datetime import date

from src.repositories.animal_repository import AnimalRepository

class AnimalService:

    def __init__(self, db):
        self.repo = AnimalRepository(db)

    def crear_animal(self, data):
        self._validar(data)

        return self.repo.crear(data)

    def listar_animales(self):
        return self.repo.listar()

    def obtener_animal(self, animal_id):
        animal = self.repo.obtener(animal_id)

        if animal is None:
            return None

        return self.repo._to_dict(animal)

    def actualizar_animal(self, animal_id, data):
        self._validar(data)

        return self.repo.actualizar(animal_id, data)

    @staticmethod
    def _validar(data):
        campos_obligatorios = [
            "identificador",
            "especie",
            "raza",
            "fecha_nacimiento",
            "estado_sanitario",
            "id_establecimiento"
        ]

        for campo in campos_obligatorios:
            if not data.get(campo):
                raise ValueError(
                    f"El campo '{campo}' es obligatorio."
                )

        fecha_nacimiento = data.get("fecha_nacimiento")

        if fecha_nacimiento:
            try:
                fecha = date.fromisoformat(fecha_nacimiento)
            except ValueError:
                raise ValueError(
                    "La fecha de nacimiento no tiene un formato válido."
                )

            if fecha > date.today():
                raise ValueError(
                    "La fecha de nacimiento no puede ser futura."
                )