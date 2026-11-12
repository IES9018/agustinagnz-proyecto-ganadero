# Wireframe responsive: Gestión Sanitaria y Vacunación

## 1. Objetivo

Reinterpretar la pantalla **Gestión Sanitaria**, utilizada para registrar y consultar vacunaciones, tratamientos y otros eventos sanitarios, para dispositivos móviles con un viewport inferior a 400 px.

La propuesta conserva los campos, las alertas, el historial y las acciones disponibles en la pantalla original. La adaptación modifica la distribución y la jerarquía de los componentes para mejorar la lectura y la interacción táctil.

## 2. Comparación de wireframes

### Vista de escritorio

**Viewport de referencia: 1440 × 900 px**

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ GANADAPP     Inicio  Inicio de Sesión  Productores  Gestión de Animales      │
│              Vacunación  Stock de Insumos  Trazabilidad       Perfil  Salir  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  GESTIÓN GANADERA                                             [Icono]        │
│  Gestión Sanitaria                                                          │
│  Registre y consulte las vacunaciones, tratamientos y demás eventos         │
│  sanitarios de sus animales.                                                │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  REGISTRAR EVENTO SANITARIO                                                 │
│                                                                              │
│  Animal                        Tipo de evento                               │
│  [Seleccionar animal ▼]        [Vacunación              ▼]                  │
│                                                                              │
│  Fecha                         Próxima fecha programada                     │
│  [____/____/________]           [____/____/________]                         │
│                                                                              │
│  Descripción                                                                  │
│  [____________________________________________________________]             │
│                                                                              │
│  [Guardar evento]  [Limpiar]                                                │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  ALERTAS SANITARIAS                                                         │
│                                                                              │
│  ┌──────────────────────┐  ┌──────────────────────┐                         │
│  │ Tipo de alerta       │  │ Tipo de alerta       │                         │
│  │ Animal: [ID]         │  │ Animal: [ID]         │                         │
│  │ Evento: [tipo]       │  │ Evento: [tipo]       │                         │
│  │ Descripción          │  │ Descripción          │                         │
│  │ Próxima fecha        │  │ Próxima fecha        │                         │
│  └──────────────────────┘  └──────────────────────┘                         │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  HISTORIAL SANITARIO                                      [Actualizar]      │
│                                                                              │
│  Animal: [Seleccionar animal ▼]                                             │
│  Cantidad de eventos: [cantidad]                                            │
│                                                                              │
│  Fecha | Tipo de evento | Descripción | Estado | Acciones                   │
│  ────────────────────────────────────────────────────────────────────────── │
│  ...                                                                         │
│  [Anular, cuando corresponda]                                               │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Vista móvil

**Viewport de referencia: 390 × 844 px. Aplicación del diseño para anchos inferiores a 400 px.**

```text
┌──────────────────────────────┐
│           GANADAPP           │
│                              │
│ Inicio   Inicio de Sesión    │
│ Productores                  │
│ Gestión de Animales          │
│ Vacunación                   │
│ Stock de Insumos             │
│ Trazabilidad                 │
│ Perfil              Salir    │
├──────────────────────────────┤
│ GESTIÓN GANADERA              │
│                              │
│ Gestión Sanitaria            │
│                              │
│ Registre y consulte las      │
│ vacunaciones, tratamientos   │
│ y demás eventos sanitarios   │
│ de sus animales.             │
├──────────────────────────────┤
│ REGISTRAR EVENTO SANITARIO   │
│                              │
│ Animal                       │
│ [Seleccionar animal       ▼] │
│                              │
│ Tipo de evento               │
│ [Vacunación               ▼] │
│                              │
│ Fecha                        │
│ [____/____/______________]   │
│                              │
│ Próxima fecha programada     │
│ [____/____/______________]   │
│                              │
│ Descripción                  │
│ [________________________]   │
│ [________________________]   │
│                              │
│ [      Guardar evento     ]  │
│ [         Limpiar         ]  │
│                              │
├──────────────────────────────┤
│ ALERTAS SANITARIAS           │
│                              │
│ ┌──────────────────────────┐ │
│ │ Tipo de alerta           │ │
│ │ Animal: [ID]             │ │
│ │ Evento: [tipo]           │ │
│ │ Descripción              │ │
│ │ Próxima fecha: [fecha]   │ │
│ └──────────────────────────┘ │
│                              │
│ ┌──────────────────────────┐ │
│ │ Tipo de alerta           │ │
│ │ Animal: [ID]             │ │
│ │ Evento: [tipo]           │ │
│ │ Descripción              │ │
│ │ Próxima fecha: [fecha]   │ │
│ └──────────────────────────┘ │
│                              │
├──────────────────────────────┤
│ HISTORIAL SANITARIO          │
│                              │
│ Animal                       │
│ [Seleccionar animal       ▼] │
│                              │
│ Cantidad de eventos: [n]     │
│                              │
│ [       Actualizar        ]  │
│                              │
│ ┌──────────────────────────┐ │
│ │ Fecha: [fecha]           │ │
│ │ Tipo de evento: [tipo]   │ │
│ │ Descripción: [texto]     │ │
│ │ Estado: [estado]         │ │
│ │                          │ │
│ │ [Anular, si corresponde] │ │
│ └──────────────────────────┘ │
│                              │
│          ...                 │
└──────────────────────────────┘
```

## 3. Cambios entre escritorio y móvil

| Elemento | Escritorio | Móvil, menos de 400 px |
|---|---|---|
| Navegación | Menú horizontal | Elementos distribuidos en varias líneas, conservando todos los accesos |
| Encabezado | Título, descripción e icono en una misma composición | Título y descripción en una columna; se oculta el icono decorativo |
| Formulario | Dos columnas para los campos | Una columna, con un campo por fila |
| Descripción | Campo integrado en la grilla del formulario | Campo a ancho completo |
| Acciones | Guardar evento y Limpiar en una fila | Botones apilados y a ancho completo |
| Alertas sanitarias | Tarjetas distribuidas en varias columnas | Una tarjeta por fila |
| Selector del historial | Integrado en el encabezado de la sección | Ocupa el ancho disponible y aparece antes del contador |
| Historial | Tabla de cinco columnas | Registros presentados como tarjetas verticales con todos los datos |
| Actualización | Botón junto al encabezado | Botón a ancho completo dentro de la sección |

## 4. Justificación de los cambios

**Navegación y encabezado.** El menú se distribuye en varias líneas para mantener visibles los accesos sin provocar desbordamientos horizontales. El encabezado adopta una composición vertical y prioriza el título y la descripción. Se oculta el icono decorativo para reservar espacio al contenido principal.

**Formulario de evento sanitario.** Los cinco campos se presentan en una columna y mantienen el orden original: Animal, Tipo de evento, Fecha, Próxima fecha programada y Descripción. Los selectores y campos de fecha ocupan el ancho disponible. La descripción conserva su límite de 500 caracteres y se presenta a ancho completo. Las acciones Guardar evento y Limpiar se ubican en líneas independientes para facilitar su selección.

**Alertas sanitarias.** Las tarjetas se reorganizan en una sola columna. Se mantiene toda la información que presenta cada alerta: tipo de alerta, identificador del animal, tipo de evento, descripción y próxima fecha. Se conserva la distinción visual entre alertas vencidas y próximas.

**Historial sanitario.** La tabla de escritorio se transforma en tarjetas verticales para evitar que las cinco columnas requieran desplazamiento horizontal. Cada tarjeta conserva fecha, tipo de evento, descripción, estado y acciones. La acción de anulación se muestra únicamente cuando corresponde, respetando el comportamiento de la pantalla original. El selector de animal y el contador de eventos permanecen disponibles.

**Jerarquía visual.** Se mantiene el orden funcional de las tres secciones: registro de evento, alertas sanitarias e historial. En móvil, cada sección ocupa el ancho disponible y se separa visualmente de la siguiente para facilitar la navegación mediante desplazamiento vertical.

## 5. Criterios de interacción móvil

Los controles interactivos deben disponer de un área táctil mínima de **48 × 48 px**, de acuerdo con las recomendaciones de Material Design y web.dev. Este criterio se aplica a los controles de navegación, selectores, campos interactivos y botones.

Apple Human Interface Guidelines utiliza como referencia un objetivo táctil de 44 × 44 pt. Para esta propuesta se adopta el criterio de 48 × 48 px como referencia de diseño.

Los botones Guardar evento, Limpiar y Actualizar deben tener altura y ancho suficientes para seleccionarse cómodamente. Los selectores de Animal y Tipo de evento deben contar con espacio suficiente para mostrar sus valores y permitir su apertura sin dificultad.

Los controles deben mantener separación visual y táctil. Los estados de foco, selección, carga y error deben ser perceptibles. Las alertas vencidas y próximas deben diferenciarse sin depender exclusivamente del color.

## 6. Contenido conservado

La adaptación mantiene todos los elementos funcionales de la pantalla original:

- Navegación y acceso al perfil.
- Selector de animal del formulario.
- Tipos de evento: Vacunación, Tratamiento, Desparasitación, Control veterinario, Enfermedad, Movimiento y Otro.
- Fecha del evento.
- Próxima fecha programada, opcional.
- Descripción obligatoria, con un máximo de 500 caracteres.
- Acciones Guardar evento y Limpiar.
- Mensajes de estado del formulario.
- Alertas sanitarias con su información y clasificación.
- Selector de animal para consultar el historial.
- Contador de eventos.
- Acción Actualizar.
- Historial con fecha, tipo de evento, descripción, estado y acciones.
- Anulación de eventos cuando corresponda, conservando el motivo y el estado del registro.

## 7. Criterio de contenido y alcance

La propuesta no elimina campos, alertas, datos del historial ni acciones existentes. La transformación principal consiste en reorganizar las alertas en una columna y presentar cada evento del historial como una tarjeta vertical en lugar de una fila de tabla.

La información de cada evento permanece completa y las acciones conservan las condiciones de disponibilidad definidas por el sistema. La propuesta no incorpora filtros, búsquedas, nuevos tipos de eventos ni funcionalidades adicionales.

El wireframe representa una especificación de diseño responsive para el TP5. No implica que estos cambios estén implementados en el código actual.