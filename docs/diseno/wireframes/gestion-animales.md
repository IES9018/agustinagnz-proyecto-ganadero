# Wireframe de baja fidelidad — Gestión de Animales

## 1. Objetivo

Permitir al usuario consultar los animales registrados y acceder al registro de un nuevo animal.

La pantalla debe diferenciar claramente:

* registros disponibles;
* ausencia de registros;
* carga en proceso;
* error de consulta.

La pantalla mantiene los criterios UX definidos previamente para GanadApp.

---

## 2. Wireframe — estado normal

```text
+----------------------------------------------------------------+
| GANADAPP | GESTIÓN DE ANIMALES                         | usuario |
+----------------------------------------------------------------+
|                                                                |
| [ + Nuevo animal ]                                             |
|                                                                |
| ANIMALES REGISTRADOS                                           |
|                                                                |
| ID        | Raza       | Estado sanitario | Establecimiento    |
|----------------------------------------------------------------|
| 01        | Angus      | Sano             | Campo 1            |
| 02        | Hereford   | Alerta           | Campo 2            |
|                                                                |
+----------------------------------------------------------------+
```

### Estructura

1. Header: identifica sistema, pantalla y usuario.
2. Acción principal: `+ Nuevo animal`.
3. Tabla: muestra información esencial para la consulta.
4. Estado sanitario: permanece visible para facilitar la identificación de información crítica.

---

## 3. Wireframe — estado de carga

```text
+----------------------------------------------------------------+
| GANADAPP | GESTIÓN DE ANIMALES                         | usuario |
+----------------------------------------------------------------+
|                                                                |
| [ + Nuevo animal ]                                             |
|                                                                |
| Consultando animales...                                       |
|                                                                |
| [ Cargando información... ]                                    |
|                                                                |
+----------------------------------------------------------------+
```

El mensaje permite distinguir una consulta en proceso de una consulta sin resultados.

---

## 4. Wireframe — estado vacío

```text
+----------------------------------------------------------------+
| GANADAPP | GESTIÓN DE ANIMALES                         | usuario |
+----------------------------------------------------------------+
|                                                                |
| [ + Nuevo animal ]                                             |
|                                                                |
| Aún no hay animales registrados.                               |
|                                                                |
| [ + Registrar primer animal ]                                  |
|                                                                |
+----------------------------------------------------------------+
```

El estado vacío no debe presentarse como un error.

La acción permite continuar directamente con el registro.

---

## 5. Wireframe — estado de error

```text
+----------------------------------------------------------------+
| GANADAPP | GESTIÓN DE ANIMALES                         | usuario |
+----------------------------------------------------------------+
|                                                                |
| [ + Nuevo animal ]                                             |
|                                                                |
| No se pudieron cargar los animales.                            |
| Verifique la conexión e intente nuevamente.                    |
|                                                                |
| [ Reintentar ]                                                 |
|                                                                |
+----------------------------------------------------------------+
```

El usuario recibe una explicación y una acción concreta de recuperación.

---

## 6. Wireframe — registro

```text
+----------------------------------------------------------------+
| GANADAPP | GESTIÓN DE ANIMALES                         | usuario |
+----------------------------------------------------------------+
|                                                                |
| NUEVO ANIMAL                                                   |
|                                                                |
| Identificador *       [________________________]               |
| Especie *             [________________________]               |
| Raza *                [________________________]               |
| Fecha de nacimiento * [________________________]               |
| Estado sanitario *    [________________________]               |
| Establecimiento *     [________________________]               |
|                                                                |
| [ Cancelar ]                         [ Guardar animal ]         |
|                                                                |
+----------------------------------------------------------------+
```

---

## 7. Objetivo de la pantalla

Administrar animales y consultar su estado sanitario.

---

## 8. Entrada principal

La acción principal es:

`+ Nuevo animal`

El formulario requiere los datos definidos por el modelo de dominio:

* identificador;
* especie;
* raza;
* fecha de nacimiento;
* estado sanitario;
* establecimiento.

---

## 9. Error más probable

El error más relevante es intentar registrar un animal utilizando un identificador que ya existe.

La especificación establece que el identificador del animal debe ser único.

---

## 10. Prevención del error

La interfaz debe:

1. identificar el campo como `Identificador`;
2. marcarlo como obligatorio;
3. validar el valor antes de completar el registro;
4. informar específicamente si el identificador ya existe;
5. mantener los datos ingresados para evitar que el usuario tenga que completar nuevamente todo el formulario.

Ejemplo de mensaje:

```text
No se puede registrar el animal.
El identificador ingresado ya existe.
Ingrese un identificador diferente.
```

---

## 11. Accesibilidad mínima 

La pantalla debe cumplir como mínimo:

* todos los controles deben poder alcanzarse mediante teclado;
* el orden de foco debe seguir una secuencia lógica;
* los botones deben tener nombres comprensibles;
* los campos deben estar asociados a sus etiquetas;
* el texto y los controles deben mantener contraste suficiente para el nivel AA definido en el alcance del TP3;
* los estados de error no deben depender exclusivamente del color.

---

## 12. Correcciones aplicadas a partir de la auditoría heurística

Se incorporan las siguientes decisiones al wireframe:

| Problema                                                                      | Corrección                                                                          |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Un error genérico no explica qué hacer.                                       | El estado de error incluye una explicación y `Reintentar`.                          |
| El estado vacío puede confundirse con un error.                               | Se utiliza un mensaje específico de ausencia de registros y una acción de registro. |
| Un identificador duplicado puede impedir el registro sin orientar al usuario. | Se define validación específica y mensaje de corrección.                            |
| Los campos obligatorios no estaban explicitados.                              | Se incorpora `*` en los campos requeridos.                                          |
| El usuario puede no saber si el registro terminó correctamente.               | Se exige confirmación y actualización visible del listado.                          |
