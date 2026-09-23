from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.animal import Animal


class AnimalRepository:

    def __init__(self, db: Session):
        self.db = db

    def crear(self, data):
        animal = Animal(
            identificador=data["identificador"],
            especie=data["especie"],
            raza=data["raza"],
            fecha_nacimiento=data.get("fecha_nacimiento"),
            estado_sanitario=data["estado_sanitario"],
            id_establecimiento=data.get("id_establecimiento")
        )

        self.db.add(animal)

        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ValueError("El identificador del animal ya existe.")

        self.db.refresh(animal)

        return self._to_dict(animal)

    def listar(self):
        statement = select(Animal).order_by(Animal.id_animal)

        animales = self.db.scalars(statement).all()

        return [
            self._to_dict(animal)
            for animal in animales
        ]

    def obtener(self, animal_id):
        return self.db.get(Animal, animal_id)

    def actualizar(self, animal_id, data):
        animal = self.db.get(Animal, animal_id)

        if animal is None:
            return None

        animal.identificador = data["identificador"]
        animal.especie = data["especie"]
        animal.raza = data["raza"]
        animal.fecha_nacimiento = data.get("fecha_nacimiento")
        animal.estado_sanitario = data["estado_sanitario"]
        animal.id_establecimiento = data.get("id_establecimiento")

        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise ValueError("El identificador del animal ya existe.")

        self.db.refresh(animal)

        return self._to_dict(animal)

    @staticmethod
    def _to_dict(animal):
        return {
            "id_animal": animal.id_animal,
            "identificador": animal.identificador,
            "especie": animal.especie,
            "raza": animal.raza,
            "fecha_nacimiento": (
                animal.fecha_nacimiento.isoformat()
                if animal.fecha_nacimiento
                else None
            ),
            "estado_sanitario": animal.estado_sanitario,
            "id_establecimiento": animal.id_establecimiento
        }