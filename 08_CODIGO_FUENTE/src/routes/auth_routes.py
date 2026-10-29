
from datetime import datetime, timezone

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select

from src.core.database import SessionLocal
from src.models.usuario import Usuario

from src.services.auth_service import verificar_password, hash_password, ROLES_VALIDOS
import hmac
import os

from dotenv import load_dotenv
import hmac
import os

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Autenticación"])



@router.post("/registro")
def registrar_usuario(
    nombre: str = Form(...),
    email: str = Form(...),
    rol: str = Form(...),
    password: str = Form(...),
    password_confirmacion: str = Form(...),
    codigo_autorizacion: str = Form(...),
):
    nombre = nombre.strip()
    email = email.strip().lower()
    rol = rol.strip().lower()
    

    if (
        not nombre
        or len(nombre) > 150
        or not email
        or len(email) > 255
        or rol not in ROLES_VALIDOS
        or len(password) < 12
        or password != password_confirmacion
    ):
        return RedirectResponse(
            "/login?registro=invalido",
            status_code=303,
        )

    with SessionLocal() as db:
        existente = db.scalar(
            select(Usuario).where(Usuario.email == email)
        )

        if existente:
            return RedirectResponse(
                "/login?registro=duplicado",
                status_code=303,
            )

        usuario = Usuario(
            nombre=nombre,
            email=email,
            password_hash=hash_password(password),
            rol=rol,
            estado_activo=True,
        )

            variables_codigo = {
                "productor": "CODIGO_REGISTRO_PRODUCTOR",
                "personal_campo": "CODIGO_REGISTRO_PERSONAL_CAMPO",
            }

            nombre_variable = variables_codigo.get(rol)
            codigo_esperado = (
                os.getenv(nombre_variable, "")
            if nombre_variable
            else ""
            )

            if not codigo_esperado:
                return RedirectResponse(
                    "/login?registro=no_configurado",
                    status_code=303,
                )

            if not hmac.compare_digest(
                codigo_autorizacion,
                codigo_esperado,
            ):
                return RedirectResponse(
                    "/login?registro=invalido",
                    status_code=303,
                )

        db.add(usuario)

        try:
            db.commit()
        except Exception:
            db.rollback()
            return RedirectResponse(
                "/login?registro=error",
                status_code=303,
            )

    return RedirectResponse("/login", status_code=303)

@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    email = email.strip().lower()

    with SessionLocal() as db:
        usuario = db.scalar(
            select(Usuario).where(Usuario.email == email)
        )

        if (
            usuario is None
            or not usuario.estado_activo
            or not verificar_password(password, usuario.password_hash)
        ):
            return RedirectResponse(
                "/login?error=1", status_code=303
            )

        usuario.ultimo_acceso = datetime.now(timezone.utc)
        db.commit()

        request.session.clear()
        request.session["usuario_id"] = usuario.id_usuario
        request.session["rol"] = usuario.rol
        request.session["nombre"] = usuario.nombre

    return RedirectResponse("/", status_code=303)


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)
