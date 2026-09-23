# SPEC-000: GanadApp - Gestión Ganadera

## 1. Contexto y Propósito

GanadApp es una aplicación orientada a la gestión de establecimientos ganaderos. Su propósito es centralizar y organizar la información relacionada con animales, lotes, movimientos y actividades del establecimiento, facilitando el registro, consulta y seguimiento de los datos.

El proyecto busca resolver la necesidad de contar con una herramienta que permita al usuario gestionar la información ganadera de manera estructurada, evitando la dispersión de datos y facilitando el acceso a información relevante para la gestión cotidiana.

En esta etapa, el objetivo es desarrollar un MVP que cubra las operaciones principales de registro y consulta de información ganadera, con una arquitectura preparada para futuras ampliaciones.

## 2. Requerimientos Funcionales

* [ ] **RF-01:** El sistema deberá permitir la autenticación de usuarios mediante control de acceso por rol.

* [ ] **RF-02:** El sistema deberá diferenciar los permisos y responsabilidades correspondientes al productor ganadero y al personal de campo.

* [ ] **RF-03:** El sistema deberá permitir registrar animales individualmente.

* [ ] **RF-04:** El sistema deberá permitir actualizar y consultar la información de los animales registrados.

* [ ] **RF-05:** El sistema deberá identificar cada animal mediante un identificador único.

* [ ] **RF-06:** El sistema deberá almacenar información básica del animal, incluyendo especie, raza, fecha de nacimiento y estado sanitario.

* [ ] **RF-07:** El sistema deberá permitir registrar eventos asociados a los animales.

* [ ] **RF-08:** El sistema deberá permitir registrar vacunaciones, tratamientos sanitarios y movimientos como eventos asociados al animal.

* [ ] **RF-09:** El sistema deberá permitir consultar el historial de eventos de un animal.

* [ ] **RF-10:** El sistema deberá permitir consultar la trazabilidad completa de un animal.

* [ ] **RF-11:** El sistema deberá permitir registrar y actualizar información de stock de insumos.

* [ ] **RF-12:** El sistema deberá permitir gestionar insumos operativos, incluyendo alimentos, medicamentos e insumos generales.

* [ ] **RF-13:** El sistema deberá controlar que la cantidad de stock no resulte negativa.

* [ ] **RF-14:** El sistema deberá generar alertas básicas cuando el stock alcance condiciones definidas como críticas o bajas.

* [ ] **RF-15:** El sistema deberá generar alertas relacionadas con eventos sanitarios próximos o pendientes.

* [ ] **RF-16:** El sistema deberá mantener la trazabilidad de los registros históricos y evitar eliminaciones físicas de información histórica.

## 3. Non-Goals (Límites del Alcance)

*Lo que explícitamente NO se construirá en esta etapa:*

* **NG-01:** No se implementará procesamiento financiero ni contabilidad formal.

* **NG-02:** No se implementará integración con SENASA ni con otros organismos externos.

* **NG-03:** No se implementará interoperabilidad con sistemas oficiales.

* **NG-04:** No se implementará integración con dispositivos IoT ni hardware especializado.

* **NG-05:** No se implementará inteligencia artificial ni analítica predictiva.

* **NG-06:** No se desarrollará una aplicación móvil nativa.

* **NG-07:** No se implementará GIS ni georreferenciación avanzada.

* **NG-08:** No se implementará una plataforma de comercio o mercado ganadero.

* **NG-09:** No se implementará gestión documental con validez legal.

* **NG-10:** No se implementará una arquitectura multi-organización o multi-región.

* **NG-11:** No se implementará arquitectura distribuida ni procesamiento en tiempo real.

Las funcionalidades excluidas se consideran posibles líneas de evolución futura del sistema.

## 4. Stack Tecnológico y Restricciones

### Stack tecnológico

* **Backend:** Python + FastAPI
* **Frontend:** HTML + CSS + JavaScript (MVP)
* **Comunicación:** API REST.
* **Persistencia:** modelo relacional.
* **Base de datos:** PostgreSQL.

### Arquitectura

El sistema utilizará una arquitectura modular monolítica, organizada mediante separación por capas y orientada al dominio.

El dominio central estará compuesto por la gestión del ganado y la trazabilidad, con módulos funcionales extensibles para eventos sanitarios y control de stock.

### Restricciones

* El sistema deberá funcionar como una aplicación web accesible desde dispositivos estándar.
* La persistencia deberá realizarse mediante una base de datos relacional.
* La arquitectura deberá mantenerse modular y extensible.
* La interfaz deberá ser simple y adecuada para usuarios de entornos rurales.
* El sistema deberá contemplar su utilización en entornos con conectividad limitada.
* No se incorporarán integraciones externas durante el MVP.

### Restricciones arquitectónicas

Las decisiones arquitectónicas del sistema se encuentran formalizadas en los siguientes Architecture Decision Records:

- **ADR-001 — Selección de arquitectura monolítica con base de datos relacional (PostgreSQL):** establece la arquitectura monolítica modular y la utilización de PostgreSQL como sistema de persistencia.
- **ADR-002 — Selección del estilo arquitectónico:** establece la utilización de una arquitectura monolítica modular como estilo arquitectónico general, considerando el tamaño del equipo, el alcance del sistema, la complejidad operativa y los plazos académicos.
- **ADR-003 — Selección del mecanismo de persistencia:** establece PostgreSQL como mecanismo de persistencia objetivo y fundamenta su elección a partir del modelo relacional de GanadApp.

Estas decisiones restringen la incorporación de nuevas tecnologías y componentes arquitectónicos. La incorporación de un framework, base de datos, servicio externo o cambio significativo del estilo arquitectónico deberá estar respaldada por una decisión arquitectónica documentada mediante un ADR aprobado.

### Requisitos de interfaz y accesibilidad

La interfaz del MVP deberá mantener una estructura simple y consistente con los criterios UX definidos para GanadApp.

Las dos pantallas críticas definidas para el TP3 son:

- Gestión de Animales.
- Vacunación.

En ambas pantallas será obligatorio:

- permitir navegación mediante teclado;
- mantener un orden de foco lógico;
- utilizar etiquetas comprensibles para los campos;
- comunicar errores mediante texto;
- mantener contraste suficiente para cumplir el nivel AA definido para el alcance del TP3;
- no utilizar el color como único medio para comunicar estados;
- mostrar confirmación después de operaciones exitosas.

Estos requisitos se aplican específicamente a las dos pantallas críticas del TP3 y no implican que el MVP deba implementar en esta etapa la totalidad de los criterios de accesibilidad existentes.

## 5. Contratos de Datos / Tipos

Los contratos principales se basan en las entidades definidas actualmente en el modelo de dominio de GanadApp.

```typescript
interface Usuario {
  id_usuario: number;
  nombre: string;
  email: string;
  rol: string;
  contacto: string;
  estado_activo: boolean;
  ultimo_acceso: string;
}

interface Productor {
  id_productor: number;
  nombre: string;
  documento: string;
  contacto: string;
  direccion: string;
  estado: string;
}

interface Establecimiento {
  id_establecimiento: number;
  nombre: string;
  ubicacion: string;
  capacidad: number;
  estado: string;
  id_productor: number;
}

interface Animal {
  id_animal: number;
  identificador: string;
  especie: string;
  raza: string;
  fecha_nacimiento: string;
  estado_sanitario: string;
  id_establecimiento: number;
}

interface EventoSanitario {
  id_evento: number;
  tipo: string;
  fecha: string;
  descripcion: string;
  dosis: string;
  id_animal: number;
  id_usuario: number;
}

interface StockInsumo {
  id_stock: number;
  tipo_insumo: string;
  cantidad: number;
  unidad: string;
  ubicacion: string;
  id_establecimiento: number;
}
```

Las relaciones principales del dominio son:

* Un `Productor` puede tener múltiples `Establecimiento`.
* Un `Establecimiento` puede contener múltiples `Animal`.
* Un `Animal` puede tener múltiples `EventoSanitario`.
* Un `Usuario` puede registrar múltiples `EventoSanitario`.
* Un `Establecimiento` administra `StockInsumo`.

Los objetos `Raza`, `Dosis`, `Estado sanitario`, `Ubicación` y `Contacto` se consideran Value Objects dentro del modelo de dominio.

Las reglas principales asociadas a estos contratos son:

* El identificador de un animal debe ser único.
* Todo animal debe pertenecer a un establecimiento válido.
* Todo evento sanitario debe estar asociado a un animal existente.
* Los eventos sanitarios se gestionan a través del agregado `Animal`.
* El stock no puede resultar negativo.
* Los registros históricos deben conservar su trazabilidad.


## 6. Criterios de Aceptación en Gherkin

Los criterios de aceptación relacionados con la interacción de usuario se expresan mediante escenarios Given/When/Then.

### RF-01 / CA-01 — Autenticación

```gherkin
Scenario: Usuario con credenciales válidas
  Given que el usuario posee credenciales válidas
  When ingresa sus credenciales y envía el formulario
  Then el sistema debe autenticarlo
  And debe mostrar la interfaz correspondiente a su rol
```

### RF-03 / CA-04 — Registro de animal

```gherkin
Scenario: Registrar un animal con información válida
  Given que el usuario se encuentra en Gestión de Animales
  And dispone de un identificador único
  When completa identificación, especie, raza, fecha de nacimiento y estado sanitario
  And confirma el registro
  Then el sistema debe guardar el animal
  And debe informar que la operación fue realizada correctamente
  And debe mostrar la información actualizada
```

### RF-04 / CA-06 — Consulta de animales

```gherkin
Scenario: Consultar animales registrados
  Given que existen animales registrados
  When el usuario accede a Gestión de Animales
  Then el sistema debe mostrar los animales disponibles
  And debe mostrar su identificador, raza, estado sanitario y establecimiento
```

### RF-05 / CA-05 — Identificador único

```gherkin
Scenario: Evitar identificador duplicado
  Given que ya existe un animal con un identificador determinado
  When el usuario intenta registrar otro animal utilizando el mismo identificador
  Then el sistema debe rechazar el registro
  And debe informar que el identificador ya existe
```

### RF-06 — Datos básicos del animal

```gherkin
Scenario: Completar datos básicos del animal
  Given que el usuario está registrando un animal
  When completa especie, raza, fecha de nacimiento y estado sanitario
  Then la interfaz debe permitir enviar los datos para su validación
```

### RF-07 — Registro de evento

```gherkin
Scenario: Registrar un evento asociado a un animal
  Given que existe el animal seleccionado
  When el usuario completa los datos requeridos del evento
  And confirma la operación
  Then el sistema debe registrar el evento asociado al animal
```

### RF-08 / CA-07 — Registro de vacunación

```gherkin
Scenario: Registrar una vacunación válida
  Given que existe el animal seleccionado
  And el usuario se encuentra en Vacunación
  When completa animal, vacuna y fecha
  And confirma el registro
  Then el sistema debe registrar la vacunación
  And debe confirmar la operación
  And debe mostrar el historial actualizado
```

### RF-08 / CA-08 — Validación de vacunación

```gherkin
Scenario: Rechazar una vacunación inválida
  Given que el usuario intenta registrar una vacunación
  When el animal no existe o faltan datos requeridos
  Then el sistema debe rechazar la operación
  And debe informar qué dato debe corregirse
```

### RF-09 / CA-09 — Historial de eventos

```gherkin
Scenario: Consultar historial sanitario
  Given que un animal posee eventos sanitarios registrados
  When el usuario consulta su historial
  Then el sistema debe mostrar los eventos disponibles
```

### RF-10 / CA-10 — Trazabilidad

```gherkin
Scenario: Consultar la trazabilidad de un animal
  Given que el animal posee información histórica registrada
  When el usuario consulta su trazabilidad
  Then el sistema debe mostrar la información histórica correspondiente
```

### RF-11 / CA-11 — Stock

```gherkin
Scenario: Actualizar stock de insumos
  Given que el usuario posee permisos para gestionar insumos
  When registra una operación válida de stock
  Then el sistema debe actualizar la cantidad correspondiente
```

### RF-13 / CA-12 — Stock no negativo

```gherkin
Scenario: Evitar stock negativo
  Given que una operación produciría una cantidad de stock inferior a cero
  When el usuario intenta confirmar la operación
  Then el sistema debe rechazarla
  And debe informar que la cantidad no puede resultar negativa
```

### RF-14 / CA-13 — Alerta de stock

```gherkin
Scenario: Detectar stock bajo o crítico
  Given que un insumo alcanza una condición definida como baja o crítica
  When el sistema actualiza o consulta el stock
  Then debe generar la alerta correspondiente
```

### RF-15 / CA-14 — Alertas sanitarias

```gherkin
Scenario: Detectar evento sanitario próximo o pendiente
  Given que existe un evento sanitario próximo o pendiente
  When el sistema consulta las condiciones de alerta
  Then debe mostrar la alerta correspondiente
```

### RF-16 / CA-15 — Trazabilidad histórica

```gherkin
Scenario: Conservar registros históricos
  Given que existe un registro histórico
  When el usuario realiza una operación sobre información actual
  Then el sistema debe conservar la trazabilidad del registro histórico
  And no debe eliminar físicamente la información histórica
```

---

## Changelog

| Versión     | Fecha      | Cambio                                                                                                                                 | Motivo                                                                                                                    |
| ----------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| v1.0        | 2026-08-25 | Versión inicial de la especificación del proyecto.                                                                                     | Definir el alcance inicial, requerimientos, modelo de dominio y restricciones del MVP.                                    |
| v1.0 → v2.0 | 2026-09-22 | Se incorporó la sección "Restricciones arquitectónicas" con referencias a ADR-001, ADR-002 y ADR-003.                                  | Formalizar las decisiones arquitectónicas adoptadas durante el desarrollo del proyecto.                                   |
| v1.0 → v2.0 | 2026-09-22 | Se estableció PostgreSQL como base de datos del sistema y se eliminó la definición de SQLite como base de datos del MVP.               | Alinear la SPEC con ADR-001 y ADR-003 y con el modelo relacional del dominio.                                             |
| v1.0 → v2.0 | 2026-09-22 | Se revisaron los Non-Goals y se mantienen los límites de alcance definidos en v1.                                                      | Las decisiones arquitectónicas no incorporan nuevos requerimientos funcionales ni modifican los límites actuales del MVP. |
| v2.0 → v3.0 | 2026-09-23 | Se incorporaron criterios de aceptación en formato Gherkin para los requerimientos relacionados con la interacción del usuario.        | Formalizar el comportamiento esperado de la interfaz mediante escenarios Given/When/Then.                                 |
| v2.0 → v3.0 | 2026-09-23 | Se incorporaron requisitos mínimos de accesibilidad para las dos pantallas críticas: navegación mediante teclado y contraste nivel AA. | Incorporar criterios HCI y accesibilidad definidos en TP3.                                                                |
| v2.0 → v3.0 | 2026-09-23 | Se formalizó la selección del stack de interfaz mediante ADR-004.                                                                      | Documentar la decisión tecnológica de la capa de presentación.                                                            |
