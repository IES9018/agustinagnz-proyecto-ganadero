from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.services.animal_service import AnimalService

from src.core.security import requiere_roles
from fastapi import Depends


router = APIRouter(
    dependencies=[
        Depends(requiere_roles("productor", "personal_campo"))
    ]
)


@router.post("/api/animales")
def crear_animal(
    animal: dict,
    db: Session = Depends(get_db)
):
    service = AnimalService(db)

    try:
        return service.crear_animal(animal)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get("/api/animales")
def listar_animales(
    db: Session = Depends(get_db)
):
    service = AnimalService(db)

    return service.listar_animales()


@router.get("/api/animales/{animal_id}")
def obtener_animal(
    animal_id: int,
    db: Session = Depends(get_db)
):
    service = AnimalService(db)

    animal = service.obtener_animal(animal_id)

    if animal is None:
        raise HTTPException(
            status_code=404,
            detail="Animal no encontrado"
        )

    return animal


@router.put("/api/animales/{animal_id}")
def actualizar_animal(
    animal_id: int,
    animal: dict,
    db: Session = Depends(get_db)
):
    service = AnimalService(db)

    try:
        resultado = service.actualizar_animal(
            animal_id,
            animal
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Animal no encontrado"
        )

    return resultado