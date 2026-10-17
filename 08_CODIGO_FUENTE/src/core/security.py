
from fastapi import HTTPException, Request, status


def usuario_actual(request: Request) -> dict:
    usuario_id = request.session.get("usuario_id")
    rol = request.session.get("rol")

    if not usuario_id or rol not in {"productor", "personal_campo"}:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Debés iniciar sesión.",
            headers={"Location": "/login"},
        )

    return {
        "id_usuario": usuario_id,
        "rol": rol,
        "nombre": request.session.get("nombre", ""),
    }


def requiere_roles(*roles_permitidos: str):
    def verificar(request: Request) -> dict:
        usuario = usuario_actual(request)

        if usuario["rol"] not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tenés permisos para realizar esta operación.",
            )

        return usuario

    return verificar
