
import getpass
import sys

from sqlalchemy import select

from src.core.database import Base, engine, SessionLocal
from src.models.animal import Animal
from src.models.establecimiento import Establecimiento
from src.models.evento_sanitario import EventoSanitario
from src.models.historial_animal import HistorialAnimal
from src.models.stock_insumo import StockInsumo
from src.models.usuario import Usuario
from src.services.auth_service import hash_password, ROLES_VALIDOS

Base.metadata.create_all(bind=engine)

nombre = input("Nombre: ").strip()
email = input("Correo electrónico: ").strip().lower()
rol = input("Rol (productor/personal_campo): ").strip().lower()
password = getpass.getpass("Contraseña (mínimo 12 caracteres): ")

if not nombre or not email or rol not in ROLES_VALIDOS:
    sys.exit("Error: revisá el nombre, correo y rol.")

if len(password) < 12:
    sys.exit("Error: la contraseña debe tener al menos 12 caracteres.")

with SessionLocal() as db:
    existente = db.scalar(
        select(Usuario).where(Usuario.email == email)
    )

    if existente:
        sys.exit("Error: ya existe un usuario con ese correo.")

    usuario = Usuario(
        nombre=nombre,
        email=email,
        password_hash=hash_password(password),
        rol=rol,
        estado_activo=True,
    )
    db.add(usuario)
    db.commit()

print(f"Usuario creado correctamente: {email} ({rol})")
