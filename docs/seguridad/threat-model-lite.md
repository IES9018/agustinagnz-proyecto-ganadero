
# Modelo de amenazas lite — GanadApp

## 1. Objetivo

Este documento identifica amenazas de seguridad relevantes para las operaciones críticas de la API REST de GanadApp.

El análisis utiliza el modelo STRIDE como marco de clasificación y considera los componentes de autenticación, autorización, validación de entradas, lógica de negocio y persistencia.

El objetivo es identificar riesgos concretos, documentar los controles existentes y establecer mitigaciones verificables.

Este modelo tiene alcance acotado al MVP y no reemplaza una auditoría de seguridad integral ni una prueba de penetración.

## 2. Alcance

Se analizan las siguientes operaciones:

| Identificador | Endpoint | Funcionalidad |
|---|---|---|
| EP-01 | `POST /api/animales` | Registrar animales |
| EP-02 | `GET /api/animales/{animal_id}` | Consultar animales |
| EP-03 | `POST /api/animales/{animal_id}/sanidad` | Registrar eventos sanitarios |
| EP-04 | `DELETE /api/sanidad/{event_id}` | Anular eventos sanitarios |
| EP-05 | `POST /api/stock/{stock_id}/movimientos` | Registrar movimientos de stock |

Las operaciones protegidas requieren autenticación mediante token Bearer.

El análisis también considera el mecanismo de autenticación de `POST /auth/login`, porque constituye el punto de emisión de credenciales utilizadas por los endpoints protegidos.

## 3. Activos que requieren protección

| Activo | Información o recurso | Necesidad de protección |
|---|---|---|
| Credenciales | Contraseñas y hashes de usuarios | Confidencialidad e integridad |
| Tokens de acceso | JWT utilizados para autenticar solicitudes | Confidencialidad, integridad y vigencia |
| Datos de animales | Identificación, especie, raza, sexo y estado sanitario | Confidencialidad e integridad |
| Información sanitaria | Vacunaciones, tratamientos y fechas | Confidencialidad, integridad y trazabilidad |
| Información de stock | Cantidades, insumos y movimientos | Integridad y disponibilidad |
| Registros históricos | Eventos y operaciones realizadas | Integridad y trazabilidad |
| Base de datos | Entidades, relaciones y registros del sistema | Confidencialidad, integridad y disponibilidad |

## 4. Supuestos y límites

El sistema utiliza FastAPI, SQLAlchemy y PostgreSQL.

La autenticación se implementa mediante JWT firmados con HS256. La clave de firma se obtiene de variables de entorno y los tokens tienen un tiempo de expiración configurable.

Los routers de animales, sanidad, stock y trazabilidad utilizan la dependencia `usuario_actual` para exigir autenticación.

La validación de datos se realiza mediante esquemas Pydantic y reglas de los servicios cuando corresponde. Sin embargo, algunas operaciones reciben diccionarios genéricos, por lo que la validación en el borde debe reforzarse mediante esquemas específicos.

La dependencia de autenticación identifica al usuario, pero no debe considerarse equivalente a una autorización completa sobre cada establecimiento o recurso.

No se considera implementado un mecanismo de rate limiting mientras no exista una configuración verificable en la aplicación o en su infraestructura.

## 5. Análisis STRIDE

| Categoría STRIDE | Endpoint afectado | Amenaza concreta | Impacto | Mitigación y ubicación |
|---|---|---|---|---|
| Spoofing (suplantación) | EP-01 a EP-05 | Un atacante intenta ejecutar operaciones utilizando una identidad falsa, un token manipulado o un token vencido. | Acceso no autorizado a operaciones y datos del sistema. | `src/core/security.py`: validación de firma, algoritmo, expiración e identidad del usuario mediante `usuario_actual`. `src/routes/animal_routes.py`, `sanidad_routes.py`, `stock_routes.py` y `trazabilidad_routes.py`: dependencia de autenticación a nivel de router. |
| Tampering (manipulación) | EP-01 | Un atacante modifica el cuerpo de la solicitud para introducir datos inválidos, identificadores incorrectos o valores que vulneren las reglas del dominio. | Registros inconsistentes o asociación de animales con establecimientos incorrectos. | `src/schemas/animal.py`: validación de estructura, tipos y límites. `src/services/animal_service.py`: reglas de negocio. `src/repositories/animal_repository.py`: persistencia mediante SQLAlchemy. |
| Tampering (inyección) | EP-01, EP-03 y EP-05 | Un atacante introduce contenido malicioso en campos de texto o parámetros con el objetivo de alterar consultas SQL o el comportamiento de la aplicación. | Lectura, modificación o eliminación no autorizada de información. | `src/repositories/`: utilización de consultas parametrizadas mediante SQLAlchemy ORM. `src/schemas/` y `src/services/`: validación de entradas. Regla del arnés: prohibición de construir consultas SQL mediante concatenación de entradas externas. |
| Repudiation (repudio) | EP-03, EP-04 y EP-05 | Un usuario niega haber registrado, anulado o modificado un evento sanitario o un movimiento de stock. | Pérdida de trazabilidad y dificultad para determinar responsabilidades. | La identidad se obtiene mediante `usuario_actual` en `src/core/security.py`. Se debe asegurar el registro persistente del usuario responsable, fecha, operación y motivo en los eventos auditables. La autenticación por sí sola no constituye una auditoría completa. |
| Information Disclosure (exposición de información) | EP-02 y EP-03 | Un usuario autenticado consulta información de animales o eventos sanitarios que no debería estar disponible para su ámbito de acceso. | Exposición de información operativa y sanitaria de otros establecimientos. | `src/core/security.py`: identificación del usuario. Se requiere autorización por establecimiento en `src/routes/animal_routes.py` y en los servicios de consulta. La filtración de datos debe prevenirse también en las consultas de los repositorios. |
| Elevation of Privilege (elevación de privilegios) | EP-01 a EP-05 | Un usuario autenticado intenta ejecutar operaciones que exceden sus permisos o acceder a recursos pertenecientes a otro establecimiento. | Modificación o consulta de información fuera de las responsabilidades autorizadas. | Se requiere una política centralizada de autorización por operación y establecimiento. La autenticación de `usuario_actual` no reemplaza esta comprobación. Las reglas deben aplicarse antes de ejecutar los servicios y persistir cambios. |
| Denial of Service (denegación de servicio) | EP-01, EP-03 y EP-05; también `/auth/login` | Un atacante envía solicitudes repetidas, cuerpos excesivamente grandes o intentos de autenticación masivos. | Consumo excesivo de CPU, memoria y conexiones; indisponibilidad del sistema. | Se requiere rate limiting en middleware o infraestructura de despliegue, límites de tamaño de solicitudes, tiempos máximos de procesamiento y controles de intentos de autenticación. No se considera mitigado hasta verificar su implementación. |
| IDOR (acceso inseguro a objetos por identificador) | EP-02, EP-03, EP-04 y EP-05 | Un usuario modifica `animal_id`, `event_id` o `stock_id` para acceder o modificar un recurso que no pertenece a su ámbito autorizado. | Acceso o modificación de datos de otros establecimientos. | Se requiere verificar la pertenencia del recurso al establecimiento autorizado en los servicios y repositorios antes de consultar, modificar o anular. No es suficiente validar que el identificador sea un entero positivo o que el usuario esté autenticado. |

## 6. Controles existentes

Los siguientes controles forman parte de la implementación identificada:

- Autenticación mediante JWT Bearer.
- Verificación de la firma y expiración del token.
- Comprobación de que el usuario exista y se encuentre activo.
- Dependencia de autenticación aplicada a los routers protegidos.
- Validaciones de entrada mediante Pydantic en los esquemas disponibles.
- Validaciones de reglas de negocio en los servicios.
- Persistencia mediante SQLAlchemy y PostgreSQL.
- Contrato de API documentado mediante OpenAPI.

Estos controles reducen riesgos, pero no eliminan por sí solos todas las amenazas identificadas.

## 7. Brechas y controles pendientes

| Control pendiente | Amenaza relacionada | Prioridad |
|---|---|---|
| Autorización por establecimiento y recurso | IDOR, exposición de información y elevación de privilegios | Alta |
| Esquemas Pydantic específicos para todas las entradas de escritura | Tampering e inyección | Alta |
| Rate limiting para autenticación y operaciones de escritura | Denegación de servicio y fuerza bruta | Alta |
| Auditoría persistente de operaciones críticas | Repudio | Media/Alta |
| Límites de tamaño de solicitudes y controles de procesamiento | Denegación de servicio | Media |
| Pruebas negativas de autorización sobre identificadores ajenos | IDOR y elevación de privilegios | Alta |

Las brechas se consideran pendientes hasta contar con una implementación y evidencia de verificación.

## 8. Reglas operativas de seguridad

El desarrollo deberá cumplir las reglas establecidas en `.opencoderules`.

En particular:

- Ningún secreto o credencial podrá almacenarse directamente en el código fuente.
- Toda entrada externa deberá validarse antes de llegar a la lógica de negocio.
- Los endpoints nuevos deberán incorporarse al contrato OpenAPI antes de su implementación.
- Las operaciones sobre recursos deberán comprobar autenticación y autorización.
- Las consultas a la base de datos deberán utilizar mecanismos parametrizados.
- Las operaciones críticas deberán conservar evidencia de quién las realizó y cuándo.
- Los controles de seguridad deberán verificarse mediante pruebas automatizadas.

## 9. Verificación

La verificación del modelo deberá contemplar:

- Solicitudes sin token y con token inválido o vencido.
- Identificadores inexistentes y recursos pertenecientes a otro establecimiento.
- Datos con tipos, longitudes y formatos inválidos.
- Intentos de manipulación de parámetros y campos de entrada.
- Operaciones de anulación y modificación con verificación de trazabilidad.
- Solicitudes repetidas para comprobar los límites de frecuencia cuando se implemente rate limiting.

Las pruebas de contrato con Schemathesis permiten verificar respuestas, validaciones y comportamiento de la API frente a entradas generadas. No sustituyen las pruebas específicas de autorización por recurso, auditoría ni limitación de frecuencia.

## 10. Referencias

- `docs/arquitectura/api-contracts.yaml`
- `src/core/security.py`
- `src/routes/animal_routes.py`
- `src/routes/sanidad_routes.py`
- `src/routes/stock_routes.py`
- `src/services/`
- `src/repositories/`
- `.opencoderules`
- `docs/adr/ADR-001-stack-tecnologico.md`
- `docs/adr/ADR-002-estilo-arquitectonico.md`


