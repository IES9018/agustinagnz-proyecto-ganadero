# Reporte de pruebas — Sprint 2

## 1. Objetivo

Documentar los resultados de las pruebas unitarias ejecutadas localmente sobre funcionalidades de gestión de stock y conservación del historial sanitario de GanadApp.

## 2. Entorno de ejecución

- Lenguaje: Python 3.12.
- Framework de pruebas: `unittest`.
- Medición de cobertura: `coverage.py`.
- Ejecución: entorno virtual de `08_CODIGO_FUENTE`.

## 3. Resultados

- Pruebas ejecutadas: 16.
- Pruebas aprobadas: 16.
- Pruebas fallidas: 0.
- Errores de ejecución: 0.
- Resultado: OK.

### Cobertura medida

| Archivo | Cobertura |
|---|---:|
| `src/core/database.py` | 73 % |
| `src/main.py` | 0 % |
| `src/models/establecimiento.py` | 100 % |
| `src/models/evento_sanitario.py` | 100 % |
| `src/models/stock_insumo.py` | 100 % |
| `src/repositories/sanidad_repository.py` | 57 % |
| `src/repositories/stock_repository.py` | 28 % |
| `src/services/stock_service.py` | 83 % |
| **Total informado por Coverage** | **57 %** |

El porcentaje total corresponde a los archivos incluidos en el reporte de Coverage (272 instrucciones ejecutables). No debe interpretarse como cobertura completa de toda la aplicación.

## 4. Casos verificados

### Gestión de stock

- Normalización de datos válidos.
- Rechazo de campos de texto obligatorios vacíos.
- Rechazo de categorías inválidas.
- Rechazo de cantidades iniciales negativas y valores no finitos.
- Validación de umbrales de stock.
- Validación del establecimiento al crear un insumo.
- Incremento de existencias mediante ingresos.
- Permisión de una salida que deja el stock en cero.
- Rechazo de operaciones que producirían stock negativo.
- Rechazo de operaciones inválidas, cantidades iguales a cero y registros inexistentes.

### Historial sanitario

- Anulación de un evento conservando el registro y el motivo.
- Protección frente a una segunda anulación que intentaría sobrescribir los datos históricos.
- Ausencia de modificaciones cuando el evento no existe.

## 5. Limitaciones

- Las pruebas de servicios utilizan dependencias simuladas (*mocks*) en los casos correspondientes; no constituyen pruebas de integración con PostgreSQL.
- No se cubrieron de forma suficiente las rutas HTTP, el flujo completo de la aplicación ni todos los métodos de los repositorios.
- `src/main.py` registra un 0 % de cobertura.
- El porcentaje total informado no demuestra que todos los módulos de la aplicación hayan sido ejercitados.
- No se verificaron en esta suite todos los requisitos funcionales del Sprint 2.

## 6. Non-Goals

Esta suite no pretende demostrar la cobertura completa de GanadApp, validar la interfaz gráfica, realizar pruebas de rendimiento o seguridad, ni sustituir las pruebas de integración con la base de datos.

## 7. Comando de reproducción

Desde `08_CODIGO_FUENTE`, con el entorno virtual activado:

```bash
python -m unittest discover -s tests -v
python -m coverage run --source=src -m unittest discover -s tests -v
python -m coverage report -m
```

## 8. Estado

La suite unitaria ejecutada localmente finalizó con 16 pruebas aprobadas. La cobertura medida fue del 57 % en los archivos incluidos en el reporte. La cobertura y las limitaciones descritas deben considerarse al evaluar la calidad del Sprint 2.