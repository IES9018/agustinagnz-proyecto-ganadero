# Auditoría de desarrollo asistido por IA y seguridad — Sprint 3

## 1. Objetivo

Registrar los incidentes identificados durante el uso de herramientas de inteligencia artificial en el desarrollo de GanadApp, las medidas de corrección aplicadas y el estado de las verificaciones de calidad y seguridad realizadas durante el Sprint 3.

La auditoría considera la intervención humana en las decisiones técnicas, la revisión de las propuestas generadas y la evidencia obtenida mediante pruebas automatizadas e inspección del código fuente.

## 2. Incidentes relacionados con el uso de IA

Durante el desarrollo se identificaron dos tipos de incidentes.

### 2.1. Propuestas de código incompatibles con la arquitectura o los requisitos

Se recibieron propuestas de implementación que no respetaban completamente la arquitectura existente o los requisitos definidos para el proyecto.

**Corrección aplicada:** se rechazaron las propuestas que no correspondían con el diseño y los requisitos de GanadApp. Se reforzó la revisión previa a cualquier implementación, contrastando las soluciones sugeridas con el código existente y las decisiones técnicas del proyecto.

### 2.2. Documentación y contratos con información incorrecta

Se identificaron propuestas de documentación y contratos que contenían información incorrecta o que no representaban fielmente el estado real del sistema.

**Corrección aplicada:** se revisó la documentación contra la implementación efectiva y los requisitos establecidos. Se corrigieron las inconsistencias antes de considerar los documentos como válidos.

### 2.3. Medidas de control adoptadas

La implementación, las decisiones de diseño, las pruebas y las verificaciones fueron realizadas por la estudiante. Las herramientas de IA se utilizaron como apoyo, sin delegarles la aceptación automática de cambios.

Se estableció como criterio de trabajo que ninguna propuesta se incorpora sin verificar su correspondencia con la arquitectura, los requisitos y el comportamiento real de la aplicación.

## 3. Estado de las verificaciones de calidad

La suite automatizada se ejecutó desde el directorio `08_CODIGO_FUENTE` mediante:

`python -m pytest -q`

Resultado obtenido:

| Indicador | Resultado |
|---|---:|
| Pruebas ejecutadas | 48 |
| Pruebas aprobadas | 48 |
| Pruebas fallidas | 0 |
| Duración | 8,07 segundos |

La ejecución finalizó correctamente, sin pruebas fallidas.

## 4. Verificaciones de seguridad

### 4.1. Autenticación

La aplicación utiliza autenticación basada en tokens JWT con el algoritmo HS256.

La configuración contempla:

- Clave de firma mediante la variable de entorno `JWT_SECRET_KEY`, con compatibilidad para `SECRET_KEY`.
- Tiempo de expiración configurable mediante `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`.
- Vigencia predeterminada de 30 minutos.
- Validación de los tokens mediante la biblioteca PyJWT.
- Esquema de autenticación HTTP Bearer.
- Rechazo de tokens inválidos o vencidos.

La aplicación impide iniciar su configuración de seguridad cuando no existe una clave de firma o cuando el tiempo de expiración configurado no es válido.

### 4.2. Validación del usuario

La dependencia `usuario_actual` obtiene el token Bearer, valida su contenido y consulta al usuario correspondiente en la base de datos.

Se rechazan las solicitudes cuando no se proporciona un token, el identificador no es válido, el usuario no existe o su cuenta está inactiva.

### 4.3. Protección de rutas API

Se verificó mediante inspección del código fuente que los siguientes routers utilizan `Depends(usuario_actual)` como dependencia:

| Router | Protección verificada |
|---|---|
| `animal_routes.py` | `usuario_actual` |
| `sanidad_routes.py` | `usuario_actual` |
| `stock_routes.py` | `usuario_actual` |
| `trazabilidad_routes.py` | `usuario_actual` |

La verificación confirma la aplicación de la dependencia de autenticación a estos grupos de rutas API.

Las rutas que entregan las páginas HTML se implementan por separado en `src/main.py`. En el código inspeccionado, estas rutas utilizan `FileResponse` sin declarar directamente `Depends(usuario_actual)`. Por lo tanto, no se considera verificada la protección de acceso a las páginas HTML en el servidor. La protección de las operaciones API no debe confundirse con la protección de la entrega de documentos HTML.

### 4.4. Gestión de secretos

Las claves de autenticación y la conexión a la base de datos se configuran mediante variables de entorno.

Durante el despliegue en Render se configuraron `DATABASE_URL` y `JWT_SECRET_KEY`, evitando incorporar sus valores al repositorio.

## 5. Verificación del despliegue

GanadApp se desplegó en Render mediante un servicio web y una instancia PostgreSQL ubicados en Virginia (US East).

Se comprobó que el servicio alcanzara el estado operativo, que estableciera conexión con la base de datos y que la aplicación pudiera utilizarse desde su dirección pública.

La configuración y el procedimiento de reproducción se documentan en `docs/deploy/deploy.md`.

## 6. Cumplimiento de los entregables de presupuestos de rendimiento

Se completaron por separado los dos entregables relacionados con los presupuestos de rendimiento, correspondientes a consignas diferentes.

### 6.1. TP4: definición de presupuestos como objetivos numéricos

Se documentaron los objetivos cuantitativos de rendimiento en `docs/arquitectura/presupuestos-rendimiento.md`. Este documento establece los valores de referencia que debe alcanzar la aplicación y funciona como criterio para evaluar su rendimiento.

### 6.2. Sprint 3: presupuestos medidos y evidencia

Se realizaron mediciones sobre las pantallas de Gestión de Animales y Sanidad en el entorno desplegado en Render. Los resultados de Lighthouse y las mediciones del JavaScript inicial se registraron y evaluaron en el documento de presupuestos de rendimiento del Sprint 3.

La evidencia de las mediciones se centralizó en `docs/performance/`, donde se incorporaron los informes de Lighthouse `lighthouse-animales.html` y `lighthouse-sanidad.html`, junto con el documento `presupuestos-sprint3.md`, que consolida los resultados obtenidos y evalúa su cumplimiento respecto de los objetivos establecidos.

Las mediciones permitieron comprobar el cumplimiento del presupuesto de JavaScript inicial en ambas pantallas y detectar que Gestión de Animales no alcanza el objetivo de LCP establecido. El INP permanece sin verificar por falta de mediciones de campo.

De esta manera, se cumple por separado con la definición de objetivos numéricos solicitada en TP4 y con la medición respaldada por evidencia solicitada en Sprint 3.

## 7. Conclusión de la auditoría

Durante el Sprint 3 se identificaron y corrigieron inconsistencias en las propuestas de código y documentación generadas con asistencia de IA. Se reforzó la revisión humana como mecanismo de control para evitar que soluciones incorrectas se incorporen al proyecto.

La suite automatizada finalizó con 48 pruebas aprobadas y se verificó la aplicación de autenticación JWT a los routers principales de la API. También se comprobó el funcionamiento del despliegue en Render y la conexión con PostgreSQL.

Se completaron los dos entregables de presupuestos de rendimiento: la definición de objetivos numéricos correspondiente a TP4 y la medición de resultados con evidencia correspondiente a Sprint 3. Los resultados muestran cumplimiento del presupuesto de JavaScript inicial en ambas pantallas, pero un incumplimiento del objetivo de LCP en Gestión de Animales. El INP permanece sin verificar.

La auditoría deja constancia de una limitación en el alcance de la verificación: las rutas que sirven páginas HTML no declaran directamente la dependencia de autenticación en el servidor. Por este motivo, no corresponde afirmar que toda la superficie de acceso de la aplicación está protegida.

El estado documentado refleja las verificaciones efectivamente realizadas y diferencia los controles comprobados de aquellos cuyo cumplimiento no se ha demostrado.