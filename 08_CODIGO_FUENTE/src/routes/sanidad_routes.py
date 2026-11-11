from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import usuario_actual
from src.services.sanidad_service import SanidadService


router = APIRouter(
    dependencies=[Depends(usuario_actual)]
)


@router.get("/api/animales/{animal_id}/sanidad")
def get_sanidad(
    animal_id: int = Path(..., ge=1, le=2147483647),
    db: Session = Depends(get_db)
):
    service = SanidadService(db)

    try:
        return service.listar_eventos(animal_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/api/animales/{animal_id}/sanidad")
def create_sanidad(
    data: dict,
    animal_id: int = Path(..., ge=1, le=2147483647),
    db: Session = Depends(get_db)
):
    service = SanidadService(db)

    try:
        return service.crear_evento(animal_id, data)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.delete("/api/sanidad/{event_id:int}")
def delete_sanidad(
    event_id: int = Path(..., ge=1, le=2147483647),
    motivo: str = "Anulación administrativa",
    db: Session = Depends(get_db)
):
    service = SanidadService(db)

    try:
        return service.eliminar_evento(event_id, motivo)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.get("/api/sanidad/alertas")
def get_alertas_sanidad(
    db: Session = Depends(get_db)
):
    return SanidadService(db).listar_alertas()