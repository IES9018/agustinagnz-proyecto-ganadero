Ganadapp

Sistema de gestión ganadera para pequeños y medianos productores rurales de Malargüe (Mendoza, Argentina).

1. Descripción del sistema

Ganadapp es un sistema de información orientado a la digitalización de procesos productivos y sanitarios en el ámbito ganadero rural. Su propósito es reemplazar registros manuales dispersos por una estructura centralizada, consistente y trazable, permitiendo mejorar la gestión operativa del ganado, el seguimiento sanitario y el control básico de insumos.

El sistema está diseñado como un proyecto educativo para la Tecnicatura Superior en Desarrollo de Software, con énfasis en arquitectura de software, modelado de dominio y buenas prácticas de ingeniería.

No busca reemplazar sistemas oficiales ni operar como solución comercial, sino funcionar como un sistema académico extensible.

2. Objetivo general

Desarrollar un sistema de gestión ganadera modular que permita registrar, consultar y mantener información estructurada sobre ganado, eventos sanitarios y recursos operativos, facilitando la trazabilidad y el control básico en entornos rurales.

3. Usuarios del sistema

El sistema contempla dos perfiles principales:

- Productor ganadero

Responsable de la gestión global del establecimiento. Accede a información consolidada, toma decisiones productivas y consulta reportes operativos.

- Personal de campo

Encargado de la carga operativa de datos en terreno. Registra eventos sanitarios, movimientos de animales y actualización de información de stock.

4. Alcance funcional del MVP

El sistema en su primera versión incluye tres módulos principales:

4.1 Gestión de ganado

Registro individual de animales con información básica:

- identificación única

- especie

- raza

- edad

- estado sanitario


4.2 Trazabilidad y eventos

Registro de eventos asociados al ciclo de vida del animal:

- vacunaciones

- tratamientos sanitarios

- movimientos entre campos o lotes

- cambios de estado


4.3 Control de stock y alertas básicas

Gestión de insumos operativos:

- alimentos

- medicamentos

- insumos generales


Sistema de alertas simples basado en umbrales:

- stock crítico

- eventos sanitarios próximos o pendientes


5. Exclusiones del sistema (MVP)

Quedan fuera de la primera versión del sistema:

- procesamiento financiero o contabilidad formal

- integración con organismos externos (SENASA u otros)

- dispositivos IoT o hardware especializado

- inteligencia artificial o analítica predictiva

- sistemas móviles nativos

- GIS o georreferenciación avanzada

- interoperabilidad con sistemas oficiales

- plataformas de comercio o mercado ganadero

- gestión documental con validez legal

- arquitectura multi-organización o multi-región


Estas capacidades se consideran evolución futura.

6. Funcionalidades futuras (roadmap)

El sistema podrá evolucionar hacia módulos avanzados:

- reportes analíticos y dashboards

- gestión económica y rentabilidad

- administración geoespacial de campos

- alertas inteligentes basadas en patrones históricos

- aplicación móvil con operación en campo

- integración con dispositivos IoT

- modelos de inteligencia artificial aplicada al ganado

- integración con organismos oficiales

- módulo de mercado ganadero

- gestión documental avanzada

- escalabilidad multi-organización


7. Arquitectura del sistema

El sistema sigue un enfoque modular orientado a dominio.

enfoque arquitectónico

- arquitectura modular monolítica

- separación por capas

- dominio central: gestión de ganado y trazabilidad

extensibilidad por módulos funcionales

- propuesta tecnológica
  
- backend: Python + FastAPI
  
- base de datos: SQLite (MVP) / PostgreSQL (evolución)
  
- frontend: React o Vue
  
- comunicación: API REST
  
- persistencia: modelo relacional

1. Estructura del proyecto

El repositorio está organizado en módulos educativos y arquitectónicos:

00_REFERENCIAS/           análisis del dominio y requisitos

01_PLAN_MAESTRO/          visión general y decisiones estratégicas

02_CASOS_DE_USO/          modelado funcional del sistema

03_ARQUITECTURA/          diseño arquitectónico (C4, ADR, patrones)

04_MODELO_DATOS/          modelo de dominio y persistencia

05_AGENTES_IA/            metodología de agentes de desarrollo

06_INTERFAZ_USUARIO/      diseño UI/UX y prototipos

07_IMPLEMENTACION/        guías técnicas y convenciones

08_CODIGO_FUENTE/         implementación real del sistema

## 🗓️ Gestión

Tablero del sprint: [Kanban](https://github.com/orgs/IES9018/projects/1)