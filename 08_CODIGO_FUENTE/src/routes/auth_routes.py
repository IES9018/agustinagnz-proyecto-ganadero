from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Form, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import crear_access_token
from src.models.usuario import Usuario
from src.services.auth_service import hash_password, verificar_password


router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/registro")
def registrar_usuario(
    nombre: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    password_confirmacion: str = Form(...),
    db: Session = Depends(get_db),
):
    nombre = nombre.strip()
    email = email.strip().lower()

    if (
        not nombre
        or len(nombre) > 150
        or not email
        or len(email) > 255
        or len(password) < 12
        or password != password_confirmacion
    ):
        return RedirectResponse(
            "/login?registro=invalido",
            status_code=303,
        )

    existente = db.scalar(
        select(Usuario).where(Usuario.email == email)
    )

    if existente is not None:
        return RedirectResponse(
            "/login?registro=duplicado",
            status_code=303,
        )

    usuario = Usuario(
        nombre=nombre,
        email=email,
        password_hash=hash_password(password),
        estado_activo=True,
    )

    db.add(usuario)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return RedirectResponse(
            "/login?registro=duplicado",
            status_code=303,
        )

    return RedirectResponse(
        "/login?registro=exitoso",
        status_code=303,
    )


@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    email = email.strip().lower()

    usuario = db.scalar(
        select(Usuario).where(Usuario.email == email)
    )

    if (
        usuario is None
        or not usuario.estado_activo
        or not verificar_password(password, usuario.password_hash)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas o cuenta inactiva.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario.ultimo_acceso = datetime.now(timezone.utc)
    db.commit()

    access_token = crear_access_token(
        usuario_id=usuario.id_usuario,
        nombre=usuario.nombre,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout():
    return Response(status_code=status.HTTP_204_NO_CONTENT)
