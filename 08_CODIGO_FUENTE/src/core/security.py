
import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select

from src.core.database import SessionLocal
from src.models.usuario import Usuario


JWT_SECRET_KEY = (
    os.getenv("JWT_SECRET_KEY")
    or os.getenv("SECRET_KEY")
)

JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)

if not JWT_SECRET_KEY:
    raise RuntimeError(
        "Debe configurarse JWT_SECRET_KEY o SECRET_KEY."
    )

if JWT_ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
    raise RuntimeError(
        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES debe ser mayor que cero."
    )

bearer_scheme = HTTPBearer(auto_error=False)


def crear_access_token(
    usuario_id: int,
    nombre: str,
    expires_delta: timedelta | None = None,
) -> str:
    ahora = datetime.now(timezone.utc)

    expiracion = (
        ahora + expires_delta
        if expires_delta is not None
        else ahora + timedelta(
            minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": str(usuario_id),
        "name": nombre,
        "iat": ahora,
        "exp": expiracion,
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def decodificar_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={
                "require": ["sub", "iat", "exp"],
            },
        )

        if not payload.get("sub"):
            raise InvalidTokenError("Token sin identificador de usuario.")

        return payload

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o vencido.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def usuario_actual(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
) -> dict:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere un token Bearer.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decodificar_access_token(credentials.credentials)

    try:
        usuario_id = int(payload["sub"])
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identificador de usuario inválido.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    with SessionLocal() as db:
        usuario = db.scalar(
            select(Usuario).where(
                Usuario.id_usuario == usuario_id
            )
        )

        if usuario is None or not usuario.estado_activo:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario inexistente o inactivo.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "id_usuario": usuario.id_usuario,
            "nombre": usuario.nombre,
        }
