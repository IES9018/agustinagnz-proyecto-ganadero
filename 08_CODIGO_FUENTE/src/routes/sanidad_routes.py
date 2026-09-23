from fastapi import APIRouter
from src.services.sanidad_service import SanidadService

router = APIRouter()

service = SanidadService()

# -----------------------------------
# OBTENER SANIDAD POR ANIMAL
# -----------------------------------
@router.get("/api/animales/{animal_id}/sanidad")
def get_sanidad(animal_id: int):
    return service.get_by_animal(animal_id)


# -----------------------------------
# CREAR EVENTO SANITARIO
# -----------------------------------
@router.post("/api/animales/{animal_id}/sanidad")
def create_sanidad(animal_id: int, data: dict):
    return service.create(animal_id, data)


# -----------------------------------
# ELIMINAR EVENTO SANITARIO
# -----------------------------------
@router.delete("/api/sanidad/{event_id}")
def delete_sanidad(event_id: int):
    return service.delete(event_id)