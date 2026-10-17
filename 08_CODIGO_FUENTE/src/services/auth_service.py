
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

ROLES_VALIDOS = {"productor", "personal_campo"}


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verificar_password(password: str, hashed: str) -> bool:
    try:
        return password_hash.verify(password, hashed)
    except Exception:
        return False
