# Modelo de Dominio – Sistema Ganadapp

## Visión general del dominio

El dominio representa la gestión ganadera orientada a la trazabilidad de animales, eventos sanitarios y control de insumos en establecimientos rurales.

Se modela bajo un enfoque de DDD simplificado, priorizando claridad sobre complejidad técnica.


## Entidades principales

### Usuario
- id_usuario: int
- nombre: string
- email: string
- rol: string
- contacto: string
- estado_activo: boolean
- ultimo_acceso: datetime

### Productor
- id_productor: int
- nombre: string
- documento: string
- contacto: string
- direccion: string
- estado: string

### Establecimiento
- id_establecimiento: int
- nombre: string
- ubicacion: string
- capacidad: int
- estado: string
- id_productor: int

### Animal
- id_animal: int
- identificador: string
- especie: string
- raza: string
- fecha_nacimiento: date
- estado_sanitario: string
- id_establecimiento: int

### EventoSanitario
- id_evento: int
- tipo: string
- fecha: datetime
- descripcion: string
- dosis: string
- id_animal: int
- id_usuario: int

### StockInsumo
- id_stock: int
- tipo_insumo: string
- cantidad: float
- unidad: string
- ubicacion: string
- id_establecimiento: int

---
## Entidades vs Value Objects

En el modelo de dominio se distinguen objetos con identidad propia (Entidades) de objetos definidos por sus valores (Value Objects).

### Entidades

- **Usuario**: entidad porque posee una identidad propia mediante `id_usuario` y mantiene su ciclo de vida independientemente de otros objetos.
- **Productor**: entidad porque posee una identidad propia mediante `id_productor`.
- **Establecimiento**: entidad porque posee una identidad propia mediante `id_establecimiento`.
- **Animal**: entidad porque posee una identidad propia mediante `id_animal` y `identificador`.
- **EventoSanitario**: entidad porque representa un evento individual con identidad propia mediante `id_evento`.
- **StockInsumo**: entidad porque representa el estado del stock de un insumo dentro de un establecimiento y posee identidad mediante `id_stock`.

### Value Objects

- **Raza**: Value Object porque representa una característica del animal que se define por su valor y no requiere identidad propia.
- **Dosis**: Value Object porque representa una cantidad o valor asociado a un evento sanitario y se compara por su valor.
- **Estado sanitario**: Value Object porque representa una condición del animal definida por su valor y no por una identidad independiente.
- **Ubicación**: Value Object porque describe dónde se encuentra un establecimiento y no posee identidad propia dentro del dominio.
- **Contacto**: Value Object porque representa información de contacto y se define por los datos que contiene, no por una identidad independiente.

## Relaciones

- Un productor tiene muchos establecimientos
- Un establecimiento tiene muchos animales
- Un animal tiene muchos eventos sanitarios
- Un usuario registra eventos sanitarios
- Un establecimiento administra stock

---

## Agregados

Los agregados definen grupos de objetos de dominio que deben mantenerse consistentes como una unidad. Cada agregado posee una raíz que controla el acceso y las modificaciones de los objetos que contiene.

### Agregado Animal

**Raíz:** Animal

**Elementos agrupados:**
- Animal
- EventoSanitario

El `Animal` es la raíz del agregado porque posee identidad propia y controla los eventos sanitarios asociados. Los `EventoSanitario` no deben gestionarse de forma independiente de su animal.

### Agregado Establecimiento

**Raíz:** Establecimiento

**Elementos agrupados:**
- Establecimiento
- Animal
- StockInsumo

El `Establecimiento` representa el límite de consistencia para los animales y el stock administrado en él. Las operaciones que afecten estos elementos deben respetar las reglas del establecimiento.

### Agregado Productor

**Raíz:** Productor

**Elementos agrupados:**
- Productor
- Establecimiento

El `Productor` es la raíz de este agregado porque es responsable de los establecimientos que administra.

### Agregado Usuario

**Raíz:** Usuario

**Elementos agrupados:**
- Usuario

El `Usuario` constituye un agregado independiente, ya que su identidad y ciclo de vida no dependen de otros objetos del modelo.

---


## Reglas de negocio

Las reglas de negocio se mantienen como invariantes del dominio y deben ser protegidas por los objetos responsables de cada comportamiento.

- **Animal:** todo animal debe pertenecer a un establecimiento válido y su identificador debe ser único.
- **EventoSanitario:** todo evento sanitario debe estar asociado a un animal existente y su creación debe realizarse a través del agregado `Animal`.
- **StockInsumo:** el stock no puede ser negativo. Esta regla se protege mediante el comportamiento `StockInsumo.AjustarStock()`, que debe rechazar cualquier operación cuyo resultado produzca una cantidad menor que cero.
- **Historial:** no se permiten eliminaciones físicas de registros históricos; los cambios deben conservar la trazabilidad de la información.

---

## Diagrama ER

```mermaid
erDiagram

PRODUCTOR ||--o{ ESTABLECIMIENTO : tiene
ESTABLECIMIENTO ||--o{ ANIMAL : contiene
ANIMAL ||--o{ EVENTO_SANITARIO : registra
USUARIO ||--o{ EVENTO_SANITARIO : crea
ESTABLECIMIENTO ||--o{ STOCK_INSUMO : administra

PRODUCTOR {
  int id_productor
  string nombre
  string documento
}

ESTABLECIMIENTO {
  int id_establecimiento
  string nombre
  string ubicacion
}

ANIMAL {
  int id_animal
  string identificador
  string especie
  string raza
}

EVENTO_SANITARIO {
  int id_evento
  string tipo
  datetime fecha
}

STOCK_INSUMO {
  int id_stock
  string tipo_insumo
  float cantidad
}