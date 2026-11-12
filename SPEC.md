# SPEC-000: GanadApp - Gestión Ganadera

## 1. Contexto y Propósito

GanadApp es una aplicación orientada a la gestión de establecimientos ganaderos. Su propósito es centralizar y organizar la información relacionada con animales, lotes, movimientos y actividades del establecimiento, facilitando el registro, consulta y seguimiento de los datos.

El proyecto busca resolver la necesidad de contar con una herramienta que permita al usuario gestionar la información ganadera de manera estructurada, evitando la dispersión de datos y facilitando el acceso a información relevante para la gestión cotidiana.

En esta etapa, el objetivo es desarrollar un MVP que cubra las operaciones principales de registro y consulta de información ganadera, con una arquitectura preparada para futuras ampliaciones.

## 2. Requerimientos Funcionales

* [x] **RF-01:** El sistema deberá permitir la autenticación de usuarios mediante correo electrónico y contraseña.

* [x] **RF-02:** El sistema deberá permitir el registro de múltiples usuarios, todos con las mismas funcionalidades y sin diferenciación de permisos por rol.

* [x] **RF-03:** El sistema deberá permitir registrar animales individualmente.

* [x] **RF-04:** El sistema deberá permitir actualizar y consultar la información de los animales registrados.

* [x] **RF-05:** El sistema deberá identificar cada animal mediante un identificador único.

* [x] **RF-06:** El sistema deberá almacenar información básica del animal, incluyendo especie, raza, sexo, fecha de nacimiento y estado sanitario.

* [x] **RF-07:** El sistema deberá permitir registrar eventos asociados a los animales.

* [x] **RF-08:** El sistema deberá permitir registrar vacunaciones, tratamientos sanitarios y movimientos como eventos asociados al animal.

* [x] **RF-09:** El sistema deberá permitir consultar el historial de eventos de un animal.

* [x] **RF-10:** El sistema deberá permitir consultar la trazabilidad completa de un animal.

* [x] **RF-11:** El sistema deberá permitir registrar y actualizar información de stock de insumos.

* [x] **RF-12:** El sistema deberá permitir gestionar insumos operativos, incluyendo alimentos, medicamentos e insumos generales.

* [x] **RF-13:** El sistema deberá controlar que la cantidad de stock no resulte negativa.

* [ ] **RF-14:** El sistema deberá generar alertas básicas cuando el stock alcance condiciones definidas como críticas o bajas.

* [x] **RF-15:** El sistema deberá generar alertas relacionadas con eventos sanitarios próximos o pendientes.

* [x] **RF-16:** El sistema deberá mantener la trazabilidad de los registros históricos y evitar eliminaciones físicas de información histórica.
  
* [ ] **RF-17**: El sistema deberá permitir registrar y consultar productores como entidades del dominio.
  
* [ ] **RF-18**: El sistema deberá permitir registrar y consultar establecimientos asociados a un productor.
  
* [x] **RF-19**: El sistema deberá permitir seleccionar un establecimiento previamente registrado al dar de alta un animal.
  

  

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
- **ADR-004 — Selección del stack de interfaz de usuario:** establece HTML, CSS y JavaScript como tecnologías de interfaz para el MVP, sin incorporar un framework SPA como dependencia obligatoria.
- **ADR-005 — Selección de la estrategia web:** establece una arquitectura MPA con páginas independientes, frontend servido por FastAPI y comunicación mediante API REST.

Estas decisiones restringen la incorporación de nuevas tecnologías y componentes arquitectónicos. La incorporación de un framework, base de datos, servicio externo o cambio significativo del estilo arquitectónico deberá estar respaldada por una decisión arquitectónica documentada mediante un ADR aprobado.

La implementación de nuevos endpoints deberá respetar el contrato OpenAPI establecido en `docs/arquitectura/api-contracts.yaml`.

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

Los contratos de datos utilizados para la comunicación entre el frontend y el backend se encuentran centralizados en:

`docs/arquitectura/api-contracts.yaml`

Este archivo constituye la fuente de verdad para la definición de los contratos HTTP de GanadApp.

La especificación utiliza OpenAPI 3.1.0 y define los esquemas reutilizables dentro de `components.schemas`.

La SPEC no duplica las estructuras de solicitudes y respuestas mediante definiciones paralelas. En su lugar, referencia los esquemas definidos en el contrato OpenAPI por su nombre.

### 5.1. Esquemas de datos

Los principales esquemas utilizados por las operaciones de la API son:

| Esquema OpenAPI | Responsabilidad |
|---|---|
| `AnimalInput` | Define los datos de entrada para registrar o actualizar animales. |
| `AnimalResponse` | Define la estructura de respuesta de los datos de un animal. |
| `EventoSanitarioInput` | Define los datos necesarios para registrar un evento sanitario. |
| `InsumoInput` | Define los datos de entrada para las operaciones de gestión de insumos. |
| `MovimientoStockInput` | Define los datos necesarios para registrar movimientos de stock. |
| `TrazabilidadResponse` | Define la estructura de respuesta de la información de trazabilidad. |

Las referencias completas corresponden a los siguientes identificadores:

- `#/components/schemas/AnimalInput`
- `#/components/schemas/AnimalResponse`
- `#/components/schemas/EventoSanitarioInput`
- `#/components/schemas/InsumoInput`
- `#/components/schemas/MovimientoStockInput`
- `#/components/schemas/TrazabilidadResponse`


Los nombres indicados corresponden a los esquemas definidos en `components.schemas` dentro de `docs/arquitectura/api-contracts.yaml`. Las referencias completas permiten identificar cada esquema de manera unívoca dentro de la especificación OpenAPI.

La incorporación, modificación o eliminación de estos esquemas deberá realizarse en el contrato OpenAPI y mantenerse sincronizada con las implementaciones correspondientes.


### 5.2. Relaciones del dominio

Las entidades principales del sistema mantienen las siguientes relaciones:

- **Productor (1) — (N) Establecimiento:** un productor puede administrar varios establecimientos ganaderos.
- **Establecimiento (1) — (N) Animal:** cada establecimiento puede contener varios animales y cada animal pertenece a un establecimiento.
- **Animal (1) — (N) EventoSanitario:** un animal puede tener múltiples eventos sanitarios asociados.
- **Establecimiento (1) — (N) StockInsumo:** cada establecimiento administra sus registros de stock de insumos.


**Reglas del dominio:**

- Cada animal debe tener un identificador único.
- Todo animal debe pertenecer a un establecimiento existente.
- Cada evento sanitario debe estar asociado a un animal existente.
- Los eventos sanitarios se gestionan en relación con el animal correspondiente.
- El stock de insumos no puede tener cantidades negativas.
- Los movimientos y eventos deben conservar la información histórica necesaria para la trazabilidad.

### 5.3. Reglas de consistencia

Los contratos deberán respetar las siguientes reglas:

- El frontend deberá enviar los datos de acuerdo con los esquemas de entrada definidos en OpenAPI.
- El backend deberá validar los datos recibidos antes de ejecutar las operaciones de negocio.
- Las respuestas deberán respetar los esquemas definidos para cada operación.
- Los identificadores deberán cumplir los tipos y restricciones establecidos en el contrato.
- Las fechas deberán utilizar los formatos documentados.
- Los campos obligatorios y opcionales deberán coincidir con sus definiciones OpenAPI.
- Los errores deberán utilizar los códigos de estado y estructuras de respuesta documentados.
- Los cambios en los contratos deberán reflejarse primero en `api-contracts.yaml` y posteriormente en la implementación.
- Las operaciones protegidas de la API, incluido el registro de eventos sanitarios, requieren autenticación mediante un token JWT Bearer válido. La autenticación controla el acceso, pero no implica que el usuario ejecutor quede registrado como autor del evento.

### 5.4. Relación entre el dominio y los contratos de API

Los esquemas OpenAPI representan los datos intercambiados mediante HTTP. No reemplazan el modelo de dominio ni las entidades utilizadas por la persistencia.

Las entidades del dominio, sus relaciones y las reglas de integridad se mantienen definidas mediante los modelos, servicios y repositorios del backend.

La separación de responsabilidades es la siguiente:

| Componente | Responsabilidad |
|---|---|
| `api-contracts.yaml` | Define los contratos externos de la API. |
| `src/schemas/` | Define los esquemas utilizados para validar y estructurar los datos de entrada y salida de las rutas que los incorporan. |
| `src/models/` | Representa las entidades persistentes del dominio. |
| `src/services/` | Implementa las reglas y operaciones de negocio. |
| `src/repositories/` | Gestiona el acceso a la persistencia. |

Esta separación evita duplicar definiciones y permite modificar la implementación interna sin alterar innecesariamente el contrato público de la API.

### 5.5. Versionado y evolución

Toda modificación de un esquema utilizado por la API deberá reflejarse en `docs/arquitectura/api-contracts.yaml`.

Los cambios deberán validarse mediante Redocly y pruebas de contrato con Schemathesis.

No se deberán introducir estructuras de solicitud o respuesta nuevas directamente en la implementación sin actualizar previamente la especificación OpenAPI.


## 6. Criterios de Aceptación en Gherkin

Los criterios de aceptación relacionados con la interacción de usuario se expresan mediante escenarios Given/When/Then.

### RF-01 / CA-01 — Autenticación

```gherkin
Scenario: Usuario con credenciales válidas
  Given que el usuario posee credenciales válidas
  When ingresa sus credenciales y envía el formulario
  Then el sistema debe autenticarlo
  And debe permitirle acceder a todas las funcionalidades del sistema
```

### RF-03 / CA-04 — Registro de animal

```gherkin
Scenario: Registrar un animal con información válida
  Given que el usuario se encuentra en Gestión de Animales
  And existe al menos un establecimiento registrado
  When completa identificación, especie, raza, sexo, fecha de nacimiento y estado sanitario
  And selecciona un establecimiento existente
  And confirma el registro
  Then el sistema debe guardar el animal asociado al establecimiento seleccionado
  And debe informar que la operación fue realizada correctamente
  And debe mostrar la información actualizada
```

### RF-04 / CA-06 — Consulta de animales

```gherkin
Scenario: Consultar animales registrados
  Given que existen animales registrados
  When el usuario accede a Gestión de Animales
  Then el sistema debe mostrar los animales disponibles
  And debe mostrar su identificador, especie, raza, sexo, edad, estado sanitario y establecimiento
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
  When completa identificador, especie, raza, sexo, fecha de nacimiento y estado sanitario
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
  Given que el usuario se encuentra en la sección de gestión de insumos
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
| v3.0 → v4.0 | 2026-11-03 | Se unificó el modelo de usuarios, eliminando la diferenciación por roles y estableciendo las mismas funcionalidades para todas las cuentas. | Alinear los requerimientos funcionales y el modelo de dominio con la definición actual de usuarios de GanadApp. |
| v3.0 → v4.0 | 2026-11-03 | Se incorporaron los requerimientos RF-17, RF-18 y RF-19 para registrar productores, establecimientos asociados y seleccionar establecimientos existentes al registrar animales. | Formalizar la gestión de productores y establecimientos como parte del dominio del sistema. |
| v3.0 → v4.0 | 2026-11-03 | Se incorporó el sexo entre los datos básicos del animal en el RF-06 y en su contrato de datos. | Completar la información contemplada para el registro y consulta de animales. |
| v4.0 → v5.0 | 2026-11-11 | Se incorporó ADR-005 para formalizar la estrategia web MPA, estableciendo páginas independientes, frontend servido por FastAPI y comunicación mediante API REST. | Documentar la estrategia de presentación y navegación seleccionada para el MVP, justificando la elección frente a SPA, SSR y otras alternativas. |
| v4.0 → v5.0 | 2026-11-11 | Se centralizaron los contratos de datos de la API en `docs/arquitectura/api-contracts.yaml`, reemplazando las definiciones duplicadas por referencias a los esquemas OpenAPI. | Evitar inconsistencias entre la especificación funcional, los contratos HTTP y la implementación del backend. |
| v4.0 → v5.0 | 2026-11-11 | Se incorporaron reglas de consistencia y evolución de contratos, estableciendo la validación mediante Redocly y Schemathesis. | Formalizar el enfoque API-first y establecer mecanismos de verificación de los contratos de la API. |
