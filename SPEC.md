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
* **Base de datos del MVP:** SQLite.
* **Evolución prevista de base de datos:** PostgreSQL.

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

## 6. Criterios de Aceptación

* [ ] **CA-01:** Un usuario puede autenticarse utilizando sus credenciales y acceder al sistema según su rol.

* [ ] **CA-02:** Un productor ganadero puede consultar información consolidada para la gestión del establecimiento.

* [ ] **CA-03:** El personal de campo puede realizar las operaciones de carga de información correspondientes a sus responsabilidades.

* [ ] **CA-04:** El sistema permite registrar un animal con su identificación, especie, raza, fecha de nacimiento y estado sanitario.

* [ ] **CA-05:** El sistema rechaza el registro de un animal cuyo identificador ya exista.

* [ ] **CA-06:** El sistema permite consultar la información registrada de un animal.

* [ ] **CA-07:** El sistema permite registrar un evento sanitario asociado a un animal existente.

* [ ] **CA-08:** El sistema rechaza un evento sanitario cuando el animal asociado no existe o los datos requeridos son inválidos.

* [ ] **CA-09:** El sistema permite consultar el historial de eventos de un animal.

* [ ] **CA-10:** El sistema permite consultar la trazabilidad completa de un animal.

* [ ] **CA-11:** El sistema permite registrar y actualizar el stock de insumos.

* [ ] **CA-12:** El sistema rechaza cualquier operación que produzca una cantidad de stock inferior a cero.

* [ ] **CA-13:** El sistema genera una alerta cuando el stock alcanza una condición definida como baja o crítica.

* [ ] **CA-14:** El sistema genera alertas correspondientes a eventos sanitarios próximos o pendientes.

* [ ] **CA-15:** Los registros históricos mantienen su trazabilidad y no pueden eliminarse físicamente.

* [ ] **CA-16:** La aplicación funciona como sistema web mediante una API REST y una interfaz web.

* [ ] **CA-17:** La estructura del sistema mantiene una separación modular y por capas que permita incorporar funcionalidades futuras.

## Changelog

### v1.0 - 2026-08-25
Versión inicial de la especificación del proyecto.