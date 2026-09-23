# Wireframe de baja fidelidad — Vacunación

## 1. Objetivo

Permitir registrar una vacunación asociada a un animal y consultar el historial resultante.

La pantalla debe hacer explícitos:

* animal;
* vacuna;
* fecha;
* acción de registro;
* historial;
* resultado de la operación.

---

## 2. Wireframe principal

```text
+----------------------------------------------------------------+
| GANADAPP | VACUNACIÓN                                  | usuario |
+----------------------------------------------------------------+
|                                                                |
| REGISTRAR VACUNACIÓN                                           |
|                                                                |
| Animal *        [____________________________]                |
| Vacuna *        [____________________________]                |
| Fecha *         [____________________________]                |
|                                                                |
| [ Registrar vacunación ]                                       |
|                                                                |
|----------------------------------------------------------------|
| HISTORIAL DE VACUNACIONES                                      |
|                                                                |
| Animal       | Vacuna             | Fecha                      |
|----------------------------------------------------------------|
| 01           | Antibrucélica      | 20/08/2026                |
|                                                                |
+----------------------------------------------------------------+
```

---

## 3. Estado de validación

```text
+----------------------------------------------------------------+
| GANADAPP | VACUNACIÓN                                  | usuario |
+----------------------------------------------------------------+
|                                                                |
| REGISTRAR VACUNACIÓN                                           |
|                                                                |
| Animal *        [____________________________]                |
| Vacuna *        [____________________________]                |
| Fecha *         [____________________________]                |
|                 La fecha es obligatoria.                      |
|                                                                |
| [ Registrar vacunación ]                                       |
|                                                                |
+----------------------------------------------------------------+
```

El mensaje debe identificar el campo que necesita corrección.

---

## 4. Estado de confirmación

```text
+----------------------------------------------------------------+
| GANADAPP | VACUNACIÓN                                  | usuario |
+----------------------------------------------------------------+
|                                                                |
| [✓] Vacunación registrada correctamente.                      |
|                                                                |
| REGISTRAR VACUNACIÓN                                           |
|                                                                |
| Animal *        [____________________________]                |
| Vacuna *        [____________________________]                |
| Fecha *         [____________________________]                |
|                                                                |
| [ Registrar vacunación ]                                       |
|                                                                |
| HISTORIAL ACTUALIZADO                                          |
|----------------------------------------------------------------|
| Animal       | Vacuna             | Fecha                      |
| 01           | Antibrucélica      | 20/08/2026                |
|                                                                |
+----------------------------------------------------------------+
```

---

## 5. Objetivo de la pantalla

Registrar y consultar vacunaciones.

---

## 6. Entrada principal

Los datos principales de entrada son:

* Animal;
* Vacuna;
* Fecha.

Todos son obligatorios para completar el registro.

---

## 7. Error más probable

El usuario puede intentar registrar una vacunación:

* sin completar uno de los campos;
* asociada a un animal inexistente;
* con datos inválidos.

Esto se relaciona con CA-08, que establece el rechazo de eventos sanitarios cuando el animal asociado no existe o los datos requeridos son inválidos.

---

## 8. Prevención del error

La interfaz debe:

1. identificar claramente cada campo;
2. marcar los campos obligatorios;
3. validar los datos antes de guardar;
4. informar exactamente qué dato debe corregirse;
5. conservar los valores válidos ya ingresados;
6. confirmar el registro cuando la operación finaliza correctamente;
7. actualizar el historial después del registro.

---

## 9. Accesibilidad mínima 

La pantalla debe cumplir como mínimo:

* navegación completa mediante teclado;
* orden lógico de foco;
* etiquetas asociadas a los campos;
* botones identificables mediante texto;
* contraste suficiente para nivel AA en textos y controles;
* mensajes de error comprensibles sin depender exclusivamente del color.

---

## 10. Correcciones aplicadas a partir de la auditoría heurística

| Problema                                                  | Corrección                                                                  |
| --------------------------------------------------------- | --------------------------------------------------------------------------- |
| El usuario puede intentar guardar información incompleta. | Los campos requeridos se identifican con `*` y se validan antes de guardar. |
| Un mensaje genérico no indica qué debe corregirse.        | El mensaje se coloca junto al campo correspondiente.                        |
| El usuario puede no saber si la vacunación se guardó.     | Se incorpora confirmación explícita.                                        |
| El historial puede quedar desactualizado visualmente.     | El wireframe muestra el historial actualizado después del registro.         |
| El error podría comunicarse solamente mediante color.     | Los mensajes utilizan texto además de cualquier indicador visual.           |
