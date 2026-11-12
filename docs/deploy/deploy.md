# Despliegue de GanadApp en Render

## 1. Objetivo

Desplegar GanadApp en un entorno accesible públicamente, utilizando Render como plataforma de alojamiento de la aplicación y PostgreSQL como sistema de gestión de base de datos.

El despliegue permite ejecutar la aplicación fuera del entorno local y verificar su funcionamiento con una base de datos alojada en la misma plataforma.

## 2. Infraestructura utilizada

El despliegue se realizó mediante dos servicios de Render:

| Componente | Configuración |
|---|---|
| Aplicación web | `ganadapp` |
| Base de datos | `ganadapp-db` |
| Plataforma | Render |
| Región | Virginia (US East) |
| Motor de base de datos | PostgreSQL |
| Framework backend | FastAPI |
| ORM | SQLAlchemy |
| Controlador PostgreSQL | Psycopg 3 |
| Servidor ASGI | Uvicorn |
| Entorno de ejecución | Python 3 |

La aplicación y la base de datos se encuentran en la misma región. Para la comunicación entre ambos servicios se configuró la conexión interna de PostgreSQL proporcionada por Render.

## 3. Configuración del servicio web

El servicio web se configuró con los siguientes parámetros:

| Parámetro | Valor |
|---|---|
| Repositorio | `IES9018/agustinagnz-proyecto-ganadero` |
| Rama desplegada | `main` |
| Directorio raíz | `08_CODIGO_FUENTE` |
| Comando de compilación | `pip install -r requirements.txt` |
| Comando de inicio | `python -m uvicorn src.main:app --host 0.0.0.0 --port $PORT` |

El directorio raíz permite que Render ejecute los comandos desde la ubicación donde se encuentran las dependencias y el paquete principal de la aplicación.

El servidor Uvicorn utiliza el puerto proporcionado dinámicamente por la plataforma mediante la variable de entorno `PORT`.

No fue necesario incorporar un Dockerfile ni modificar la estructura del proyecto para realizar el despliegue.

## 4. Variables de entorno y configuración

La configuración utiliza variables de entorno para separar los parámetros sensibles del código fuente.

Se configuraron las siguientes variables en Render:

| Variable | Finalidad |
|---|---|
| `DATABASE_URL` | Cadena de conexión a PostgreSQL |
| `JWT_SECRET_KEY` | Clave utilizada para firmar los tokens JWT |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Tiempo de vigencia de los tokens de acceso |

La variable `DATABASE_URL` utiliza la dirección interna de PostgreSQL. Su esquema se configuró para utilizar el controlador Psycopg 3, compatible con las dependencias declaradas en `requirements.txt`.

La clave JWT se generó de forma segura y se almacenó directamente en la configuración del servicio. No se incorporaron credenciales ni secretos al repositorio.

El tiempo de expiración de los tokens se configuró en 30 minutos.

## 5. Inicialización de la base de datos

La aplicación inicializa la estructura de la base de datos durante el inicio del servicio.

En `src/main.py`, el ciclo de vida de FastAPI ejecuta:

`Base.metadata.create_all(bind=engine)`

Esta operación crea las tablas correspondientes a los modelos registrados cuando todavía no existen en la base de datos.

La conexión se administra mediante SQLAlchemy y las sesiones se generan a través de `SessionLocal`, utilizando el motor configurado en `src/core/database.py`.

## 6. Verificación del despliegue

Una vez finalizado el proceso de publicación, se comprobó que Render informara el estado operativo del servicio y que la aplicación respondiera desde su dirección pública.

También se verificó el acceso a las principales rutas de la aplicación:

- `/`: página inicial.
- `/login`: inicio de sesión.
- `/animales`: gestión de animales.
- `/sanidad`: gestión sanitaria y vacunaciones.
- `/docs`: documentación interactiva de la API.

Se comprobó el funcionamiento de la aplicación desplegada y su conexión con PostgreSQL. Las operaciones de la aplicación se ejecutan contra la base de datos alojada en Render, en lugar de utilizar la instancia local.

El despliegue se considera funcional porque el servicio inicia correctamente, establece la conexión con la base de datos y permite utilizar las funcionalidades verificadas desde el navegador.

## 7. Procedimiento para reproducir el despliegue

Para reproducir el despliegue se requiere una cuenta de Render y acceso al repositorio de GitHub.

1. Crear una instancia PostgreSQL en Render, utilizando la región Virginia (US East).
2. Crear un servicio Web Service asociado al repositorio de GanadApp.
3. Seleccionar la rama `main`.
4. Establecer `08_CODIGO_FUENTE` como directorio raíz.
5. Configurar el comando de compilación `pip install -r requirements.txt`.
6. Configurar el comando de inicio `python -m uvicorn src.main:app --host 0.0.0.0 --port $PORT`.
7. Configurar las variables de entorno `DATABASE_URL`, `JWT_SECRET_KEY` y `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`.
8. Utilizar la conexión interna de PostgreSQL para vincular la aplicación con la base de datos.
9. Iniciar el despliegue y comprobar que el servicio alcance el estado operativo.
10. Acceder a la dirección pública asignada por Render y verificar las rutas y funcionalidades principales.

Las credenciales y claves deben generarse nuevamente para cada entorno y almacenarse como variables de entorno, nunca en el repositorio.

## 8. Evaluación del proceso y posibles mejoras

El despliegue permitió comprobar que la arquitectura de GanadApp puede ejecutarse en un entorno de alojamiento externo sin incorporar una infraestructura adicional basada en contenedores.

Para una futura evolución del proyecto, sería conveniente incorporar un proceso de migraciones de base de datos mediante Alembic, en lugar de depender exclusivamente de `create_all()`. Esto permitiría administrar de forma controlada los cambios de esquema entre versiones.

También sería conveniente establecer verificaciones automatizadas posteriores a cada despliegue y configurar un procedimiento de copias de seguridad de la base de datos.

Estas mejoras no forman parte de la configuración implementada en este despliegue, sino que se identifican como trabajo futuro.