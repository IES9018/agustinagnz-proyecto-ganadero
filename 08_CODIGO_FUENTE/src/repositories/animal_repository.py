from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.animal import Animal
from src.models.historial_animal import HistorialAnimal


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
            self.db.flush()

            self._registrar_historial(
                animal.id_animal,
                "alta",
                f"Alta del animal {animal.identificador}."
            )

            self.db.commit()
        except IntegrityError as error:
            self.db.rollback()

            existente = self.db.scalar(
                select(Animal.id_animal).where(
                    Animal.identificador == data["identificador"]
                )
            )

            if existente is not None:
                raise ValueError(
                    "El identificador del animal ya existe."
                ) from error

            raise

        self.db.refresh(animal)
        return self._to_dict(animal)

    def listar(self):
        statement = select(Animal).order_by(Animal.id_animal)
        animales = self.db.scalars(statement).all()
        return [self._to_dict(animal) for animal in animales]

    def obtener(self, animal_id):
        return self.db.get(Animal, animal_id)

    def actualizar(self, animal_id, data):
        animal = self.db.get(Animal, animal_id)

        if animal is None:
            return None

        campos = (
            "identificador",
            "especie",
            "raza",
            "fecha_nacimiento",
            "estado_sanitario",
            "id_establecimiento"
        )

        cambios = []

        for campo in campos:
            anterior = getattr(animal, campo)
            nuevo = data.get(campo)

            if campo == "fecha_nacimiento" and nuevo:
                from datetime import date
                nuevo = date.fromisoformat(str(nuevo))

            if campo == "id_establecimiento" and nuevo is not None:
                nuevo = int(nuevo)

            if anterior != nuevo:
                cambios.append(
                    f"{campo}: {anterior!s} → {nuevo!s}"
                )
                setattr(animal, campo, nuevo)

        if cambios:
            descripcion = (
                f"Modificación del animal {animal.identificador}. "
                f"Cambios: {'; '.join(cambios)}."
            )

            self._registrar_historial(
                animal.id_animal,
                "modificacion",
                descripcion
            )

        try:
            self.db.commit()
        except IntegrityError as error:
            self.db.rollback()

            identificador = data.get("identificador")
            if identificador is not None:
                existente = self.db.scalar(
                    select(Animal.id_animal).where(
                        Animal.identificador == identificador,
                        Animal.id_animal != animal_id
                    )
                )

                if existente is not None:
                    raise ValueError(
                        "El identificador del animal ya existe."
                    ) from error

            raise

        self.db.refresh(animal)
        return self._to_dict(animal)

    def _registrar_historial(
        self,
        animal_id: int,
        tipo_evento: str,
        descripcion: str
    ):
        registro = HistorialAnimal(
            id_animal=animal_id,
            tipo_evento=tipo_evento,
            descripcion=descripcion,
            fecha_evento=datetime.now(timezone.utc)
        )
        self.db.add(registro)

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
