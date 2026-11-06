# GanadApp

Sistema web de gestión ganadera para pequeños y medianos productores rurales de Malargüe, Mendoza, Argentina.

## 1. Descripción del sistema

GanadApp es un sistema de información orientado a la digitalización de procesos productivos y sanitarios en el ámbito ganadero rural. Su propósito es centralizar y organizar la información relacionada con productores, establecimientos, animales, eventos sanitarios y stock de insumos, facilitando la gestión operativa y la trazabilidad de los registros.

El sistema está diseñado como un proyecto educativo para la Tecnicatura Superior en Desarrollo de Software, con énfasis en arquitectura de software, modelado de dominio y buenas prácticas de ingeniería.

No busca reemplazar sistemas oficiales ni operar como solución comercial, sino funcionar como un sistema académico extensible.

## 2. Objetivo general

Desarrollar un sistema de gestión ganadera modular que permita registrar, consultar y mantener información estructurada sobre productores, establecimientos, animales, eventos sanitarios y recursos operativos, facilitando la trazabilidad y el control básico en entornos rurales.

## 3. Usuarios del sistema

GanadApp permite el acceso de múltiples usuarios mediante cuentas individuales.

Todos los usuarios cuentan con las mismas funcionalidades y no existen roles ni permisos diferenciados.

Los usuarios pueden trabajar sobre los establecimientos registrados y realizar las operaciones disponibles en el sistema.

**Productor** es una entidad del dominio que representa al titular de la actividad ganadera. No constituye un tipo de usuario ni una cuenta de acceso.

## 4. Alcance funcional del MVP

El sistema incluye las siguientes áreas funcionales:

### 4.1 Gestión de productores y establecimientos

Registro y consulta de productores y sus establecimientos asociados.

Los establecimientos se registran previamente y luego pueden seleccionarse al dar de alta animales.

### 4.2 Gestión de ganado

Registro individual, consulta y actualización de animales con información básica:

- Identificador único.
- Especie.
- Raza.
- Sexo.
- Fecha de nacimiento.
- Estado sanitario.
- Establecimiento al que pertenece.

### 4.3 Trazabilidad y eventos sanitarios

Registro y consulta de eventos asociados al animal, incluyendo:

- Vacunaciones.
- Tratamientos sanitarios.
- Movimientos.
- Historial de eventos.
- Trazabilidad de la información histórica.

### 4.4 Control de stock y alertas básicas

Gestión de insumos operativos:

- Alimentos.
- Medicamentos.
- Insumos generales.

Control de cantidades y alertas básicas relacionadas con:

- Stock bajo o crítico.
- Eventos sanitarios próximos o pendientes.

## 5. Exclusiones del sistema (MVP)

Quedan fuera de la primera versión del sistema:

- Procesamiento financiero o contabilidad formal.
- Integración con organismos externos, como SENASA.
- Dispositivos IoT o hardware especializado.
- Inteligencia artificial o analítica predictiva.
- Aplicaciones móviles nativas.
- GIS o georreferenciación avanzada.
- Interoperabilidad con sistemas oficiales.
- Plataformas de comercio o mercado ganadero.
- Gestión documental con validez legal.
- Arquitectura multi-organización o multi-región.
- Arquitectura distribuida y procesamiento en tiempo real.

Estas capacidades se consideran posibles líneas de evolución futura.

## 6. Funcionalidades futuras (roadmap)

El sistema podrá evolucionar hacia módulos y capacidades adicionales:

- Reportes analíticos y dashboards.
- Gestión económica y rentabilidad.
- Administración geoespacial de campos.
- Alertas inteligentes basadas en patrones históricos.
- Aplicación móvil para operaciones en campo.
- Integración con dispositivos IoT.
- Modelos de inteligencia artificial aplicados a la actividad ganadera.
- Integración con organismos oficiales.
- Módulo de mercado ganadero.
- Gestión documental avanzada.
- Escalabilidad multi-organización.

## 7. Arquitectura del sistema

El sistema utiliza una arquitectura modular monolítica, organizada mediante separación por capas y orientada al dominio.

### Enfoque arquitectónico

- Arquitectura modular monolítica.
- Separación por capas.
- Dominio central: gestión ganadera y trazabilidad.
- Extensibilidad mediante módulos funcionales.

### Stack tecnológico

- **Backend:** Python + FastAPI.
- **Frontend:** HTML, CSS y JavaScript.
- **Comunicación:** API REST.
- **Persistencia:** modelo relacional.
- **Base de datos:** PostgreSQL.

## 8. Estructura del proyecto

El repositorio está organizado en módulos educativos y arquitectónicos:

```text
00_REFERENCIAS/           análisis del dominio y requisitos
01_PLAN_MAESTRO/          visión general y decisiones estratégicas
02_CASOS_DE_USO/          modelado funcional del sistema
03_ARQUITECTURA/          diseño arquitectónico (C4, ADR, patrones)
04_MODELO_DATOS/          modelo de dominio y persistencia
05_AGENTES_IA/            metodología de agentes de desarrollo
06_INTERFAZ_USUARIO/      diseño UI/UX y prototipos
07_IMPLEMENTACION/        guías técnicas y convenciones
08_CODIGO_FUENTE/         implementación real del sistema
```

## 9. Gestión del proyecto

Tablero del sprint: [Kanban](https://github.com/orgs/IES9018/projects/1)