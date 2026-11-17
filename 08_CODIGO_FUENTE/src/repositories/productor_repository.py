from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.productor import Productor
from src.models.establecimiento import Establecimiento


class ProductorRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        productores = self.db.scalars(
            select(Productor).order_by(Productor.nombre)
        ).all()

        return [self._to_dict(productor) for productor in productores]

    def obtener(self, productor_id: int):
        return self.db.get(Productor, productor_id)

    def obtener_por_documento(self, documento: str):
        return self.db.scalar(
            select(Productor).where(
                Productor.documento == documento
            )
        )

    def crear(self, data: dict):
        productor = Productor(**data)
        self.db.add(productor)

        try:
            self.db.commit()
            self.db.refresh(productor)
        except Exception:
            self.db.rollback()
            raise

        return self._to_dict(productor)

    def actualizar(self, productor: Productor, data: dict):
        for campo, valor in data.items():
            setattr(productor, campo, valor)

        try:
            self.db.commit()
            self.db.refresh(productor)
        except Exception:
            self.db.rollback()
            raise

        return self._to_dict(productor)

    def cambiar_estado(self, productor: Productor, estado: str):
        productor.estado = estado

        try:
            self.db.commit()
            self.db.refresh(productor)
        except Exception:
            self.db.rollback()
            raise

        return self._to_dict(productor)

    def listar_establecimientos(self, productor_id: int):
        establecimientos = self.db.scalars(
            select(Establecimiento)
            .where(
                Establecimiento.id_productor == productor_id
            )
            .order_by(Establecimiento.nombre)
        ).all()

        return [
            self._establecimiento_to_dict(item)
            for item in establecimientos
        ]

    def crear_establecimiento(self, productor_id: int, data: dict):
        establecimiento = Establecimiento(
            id_productor=productor_id,
            **data,
        )

        self.db.add(establecimiento)

        try:
            self.db.commit()
            self.db.refresh(establecimiento)
        except Exception:
            self.db.rollback()
            raise

        return self._establecimiento_to_dict(establecimiento)

    def obtener_establecimiento(self, establecimiento_id: int):
        return self.db.get(Establecimiento, establecimiento_id)

    def actualizar_establecimiento(
        self,
        establecimiento: Establecimiento,
        data: dict,
    ):
        for campo, valor in data.items():
            setattr(establecimiento, campo, valor)

        try:
            self.db.commit()
            self.db.refresh(establecimiento)
        except Exception:
            self.db.rollback()
            raise

        return self._establecimiento_to_dict(establecimiento)

    def cambiar_estado_establecimiento(
        self,
        establecimiento: Establecimiento,
        estado: str,
    ):
        establecimiento.estado = estado

        try:
            self.db.commit()
            self.db.refresh(establecimiento)
        except Exception:
            self.db.rollback()
            raise

        return self._establecimiento_to_dict(establecimiento)

    def _to_dict(self, productor: Productor):
        establecimientos = self.listar_establecimientos(
            productor.id_productor
        )

        return {
            "id_productor": productor.id_productor,
            "nombre": productor.nombre,
            "documento": productor.documento,
            "telefono": productor.telefono,
            "email": productor.email,
            "localidad": productor.localidad,
            "domicilio": productor.domicilio,
            "observaciones": productor.observaciones,
            "estado": productor.estado,
            "establecimientos": establecimientos,
        }

    @staticmethod
    def _establecimiento_to_dict(item: Establecimiento):
        return {
            "id_establecimiento": item.id_establecimiento,
            "id_productor": item.id_productor,
            "nombre": item.nombre,
            "ubicacion": item.ubicacion,
            "capacidad": item.capacidad,
            "estado": item.estado,
        }