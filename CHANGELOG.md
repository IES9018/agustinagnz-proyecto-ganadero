# Changelog

Todos los cambios relevantes de GanadApp se documentan en este archivo.

El formato sigue las convenciones de Keep a Changelog y utiliza versionado
semántico.

## [0.1.0] - 2026-11-16

### Added

- Autenticación de usuarios mediante correo electrónico y contraseña.
- Autenticación basada en tokens JWT.
- Registro, consulta y actualización de animales.
- Gestión de eventos sanitarios y vacunaciones.
- Consulta del historial sanitario y trazabilidad de animales.
- Gestión de insumos y operaciones de stock.
- Control para impedir cantidades de stock negativas.
- Interfaz web organizada mediante una arquitectura MPA.
- Adaptación responsive de las pantallas críticas de Gestión de Animales
  y Vacunación.
- Contrato de API REST documentado mediante OpenAPI.
- Pruebas automatizadas de seguridad y reglas de negocio.
- Despliegue de la aplicación en Render.

### Fixed

- Correcciones de validaciones de animales, sanidad y stock.
- Normalización de fechas de nacimiento.
- Correcciones de validación de fechas sanitarias opcionales.
- Unificación de la autenticación de usuarios.
- Eliminación de la diferenciación de permisos por rol.
- Corrección de inconsistencias en las operaciones de la API.
- Correcciones de navegación y estados de la interfaz.

### Documentation

- Incorporación de decisiones arquitectónicas ADR-001 a ADR-006.
- Documentación del contrato OpenAPI.
- Incorporación del modelo de amenazas.
- Documentación del despliegue.
- Documentación de presupuestos y mediciones de rendimiento.
- Documentación de la estrategia mobile y del alcance offline.
- Incorporación de wireframes responsive.
- Registro de auditorías y verificaciones de calidad.
- Consolidación de las reglas de asistencia mediante IA.
- Incorporación del postmortem del cuatrimestre.