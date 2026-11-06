# Auditoría de calidad — Sprint 2

## 1. Objetivo

Registrar las incidencias detectadas durante la implementación y verificación de GanadApp, las correcciones realizadas, las pruebas ejecutadas y las limitaciones identificadas.

## 2. Incidencias y correcciones

### 2.1. Dependencia ausente en el entorno de ejecución

**Incidencia:** una primera ejecución de la suite falló durante la importación de módulos porque Python no encontraba `dotenv`.

**Análisis:** el módulo `src/core/database.py` importa `load_dotenv` desde `python-dotenv`. La dependencia estaba declarada en los requisitos; el problema correspondía al entorno utilizado para ejecutar las pruebas.

**Corrección:** se instaló la dependencia en el entorno activo y se verificó posteriormente la instalación del conjunto de dependencias.

**Verificación:** `python -m pip check` finalizó con el mensaje `No broken requirements found`.

### 2.2. Validaciones insuficientes

**Hallazgo:** se identificó la necesidad de reforzar las validaciones de datos en las operaciones de animales, sanidad y stock.

**Corrección:** se incorporaron validaciones de estructura, campos obligatorios, límites de longitud, identificadores, fechas, cantidades, categorías y coherencia de umbrales.

**Verificación:** se incorporaron pruebas unitarias específicas para los escenarios válidos e inválidos.

### 2.3. Historial y trazabilidad

**Hallazgo:** era necesario verificar la conservación de los cambios históricos de animales y eventos sanitarios, así como la integración y ordenamiento cronológico de los registros.

**Corrección:** se incorporaron verificaciones del historial de animales, la integración con eventos sanitarios, el ordenamiento temporal y la conservación de anulaciones.

**Verificación:** los casos correspondientes finalizaron correctamente en la suite unitaria.

### 2.4. Dependencias del proyecto

**Hallazgo:** el archivo de requisitos contenía dependencias no utilizadas por la implementación, entradas duplicadas y paquetes sin versión fijada.

**Corrección:** se depuró `08_CODIGO_FUENTE/requirements.txt`, conservando las dependencias necesarias para la ejecución de la aplicación. Las herramientas de desarrollo se separaron en `08_CODIGO_FUENTE/requirements-dev.txt`.

**Verificación:** la instalación de dependencias y `pip check` finalizaron correctamente. La suite de 45 pruebas también se ejecutó satisfactoriamente.

## 3. Resultados de las pruebas

La suite automatizada se ejecutó mediante:

```bash
python -m unittest discover -s tests -v
```

Resultados:

- Pruebas ejecutadas: 45.
- Pruebas aprobadas: 45.
- Pruebas fallidas: 0.
- Errores: 0.

La medición de cobertura se realizó mediante:

```
python -m coverage run --source=src -m unittest discover -s tests
python -m coverage report -m
```

Cobertura global informada: 67 %, sobre 560 instrucciones ejecutables.

Los resultados detallados por módulo se encuentran en `docs/pruebas/reporte-sprint2.md`.

## 4. Alcance de la auditoría

La suite verifica reglas de negocio y validaciones de animales, sanidad y stock, conservación de historiales y trazabilidad.

La cobertura obtenida permite identificar módulos con mayor y menor nivel de ejercicio. Los modelos y el repositorio de trazabilidad alcanzaron el 100 % en esta medición.

## 5. Limitaciones identificadas

- `src/main.py` registra un 0 % de cobertura.
- `src/repositories/stock_repository.py` registra un 28 %.
- `src/repositories/sanidad_repository.py` registra un 57 %.
- Las pruebas unitarias utilizan dependencias simuladas en los casos correspondientes.
- No se considera validada la integración completa con PostgreSQL.
- No se cubrieron exhaustivamente todas las rutas HTTP ni los flujos de interfaz.
- La cobertura del 67 % no representa cobertura completa de la aplicación.
- No se realizaron pruebas de rendimiento ni una auditoría exhaustiva de seguridad.

## 6. Integración continua

El workflow `.github/workflows/ci.yml` contempla:

- Configuración de Python 3.12.
- Instalación de dependencias de desarrollo.
- Compilación de los módulos Python.
- Ejecución de pruebas unitarias con medición de cobertura.
- Validación de mensajes de commit mediante Commitlint.

La aprobación efectiva del workflow debe confirmarse en GitHub Actions después de publicar los cambios y ejecutar el flujo mediante `push` o `pull_request`.

## 7. Evidencias y trazabilidad

- Suite unitaria: `08_CODIGO_FUENTE/tests/test_sprint2.py`.
- Dependencias de ejecución: `08_CODIGO_FUENTE/requirements.txt`.
- Dependencias de desarrollo: `08_CODIGO_FUENTE/requirements-dev.txt`.
- Workflow: `.github/workflows/ci.yml`.
- Reporte de pruebas: `docs/pruebas/reporte-sprint2.md`.
- Medición de cobertura: `python -m coverage report -m`.
- Commits y Pull Requests: consultar el historial del repositorio y GitHub.

## 8. Estado de la auditoría

La verificación local del Sprint 2 registra 45 pruebas aprobadas, sin fallos ni errores, compilación correcta y 67 % de cobertura sobre los módulos incluidos.

Las dependencias fueron depuradas y las herramientas de desarrollo quedaron separadas de las dependencias de ejecución. La documentación refleja los resultados medidos y las limitaciones detectadas.

La validación local queda completada. La aprobación de integración continua y la revisión mediante Pull Request requieren la ejecución correspondiente en GitHub.