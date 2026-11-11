
# ADR-005: Selección de la estrategia web

## Estado

Aceptado

## Fecha

2026-11-11

## Decisión

Se adopta una estrategia web basada en una **Multiple Page Application (MPA)**, utilizando HTML, CSS y JavaScript, con FastAPI como servidor de aplicación y proveedor de los archivos de interfaz.

La comunicación entre la interfaz y el backend se realizará mediante la API REST definida en `docs/arquitectura/api-contracts.yaml`.

Cada módulo funcional contará con una página HTML independiente. La navegación entre módulos se realizará mediante rutas web tradicionales, mientras que las operaciones de consulta, registro, modificación y actualización de información utilizarán JavaScript para consumir los endpoints correspondientes.

La estrategia seleccionada no incorpora un framework SPA ni requiere un frontend desplegado como aplicación independiente.

La implementación deberá mantener las siguientes responsabilidades:

- **Presentación:** HTML para la estructura semántica y CSS para la presentación visual.
- **Interacción:** JavaScript para gestionar formularios, eventos y solicitudes a la API.
- **Backend:** FastAPI para servir las páginas, autenticar usuarios y exponer los servicios REST.
- **Persistencia:** PostgreSQL para almacenar la información del dominio.

## 1. Contexto

GanadApp es una aplicación web orientada a la gestión de establecimientos ganaderos de pequeños y medianos productores de Malargüe, Mendoza.

El MVP contempla funcionalidades de autenticación, gestión de animales, eventos sanitarios, trazabilidad y stock de insumos.

La interfaz está dirigida principalmente a usuarios autenticados que realizan operaciones administrativas y operativas sobre información del establecimiento.

La implementación tecnológica definida en ADR-004 utiliza HTML, CSS y JavaScript, sin incorporar un framework SPA como dependencia obligatoria.

La aplicación utiliza FastAPI como backend y expone una API REST para las operaciones del sistema.

La estrategia web debe resolver la organización de la navegación, la interacción entre interfaz y backend y las necesidades de despliegue, considerando las siguientes condiciones:

- El equipo de desarrollo está compuesto por una persona.
- El alcance corresponde a un MVP académico.
- La aplicación no requiere posicionamiento en buscadores para sus funcionalidades privadas.
- Las operaciones principales se realizan mediante formularios, tablas y consultas de información.
- El estado de la interfaz se concentra principalmente en cada módulo funcional.
- Se busca mantener una implementación compatible con el entorno de despliegue previsto para PP3.

## 2. Problema arquitectónico

Se deben evaluar distintas estrategias para organizar la interfaz web y su comunicación con el backend.

Las alternativas consideradas son:

1. SPA: aplicación de una sola página con navegación y estado gestionados principalmente en el cliente.
2. SSR: generación de HTML dinámico en el servidor para cada solicitud o navegación.
3. MPA: aplicación organizada en páginas independientes con navegación tradicional.
4. Solo API + frontend existente: backend limitado a proporcionar servicios REST y una interfaz desplegada y administrada por separado.

La elección debe minimizar la complejidad sin limitar las funcionalidades requeridas por el MVP.

## 3. Criterios de decisión

### 3.1 Necesidad de SEO

GanadApp es una aplicación de gestión cuyo contenido principal requiere autenticación.

Las páginas no representan contenido público que necesite posicionamiento en buscadores. Por lo tanto, SEO no constituye un requerimiento determinante para la selección de la estrategia web.

La generación dinámica de contenido optimizado para buscadores no justifica incorporar complejidad adicional al MVP.

### 3.2 Complejidad de estado

Las funcionalidades principales se organizan en módulos independientes.

La gestión de animales, sanidad, stock y trazabilidad utiliza formularios, tablas y respuestas de la API.

El estado necesario para estas operaciones puede mantenerse dentro de cada página mediante JavaScript, sin requerir un estado global complejo ni un mecanismo de navegación completamente controlado por el cliente.

Una SPA introduciría herramientas y convenciones adicionales para resolver necesidades que actualmente no justifican esa complejidad.

### 3.3 Hosting objetivo de PP3

La estrategia seleccionada permite desplegar la interfaz y el backend dentro del mismo servicio de aplicación FastAPI.

Esto evita mantener dos aplicaciones independientes y simplifica:

- la configuración del entorno;
- la gestión de variables de entorno;
- la comunicación entre frontend y backend;
- la configuración de dominios;
- la administración de CORS;
- el proceso de despliegue.

El diseño es compatible con un entorno de despliegue que permita ejecutar FastAPI y conectar el servicio con PostgreSQL.

La decisión no depende de un proveedor específico de hosting.

### 3.4 Tamaño del equipo

El desarrollo está a cargo de una sola persona dentro de un contexto académico.

Por lo tanto, se prioriza una estrategia que reduzca la cantidad de tecnologías, dependencias y componentes que deben configurarse, probarse y mantenerse.

La utilización de páginas independientes y JavaScript nativo permite concentrar el esfuerzo en las funcionalidades del dominio y en la calidad de la API.

## 4. Alternativas consideradas

### Opción A: SPA — descartada

Una Single Page Application concentra la navegación y la actualización de vistas en una única aplicación ejecutada en el navegador.

Normalmente utiliza un framework o biblioteca como React, Vue o Angular y administra el estado de la interfaz mediante mecanismos específicos.

Ventajas:

- Navegación fluida sin recargar completamente el documento.
- Administración centralizada del estado.
- Adecuada para interfaces altamente interactivas.
- Permite desarrollar experiencias de usuario complejas.

Desventajas para GanadApp:

- Introduce mayor complejidad de configuración y mantenimiento.
- Requiere administrar el ciclo de vida de componentes y el estado de la aplicación.
- Puede necesitar herramientas adicionales de compilación y empaquetado.
- No existe actualmente una necesidad de interacción que justifique su adopción.
- Aumenta el esfuerzo de desarrollo para un equipo de una persona.

Se descarta para el MVP porque sus ventajas no compensan la complejidad adicional.

### Opción B: SSR — descartada

Server-Side Rendering consiste en generar HTML dinámicamente desde el servidor y enviarlo al navegador.

Puede resultar adecuado para sitios con contenido público, necesidades de SEO o páginas cuyo contenido deba generarse según los datos de cada solicitud.

Ventajas:

- El navegador recibe HTML generado por el servidor.
- Puede favorecer la indexación de contenido público.
- Permite centralizar parte de la generación de vistas en el backend.

Desventajas para GanadApp:

- No existe un requerimiento significativo de SEO.
- La aplicación está orientada a usuarios autenticados.
- Introducir un motor de plantillas y una estrategia de renderizado dinámico no es necesario para las pantallas actuales.
- Aumentaría la responsabilidad del backend sobre la generación de las vistas.

Se descarta como estrategia específica de renderizado para el MVP. La implementación actual utiliza archivos HTML servidos por FastAPI, no generación dinámica de plantillas.

### Opción C: MPA — seleccionada

Una Multiple Page Application organiza la interfaz en páginas independientes, cada una asociada a una funcionalidad o módulo.

La navegación entre módulos se realiza mediante rutas web tradicionales. JavaScript permite implementar interacciones y consumir la API REST sin necesidad de convertir toda la aplicación en una SPA.

Ventajas:

- Menor complejidad de implementación.
- Separación clara entre módulos y páginas.
- No requiere un framework SPA.
- Compatible con HTML, CSS y JavaScript nativo.
- Permite reutilizar una estructura visual común.
- Facilita las pruebas y el mantenimiento por funcionalidad.
- Puede servirse desde el mismo backend FastAPI.
- Se ajusta al tamaño del equipo y al alcance académico.

Desventajas:

- La navegación entre páginas puede provocar recargas del documento.
- El estado compartido entre páginas requiere mecanismos explícitos.
- La reutilización de componentes depende de convenciones y organización del código.

Se selecciona porque satisface los requerimientos actuales con una complejidad proporcional al alcance del sistema.

### Opción D: Solo API + frontend existente independiente — descartada

Consiste en mantener el backend exclusivamente como proveedor de servicios REST y desplegar la interfaz como una aplicación independiente.

Ventajas:

- Separación física entre frontend y backend.
- Posibilidad de desplegar cada componente de manera independiente.
- Facilita incorporar otros clientes que consuman la misma API.

Desventajas para GanadApp:

- Requiere administrar dos componentes desplegables.
- Puede introducir configuración adicional de CORS.
- Aumenta la complejidad de configuración de dominios y entornos.
- No existe actualmente un frontend independiente que justifique esta separación.
- Incrementa el esfuerzo operativo para un equipo de una persona.

Se descarta para el MVP porque la interfaz existente puede servirse desde FastAPI sin introducir una infraestructura adicional.

## 5. Comparación de alternativas

| Criterio | SPA | SSR | MPA | Solo API + frontend independiente |
|---|---|---|---|---|
| Necesidad de SEO | No determinante | Ventaja potencial | Suficiente para aplicación privada | Depende del frontend |
| Complejidad de estado | Media/Alta | Baja/Media | Baja/Media | Depende del frontend |
| Complejidad de implementación | Media/Alta | Media | Baja | Media |
| Compatibilidad con FastAPI | Alta | Alta | Alta | Alta |
| Complejidad de despliegue | Media | Baja/Media | Baja | Media/Alta |
| Adecuación a equipo de una persona | Media/Baja | Media | Alta | Media/Baja |
| Adecuación al MVP | Baja/Media | Media | Alta | Baja/Media |

La evaluación prioriza la simplicidad de implementación y operación, la compatibilidad con la arquitectura existente y el tamaño del equipo.

## 6. Consecuencias de la decisión

### Consecuencias positivas

- Se mantiene coherencia con ADR-004.
- Se aprovecha el frontend HTML, CSS y JavaScript existente.
- No se incorporan dependencias de frameworks SPA.
- La interfaz y la API pueden desplegarse dentro de una misma aplicación.
- Se mantiene una separación funcional entre páginas y módulos.
- Se simplifica la configuración del entorno de desarrollo y despliegue.
- Las operaciones de datos continúan centralizadas en la API REST.
- Se facilita la evolución incremental del MVP.

### Consecuencias negativas

- La navegación tradicional puede generar recargas completas de página.
- El estado de interacción no se comparte automáticamente entre módulos.
- La reutilización de componentes requiere convenciones de desarrollo.
- Una evolución hacia una interfaz altamente interactiva podría justificar una nueva evaluación.
- El frontend y el backend comparten el mismo ciclo de despliegue.

## 7. Riesgos y mitigaciones

### Acoplamiento entre interfaz y backend

Existe el riesgo de que el JavaScript de cada página dependa directamente de detalles internos de la implementación del backend.

Como mitigación, la comunicación deberá realizarse mediante los contratos documentados en `docs/arquitectura/api-contracts.yaml`.

### Duplicación de lógica de presentación

La existencia de múltiples páginas puede provocar duplicación de código HTML, CSS o JavaScript.

Como mitigación, se deberán mantener convenciones de estructura, componentes reutilizables y recursos compartidos.

### Complejidad creciente de la interfaz

Si se incorporan funcionalidades que requieren estado global, navegación compleja o actualizaciones intensivas, la estrategia MPA podría resultar insuficiente.

Como mitigación, se deberá reevaluar la estrategia mediante un nuevo ADR antes de incorporar un framework SPA.

### Despliegue conjunto

La interfaz y el backend comparten el servicio de aplicación.

Como mitigación, se mantendrán separadas las responsabilidades del frontend, la API y la persistencia, evitando dependencias innecesarias entre sus componentes.

## 8. Relación con otras decisiones arquitectónicas

Esta decisión se relaciona con:

- **ADR-001:** establece la arquitectura monolítica modular y el backend centralizado.
- **ADR-002:** establece la separación modular y por capas.
- **ADR-003:** define PostgreSQL como mecanismo de persistencia.
- **ADR-004:** establece HTML, CSS y JavaScript como stack de interfaz sin framework SPA obligatorio.
- **SPEC-000:** define los requerimientos funcionales y las restricciones del MVP.
- **Contrato OpenAPI:** establece las operaciones disponibles para la comunicación entre interfaz y backend.

## 9. Alcance de la decisión

Esta decisión establece la estrategia de organización y comunicación de la interfaz web para el MVP.

No impide incorporar posteriormente un framework de frontend, un mecanismo de renderizado dinámico o un frontend independiente si aparecen requerimientos que justifiquen esa evolución.

Cualquier modificación significativa deberá documentarse mediante un nuevo ADR.

## 10. Revisión de la decisión

La estrategia deberá reevaluarse si ocurre alguno de los siguientes escenarios:

- Se incorporan funcionalidades que requieren estado global complejo.
- La navegación tradicional afecta significativamente la experiencia de usuario.
- Se incorpora una aplicación móvil o un frontend independiente.
- Aparecen requerimientos de SEO para contenido público.
- El despliegue conjunto limita la evolución o disponibilidad del sistema.
- La complejidad de la interfaz justifica adoptar un framework especializado.


## Referencias

- [ADR-001 — Selección del stack tecnológico](ADR-001-stack-tecnologico.md).
- [ADR-002 — Selección del estilo arquitectónico](ADR-002-estilo-arquitectonico.md).
- [ADR-003 — Selección de persistencia](ADR-003-persistencia.md).
- [ADR-004 — Selección del stack de interfaz de usuario](ADR-004-stack-ui.md).
- [SPEC — Especificación de requisitos de GanadApp](../SPEC.md).
- [Contrato de API — OpenAPI](../arquitectura/api-contracts.yaml).