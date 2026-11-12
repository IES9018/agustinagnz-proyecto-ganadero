# ADR-006 — Estrategia de adaptación mobile

## Estado

Aceptado

## Fecha

2026-11-12


## 1. Contexto y problema

GanadApp está orientado a pequeños y medianos productores ganaderos. Sus usuarios necesitan consultar y registrar información relacionada con animales, movimientos y actividades sanitarias. Parte de estas tareas puede realizarse desde establecimientos rurales, donde el acceso a internet y la calidad de la conexión pueden ser variables.

El proyecto se desarrolla de manera individual y tiene un alcance académico definido. La estrategia mobile debe permitir utilizar las funcionalidades principales desde teléfonos y tabletas sin introducir una complejidad de desarrollo y mantenimiento que comprometa la continuidad del proyecto.

Se deben evaluar cuatro alternativas: aplicación web responsive, Progressive Web App (PWA), aplicación nativa y aplicación híbrida.

## 2. Criterios de decisión

Se consideran los siguientes criterios:

1. **Costo de mantenimiento para una persona:** cantidad de tecnologías, bases de código, procesos de publicación y componentes adicionales que debe mantener una sola desarrolladora.
2. **Necesidad de funcionamiento offline:** capacidad para consultar o registrar información cuando el dispositivo no tiene conexión y sincronizarla posteriormente.
3. **Acceso al hardware:** disponibilidad de funciones del dispositivo, como cámara, almacenamiento, notificaciones y otros sensores.
4. **Tiempo hasta el cierre de PP3:** esfuerzo necesario para implementar, probar y documentar la solución dentro del plazo académico.

La evaluación considera el alcance actual de GanadApp y no presupone que todas las capacidades posibles de cada tecnología sean necesarias para el MVP.

## 3. Matriz de decisión

| Criterio | Web responsive | PWA | Nativa | Híbrida (Flutter, React Native o Capacitor) |
|---|---|---|---|---|
| Costo de mantenimiento para una persona | **Bajo.** Se conserva la aplicación web existente, con una única base de código, tecnologías conocidas y un solo proceso de despliegue. | **Medio.** Reutiliza la aplicación web, pero incorpora configuración de instalación, manifest, Service Worker, estrategias de caché y pruebas adicionales. | **Alto.** Requiere desarrollar y mantener una aplicación móvil específica. Según la plataforma, puede implicar herramientas y procesos de publicación adicionales. | **Medio-alto.** Puede reutilizar parte de la lógica o la interfaz, pero incorpora un framework, dependencias y un ciclo de compilación y distribución móvil. |
| ¿Requiere funcionamiento offline? | **No lo proporciona por defecto.** La aplicación depende de la conexión con el servidor para consultar y guardar información. | **Puede proporcionarlo.** Permite almacenar recursos y datos localmente, pero requiere diseñar políticas de caché y sincronización. | **Puede proporcionarlo.** Permite implementar almacenamiento local y sincronización, aunque estas capacidades deben desarrollarse. | **Puede proporcionarlo.** Depende de la arquitectura y de las bibliotecas utilizadas para almacenamiento y sincronización. |
| Acceso al hardware | **Limitado al navegador.** Puede acceder a determinadas capacidades mediante APIs web y permisos del navegador. | **Intermedio.** Dispone de capacidades web y algunas integraciones adicionales, sujetas al navegador y al sistema operativo. | **Amplio.** Ofrece acceso directo a las APIs y capacidades de cada plataforma. | **Amplio, con dependencias.** El acceso se realiza mediante plugins, módulos nativos o APIs del framework. |
| Tiempo hasta el cierre de PP3 | **Bajo.** La adaptación se concentra en las interfaces existentes, sin crear otra aplicación ni modificar la arquitectura general. | **Medio.** Además del diseño responsive, exige implementar y validar capacidades propias de una PWA. | **Alto.** Requiere desarrollar una aplicación móvil adicional, integrar servicios y realizar pruebas específicas. | **Medio-alto.** Exige incorporar el framework, preparar el entorno de desarrollo y resolver la integración con el backend. |

## 4. Decisión

Se adopta **Responsive Web Design (RWD)** como estrategia de adaptación mobile para GanadApp.

La aplicación conservará su arquitectura monolítica por capas, su organización multipágina (MPA), FastAPI como backend y las tecnologías actuales del frontend. Las interfaces se adaptarán a distintos tamaños de pantalla mediante diseño responsive, sin desarrollar una aplicación móvil independiente.

La prioridad de adaptación corresponde a las dos pantallas críticas del proyecto: Gestión de animales y Vacunación.

Esta decisión evita mantener dos aplicaciones, reduce la cantidad de tecnologías y permite concentrar el esfuerzo en mejorar la interfaz existente y verificar su comportamiento en dispositivos móviles.

## 5. Consecuencias de la decisión

### Consecuencias positivas

- Se conserva una única base de código.
- Se reutilizan las rutas, servicios, modelos y mecanismos de autenticación existentes.
- Se evita incorporar dependencias de frameworks móviles.
- Se reduce el esfuerzo de mantenimiento y despliegue.
- Las mejoras responsive pueden incorporarse progresivamente a las pantallas existentes.
- La solución puede utilizarse desde un navegador móvil sin requerir instalación.

### Limitaciones y capacidades que quedan fuera

- No se garantiza el funcionamiento de la aplicación sin conexión.
- No se implementa almacenamiento local persistente de operaciones.
- No se dispone de una cola de operaciones pendientes ni de sincronización automática posterior.
- No se garantiza la instalación de GanadApp como aplicación PWA.
- No se implementan notificaciones push.
- El acceso a cámara, almacenamiento y otras capacidades del dispositivo queda limitado a las APIs disponibles en el navegador y a sus permisos.
- La aplicación no ofrece las mismas posibilidades de integración con el sistema operativo que una aplicación nativa.
- Las operaciones que requieren consultar o modificar información del servidor dependen de una conexión disponible.

Si se interrumpe la conexión durante una operación, la interfaz deberá informar el problema, conservar los datos ingresados cuando sea técnicamente posible y evitar mostrar una confirmación de éxito hasta recibir una respuesta válida del servidor.

## 6. Riesgos y medidas de mitigación

| Riesgo | Medida de mitigación |
|---|---|
| Conexión inestable durante el uso en establecimientos rurales | Informar claramente los errores de conectividad y no confirmar operaciones sin respuesta del servidor. |
| Interfaz difícil de utilizar desde pantallas pequeñas | Diseñar y verificar las pantallas críticas con un viewport inferior a 400 CSS px. |
| Acciones táctiles difíciles de seleccionar | Mantener objetivos táctiles de al menos 48 × 48 CSS px. |
| Demoras en la carga de las pantallas | Establecer presupuestos de rendimiento y verificarlos mediante herramientas automatizables. |
| Diferencias de visualización entre navegadores | Realizar pruebas en navegadores móviles y de escritorio compatibles. |

## 7. Condiciones para revisar esta decisión

La decisión podrá revisarse si se obtiene evidencia de que los usuarios necesitan completar operaciones críticas sin conectividad y no pueden postergarlas hasta recuperar el acceso a internet.

También podrá revisarse si las pruebas de uso identifican necesidades de integración con hardware que no puedan resolverse de manera adecuada mediante APIs web.

Una eventual adopción de PWA deberá justificar el costo de almacenamiento local, resolución de conflictos y sincronización. La incorporación de una aplicación nativa o híbrida deberá justificarse mediante necesidades que no puedan satisfacerse con la aplicación web existente.

## 8. Alternativas descartadas

- **PWA:** descartada para el alcance actual porque agrega instalación, Service Worker, caché y posibles mecanismos de sincronización que no son requisitos de aceptación del MVP.
- **Nativa:** descartada porque requiere desarrollar y mantener una aplicación móvil adicional, con un costo desproporcionado para el equipo unipersonal.
- **Híbrida:** descartada porque incorpora un framework y un proceso de compilación móvil sin una necesidad funcional actual que justifique esa complejidad.

## 9. Referencias

- `SPEC.md`
- `docs/adr/ADR-004-stack-ui.md`
- `docs/adr/ADR-005-estrategia-web.md`
- `docs/arquitectura/presupuestos-rendimiento.md`.
- `docs/arquitectura/offline-sync.md`.
- `docs/diseno/wireframes/gestion-animales-mobile.md`.
- `docs/diseno/wireframes/vacunacion-mobile.md`.