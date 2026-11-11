# Arquitectura de GanadApp

Esta carpeta contiene la documentación de arquitectura del sistema GanadApp, incluyendo los diagramas C4 y el contrato de la API REST.

## Contenido de la carpeta

| Archivo | Descripción |
|---|---|
| `C4-contexto.md` | Diagrama C4 de nivel 1. Describe el sistema, sus actores y sus relaciones con el entorno. |
| `C4-contenedores.md` | Diagrama C4 de nivel 2. Representa la aplicación web, el backend FastAPI y la base de datos PostgreSQL. |
| `api-contracts.yaml` | Contrato OpenAPI 3.1.0 de las operaciones críticas de la API REST. |
| `README.md` | Índice y descripción de la documentación de esta carpeta. |

## Arquitectura general

GanadApp utiliza una arquitectura de aplicación web con un backend desarrollado en FastAPI, una interfaz implementada con HTML, CSS y JavaScript, y PostgreSQL como sistema de persistencia.

El backend centraliza las operaciones de negocio y expone los recursos mediante una API REST.

## Diagramas C4

### Nivel 1 — Contexto

El archivo `C4-contexto.md` describe GanadApp como sistema, sus usuarios y la relación con PostgreSQL.

### Nivel 2 — Contenedores

El archivo `C4-contenedores.md` representa los principales contenedores tecnológicos:

- Web App: HTML, CSS y JavaScript.
- Backend API: FastAPI.
- Base de datos: PostgreSQL.

## Contrato de API

El archivo `api-contracts.yaml` define las operaciones críticas mediante OpenAPI 3.1.0.

Incluye:

- `POST /auth/login`: autenticación y emisión de un token JWT.
- `GET /auth/perfil`: consulta del perfil del usuario autenticado.
- `POST /api/animales`: registro de animales.
- `GET /api/animales/{animal_id}`: consulta de un animal.
- `POST /api/animales/{animal_id}/sanidad`: registro de eventos sanitarios.
- `POST /api/stock/{stock_id}/movimientos`: registro de movimientos de stock.

Las operaciones protegidas utilizan autenticación HTTP Bearer mediante tokens JWT. El cliente debe enviar el token en el encabezado `Authorization` para acceder a los recursos protegidos.

La interfaz web utiliza JavaScript para administrar el token de acceso y adjuntarlo a las solicitudes HTTP. La protección de los datos se aplica en el backend mediante la validación del token en los endpoints protegidos.

## Validación del contrato

Se utiliza Redocly CLI para validar la sintaxis y consistencia del documento OpenAPI.


## Configuración de Redocly

La configuración del linter se encuentra en el archivo `redocly.yaml`, ubicado en la raíz del repositorio. Este archivo extiende las reglas recomendadas de Redocly y establece excepciones específicas para las respuestas HTTP que no siguen el patrón genérico de respuestas 2XX y 4XX.

Estas excepciones corresponden al comportamiento implementado en la API: el registro de usuarios responde mediante una redirección HTTP 303 y el cierre de sesión responde con HTTP 204 sin contenido.

## Ejecución y resultado de la validación

Para validar el contrato, ejecutar desde la raíz del repositorio:

```bash
npx --yes @redocly/cli lint docs/arquitectura/api-contracts.yaml
```

La validación se considera satisfactoria cuando Redocly informa que la descripción de la API es válida y no presenta errores ni advertencias pendientes.

Resultado obtenido:

- Herramienta: Redocly CLI.
- Formato del contrato: OpenAPI 3.1.0.
- Estado: validación exitosa.


El contrato debe mantenerse sincronizado con la implementación del backend. Toda modificación de los endpoints, parámetros, esquemas, mecanismos de autenticación o respuestas debe reflejarse en `api-contracts.yaml` y validarse nuevamente antes de registrar los cambios.

