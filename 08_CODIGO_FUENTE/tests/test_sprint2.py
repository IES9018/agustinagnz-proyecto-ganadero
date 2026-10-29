import unittest
from datetime import date, datetime, timezone
from types import SimpleNamespace
from unittest.mock import Mock, patch

from src.models.establecimiento import Establecimiento
from src.models.evento_sanitario import EventoSanitario
from src.repositories.sanidad_repository import SanidadRepository
from src.services.stock_service import StockService


class TestStockService(unittest.TestCase):

    def setUp(self):
        patcher = patch("src.services.stock_service.StockRepository")
        self.addCleanup(patcher.stop)
        self.repository_class = patcher.start()

        self.db = Mock()
        self.db.get.return_value = SimpleNamespace()
        self.service = StockService(self.db)
        self.repo = self.repository_class.return_value

    def datos_validos(self):
        return {
            "tipo_insumo": "  Alimento balanceado  ",
            "categoria": "Alimentos",
            "cantidad": 10,
            "stock_minimo": 10,
            "stock_critico": 5,
            "unidad": "kg",
            "ubicacion": "Depósito",
            "id_establecimiento": 1,
        }

    def test_01_normaliza_datos_validos(self):
        datos = StockService._validar_datos(
            self.datos_validos(), incluir_cantidad=True
        )
        self.assertEqual(datos["tipo_insumo"], "Alimento balanceado")
        self.assertEqual(datos["cantidad"], 10.0)

    def test_02_rechaza_texto_obligatorio_vacio(self):
        datos = self.datos_validos()
        datos["tipo_insumo"] = "   "
        with self.assertRaises(ValueError):
            StockService._validar_datos(datos, incluir_cantidad=True)

    def test_03_rechaza_categoria_invalida(self):
        datos = self.datos_validos()
        datos["categoria"] = "Otra categoría"
        with self.assertRaises(ValueError):
            StockService._validar_datos(datos, incluir_cantidad=True)

    def test_04_rechaza_cantidad_inicial_negativa(self):
        datos = self.datos_validos()
        datos["cantidad"] = -1
        with self.assertRaises(ValueError):
            StockService._validar_datos(datos, incluir_cantidad=True)

    def test_05_rechaza_cantidad_no_finita(self):
        datos = self.datos_validos()
        datos["cantidad"] = float("nan")
        with self.assertRaises(ValueError):
            StockService._validar_datos(datos, incluir_cantidad=True)

    def test_06_rechaza_umbral_critico_superior_al_minimo(self):
        datos = self.datos_validos()
        datos["stock_minimo"] = 5
        datos["stock_critico"] = 6
        with self.assertRaises(ValueError):
            StockService._validar_datos(datos, incluir_cantidad=True)

    def test_07_crear_valida_establecimiento_y_guarda(self):
        self.repo.crear.return_value = {"id_stock": 1}
        resultado = self.service.crear(self.datos_validos())

        self.db.get.assert_called_once_with(Establecimiento, 1)
        self.repo.crear.assert_called_once()
        self.assertEqual(resultado["id_stock"], 1)

    def test_08_ingreso_incrementa_stock(self):
        item = SimpleNamespace(cantidad=10.0)
        self.repo.obtener.return_value = item
        self.repo.ajustar_cantidad.return_value = {"cantidad": 15.0}

        resultado = self.service.ajustar_cantidad(1, "ingreso", 5)

        self.repo.ajustar_cantidad.assert_called_once_with(item, 15.0)
        self.assertEqual(resultado["cantidad"], 15.0)

    def test_09_salida_puede_dejar_stock_en_cero(self):
        item = SimpleNamespace(cantidad=10.0)
        self.repo.obtener.return_value = item

        self.service.ajustar_cantidad(1, "salida", 10)

        self.repo.ajustar_cantidad.assert_called_once_with(item, 0.0)

    def test_10_rechaza_salida_que_produce_stock_negativo(self):
        item = SimpleNamespace(cantidad=5.0)
        self.repo.obtener.return_value = item

        with self.assertRaisesRegex(ValueError, "no puede resultar negativa"):
            self.service.ajustar_cantidad(1, "salida", 6)

        self.repo.ajustar_cantidad.assert_not_called()

    def test_11_rechaza_tipo_de_operacion_invalido(self):
        self.repo.obtener.return_value = SimpleNamespace(cantidad=10.0)

        with self.assertRaises(ValueError):
            self.service.ajustar_cantidad(1, "desconocida", 1)

        self.repo.ajustar_cantidad.assert_not_called()

    def test_12_rechaza_cantidad_de_operacion_cero(self):
        self.repo.obtener.return_value = SimpleNamespace(cantidad=10.0)

        with self.assertRaises(ValueError):
            self.service.ajustar_cantidad(1, "salida", 0)

        self.repo.ajustar_cantidad.assert_not_called()

    def test_13_rechaza_stock_inexistente(self):
        self.repo.obtener.return_value = None

        with self.assertRaises(LookupError):
            self.service.ajustar_cantidad(999, "salida", 1)


class TestAnulacionHistoricaSanitaria(unittest.TestCase):

    def crear_evento(self, estado="vigente"):
        return SimpleNamespace(
            id_evento=1,
            id_animal=10,
            tipo_evento="Vacunación",
            descripcion="Aplicación de vacuna",
            fecha=date(2026, 10, 1),
            fecha_proxima=None,
            estado=estado,
            motivo_anulacion="Motivo anterior" if estado == "anulado" else None,
            fecha_anulacion=(
                datetime(2026, 10, 2, tzinfo=timezone.utc)
                if estado == "anulado"
                else None
            ),
        )

    def test_14_anulacion_conserva_evento_y_registra_motivo(self):
        evento = self.crear_evento()
        db = Mock()
        db.get.return_value = evento
        repo = SanidadRepository(db)

        resultado = repo.anular_evento(1, "Registro duplicado")

        self.assertEqual(evento.estado, "anulado")
        self.assertEqual(evento.motivo_anulacion, "Registro duplicado")
        self.assertIsNotNone(evento.fecha_anulacion)
        self.assertEqual(resultado["id_evento"], 1)
        db.delete.assert_not_called()
        db.commit.assert_called_once()
        db.refresh.assert_called_once_with(evento)

    def test_15_segunda_anulacion_no_sobrescribe_el_historial(self):
        evento = self.crear_evento(estado="anulado")
        fecha_original = evento.fecha_anulacion
        db = Mock()
        db.get.return_value = evento
        repo = SanidadRepository(db)

        resultado = repo.anular_evento(1, "Otro motivo")

        self.assertEqual(evento.motivo_anulacion, "Motivo anterior")
        self.assertEqual(evento.fecha_anulacion, fecha_original)
        self.assertEqual(resultado["estado"], "anulado")
        db.commit.assert_not_called()
        db.delete.assert_not_called()

    def test_16_evento_inexistente_no_se_modifica(self):
        db = Mock()
        db.get.return_value = None
        repo = SanidadRepository(db)

        resultado = repo.anular_evento(999, "Motivo")

        self.assertIsNone(resultado)
        db.commit.assert_not_called()
        db.delete.assert_not_called()


if __name__ == "__main__":
    unittest.main()
