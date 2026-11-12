# Wireframe responsive: Gestión de Animales

## 1. Objetivo

Reinterpretar la pantalla **Gestión de Animales** del TP3 para dispositivos móviles con un viewport inferior a 400 px, conservando todas las funcionalidades, los campos y las acciones existentes.

El diseño móvil reorganiza la distribución y la jerarquía visual para facilitar la lectura, la carga de datos y la interacción táctil. No incorpora funcionalidades nuevas ni elimina información del sistema.

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
│  Gestión de Animales                                                        │
│  Registre, consulte y administre los animales de su hacienda                │
│  desde un único lugar.                                                      │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  REGISTRAR ANIMAL                                                           │
│                                                                              │
│  Identificador                 Especie                                      │
│  [____________________]        [____________________]                       │
│                                                                              │
│  Sexo                          Raza                                         │
│  [____________________]        [____________________]                       │
│                                                                              │
│  Fecha de nacimiento           Establecimiento                              │
│  [____________________]        [____________________]                       │
│                                                                              │
│  Edad                          Estado Sanitario                             │
│  [Calculada automáticamente]   [Sano                  ▼]                   │
│                                                                              │
│  [Guardar Animal]  [Cancelar, si se está editando]                          │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  ANIMALES REGISTRADOS                                      [Actualizar]     │
│  Total: [cantidad]                                                          │
│                                                                              │
│  ID | Identificador | Especie | Sexo | Raza | Edad | Estado | Estab. | Acc. │
│  ────────────────────────────────────────────────────────────────────────── │
│  ...                                                                        │
│  [Editar] [Sanidad]                                                         │
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
│ Gestión de Animales          │
│                              │
│ Registre, consulte y          │
│ administre los animales de   │
│ su hacienda desde un único   │
│ lugar.                       │
├──────────────────────────────┤
│ REGISTRAR ANIMAL             │
│                              │
│ Identificador                │
│ [________________________]   │
│                              │
│ Especie                      │
│ [________________________]   │
│                              │
│ Sexo                         │
│ [________________________]   │
│                              │
│ Raza                         │
│ [________________________]   │
│                              │
│ Fecha de nacimiento          │
│ [________________________]   │
│                              │
│ Establecimiento              │
│ [________________________]   │
│                              │
│ Edad                         │
│ [Calculada automáticamente] │
│                              │
│ Estado Sanitario              │
│ [Sano                     ▼] │
│                              │
│ [      Guardar Animal      ] │
│ [       Cancelar           ] │
│                              │
├──────────────────────────────┤
│ ANIMALES REGISTRADOS         │
│                              │
│ Total: [cantidad]            │
│ [       Actualizar         ] │
│                              │
│ ┌──────────────────────────┐ │
│ │ ID: [valor]              │ │
│ │ Identificador: [valor]   │ │
│ │ Especie: [valor]         │ │
│ │ Sexo: [valor]            │ │
│ │ Raza: [valor]            │ │
│ │ Edad: [valor]            │ │
│ │ Estado sanitario: [valor]│ │
│ │ Establecimiento: [valor] │ │
│ │                          │ │
│ │ [Editar]     [Sanidad]   │ │
│ └──────────────────────────┘ │
│                              │
│       ... más animales       │
└──────────────────────────────┘
```

## 3. Cambios entre escritorio y móvil

| Elemento | Escritorio | Móvil, menos de 400 px |
|---|---|---|
| Navegación | Menú horizontal | Elementos distribuidos en varias líneas, conservando todos los accesos |
| Encabezado | Título, descripción e icono en una misma composición | Título y descripción en una columna; se oculta el icono decorativo |
| Formulario | Dos columnas | Una columna, con un campo por fila |
| Campos | Controles distribuidos en paralelo | Controles ocupan el ancho disponible |
| Acciones del formulario | Botones en una misma fila | Botones apilados y a ancho completo |
| Listado | Tabla de nueve columnas | Registros presentados como tarjetas verticales con todos los datos |
| Acciones por registro | Editar y Sanidad en la misma fila | Editar y Sanidad dentro de cada tarjeta |
| Actualización | Botón junto al encabezado del listado | Botón a ancho completo debajo del contador |

## 4. Justificación de los cambios

**Navegación y encabezado.** El menú deja de depender de una única línea horizontal y se distribuye en varias líneas para evitar desbordamientos. Se conserva el acceso a todas las secciones. El encabezado adopta una composición vertical y prescinde del icono decorativo para priorizar el título y la descripción.

**Formulario.** Los ocho campos se presentan en una sola columna y mantienen el orden de la pantalla original. Esta disposición evita controles demasiado estrechos y facilita completar el formulario con el teclado virtual. El campo Edad continúa siendo de solo lectura y conserva su cálculo automático. Los botones Guardar Animal y Cancelar se muestran en líneas independientes para facilitar su selección.

**Listado de animales.** La tabla horizontal de escritorio se reorganiza en tarjetas verticales. Cada tarjeta conserva los nueve datos de la tabla original: ID, identificador, especie, sexo, raza, edad, estado sanitario, establecimiento y acciones. No se elimina información ni se reemplazan los valores por resúmenes. Las acciones Editar y Sanidad permanecen disponibles para cada registro.

**Jerarquía visual.** Se conserva la separación entre el encabezado de la página, el formulario de registro y el listado. En móvil, el formulario aparece antes que el listado, manteniendo la secuencia de uso de la pantalla.

## 5. Criterios de interacción móvil

Los controles interactivos deben disponer de un área táctil mínima de **48 × 48 px**, de acuerdo con las recomendaciones de Material Design y web.dev. Este criterio se aplica a botones, controles de navegación y acciones por registro. Los campos de formulario deben contar con una altura suficiente para facilitar su selección y edición.

Apple Human Interface Guidelines utiliza como referencia un objetivo táctil de 44 × 44 pt. Se adopta el criterio de 48 × 48 px como referencia de diseño para esta propuesta.

Los espacios entre controles deben evitar pulsaciones accidentales. Los botones principales y secundarios deben diferenciarse visualmente y mantener estados de foco perceptibles.

## 6. Contenido conservado

La adaptación mantiene todos los elementos funcionales de la pantalla original:

Navegación y acceso al perfil.

Identificador, especie, sexo, raza, fecha de nacimiento, establecimiento, edad y estado sanitario.

Cálculo automático de edad.

Registro y edición de animales.

Cancelación durante la edición.

Mensajes de estado del formulario.

Contador de animales registrados.

Actualización del listado.

Visualización de todos los datos de cada animal.

Acciones Editar y Sanidad.

Mensaje de listado vacío cuando no existen registros.

## 7. Criterio de contenido y alcance

La propuesta no elimina campos, columnas, acciones ni información de los registros. El único cambio estructural relevante es la sustitución de la tabla horizontal por tarjetas verticales en el viewport móvil, para evitar que el usuario tenga que desplazarse horizontalmente para consultar los datos de un animal.

El wireframe representa una especificación de diseño responsive para el TP5. No implica que estos cambios estén implementados en el código actual.