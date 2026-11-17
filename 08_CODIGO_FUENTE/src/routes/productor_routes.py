from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import usuario_actual
from src.services.productor_service import ProductorService


router = APIRouter(
    dependencies=[Depends(usuario_actual)]
)


@router.get("/api/productores")
def listar_productores(db: Session = Depends(get_db)):
    return ProductorService(db).listar()


@router.post("/api/productores", status_code=201)
def crear_productor(data: dict, db: Session = Depends(get_db)):
    try:
        return ProductorService(db).crear(data)
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="No se pudo registrar el productor.",
        )


@router.get("/api/productores/{productor_id}")
def obtener_productor(
    productor_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    try:
        return ProductorService(db).obtener(productor_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.put("/api/productores/{productor_id}")
def actualizar_productor(
    data: dict,
    productor_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    try:
        return ProductorService(db).actualizar(productor_id, data)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="No se pudo actualizar el productor.",
        )


@router.patch("/api/productores/{productor_id}/estado")
def cambiar_estado_productor(
    data: dict,
    productor_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    try:
        return ProductorService(db).cambiar_estado(
            productor_id,
            data.get("estado"),
        )
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.get("/api/productores/{productor_id}/establecimientos")
def listar_establecimientos_productor(
    productor_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    try:
        return ProductorService(db).listar_establecimientos(productor_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post(
    "/api/productores/{productor_id}/establecimientos",
    status_code=201,
)
def crear_establecimiento_productor(
    data: dict,
    productor_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    try:
        return ProductorService(db).crear_establecimiento(
            productor_id,
            data,
        )
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="No se pudo registrar el establecimiento.",
        )


@router.put("/api/establecimientos/{establecimiento_id}")
def actualizar_establecimiento(
    data: dict,
    establecimiento_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    try:
        return ProductorService(db).actualizar_establecimiento(
            establecimiento_id,
            data,
        )
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.patch("/api/establecimientos/{establecimiento_id}/estado")
def cambiar_estado_establecimiento(
    data: dict,
    establecimiento_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    try:
        return ProductorService(db).cambiar_estado_establecimiento(
            establecimiento_id,
            data.get("estado"),
        )
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))