# ADR-003: Selección del mecanismo de persistencia

## Estado

Aceptado

## Contexto

GanadApp requiere almacenar información relacionada con productores, establecimientos, usuarios, animales, eventos sanitarios, trazabilidad y stock de insumos.

El modelo de dominio definido en la SPEC presenta relaciones explícitas entre sus entidades:

- Un productor puede tener múltiples establecimientos.
- Un establecimiento puede contener múltiples animales.
- Un animal puede tener múltiples eventos sanitarios.
- Un usuario puede registrar múltiples eventos sanitarios.
- Un establecimiento administra stock de insumos.

Además, existen reglas de integridad que deben mantenerse en la persistencia, entre ellas:

- El identificador de cada animal debe ser único.
- Todo animal debe pertenecer a un establecimiento válido.
- Todo evento sanitario debe estar asociado a un animal existente.
- El stock no puede resultar negativo.
- Los registros históricos deben conservar su trazabilidad.

Estas características hacen que la persistencia deba soportar relaciones entre entidades, restricciones de integridad y consultas sobre información relacionada.

El sistema se encuentra actualmente en un contexto académico, con una estimación inicial de entre 20 y 100 productores y una concurrencia aproximada de entre 10 y 30 usuarios simultáneos. Sin embargo, la persistencia seleccionada debe permitir que el sistema evolucione sin requerir un cambio de modelo de datos por el solo hecho de aumentar moderadamente su utilización.

## Decisión

Se adopta una **base de datos relacional PostgreSQL** como mecanismo de persistencia de GanadApp.

PostgreSQL se utilizará como sistema de gestión de base de datos para almacenar las entidades y relaciones principales del dominio.

La decisión se fundamenta en que el modelo de GanadApp presenta una estructura fuertemente relacional y requiere mantener integridad entre entidades relacionadas.

Las relaciones principales serán representadas mediante claves primarias y foráneas, restricciones de integridad y estructuras relacionales adecuadas al dominio.

La persistencia mediante PostgreSQL es coherente con la arquitectura monolítica modular definida en ADR-001.

## Alternativas consideradas

### Opción A: PostgreSQL — seleccionada

PostgreSQL es un sistema de gestión de bases de datos relacional que permite representar las entidades del dominio mediante tablas relacionadas.

Ventajas:

- Soporta relaciones mediante claves primarias y foráneas.
- Permite aplicar restricciones de integridad.
- Es adecuado para modelos de datos estructurados y relacionados.
- Permite realizar consultas sobre múltiples entidades mediante operaciones relacionales.
- Proporciona mecanismos de transacciones.
- Permite mantener la consistencia de los datos.
- Es adecuado para el volumen de información previsto.
- Permite evolucionar el sistema sin cambiar el paradigma de persistencia.
- Es compatible con el stack tecnológico definido para el backend.

Desventajas:

- Requiere un servidor o servicio de base de datos.
- Su configuración y administración son mayores que las de una base de datos embebida como SQLite.
- Introduce una dependencia de infraestructura adicional durante el desarrollo.

### Opción B: SQLite — descartada como persistencia objetivo

SQLite es una base de datos relacional embebida que almacena la información en un archivo.

Presenta ventajas importantes para desarrollo local y prototipos:

- Configuración sencilla.
- No requiere un servidor de base de datos independiente.
- Facilita la ejecución local del proyecto.
- Tiene un costo operativo inicial bajo.

Sin embargo, se descarta como persistencia objetivo de GanadApp por las características del sistema.

La aplicación debe contemplar acceso concurrente de múltiples usuarios y una evolución hacia un entorno de utilización real. PostgreSQL proporciona mecanismos más adecuados para un sistema centralizado que debe administrar concurrencia, transacciones y crecimiento.

SQLite puede continuar siendo utilizada como herramienta auxiliar para desarrollo local o pruebas cuando resulte conveniente, pero no constituye la base de datos objetivo definida por esta decisión arquitectónica.

### Opción C: Base de datos NoSQL — descartada

Una alternativa NoSQL permitiría almacenar información mediante documentos, pares clave-valor u otros modelos no relacionales.

Se descarta porque el modelo de GanadApp presenta relaciones explícitas entre entidades que forman parte de las operaciones principales del sistema.

Por ejemplo:

- los animales pertenecen a establecimientos;
- los establecimientos pertenecen a productores;
- los eventos sanitarios se relacionan con animales;
- los eventos son registrados por usuarios;
- el stock se relaciona con establecimientos.

El uso de una base NoSQL requeriría resolver estas relaciones mediante estructuras embebidas, referencias o lógica adicional de aplicación. Esto no aporta una ventaja necesaria para el modelo actual.

La elección no se basa en que NoSQL sea técnicamente inadecuado en términos generales, sino en que sus características no proporcionan una ventaja suficiente para los requerimientos actuales de GanadApp.

### Opción D: Archivos estructurados — descartada

Otra alternativa sería almacenar la información directamente en archivos, por ejemplo JSON o CSV.

Esta alternativa puede ser útil para intercambio de datos, configuración o prototipos simples, pero no resulta adecuada como mecanismo principal de persistencia.

No proporciona de forma equivalente:

- relaciones entre entidades;
- restricciones de integridad referencial;
- transacciones;
- consultas relacionales;
- control adecuado de modificaciones concurrentes;
- mecanismos de integridad apropiados para los datos históricos.

Por estas razones, los archivos estructurados quedan fuera como mecanismo principal de persistencia.

## Criterios de decisión

Las alternativas se comparan según las características reales del modelo de GanadApp.

| Criterio | PostgreSQL | SQLite | NoSQL | Archivos |
|---|---|---|---|---|
| Relaciones entre entidades | Alta | Alta | Variable | Baja |
| Integridad referencial | Alta | Alta | Variable | Baja |
| Soporte de transacciones | Alta | Alta | Variable | Baja |
| Concurrencia multiusuario | Alta | Limitada | Alta/Variable | Baja |
| Consultas relacionales | Alta | Alta | Variable | Baja |
| Complejidad inicial | Media | Baja | Media/Alta | Baja |
| Adecuación al modelo de GanadApp | Alta | Media | Baja/Media | Baja |
| Evolución del sistema | Alta | Media | Variable | Baja |

La selección de PostgreSQL se basa principalmente en la estructura relacional del dominio, las reglas de integridad y la necesidad de disponer de una persistencia adecuada para un sistema multiusuario.

## Consecuencias

### Consecuencias positivas

- Las relaciones entre productores, establecimientos, animales, eventos y stock pueden representarse directamente mediante el modelo relacional.
- Las restricciones de integridad pueden mantenerse en la base de datos.
- Se facilita la conservación de la trazabilidad histórica.
- Las transacciones permiten mantener operaciones relacionadas de forma consistente.
- Se dispone de una solución adecuada para el escenario multiusuario previsto.
- La persistencia puede evolucionar junto con el modelo de dominio.
- Se mantiene coherencia con la decisión arquitectónica registrada en ADR-001.

### Consecuencias negativas

- PostgreSQL requiere mayor configuración que SQLite.
- El entorno de desarrollo debe disponer de una instancia de PostgreSQL cuando se utilice la configuración objetivo.
- El despliegue requiere administrar una base de datos independiente.
- Las migraciones del esquema deben gestionarse de manera controlada.
- Para un prototipo extremadamente pequeño, PostgreSQL puede representar una infraestructura mayor que la estrictamente necesaria.

## Riesgos y mitigaciones

### Configuración del entorno

La utilización de PostgreSQL requiere que el entorno de desarrollo y despliegue tenga acceso a una instancia configurada correctamente.

Como mitigación, la configuración de la base de datos deberá documentarse y mantenerse separada de las credenciales y parámetros sensibles.

### Evolución del esquema

Los cambios en las entidades pueden requerir modificaciones en el esquema de la base de datos.

Como mitigación, los cambios estructurales deberán gestionarse mediante migraciones versionadas.

### Dependencia de infraestructura

A diferencia de SQLite, PostgreSQL requiere un servicio de base de datos disponible.

Como mitigación, el entorno de desarrollo podrá utilizar una instancia local o una instancia equivalente al entorno de ejecución definido para el proyecto.

## Relación con otras decisiones arquitectónicas

Esta decisión se relaciona directamente con:

- **ADR-001:** establece la arquitectura monolítica modular y define PostgreSQL como base de datos relacional.
- **ADR-002:** establece el estilo arquitectónico monolítico modular.
- **SPEC-000:** define las entidades, relaciones y reglas de integridad del dominio.

ADR-003 especifica y fundamenta la decisión de persistencia que ADR-001 establece de forma general.

## Alcance de la decisión

Esta decisión establece PostgreSQL como persistencia objetivo del sistema.

La utilización eventual de SQLite para pruebas locales, prototipos o escenarios de desarrollo no modifica esta decisión mientras PostgreSQL continúe siendo la persistencia objetivo del sistema.

No se adopta ninguna tecnología NoSQL ni almacenamiento mediante archivos como mecanismo principal de persistencia.

## Revisión de la decisión

La decisión deberá reevaluarse si cambian sustancialmente las características del dominio o aparecen requerimientos que hagan necesario otro modelo de persistencia.

Entre los escenarios que podrían justificar una revisión se encuentran:

- incorporación de grandes volúmenes de datos no estructurados;
- requerimientos de escalabilidad que no puedan resolverse mediante PostgreSQL;
- incorporación de funcionalidades que requieran otro paradigma de almacenamiento;
- cambios significativos en el modelo de dominio;
- requerimientos de procesamiento que hagan necesaria una persistencia especializada.

Cualquier cambio deberá documentarse mediante un nuevo ADR.

## Referencias

- ADR-001 — Selección de arquitectura monolítica con base de datos relacional (PostgreSQL).
- ADR-002 — Selección del estilo arquitectónico.
- SPEC-000 — GanadApp - Gestión Ganadera.