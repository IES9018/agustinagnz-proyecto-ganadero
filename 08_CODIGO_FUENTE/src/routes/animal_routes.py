from fastapi import APIRouter, HTTPException

from services.animal_service import AnimalService


router = APIRouter()

service = AnimalService()


@router.post("/api/animales")
def crear_animal(animal: dict):
    return service.crear_animal(animal)


@router.get("/api/animales")
def listar_animales():
    return service.listar_animales()


@router.get("/api/animales/{animal_id}")
def obtener_animal(animal_id: int):
    animal = service.obtener_animal(animal_id)

    if animal is None:
        raise HTTPException(
            status_code=404,
            detail="Animal no encontrado"
        )

    return animal


@router.put("/api/animales/{animal_id}")
def actualizar_animal(animal_id: int, animal: dict):
    resultado = service.actualizar_animal(animal_id, animal)

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Animal no encontrado"
        )

    return resultado


@router.delete("/api/animales/{animal_id}")
def eliminar_animal(animal_id: int):
    resultado = service.eliminar_animal(animal_id)

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Animal no encontrado"
        )

    return resultado