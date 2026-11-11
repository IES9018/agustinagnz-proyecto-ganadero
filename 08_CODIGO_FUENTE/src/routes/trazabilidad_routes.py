
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import usuario_actual
from src.services.trazabilidad_service import TrazabilidadService


router = APIRouter(
    dependencies=[Depends(usuario_actual)]
)


@router.get("/api/animales/{animal_id}/trazabilidad")
def get_trazabilidad(
    animal_id: int = Path(..., ge=1, le=2147483647),
    db: Session = Depends(get_db)
):
    service = TrazabilidadService(db)

    try:
        return service.listar_por_animal(animal_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
