import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from fastapi import Depends, FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

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

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "La variable SECRET_KEY no está configurada en el entorno."
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    same_site="lax",
    https_only=os.getenv("HTTPS_ONLY", "false").lower() == "true",
    session_cookie="ganadapp_session",
    max_age=60 * 60 * 8,
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

@app.get("/auth/perfil")
def obtener_perfil(usuario: dict = Depends(usuario_actual)):
    return {
        "nombre": usuario["nombre"]
    }

@app.get("/")
def home():
    return FileResponse(
        BASE_DIR / "templates" / "index.html",
        headers={"Cache-Control": "no-store, no-cache, must-revalidate"}
    )

@app.get("/animales")
def animales_page(request: Request):
    return pagina_protegida(request, "animales.html")


@app.get("/sanidad")
def sanidad_page(request: Request):
    return pagina_protegida(request, "sanidad.html")


@app.get("/stock")
def stock_page(request: Request):
    return pagina_protegida(request, "stock.html")


@app.get("/trazabilidad")
def trazabilidad_page(request: Request):
    return pagina_protegida(request, "trazabilidad.html")


from src.routes.animal_routes import router as animal_router
from src.routes.sanidad_routes import router as sanidad_router
from src.routes.trazabilidad_routes import router as trazabilidad_router
from src.routes.stock_routes import router as stock_router


app.include_router(animal_router)
app.include_router(sanidad_router)
app.include_router(trazabilidad_router)
app.include_router(stock_router)
app.include_router(auth_router)

@app.get("/login")
def login_page(request: Request):
    if request.session.get("usuario_id"):
        return RedirectResponse("/", status_code=303)

    return FileResponse(
        BASE_DIR / "templates" / "login.html",
        headers={"Cache-Control": "no-store, no-cache, must-revalidate"}
    )

def pagina_protegida(request: Request, nombre_archivo: str):
    if not request.session.get("usuario_id"):
        return RedirectResponse(
            f"/login?next=/{nombre_archivo}",
            status_code=303
        )

    return FileResponse(
        BASE_DIR / "templates" / nombre_archivo,
        headers={"Cache-Control": "no-store, no-cache, must-revalidate"}
    )