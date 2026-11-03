
from fastapi import HTTPException, Request, status


def usuario_actual(request: Request) -> dict:
    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Debés iniciar sesión."
        )

    return {
        "id_usuario": usuario_id,
        "nombre": request.session.get("nombre", ""),
    }
