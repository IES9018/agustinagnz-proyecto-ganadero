from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.models.establecimiento import Establecimiento

from src.core.database import get_db
from src.services.stock_service import StockService

from src.core.security import requiere_roles

router = APIRouter(
    dependencies=[
        Depends(requiere_roles("productor", "personal_campo"))
    ]
)


@router.get("/api/establecimientos")
def listar_establecimientos(db: Session = Depends(get_db)):
    statement = select(Establecimiento).order_by(
        Establecimiento.nombre
    )
    establecimientos = db.scalars(statement).all()

    return [
        {
            "id_establecimiento": item.id_establecimiento,
            "nombre": item.nombre,
            "ubicacion": item.ubicacion
        }
        for item in establecimientos
    ]


@router.get("/api/stock")
def listar_stock(db: Session = Depends(get_db)):
    return StockService(db).listar()


@router.post("/api/stock", status_code=201)
def crear_insumo(data: dict, db: Session = Depends(get_db)):
    try:
        return StockService(db).crear(data)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="No se pudo guardar el insumo. Verifique los datos."
        )


@router.put("/api/stock/{stock_id}")
def actualizar_insumo(
    stock_id: int,
    data: dict,
    db: Session = Depends(get_db)
):
    try:
        return StockService(db).actualizar(stock_id, data)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="No se pudo actualizar el insumo. Verifique los datos."
        )


@router.post("/api/stock/{stock_id}/movimientos")
def ajustar_stock(
    stock_id: int,
    data: dict,
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
        raise HTTPException(status_code=400, detail=str(error))
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="La operación no cumple las restricciones del stock."
        )
