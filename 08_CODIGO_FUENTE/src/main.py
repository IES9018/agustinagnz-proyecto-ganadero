
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi.responses import FileResponse, RedirectResponse, Response

from dotenv import load_dotenv

load_dotenv()

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from src.core.database import Base, engine
from src.core.security import usuario_actual

from src.models.usuario import Usuario
from src.models.animal import Animal
from src.models.establecimiento import Establecimiento
from src.models.evento_sanitario import EventoSanitario
from src.models.historial_animal import HistorialAnimal
from src.models.stock_insumo import StockInsumo

from src.routes.auth_routes import router as auth_router
from src.routes.animal_routes import router as animal_router
from src.routes.sanidad_routes import router as sanidad_router
from src.routes.trazabilidad_routes import router as trazabilidad_router
from src.routes.stock_routes import router as stock_router


BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


@app.get("/auth/perfil")
def obtener_perfil(usuario: dict = Depends(usuario_actual)):
    return {
        "id_usuario": usuario["id_usuario"],
        "nombre": usuario["nombre"],
    }


@app.get("/")
def home():
    return FileResponse(
        BASE_DIR / "templates" / "index.html",
        headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
    )


@app.get("/animales")
def animales_page():
    return pagina_protegida("animales.html")


@app.get("/sanidad")
def sanidad_page():
    return pagina_protegida("sanidad.html")


@app.get("/stock")
def stock_page():
    return pagina_protegida("stock.html")


@app.get("/trazabilidad")
def trazabilidad_page():
    return pagina_protegida("trazabilidad.html")


app.include_router(animal_router)
app.include_router(sanidad_router)
app.include_router(trazabilidad_router)
app.include_router(stock_router)
app.include_router(auth_router)


@app.options("/api/animales", include_in_schema=False)
def options_animales():
    return Response(
        status_code=204,
        headers={"Allow": "GET, HEAD, POST, OPTIONS"}
    )


@app.options("/api/animales/{animal_id}", include_in_schema=False)
def options_animal():
    return Response(
        status_code=204,
        headers={"Allow": "GET, HEAD, PUT, OPTIONS"}
    )


@app.options(
    "/api/animales/{animal_id}/sanidad",
    include_in_schema=False
)
def options_sanidad_animal():
    return Response(
        status_code=204,
        headers={"Allow": "GET, HEAD, POST, OPTIONS"}
    )


@app.options("/api/sanidad/alertas", include_in_schema=False)
def options_alertas_sanidad():
    return Response(
        status_code=204,
        headers={"Allow": "GET, HEAD, OPTIONS"}
    )


@app.options("/api/stock", include_in_schema=False)
def options_stock():
    return Response(
        status_code=204,
        headers={"Allow": "GET, HEAD, POST, OPTIONS"}
    )


@app.get("/login")
def login_page():
    return FileResponse(
        BASE_DIR / "templates" / "login.html",
        headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
    )


def pagina_protegida(nombre_archivo: str):
    return FileResponse(
        BASE_DIR / "templates" / nombre_archivo,
        headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
    )
