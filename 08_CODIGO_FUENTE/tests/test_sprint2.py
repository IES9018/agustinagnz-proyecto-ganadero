import unittest
from datetime import date, datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import Mock, patch

from src.models.establecimiento import Establecimiento
from src.models.evento_sanitario import EventoSanitario
from src.repositories.sanidad_repository import SanidadRepository
from src.services.stock_service import StockService
from src.services.animal_service import AnimalService
from src.services.sanidad_service import SanidadService


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


class TestAnimalServiceValidaciones(unittest.TestCase):

    def setUp(self):
        patcher = patch("src.services.animal_service.AnimalRepository")
        self.addCleanup(patcher.stop)
        self.repository_class = patcher.start()

        self.db = Mock()
        self.db.get.return_value = SimpleNamespace()
        self.service = AnimalService(self.db)
        self.repo = self.repository_class.return_value

    def datos_validos(self):
        return {
            "identificador": "AN-001",
            "especie": "Bovino",
            "raza": "Hereford",
            "fecha_nacimiento": "2024-05-10",
            "estado_sanitario": "Saludable",
            "id_establecimiento": 1,
        }

    def test_17_acepta_datos_validos(self):
        datos = self.service._validar(self.datos_validos())

        self.assertEqual(datos["identificador"], "AN-001")
        self.assertEqual(datos["fecha_nacimiento"], date(2024, 5, 10))
        self.assertEqual(datos["id_establecimiento"], 1)

    def test_18_rechaza_datos_que_no_son_diccionario(self):
        with self.assertRaises(ValueError):
            self.service._validar(None)

    def test_19_rechaza_campo_obligatorio_vacio(self):
        datos = self.datos_validos()
        datos["identificador"] = "   "

        with self.assertRaises(ValueError):
            self.service._validar(datos)

    def test_20_rechaza_texto_que_supera_limite_del_modelo(self):
        datos = self.datos_validos()
        datos["identificador"] = "A" * 101

        with self.assertRaises(ValueError):
            self.service._validar(datos)

    def test_21_rechaza_fecha_con_formato_invalido(self):
        datos = self.datos_validos()
        datos["fecha_nacimiento"] = "10/05/2024"

        with self.assertRaises(ValueError):
            self.service._validar(datos)

    def test_22_rechaza_fecha_de_nacimiento_futura(self):
        datos = self.datos_validos()
        datos["fecha_nacimiento"] = (
            date.today() + timedelta(days=1)
        ).isoformat()

        with self.assertRaises(ValueError):
            self.service._validar(datos)

    def test_23_rechaza_identificador_de_establecimiento_invalido(self):
        datos = self.datos_validos()
        datos["id_establecimiento"] = 0

        with self.assertRaises(ValueError):
            self.service._validar(datos)

    def test_24_rechaza_establecimiento_inexistente(self):
        self.db.get.return_value = None

        with self.assertRaisesRegex(ValueError, "no existe"):
            self.service._validar(self.datos_validos())

class TestSanidadServiceValidaciones(unittest.TestCase):

    def setUp(self):
        patcher = patch("src.services.sanidad_service.SanidadRepository")
        self.addCleanup(patcher.stop)
        self.repository_class = patcher.start()

        self.db = Mock()
        self.db.get.return_value = SimpleNamespace()
        self.service = SanidadService(self.db)
        self.repo = self.repository_class.return_value

    def datos_validos(self):
        return {
            "tipo_evento": "Vacunación",
            "descripcion": "Aplicación de vacuna",
            "fecha": date.today().isoformat(),
            "fecha_proxima": None,
        }

    def test_25_crea_evento_con_datos_validos(self):
        self.repo.crear_evento.return_value = {"id_evento": 1}

        resultado = self.service.crear_evento(10, self.datos_validos())

        self.repo.crear_evento.assert_called_once()
        self.assertEqual(resultado["id_evento"], 1)

    def test_26_rechaza_datos_que_no_son_diccionario(self):
        with self.assertRaises(ValueError):
            self.service.crear_evento(10, None)

    def test_27_rechaza_animal_inexistente(self):
        self.db.get.return_value = None

        with self.assertRaises(LookupError):
            self.service.crear_evento(999, self.datos_validos())

        self.repo.crear_evento.assert_not_called()

    def test_28_rechaza_tipo_de_evento_vacio(self):
        datos = self.datos_validos()
        datos["tipo_evento"] = "   "

        with self.assertRaises(ValueError):
            self.service.crear_evento(10, datos)

    def test_29_rechaza_tipo_de_evento_superior_a_100_caracteres(self):
        datos = self.datos_validos()
        datos["tipo_evento"] = "A" * 101

        with self.assertRaises(ValueError):
            self.service.crear_evento(10, datos)

    def test_30_rechaza_fecha_de_evento_invalida(self):
        datos = self.datos_validos()
        datos["fecha"] = "fecha incorrecta"

        with self.assertRaises(ValueError):
            self.service.crear_evento(10, datos)

    def test_31_rechaza_fecha_de_evento_futura(self):
        datos = self.datos_validos()
        datos["fecha"] = (
            date.today() + timedelta(days=1)
        ).isoformat()

        with self.assertRaises(ValueError):
            self.service.crear_evento(10, datos)

    def test_32_rechaza_fecha_proxima_anterior_al_evento(self):
        datos = self.datos_validos()
        datos["fecha"] = "2026-10-10"
        datos["fecha_proxima"] = "2026-10-09"

        with self.assertRaises(ValueError):
            self.service.crear_evento(10, datos)

    def test_33_rechaza_motivo_de_anulacion_vacio(self):
        with self.assertRaises(ValueError):
            self.service.eliminar_evento(1, "   ")

        self.repo.anular_evento.assert_not_called()

class TestStockServiceValidacionesAdicionales(unittest.TestCase):

    def datos_validos(self):
        return {
            "tipo_insumo": "Alimento balanceado",
            "categoria": "Alimentos",
            "cantidad": 10,
            "stock_minimo": 10,
            "stock_critico": 5,
            "unidad": "kg",
            "ubicacion": "Depósito",
            "id_establecimiento": 1,
        }

    def test_34_rechaza_tipo_insumo_superior_a_150_caracteres(self):
        datos = self.datos_validos()
        datos["tipo_insumo"] = "A" * 151

        with self.assertRaises(ValueError):
            StockService._validar_datos(datos, incluir_cantidad=True)

    def test_35_rechaza_unidad_superior_a_30_caracteres(self):
        datos = self.datos_validos()
        datos["unidad"] = "A" * 31

        with self.assertRaises(ValueError):
            StockService._validar_datos(datos, incluir_cantidad=True)

    def test_36_rechaza_ubicacion_superior_a_200_caracteres(self):
        datos = self.datos_validos()
        datos["ubicacion"] = "A" * 201

        with self.assertRaises(ValueError):
            StockService._validar_datos(datos, incluir_cantidad=True)

    def test_37_rechaza_cantidad_booleana(self):
        datos = self.datos_validos()
        datos["cantidad"] = True

        with self.assertRaises(ValueError):
            StockService._validar_datos(datos, incluir_cantidad=True)

    def test_38_rechaza_identificador_de_establecimiento_decimal(self):
        datos = self.datos_validos()
        datos["id_establecimiento"] = 1.5

        with self.assertRaises(ValueError):
            StockService._validar_datos(datos, incluir_cantidad=True)

if __name__ == "__main__":
    unittest.main()