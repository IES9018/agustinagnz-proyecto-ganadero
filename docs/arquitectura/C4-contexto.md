# C4 - Nivel Contexto (GanadApp)

```mermaid
flowchart LR
    GA[GanadApp\nSistema de Gestión Ganadera]

    P[Productor Ganadero]
    PC[Personal de Campo]

    P -->|Gestiona información, consulta reportes| GA
    PC -->|Registra ganado, movimientos y sanidad| GA

    DB[(PostgreSQL)]

    GA -->|Persistencia de datos| DB

```
Descripción del sistema

GanadApp es un sistema de gestión ganadera orientado a productores rurales de Malargüe. Permite digitalizar procesos de administración de ganado, sanidad, stock y trazabilidad.

Actores
Productor ganadero: usuario con rol de análisis y control.
Personal de campo: usuario operativo que registra datos diarios.
Sistema externo
Base de datos PostgreSQL: almacenamiento persistente de la información del sistema.
