# ADR-001: Selección de arquitectura monolítica con base de datos relacional (PostgreSQL)

## Contexto

El sistema GanadApp se desarrolla para la gestión ganadera de pequeños y medianos productores de Malargüe, junto con usuarios institucionales en un entorno académico.

Se estima una concurrencia baja a media (10 a 30 usuarios simultáneos) y un volumen moderado de usuarios (20 a 100 productores). El dominio está compuesto por entidades altamente relacionales como productores, ganado, eventos sanitarios y stock.

---

## Decisión

Se adopta una arquitectura monolítica modular con backend único y base de datos relacional PostgreSQL. El sistema se expondrá mediante una API centralizada consumida por aplicaciones web y móvil.

---

## Opciones consideradas

### Opción A: Arquitectura monolítica modular (seleccionada)
Ventajas:
- Menor complejidad de implementación.
- Adecuada para el volumen de usuarios previsto.
- Facilita el desarrollo en contexto académico.
- Integración natural con PostgreSQL.

Desventajas:
- Escalabilidad limitada a largo plazo.
- Riesgo de acoplamiento si no se modulariza correctamente.

---

### Opción B: Arquitectura de microservicios
Ventajas:
- Escalabilidad independiente por servicio.
- Alta flexibilidad tecnológica.

Desventajas:
- Alta complejidad de infraestructura.
- No justificado para la carga del sistema.
- Exceso de overhead para un cuatrimestre académico.

---
### Criterios de selección ponderados

Para seleccionar la arquitectura se utilizaron los siguientes criterios, considerando el contexto académico, la carga estimada y las necesidades funcionales de GanadApp. La escala utilizada es de 1 a 5, donde 1 representa una situación muy desfavorable y 5 una situación muy favorable.

| Criterio | Peso | Monolito modular | Microservicios |
|---|---:|---:|---:|
| Complejidad de implementación y operación | 30% | 5 | 2 |
| Tiempo de desarrollo | 25% | 5 | 2 |
| Costo de infraestructura | 20% | 5 | 2 |
| Escalabilidad | 25% | 3 | 5 |
| **Puntaje ponderado** | **100%** | **4,50** | **2,75** |

El resultado favorece la arquitectura monolítica modular debido a su menor complejidad, menor tiempo de implementación y menor costo de infraestructura. La arquitectura de microservicios obtiene una mejor puntuación en escalabilidad, pero esta ventaja no compensa su mayor complejidad para la carga y el alcance previstos para GanadApp.

### Trazabilidad con los diagramas C4

La decisión de utilizar una arquitectura monolítica modular se refleja en los diagramas C4 del sistema.

En el C4 de Contexto (Nivel 1), GanadApp se representa como un único sistema que interactúa con sus usuarios y sistemas externos.

En el C4 de Contenedores (Nivel 2), la decisión se materializa principalmente en el contenedor **Backend API**, que centraliza la lógica de negocio y expone la API utilizada por las aplicaciones Web y Mobile. La persistencia se realiza mediante el contenedor **PostgreSQL**.

Esta estructura permite mantener un único backend desplegable, organizado internamente en módulos, evitando distribuir prematuramente la lógica de negocio en múltiples servicios independientes.

La representación detallada de esta decisión se encuentra en el diagrama C4 de Contenedores (Nivel 2), que se encuentra documentado en [`c4-contenedores.md`](https://github.com/Agustinagnz/ADI-Proyecto-ganadero/blob/feat/ej-02-c4-contexto/03_ARQUITECTURA/diagramas/c4-contenedores.md).

## Consecuencias

### Positivas
- Desarrollo más rápido y controlado.
- Consistencia fuerte de datos con PostgreSQL.
- Despliegue simple.
- Adecuado para evolución incremental del sistema.

### Negativas

- La escalabilidad horizontal está limitada por el hecho de que la lógica de negocio se concentra en un único backend.
- La capacidad real del monolito deberá validarse mediante pruebas de carga antes de considerar una evolución arquitectónica.
- Se establece como referencia inicial la carga estimada de 10 a 30 usuarios simultáneos indicada en este ADR, con un escenario de crecimiento de hasta 100 usuarios simultáneos.
- Si las pruebas de carga muestran que el backend no puede sostener el escenario objetivo de 100 usuarios simultáneos con tiempos de respuesta aceptables, se deberá reevaluar la arquitectura y analizar la separación de componentes en servicios independientes.

### Riesgos

- **Acoplamiento entre módulos:** si los módulos del backend comparten responsabilidades o acceden directamente a componentes internos de otros módulos, puede aumentar el costo de mantenimiento. Se mitigará manteniendo responsabilidades y límites claros entre módulos.
- **Sobrecarga del backend:** el crecimiento de usuarios o de operaciones puede aumentar la carga sobre el backend único. Se mitigará mediante pruebas de carga y monitoreo de tiempos de respuesta y utilización de recursos.
- **Necesidad de evolución arquitectónica:** si la carga real supera la capacidad del monolito o determinados módulos requieren escalabilidad independiente, se deberá reevaluar esta decisión y analizar una posible separación de servicios.