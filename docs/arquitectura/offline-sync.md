# Estrategia offline — Non-Goal del MVP

## 1. Declaración del Non-Goal

El funcionamiento offline no forma parte del alcance del MVP de GanadApp.

La aplicación requiere conexión con el servidor para consultar y registrar información persistente. No se implementarán en esta etapa mecanismos de almacenamiento local de operaciones, colas de sincronización ni sincronización automática cuando se recupere la conexión.

Esta decisión se aplica especialmente a las operaciones de Gestión de animales y Vacunación.

## 2. Justificación

GanadApp está destinado a productores ganaderos y contempla escenarios de uso en establecimientos rurales, donde la conectividad puede ser intermitente o limitada. Por lo tanto, el funcionamiento offline es una necesidad potencial del dominio y no se descarta como una necesidad futura.

Sin embargo, no se considera un requisito obligatorio de aceptación del MVP actual porque incorporar esta capacidad requiere resolver aspectos adicionales de arquitectura y consistencia de datos:

- Persistencia local segura de información.
- Identificación de operaciones pendientes.
- Envío diferido de operaciones al servidor.
- Resolución de conflictos cuando los datos cambian en más de un dispositivo.
- Validación de operaciones durante la sincronización.
- Tratamiento de duplicados y errores de transmisión.
- Protección de información sensible almacenada en el dispositivo.

Implementar estas capacidades sin definir previamente sus reglas de consistencia podría producir registros duplicados, información desactualizada o modificaciones incompatibles.

El alcance actual prioriza la adaptación responsive y el correcto funcionamiento de las operaciones cuando existe conexión con el servidor.

## 3. Comportamiento esperado ante pérdida de conectividad

Aunque el funcionamiento offline completo queda fuera del alcance, la aplicación deberá gestionar adecuadamente los errores de conexión.

Ante una interrupción de conectividad:

- Informará que no fue posible completar la operación.
- No mostrará una confirmación de éxito sin una respuesta válida del servidor.
- Conservará los datos ingresados cuando sea técnicamente posible.
- Permitirá al usuario identificar que la operación debe volver a intentarse.
- Evitará reenviar automáticamente una operación sin mecanismos que permitan controlar posibles duplicados.

La aplicación no deberá presentar datos almacenados temporalmente como si fueran información actualizada del servidor.

## 4. Condición para reabrir la decisión

El Non-Goal deberá revisarse si las pruebas con productores o la evidencia de uso demuestran que las operaciones críticas de registro de animales o vacunación deben completarse en establecimientos sin conectividad y no pueden postergarse hasta recuperar el acceso a internet.

La revisión deberá documentar:

1. Las operaciones que necesitan funcionar offline.
2. El volumen y tipo de información que debe estar disponible localmente.
3. Las reglas de sincronización y resolución de conflictos.
4. Los controles para evitar duplicados.
5. Los requisitos de seguridad y protección de datos del almacenamiento local.

La incorporación de offline-first deberá aprobarse mediante una nueva decisión arquitectónica (ADR), con su correspondiente actualización de la SPEC y de los contratos de API afectados.

## 5. Relación con la estrategia mobile

La estrategia adoptada en ADR-006 es Responsive Web Design. Esta decisión no implica que la aplicación sea offline-first ni que disponga de capacidades PWA.

El diseño responsive permite utilizar las pantallas desde dispositivos móviles, pero las operaciones que requieren consultar o persistir información continúan dependiendo del backend.

El Non-Goal de funcionamiento offline es, por lo tanto, una limitación conocida y documentada del MVP, no una capacidad implementada parcialmente.

## 6. Referencias

- `docs/adr/ADR-006-estrategia-mobile.md`
- `SPEC.md`
- `docs/arquitectura/presupuestos-rendimiento.md`.