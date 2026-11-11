
import os
import unittest
from datetime import timedelta

os.environ.setdefault(
    "SECRET_KEY",
    "clave-de-prueba-para-validacion-jwt-32-caracteres",
)

from fastapi import HTTPException

from src.core.security import (
    crear_access_token,
    decodificar_access_token,
)


class TestJWTSecurity(unittest.TestCase):

    def test_generar_y_validar_token(self):
        token = crear_access_token(
            usuario_id=1,
            nombre="Usuario de prueba",
        )

        payload = decodificar_access_token(token)

        self.assertEqual(payload["sub"], "1")
        self.assertEqual(payload["name"], "Usuario de prueba")
        self.assertIn("iat", payload)
        self.assertIn("exp", payload)

    def test_rechazar_token_invalido(self):
        with self.assertRaises(HTTPException) as contexto:
            decodificar_access_token("token.invalido")

        self.assertEqual(contexto.exception.status_code, 401)

    def test_rechazar_token_vencido(self):
        token = crear_access_token(
            usuario_id=1,
            nombre="Usuario de prueba",
            expires_delta=timedelta(seconds=-1),
        )

        with self.assertRaises(HTTPException) as contexto:
            decodificar_access_token(token)

        self.assertEqual(contexto.exception.status_code, 401)


if __name__ == "__main__":
    unittest.main()
