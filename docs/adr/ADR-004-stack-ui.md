# ADR-004: Selección del stack de interfaz de usuario

* **Estado:** Aceptado
* **Fecha:** 2026-09-23
* **Decisión:** Utilizar HTML + CSS + JavaScript como base de la interfaz, incorporando un enfoque de componentes y criterios de diseño consistentes sin adoptar un framework SPA para el MVP.

---

## 1. Contexto

GanadApp es una aplicación web para la gestión de información ganadera.

La SPEC v2 establece actualmente:

* Backend: Python + FastAPI.
* Frontend: HTML + CSS + JavaScript (MVP).
* Comunicación: API REST.
* Persistencia: PostgreSQL.
* Arquitectura: monolítica modular.

ADR-002 establece una arquitectura monolítica modular como estilo arquitectónico general.

El TP3 requiere formalizar la decisión sobre el stack de interfaz de usuario considerando:

1. curva de aprendizaje;
2. ecosistema;
3. accesibilidad disponible;
4. compatibilidad con ADR-002.

---

## 2. Decisión

Se mantiene para el MVP un stack de interfaz basado en:

* HTML5 para estructura semántica.
* CSS3 para presentación y diseño.
* JavaScript para comportamiento e interacción.
* Componentes reutilizables definidos mediante convenciones del proyecto.
* Criterios de accesibilidad aplicados explícitamente a los controles y flujos críticos.

No se incorpora un framework SPA como dependencia obligatoria del MVP.

La interfaz deberá conservar los patrones definidos en los documentos UX:

* header consistente;
* acción principal debajo del header;
* formularios con etiquetas claras;
* tablas para consulta;
* estados de carga;
* estados vacíos;
* estados de error;
* confirmaciones;
* navegación mediante teclado;
* contraste adecuado.

---

## 3. Criterios de decisión

### 3.1 Curva de aprendizaje

HTML, CSS y JavaScript forman parte de las tecnologías básicas necesarias para una interfaz web y permiten que el equipo académico trabaje directamente sobre la estructura y comportamiento de las pantallas.

La incorporación de un framework adicional implicaría aprender convenciones y estructuras específicas que no son necesarias para el alcance actual.

### 3.2 Ecosistema

HTML, CSS y JavaScript cuentan con un ecosistema web amplio y estable.

La decisión no impide incorporar posteriormente una biblioteca o framework si una necesidad concreta del sistema lo justifica.

### 3.3 Accesibilidad

El stack seleccionado no proporciona automáticamente todas las garantías de accesibilidad.

Por esta razón, la accesibilidad se establece como responsabilidad explícita del diseño y desarrollo:

* HTML semántico;
* etiquetas asociadas a controles;
* navegación por teclado;
* foco visible;
* mensajes de error comprensibles;
* contraste adecuado;
* no depender exclusivamente del color.


### 3.4 Compatibilidad con ADR-002

La decisión es compatible con ADR-002 porque la interfaz constituye la capa de presentación del sistema y no modifica el estilo arquitectónico monolítico modular.

El uso de HTML, CSS y JavaScript no introduce:

* microservicios;
* procesamiento distribuido;
* nuevos servicios externos;
* una arquitectura independiente;
* una segunda aplicación backend.

---

## 4. Alternativas consideradas

| Alternativa             | Curva de aprendizaje | Ecosistema | Accesibilidad de base                                        | Compatibilidad con ADR-002          | Decisión                                          |
| ----------------------- | -------------------- | ---------- | ------------------------------------------------------------ | ----------------------------------- | ------------------------------------------------- |
| HTML + CSS + JavaScript | Baja                 | Amplio     | Depende de implementación                                    | Compatible                          | Seleccionada                                      |
| React                   | Media                | Amplio     | Requiere aplicación correcta de prácticas de accesibilidad   | Compatible, pero agrega complejidad | Descartada para el MVP                            |
| Vue                     | Media                | Amplio     | Requiere aplicación correcta de prácticas de accesibilidad   | Compatible, pero agrega complejidad | Descartada para el MVP                            |
| Biblioteca CSS/UI       | Baja-media           | Amplio     | Puede aportar componentes accesibles, pero depende de su uso | Compatible                          | No necesaria como dependencia obligatoria del MVP |

---

## 5. Consecuencias positivas

* Mantiene coherencia con la SPEC v2.
* Reduce dependencias del MVP.
* Facilita la comprensión de la estructura de las interfaces.
* Permite implementar los wireframes directamente.
* Mantiene compatibilidad con FastAPI y la API REST.
* No modifica la arquitectura definida en ADR-002.
* Permite incorporar progresivamente componentes reutilizables.

---

## 6. Consecuencias negativas

* La accesibilidad no está garantizada automáticamente por un framework.
* El equipo debe aplicar correctamente las prácticas de accesibilidad.
* La reutilización de componentes debe mantenerse mediante convenciones y estructura de código.
* Una futura interfaz con mayor complejidad podría justificar la evaluación de un framework.

---

## 7. Relación con SPEC

La decisión mantiene:

```text
Frontend
HTML + CSS + JavaScript
        ↓
API REST
        ↓
FastAPI
        ↓
PostgreSQL
```

La incorporación futura de un framework de interfaz requeriría revisar esta decisión y documentarla mediante un nuevo ADR si supone un cambio significativo del stack definido.

---

## 8. Referencias internas

* `SPEC.md`
* `docs/adr/ADR-002-estilo-arquitectonico.md`
* Documentación UX existente de GanadApp.
* Wireframes de `docs/diseno/wireframes/`.
