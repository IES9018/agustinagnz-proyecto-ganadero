# Auditoría heurística de interfaz — GanadApp

## 1. Objetivo

Evaluar las dos pantallas críticas seleccionadas para TP3 mediante las 10 heurísticas de usabilidad de Jakob Nielsen.

Pantallas auditadas:

1. Gestión de Animales.
2. Vacunación.

La auditoría se realiza sobre los wireframes de baja fidelidad y propone correcciones concretas. Las correcciones indicadas en este documento fueron incorporadas a los wireframes correspondientes.

---

## 2. Escala utilizada

* **Sí:** la heurística se encuentra contemplada.
* **Parcial:** existe algún elemento compatible, pero requiere refuerzo.
* **No:** se identifica un problema que necesita corrección.

---

## 3. Auditoría

| Heurística                                                   | Cumple         | Evidencia                                                                                                                                    | Corrección propuesta/aplicada                                                                                   |
| ------------------------------------------------------------ | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| 1. Visibilidad del estado del sistema                        | Parcial        | Gestión de Animales ya contempla carga, vacío y error. Vacunación contempla confirmación, pero el estado de operación debe quedar explícito. | Se incorporan mensajes explícitos de carga, confirmación y actualización del historial.                         |
| 2. Correspondencia entre sistema y mundo real                | Sí             | Se utilizan conceptos del dominio: animal, vacuna, fecha, establecimiento y estado sanitario.                                                | Mantener terminología del dominio y evitar nombres técnicos innecesarios.                                       |
| 3. Control y libertad del usuario                            | Parcial        | Las pantallas permiten iniciar acciones principales, pero el registro necesita una salida clara.                                             | Incorporar `Cancelar` en el formulario de animales y mantener las acciones claramente separadas.                |
| 4. Consistencia y estándares                                 | Sí             | Las pantallas utilizan el mismo header, acción principal y estructura general.                                                               | Mantener los mismos patrones entre módulos.                                                                     |
| 5. Prevención de errores                                     | No → corregido | Un identificador duplicado puede impedir el registro de un animal; datos incompletos pueden impedir una vacunación.                          | Validación de identificador, campos obligatorios y validaciones antes del guardado.                             |
| 6. Reconocimiento antes que recuerdo                         | Parcial        | La información principal se muestra en tablas y formularios, pero los errores deben orientar al usuario.                                     | Mostrar etiquetas claras, estados visibles y mensajes próximos al campo afectado.                               |
| 7. Flexibilidad y eficiencia de uso                          | Parcial        | Las acciones principales están directamente disponibles.                                                                                     | Mantener acciones principales debajo del header y evitar pasos innecesarios.                                    |
| 8. Diseño estético y minimalista                             | Sí             | Los wireframes contienen solamente información relevante para cada operación.                                                                | Mantener la baja fidelidad y evitar información no necesaria en las pantallas críticas.                         |
| 9. Ayudar a reconocer, diagnosticar y recuperarse de errores | No → corregido | Un mensaje genérico de error no resulta suficiente para orientar al usuario.                                                                 | Los mensajes deben explicar el problema y ofrecer una acción de recuperación.                                   |
| 10. Ayuda y documentación                                    | Parcial        | La interfaz busca ser autoexplicativa, pero no todos los errores están documentados.                                                         | Utilizar etiquetas, instrucciones breves y mensajes contextuales en lugar de depender de documentación externa. |

---

# 4. Problemas detectados y correcciones

## Problema 1 — Estado de error poco orientativo

### Heurística afectada

Heurística 9: ayudar a reconocer, diagnosticar y recuperarse de errores.

### Situación

Un mensaje como:

```text
No se pudieron cargar los animales.
```

informa que existe un problema, pero no proporciona una acción concreta.

### Corrección

El wireframe actualizado utiliza:

```text
No se pudieron cargar los animales.
Verifique la conexión e intente nuevamente.

[ Reintentar ]
```

De esta forma, el usuario puede identificar el problema y continuar con una acción de recuperación.

---

## Problema 2 — Confusión entre estado vacío y error

### Heurísticas afectadas

* Heurística 1: visibilidad del estado del sistema.
* Heurística 9: recuperación frente a errores.

### Situación

Una lista sin registros podría interpretarse como un fallo de consulta.

### Corrección

Se diferencia explícitamente:

```text
Aún no hay animales registrados.

[ + Registrar primer animal ]
```

de:

```text
No se pudieron cargar los animales.

[ Reintentar ]
```

El primero representa ausencia válida de información; el segundo representa un problema de consulta.

---

## Problema 3 — Identificador duplicado

### Heurística afectada

Heurística 5: prevención de errores.

### Situación

El modelo de dominio establece que el identificador de cada animal debe ser único. Si el usuario ingresa un identificador existente, el registro no puede completarse.

### Corrección

El formulario identifica el campo como obligatorio y se define una validación específica:

```text
No se puede registrar el animal.
El identificador ingresado ya existe.
Ingrese un identificador diferente.
```

Los datos que el usuario ya ingresó deben conservarse para evitar una carga repetida.

---

## Problema 4 — Datos incompletos en vacunación

### Heurística afectada

Heurística 5: prevención de errores.

### Situación

La vacunación requiere animal, vacuna y fecha. Si falta uno de estos datos, la operación no debe completarse.

### Corrección

Los campos se marcan como obligatorios:

```text
Animal *
Vacuna *
Fecha *
```

y se informa específicamente el campo que debe completarse.

---

## Problema 5 — Falta de confirmación explícita

### Heurística afectada

Heurística 1: visibilidad del estado del sistema.

### Situación

Después de guardar una vacunación, el usuario necesita saber si la operación fue realizada.

### Corrección

Se incorpora:

```text
[✓] Vacunación registrada correctamente.
```

y se muestra el historial actualizado.

---

# 5. Accesibilidad

Dentro del alcance definido por TP3, las dos pantallas críticas incorporan dos requisitos mínimos:

## Navegación mediante teclado

Todos los controles interactivos deben poder alcanzarse y utilizarse mediante teclado.

El orden esperado debe ser lógico:

```text
Header
↓
Acción principal
↓
Campos
↓
Acciones secundarias
↓
Historial / contenido
```

El foco no debe quedar atrapado ni desaparecer durante la interacción.

## Contraste nivel AA

Los textos y controles de las dos pantallas críticas deben utilizar combinaciones de color que permitan cumplir el contraste requerido por WCAG 2.1 nivel AA.

La comunicación de errores, estados y acciones no debe depender exclusivamente del color.

---

# 6. Resultado de la auditoría

La auditoría permitió identificar y corregir cinco situaciones concretas:

1. errores poco orientativos;
2. confusión entre ausencia de datos y error;
3. posibilidad de identificadores duplicados;
4. envío de formularios incompletos;
5. falta de confirmación visible.

Las correcciones fueron incorporadas a los wireframes de `Gestión de Animales` y `Vacunación`.

Las pantallas mantienen los criterios UX previamente definidos para GanadApp: navegación directa, acciones principales identificables, estados diferenciados, confirmación de operaciones y actualización de información.
