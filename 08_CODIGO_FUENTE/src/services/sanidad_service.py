from src.repositories.sanidad_repository import SanidadRepository


class SanidadService:

    def __init__(self):
        self.repo = SanidadRepository()

    def crear_evento(self, animal_id, data):
        return self.repo.crear_evento(animal_id, data)

    def listar_eventos(self, animal_id):
        return self.repo.listar_por_animal(animal_id)

    def eliminar_evento(self, evento_id):
        return self.repo.eliminar_evento(evento_id)