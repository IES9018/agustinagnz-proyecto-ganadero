# Reporte de pruebas — Sprint 2

## 1. Objetivo

Documentar los resultados de las pruebas automatizadas ejecutadas localmente sobre las funcionalidades de GanadApp verificadas durante el Sprint 2.

## 2. Entorno de ejecución

- Lenguaje: Python 3.12.
- Framework de pruebas: `unittest`.
- Medición de cobertura: `coverage.py` 7.17.2.
- Base de datos de desarrollo: PostgreSQL.
- Suite: `08_CODIGO_FUENTE/tests/test_sprint2.py`.

## 3. Resultados generales

- Pruebas ejecutadas: 45.
- Pruebas aprobadas: 45.
- Pruebas fallidas: 0.
- Errores de ejecución: 0.
- Resultado: OK.

## 4. Cobertura de código

La medición se realizó con:

```bash
python -m coverage run --source=src -m unittest discover -s tests
python -m coverage report -m
```

| Archivo                                       | Cobertura |
| --------------------------------------------- | --------- |
| `src/core/database.py`                        | 73 %      |
| `src/main.py`                                 | 0 %       |
| `src/models/animal.py`                        | 100 %     |
| `src/models/establecimiento.py`               | 100 %     |
| `src/models/evento_sanitario.py`              | 100 %     |
| `src/models/historial_animal.py`              | 100 %     |
| `src/models/stock_insumo.py`                  | 100 %     |
| `src/repositories/animal_repository.py`       | 72 %      |
| `src/repositories/sanidad_repository.py`      | 57 %      |
| `src/repositories/stock_repository.py`        | 28 %      |
| `src/repositories/trazabilidad_repository.py` | 100 %     |
| `src/services/animal_service.py`              | 75 %      |
| `src/services/sanidad_service.py`             | 81 %      |
| `src/services/stock_service.py`               | 83 %      |
| Total                                         | 67 %      |

La medición comprende 560 instrucciones ejecutables, de las cuales 373 fueron cubiertas. El porcentaje corresponde a los módulos incluidos bajo `src`; no representa una validación completa de toda la aplicación.

## 5. Casos verificados

### Gestión de stock

- Normalización y validación de datos.
- Rechazo de campos obligatorios vacíos.
- Validación de categorías y límites de campos.
- Rechazo de cantidades negativas, no finitas, booleanas o iguales a cero cuando no corresponden.
- Validación de umbrales y establecimientos.
- Ingreso de insumos y actualización de existencias.
- Salidas que dejan el stock en cero.
- Prevención de operaciones que generan stock negativo.
- Rechazo de operaciones inválidas y registros inexistentes.

### Validaciones de animales

- Aceptación de datos válidos.
- Rechazo de estructuras de datos incorrectas.
- Validación de campos obligatorios y límites de longitud.
- Validación del formato y coherencia de fechas.
- Rechazo de fechas de nacimiento futuras.
- Validación del identificador y existencia del establecimiento.

### Validaciones sanitarias

- Creación de eventos con datos válidos.
- Validación de estructura, animal asociado y tipo de evento.
- Validación de longitud de campos y fechas.
- Rechazo de fechas futuras y fechas próximas anteriores al evento.
- Validación del motivo de anulación.
- Conservación del evento y del motivo de anulación.
- Protección frente a una segunda anulación que intente sobrescribir el historial.

### Historial y trazabilidad

- Registro histórico del alta de animales.
- Registro de modificaciones de animales.
- Ausencia de eventos históricos cuando no existen cambios.
- Consulta de trazabilidad de animales existentes e inexistentes.
- Integración del historial del animal con el historial sanitario.
- Orden cronológico de eventos, contemplando fechas con zona horaria.
- Conservación de las anulaciones en la trazabilidad.

## 6. Limitaciones

- Las pruebas unitarias utilizan dependencias simuladas (mocks) en los casos correspondientes.
- La suite no constituye una prueba integral de integración con PostgreSQL.
- `src/main.py` registra un 0 % de cobertura.
- Los repositorios de stock y sanidad conservan métodos sin cubrir.
- No se cubrieron exhaustivamente todas las rutas HTTP ni todos los flujos de interfaz.
- La cobertura del 67 % no demuestra que todos los requisitos funcionales estén validados.
- No se realizaron pruebas de rendimiento ni una auditoría exhaustiva de seguridad.

## 7. Non-Goals

Esta suite no pretende demostrar la cobertura completa de GanadApp, validar integralmente la interfaz gráfica, realizar pruebas de rendimiento o seguridad, ni sustituir las pruebas de integración con la base de datos.

## 8. Reproducción

Desde `08_CODIGO_FUENTE`, con Python 3.12:

```
python -m pip install -r requirements-dev.txt
python -m compileall -q src tests
python -m coverage run --source=src -m unittest discover -s tests -v
python -m coverage report -m
```

## 9. Estado

La ejecución local finalizó con 45 pruebas aprobadas, sin fallos ni errores. La cobertura global informada por Coverage fue del 67 % sobre los módulos incluidos.
