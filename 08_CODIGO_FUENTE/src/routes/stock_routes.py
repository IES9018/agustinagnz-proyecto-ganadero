from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import usuario_actual
from src.models.establecimiento import Establecimiento
from src.services.stock_service import StockService


router = APIRouter(
    dependencies=[Depends(usuario_actual)]
)


@router.get("/api/establecimientos")
def listar_establecimientos(
    activos: bool = False,
    db: Session = Depends(get_db),
):
    statement = select(Establecimiento)

    if activos:
        statement = statement.where(
            Establecimiento.estado == "activo"
        )

    statement = statement.order_by(Establecimiento.nombre)

    establecimientos = db.scalars(statement).all()

    return [
        {
            "id_establecimiento": item.id_establecimiento,
            "id_productor": item.id_productor,
            "nombre": item.nombre,
            "ubicacion": item.ubicacion,
            "capacidad": item.capacidad,
            "estado": item.estado,
        }
        for item in establecimientos
    ]


@router.get("/api/stock")
def listar_stock(db: Session = Depends(get_db)):
    return StockService(db).listar()

@router.get("/api/stock/alertas")
def listar_alertas_stock(db: Session = Depends(get_db)):
    return StockService(db).listar_alertas()

@router.post("/api/stock", status_code=201)
def crear_insumo(data: dict, db: Session = Depends(get_db)):
    try:
        return StockService(db).crear(data)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="No se pudo guardar el insumo. Verifique los datos."
        )


@router.put("/api/stock/{stock_id}")
def actualizar_insumo(
    data: dict,
    stock_id: int = Path(..., ge=1, le=2147483647),
    db: Session = Depends(get_db)
):
    try:
        return StockService(db).actualizar(stock_id, data)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="No se pudo actualizar el insumo. Verifique los datos."
        )


@router.post("/api/stock/{stock_id}/movimientos")
def ajustar_stock(
    data: dict,
    stock_id: int = Path(..., ge=1, le=2147483647),
    db: Session = Depends(get_db)
):
    try:
        return StockService(db).ajustar_cantidad(
            stock_id=stock_id,
            tipo_operacion=data.get("tipo_operacion"),
            cantidad=data.get("cantidad")
        )
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="La operación no cumple las restricciones del stock."
        )