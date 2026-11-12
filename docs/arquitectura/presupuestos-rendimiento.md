# Presupuestos de rendimiento — GanadApp

## 1. Objetivo

Establecer presupuestos cuantificables de rendimiento para las dos pantallas críticas de GanadApp definidas para TP5: Gestión de animales y Vacunación.

Los presupuestos permiten establecer límites verificables para la experiencia móvil, detectar regresiones de rendimiento y preparar su incorporación al proceso de Integración Continua (CI) previsto para TP6.

Los valores definidos son objetivos de aceptación. No representan resultados de mediciones realizadas ni implican que las pantallas ya cumplan estos límites.

## 2. Alcance y condiciones de medición

Los presupuestos se aplican a las siguientes pantallas:

- **Gestión de animales:** consulta y administración del listado de animales.
- **Vacunación:** consulta y registro de actividades de vacunación.

Las mediciones se realizarán en las versiones adaptativas de ambas pantallas, utilizando un viewport móvil de referencia de 390 × 844 CSS px. Se comprobará también su visualización en anchos inferiores a 400 CSS px.

Para las pruebas de laboratorio se utilizará un perfil móvil y una condición de red 4G simulada. Se mantendrán constantes las condiciones de prueba para facilitar la comparación entre versiones.

Los resultados de laboratorio y los datos de experiencia real de los usuarios se identificarán por separado. No se considerarán equivalentes.

## 3. Tabla de presupuestos

| Métrica | Presupuesto | Pantalla o alcance | Cómo se mide |
|---|---:|---|---|
| LCP móvil (Largest Contentful Paint) | < 2,5 s en 4G | Gestión de animales | Lighthouse CI, auditoría móvil con red 4G simulada. |
| LCP móvil (Largest Contentful Paint) | < 2,5 s en 4G | Vacunación | Lighthouse CI, auditoría móvil con red 4G simulada. |
| INP (Interaction to Next Paint) | < 200 ms | Gestión de animales | Biblioteca `web-vitals`, mediante medición de campo de las interacciones reales. |
| INP (Interaction to Next Paint) | < 200 ms | Vacunación | Biblioteca `web-vitals`, mediante medición de campo de las interacciones reales. |
| Peso inicial de JavaScript | < 200 KB gzip | Recursos JavaScript iniciales de cada pantalla | `source-map-explorer --gzip`, sobre los bundles JavaScript y sus respectivos source maps. |

Los límites son estrictos: un resultado igual o superior al valor máximo no cumple el presupuesto.

## 4. Herramientas y procedimiento de verificación

### 4.1. LCP móvil — Lighthouse CI

**Herramienta:** Lighthouse CI.

Lighthouse CI se utilizará para ejecutar auditorías automatizadas sobre las URLs correspondientes a Gestión de animales y Vacunación.

La configuración de recolección deberá utilizar un perfil móvil y una condición de red 4G simulada. Se registrará el valor de Largest Contentful Paint de cada pantalla.

**Criterio de aceptación:** el LCP debe ser inferior a 2,5 segundos en cada una de las dos pantallas.

**Evidencia:** reportes de Lighthouse CI con la URL evaluada, configuración móvil, condición de red y valor de LCP obtenido.

Este control podrá automatizarse en CI durante TP6 mediante una aserción de Lighthouse CI sobre el identificador de auditoría `largest-contentful-paint`, con un límite de 2500 milisegundos. La aserción deberá configurarse con nivel de error para que un incumplimiento produzca un resultado fallido del control.

### 4.2. INP — web-vitals

**Herramienta:** biblioteca `web-vitals`.

INP mide el tiempo que transcurre desde una interacción del usuario hasta que la siguiente actualización visual se presenta en pantalla.

A diferencia de una auditoría de laboratorio, el INP real se obtiene mediante la observación de interacciones realizadas durante el uso de la aplicación. Por ese motivo, se utilizará `web-vitals` para recopilar la métrica en las visitas reales a Gestión de animales y Vacunación.

La instrumentación deberá identificar la pantalla de origen y permitir agrupar los resultados por URL o tipo de pantalla.

**Criterio de aceptación:** INP inferior a 200 milisegundos en el percentil 75 (p75) de las visitas con datos suficientes para cada pantalla.

El percentil 75 permite evaluar la experiencia de la mayoría de las visitas sin depender de una única interacción aislada.

La recolección deberá contemplar que INP requiere interacciones del usuario. Una visita sin interacciones no produce necesariamente un valor de INP.

**Evidencia:** registros de INP recopilados con `web-vitals`, identificados por pantalla y con el percentil calculado sobre una cantidad suficiente de visitas.

Lighthouse CI podrá utilizarse como herramienta complementaria de laboratorio para identificar problemas de interactividad. Su Total Blocking Time (TBT) puede servir como indicador diagnóstico, pero no debe presentarse como una medición equivalente ni como sustituto del INP real.

### 4.3. Peso inicial de JavaScript — source-map-explorer

**Herramienta:** `source-map-explorer`.

Se utilizará `source-map-explorer` para analizar la composición de los recursos JavaScript incluidos en la carga inicial de cada pantalla.

El análisis permitirá identificar los módulos, dependencias y componentes que contribuyen al peso del JavaScript entregado al navegador.

Se utilizará la opción `--gzip` para obtener el tamaño comprimido. Esta opción permite analizar el tamaño gzip de los recursos mapeados; por ello, los archivos JavaScript deberán contar con sus respectivos source maps válidos.

El análisis deberá considerar exclusivamente los recursos JavaScript necesarios para la carga inicial de cada pantalla. No se sumarán recursos que se descarguen únicamente después de una interacción o de una navegación posterior.

**Criterio de aceptación:** el peso inicial total de JavaScript debe ser inferior a 200 KB gzip por pantalla.

**Evidencia:** salida del análisis de source-map-explorer, identificación de los archivos analizados y registro del tamaño gzip correspondiente.

Si la implementación no dispone de bundles o source maps, deberá prepararse el proceso de generación de esos artefactos antes de utilizar esta herramienta. No se considerará válido un resultado obtenido sobre archivos que no representen los recursos efectivamente entregados al navegador.

## 5. Preparación para Integración Continua (TP6)

Los presupuestos se establecen en TP5 para permitir que sus verificaciones se incorporen al pipeline de CI durante TP6.

Se prevé automatizar los siguientes controles:

| Control | Herramienta | Integración prevista en CI |
|---|---|---|
| LCP móvil | Lighthouse CI | Ejecutar auditorías de Gestión de animales y Vacunación y aplicar el límite de 2500 ms. |
| INP | web-vitals | Recopilar métricas de campo y evaluar el percentil 75 por pantalla. No se sustituirá la medición de campo por una auditoría de laboratorio. |
| Peso inicial de JavaScript | source-map-explorer | Analizar los bundles con `--gzip` y comprobar que el tamaño inicial no alcance los 200 KB. |

La integración de Lighthouse CI permitirá que el control de LCP se ejecute automáticamente en el pipeline y que una regresión respecto del presupuesto produzca un fallo verificable.

El análisis del peso JavaScript deberá incorporarse como un paso automatizado posterior a la generación de los bundles y source maps.

La medición de INP requiere datos de interacciones reales. Por lo tanto, su evaluación se realizará sobre los datos de campo recopilados y no se declarará automáticamente cumplida por el solo hecho de superar una auditoría Lighthouse.

La configuración concreta del pipeline, la instrumentación de campo y la generación de los artefactos necesarios se implementarán y validarán durante TP6.

## 6. Evidencias de cumplimiento

Para declarar cumplidos los presupuestos se deberán conservar las siguientes evidencias:

- Reportes de Lighthouse CI de Gestión de animales y Vacunación, con configuración móvil y red 4G.
- Valores de LCP de ambas pantallas.
- Datos de INP recopilados mediante `web-vitals`, identificados por pantalla y con su percentil 75.
- Resultados de `source-map-explorer --gzip` para los recursos JavaScript iniciales de cada pantalla.
- Evidencia de la ejecución automatizada de los controles incorporados al pipeline de CI durante TP6.

La ausencia de mediciones no implica cumplimiento. Hasta obtener evidencias reproducibles, los valores se considerarán presupuestos establecidos pendientes de validación.

## 7. Relación con otros documentos

- `docs/adr/ADR-006-estrategia-mobile.md`: decisión de adaptación mobile mediante Responsive Web Design.
- `docs/arquitectura/offline-sync.md`: declaración del funcionamiento offline como Non-Goal del MVP.
- `docs/diseno/wireframes/gestion-animales-mobile.md`: adaptación de la pantalla de Gestión de animales.
- `docs/diseno/wireframes/vacunacion-mobile.md`: adaptación de la pantalla de Vacunación.
- `SPEC.md`: requisitos no funcionales asociados a los presupuestos de rendimiento.