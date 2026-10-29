# Auditoría de calidad — Sprint 2

## 1. Objetivo

Registrar las incidencias detectadas durante la implementación y verificación de GanadApp, las correcciones realizadas y las limitaciones identificadas en las pruebas.

## 2. Incidencias y correcciones

### 2.1. Dependencia ausente en el entorno de ejecución de pruebas

**Incidencia:** la primera ejecución de la suite falló durante la importación de los módulos porque Python no encontraba `dotenv`.

**Análisis:** el módulo `src/core/database.py` importa `load_dotenv` desde `python-dotenv`. La dependencia ya estaba declarada en `08_CODIGO_FUENTE/requirements.txt`; el problema observado correspondía al entorno virtual utilizado para ejecutar las pruebas.

**Corrección:** se instaló `python-dotenv` en el entorno virtual activo.

**Verificación:** la suite se ejecutó nuevamente y finalizó con 16 pruebas aprobadas, sin fallos ni errores.

**Evidencia:** salida de `python -m unittest discover -s tests -v`.

### 2.2. Cobertura de pruebas insuficiente para considerar validada toda la aplicación

**Hallazgo:** la medición local informó un 57 % de cobertura global entre los archivos incluidos. `src/main.py` registró 0 %, `src/repositories/stock_repository.py` 28 % y `src/services/stock_service.py` 83 %.

**Corrección realizada:** se incorporó una suite de 16 pruebas unitarias para validar reglas de negocio de stock y la conservación de registros sanitarios al anular eventos.

**Limitación pendiente:** la suite no cubre suficientemente las rutas HTTP, la integración con PostgreSQL ni todos los métodos de los repositorios. El resultado no demuestra que toda la aplicación esté validada.

**Evidencia:** salida de `python -m coverage report -m`.

## 3. Alcance de las pruebas

Las pruebas unitarias cubren validaciones de datos de stock, operaciones de ingreso y salida, prevención de cantidades negativas y comportamiento de anulación de eventos sanitarios. Los casos implementados utilizan dependencias simuladas cuando corresponde.

No se consideran cubiertas por esta suite la totalidad de los requisitos funcionales, las pruebas de integración con PostgreSQL, las pruebas de interfaz, el rendimiento ni una auditoría exhaustiva de seguridad.

## 4. Errores de código asistido por IA

Durante esta etapa se detectó un problema de entorno al ejecutar las pruebas: faltaba instalar una dependencia que ya estaba declarada en el archivo de requisitos. La incidencia se corrigió instalando el paquete en el entorno virtual.

No se afirma que esta incidencia haya sido un defecto del código productivo. Cualquier otro error atribuido a código generado o asistido por IA deberá documentarse únicamente si se identifica y verifica con evidencia concreta.

## 5. Evidencias y trazabilidad

- Suite unitaria: `08_CODIGO_FUENTE/tests/test_sprint2.py`.
- Reporte de pruebas: `docs/pruebas/reporte-sprint2.md`.
- Medición de cobertura: comando `python -m coverage report -m`.
- Pull requests: incorporar los identificadores y enlaces correspondientes una vez verificados en GitHub.

## 6. Estado de la auditoría

La suite unitaria ejecutada localmente finalizó con 16 pruebas aprobadas. La cobertura medida fue del 57 % en los archivos incluidos en el reporte.

La auditoría queda pendiente de completar con la revisión de los entregables restantes del Sprint 2 y la incorporación de referencias verificadas a los Pull Requests. No se considera cerrado el sprint hasta completar esa revisión.