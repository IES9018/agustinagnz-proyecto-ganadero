from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.services.trazabilidad_service import TrazabilidadService

from src.core.security import requiere_roles

router = APIRouter(
    dependencies=[
        Depends(requiere_roles("productor"))
    ]
)


@router.get("/api/animales/{animal_id}/trazabilidad")
def get_trazabilidad(
    animal_id: int,
    db: Session = Depends(get_db)
):
    service = TrazabilidadService(db)

    try:
        return service.listar_por_animal(animal_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
