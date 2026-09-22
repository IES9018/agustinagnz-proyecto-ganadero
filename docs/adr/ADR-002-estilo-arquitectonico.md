# ADR-002: Selección del estilo arquitectónico

## Estado

Aceptado

## Contexto

GanadApp es un sistema académico orientado a la gestión ganadera de pequeños y medianos productores de Malargüe. El sistema debe permitir gestionar usuarios, productores, establecimientos, animales, eventos sanitarios, trazabilidad y stock de insumos.

El proyecto se desarrolla en un contexto académico y el equipo de desarrollo está compuesto por una sola persona. Por lo tanto, la arquitectura debe permitir implementar, probar y mantener el sistema dentro de los plazos establecidos para las materias del proyecto, particularmente Prácticas Profesionales III.

La carga prevista para el sistema es baja a media, con una estimación inicial de entre 10 y 30 usuarios simultáneos y un volumen aproximado de entre 20 y 100 productores. No existe actualmente un requerimiento que justifique la distribución de la lógica de negocio en múltiples servicios independientes.

Los principales requerimientos funcionales presentan relaciones entre sí. La gestión de animales se vincula con establecimientos, los animales con eventos sanitarios y trazabilidad, y los establecimientos con el stock de insumos. Esta relación entre funcionalidades favorece una arquitectura que permita mantener la lógica de negocio integrada y organizada en módulos.

Además, el proyecto contempla una API REST y una interfaz web, con posibilidad de evolución futura. La arquitectura debe permitir incorporar nuevos módulos sin introducir una complejidad operativa desproporcionada para el tamaño y alcance del sistema.

## Decisión

Se adopta una **arquitectura monolítica modular**, organizada internamente mediante separación por capas y responsabilidades.

La aplicación se implementará como un único sistema desplegable, con un backend central que expone la API REST y contiene los módulos correspondientes a las distintas áreas funcionales del dominio.

La estructura modular permitirá separar responsabilidades dentro del monolito, evitando que la elección de una arquitectura monolítica implique concentrar toda la lógica en un único componente sin límites internos.

Los principales módulos funcionales estarán relacionados con:

- autenticación y control de acceso;
- productores y establecimientos;
- animales;
- eventos sanitarios y vacunación;
- trazabilidad;
- stock de insumos;
- reportes y alertas.

La arquitectura mantendrá separación por capas, diferenciando las responsabilidades de dominio, aplicación, infraestructura y presentación/API cuando corresponda.

Esta decisión es coherente con ADR-001, que establece la utilización de una arquitectura monolítica modular con un backend único.

## Alternativas consideradas

### Opción A: Arquitectura monolítica modular — seleccionada

Consiste en mantener el sistema como una única aplicación desplegable, pero organizada internamente mediante módulos y separación de responsabilidades.

Ventajas:

- Menor complejidad de implementación para un equipo de una persona.
- Menor cantidad de componentes que desarrollar, configurar y mantener.
- Facilita el desarrollo dentro de los plazos académicos.
- Permite compartir modelos y reglas de negocio relacionadas.
- Simplifica las pruebas y la depuración.
- Permite evolucionar progresivamente la estructura interna del sistema.
- Es adecuada para la carga de usuarios prevista.
- No requiere infraestructura distribuida para el escenario actual.

Desventajas:

- Los módulos comparten el mismo proceso de ejecución y despliegue.
- Una falla grave en el backend puede afectar al conjunto de la aplicación.
- La escalabilidad de componentes individuales es más limitada que en una arquitectura distribuida.
- Si no se respetan los límites entre módulos, puede producirse acoplamiento interno.

### Opción B: Arquitectura de microservicios — descartada

Consiste en dividir el sistema en múltiples servicios independientes, cada uno responsable de una parte del dominio, por ejemplo animales, sanidad, stock o usuarios.

La alternativa fue descartada para esta etapa debido principalmente a la relación entre complejidad, tamaño del equipo, carga prevista y tiempo disponible.

Desventajas frente a las necesidades actuales:

- Requiere administrar múltiples servicios independientes.
- Introduce complejidad de comunicación entre servicios.
- Requiere mayor esfuerzo de configuración, despliegue y monitoreo.
- Aumenta la cantidad de componentes que debe desarrollar y mantener una sola persona.
- La carga prevista de 10 a 30 usuarios simultáneos no requiere actualmente distribución de servicios para resolver problemas de escalabilidad.
- El tiempo disponible para el desarrollo académico hace que la infraestructura adicional represente un costo significativo.
- La separación prematura podría dificultar la depuración y las pruebas del sistema.

La principal ventaja de los microservicios, la posibilidad de escalar componentes de manera independiente, no constituye actualmente un requerimiento del sistema.

### Opción C: Arquitectura serverless — descartada

Consiste en ejecutar la lógica de backend mediante funciones o servicios administrados por un proveedor de infraestructura, evitando mantener un servidor de aplicación tradicional.

La alternativa fue descartada para esta etapa por las siguientes razones:

- Introduce dependencia de servicios y mecanismos específicos del proveedor utilizado.
- Requiere adaptar la arquitectura y el despliegue a un modelo de ejecución diferente.
- Puede aumentar la complejidad de configuración y operación para un proyecto desarrollado por una sola persona.
- No existe un requerimiento actual de escalabilidad automática que justifique adoptar este modelo.
- El sistema necesita mantener una estructura de dominio y módulos relacionados que puede implementarse de forma más directa dentro de un monolito modular.
- Incorporar servicios externos durante el MVP contradice el alcance definido actualmente en la SPEC.

La posibilidad de utilizar servicios administrados o serverless puede considerarse en una evolución futura si aparecen requerimientos que justifiquen ese cambio.

## Criterios de decisión

La comparación se realiza considerando las condiciones concretas de GanadApp:

| Criterio | Monolito modular | Microservicios | Serverless |
|---|---|---|---|
| Adecuación para un equipo de 1 persona | Alta | Baja | Media |
| Complejidad de implementación | Baja | Alta | Media/Alta |
| Complejidad operativa | Baja | Alta | Media |
| Tiempo de desarrollo académico | Bajo/Medio | Alto | Medio/Alto |
| Costo inicial de infraestructura | Bajo | Medio/Alto | Variable |
| Facilidad de pruebas y depuración | Alta | Media/Baja | Media |
| Necesidad de escalabilidad independiente | No requerida actualmente | Requerida principalmente en escenarios de mayor escala | No requerida actualmente |
| Adecuación al alcance del MVP | Alta | Baja | Baja/Media |
| Facilidad de evolución modular | Alta | Alta | Media |

La selección se basa principalmente en que el monolito modular satisface los requerimientos actuales con menor complejidad de implementación y operación, sin impedir una futura evolución arquitectónica si las necesidades del sistema cambian.

## Consecuencias

### Consecuencias positivas

- El desarrollo puede concentrarse en una única aplicación.
- Se reduce la cantidad de infraestructura necesaria para ejecutar el sistema.
- La comunicación entre los módulos internos es más sencilla que la comunicación entre servicios distribuidos.
- Las pruebas funcionales y de integración pueden realizarse sobre un entorno más simple.
- Se facilita la depuración durante el desarrollo académico.
- Los datos y reglas de negocio relacionadas pueden mantenerse coordinados dentro de la misma aplicación.
- La organización modular permite mantener límites internos y facilita futuras ampliaciones.
- El estilo arquitectónico es compatible con el alcance actual definido en la SPEC.

### Consecuencias negativas

- Los módulos comparten el mismo proceso de ejecución y despliegue.
- Una falla en el backend puede afectar a diferentes funcionalidades del sistema.
- La escalabilidad de cada módulo no puede realizarse de manera independiente.
- El crecimiento significativo de la carga podría requerir una revisión de la arquitectura.
- Si los límites entre módulos no se mantienen correctamente, puede aumentar el acoplamiento y dificultar el mantenimiento.
- La evolución hacia microservicios, si posteriormente fuera necesaria, requeriría separar componentes que inicialmente estarán dentro del mismo sistema.

## Riesgos y mitigaciones

### Acoplamiento entre módulos

Existe el riesgo de que los módulos compartan responsabilidades o accedan directamente a detalles internos de otros módulos.

Como mitigación, se mantendrán responsabilidades diferenciadas, interfaces claras y separación por capas.

### Sobrecarga del backend

El backend único concentra las operaciones del sistema y podría convertirse en un punto de saturación ante un crecimiento significativo.

Como mitigación, se deberán realizar pruebas de carga y monitorear los tiempos de respuesta y el consumo de recursos antes de aumentar significativamente la capacidad prevista.

### Crecimiento futuro del sistema

Si GanadApp incorpora un volumen de usuarios significativamente superior al previsto, requerimientos de escalabilidad independiente o funcionalidades que requieran despliegues separados, la arquitectura deberá ser reevaluada.

La adopción del monolito modular no impide analizar posteriormente una separación de componentes. En ese caso, la extracción de módulos deberá justificarse mediante un nuevo ADR.

## Restricciones relacionadas

Esta decisión se relaciona con las siguientes decisiones arquitectónicas:

- **ADR-001:** establece la adopción de una arquitectura monolítica modular para GanadApp.
- **ADR-003:** definirá la decisión específica sobre el mecanismo de persistencia.

La arquitectura seleccionada deberá mantenerse coherente con las restricciones establecidas en estos ADR.

## Alcance de la decisión

Esta decisión corresponde al estilo arquitectónico general del sistema y no determina en detalle la implementación interna de cada módulo.

La organización concreta de las capas, componentes, modelos y dependencias podrá evolucionar mientras se mantengan los límites arquitectónicos definidos y no se contradigan las decisiones registradas en los ADR correspondientes.

## Revisión de la decisión

La decisión deberá reevaluarse si ocurre alguno de los siguientes escenarios:

- El número de usuarios simultáneos supera de forma sostenida la capacidad prevista.
- Un módulo requiere escalabilidad independiente.
- Aparece un requerimiento que justifique despliegues independientes.
- La complejidad interna del monolito dificulta significativamente el mantenimiento.
- Se incorporan integraciones externas que requieran una arquitectura diferente.
- Las pruebas de carga demuestran que el backend único no puede satisfacer los objetivos de rendimiento establecidos.

En cualquiera de estos casos deberá analizarse una nueva decisión arquitectónica mediante un ADR.

## Referencias

- ADR-001 — Selección de arquitectura monolítica con base de datos relacional (PostgreSQL).
- SPEC-000 — GanadApp - Gestión Ganadera.
- C4 de Contexto — `docs/arquitectura/C4-contexto.md`.
- C4 de Contenedores — `docs/arquitectura/C4-contenedores.md`.