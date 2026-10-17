from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.services.sanidad_service import SanidadService

from src.core.security import requiere_roles

router = APIRouter(
    dependencies=[
        Depends(requiere_roles("personal_campo"))
    ]
)


@router.get("/api/animales/{animal_id}/sanidad")
def get_sanidad(
    animal_id: int,
    db: Session = Depends(get_db)
):
    service = SanidadService(db)

    try:
        return service.listar_eventos(animal_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/api/animales/{animal_id}/sanidad")
def create_sanidad(
    animal_id: int,
    data: dict,
    db: Session = Depends(get_db)
):
    service = SanidadService(db)

    try:
        return service.crear_evento(animal_id, data)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.delete("/api/sanidad/{event_id}")
def delete_sanidad(
    event_id: int,
    motivo: str = "Anulación administrativa",
    db: Session = Depends(get_db)
):
    service = SanidadService(db)

    try:
        return service.eliminar_evento(event_id, motivo)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.get("/api/sanidad/alertas")
def get_alertas_sanidad(
    db: Session = Depends(get_db)
):
    return SanidadService(db).listar_alertas()