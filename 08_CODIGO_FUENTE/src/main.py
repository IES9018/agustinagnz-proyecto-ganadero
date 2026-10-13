from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.core.database import Base, engine
from src.models.animal import Animal
from src.models.establecimiento import Establecimiento

from src.models.evento_sanitario import EventoSanitario

BASE_DIR = Path(__file__).resolve().parent

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "templates" / "index.html")

@app.get("/animales")
def animales_page():
    return FileResponse(BASE_DIR / "templates" / "animales.html")

@app.get("/sanidad")
def sanidad_page():
    return FileResponse(BASE_DIR / "templates" / "sanidad.html")

from src.routes.animal_routes import router as animal_router
from src.routes.sanidad_routes import router as sanidad_router


app.include_router(animal_router)
app.include_router(sanidad_router)