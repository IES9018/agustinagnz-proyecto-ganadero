# Postmortem del cuatrimestre — GanadApp

## 1. Objetivo

Documentar los principales incidentes relacionados con el uso de
herramientas de inteligencia artificial durante el desarrollo de
GanadApp.

El análisis identifica las situaciones detectadas, sus consecuencias,
los mecanismos de corrección y las medidas preventivas incorporadas
al proceso de desarrollo.

El objetivo no es atribuir decisiones a las herramientas de IA, sino
evaluar cómo se utilizaron, qué controles resultaron necesarios y
cómo mejorar la calidad de los entregables.

## 2. Contexto

GanadApp fue desarrollado individualmente como proyecto académico
de la Tecnicatura Superior en Desarrollo de Software.

Las herramientas de IA se utilizaron como apoyo para:

- Análisis y organización de requisitos.
- Redacción de especificaciones.
- Elaboración de decisiones arquitectónicas.
- Revisión de documentación.
- Propuestas de implementación.
- Análisis de problemas técnicos.

La aceptación de cambios y las decisiones finales permanecieron bajo
responsabilidad de la estudiante.

## 3. Incidentes identificados

### INC-01 — Entregable arquitectónico inicialmente incompleto

**Descripción**

Durante la elaboración de ADR-001 se detectó que una primera propuesta
generada mediante IA presentaba una estructura aparentemente completa,
pero no cumplía todos los criterios necesarios para justificar la
decisión arquitectónica.

La versión inicial debió mejorarse incorporando criterios ponderados
y trazabilidad.

**Detección**

Revisión humana del documento contra los criterios solicitados
para el entregable.

**Consecuencia**

La primera propuesta no podía considerarse una decisión arquitectónica
suficientemente fundamentada.

**Corrección**

Se revisó y mejoró ADR-001 antes de aceptarlo como documento oficial.

**Capa de prevención**

- Revisión de la consigna antes de redactar.
- Verificación de criterios de decisión.
- Revisión humana de la justificación.
- Comparación del documento final con los requisitos solicitados.

**Estado**

Corregido.

### INC-02 — Propuestas de implementación incompatibles con la arquitectura

**Descripción**

Durante el desarrollo se recibieron propuestas de implementación
que no respetaban completamente la arquitectura existente o los
requisitos definidos para GanadApp.

**Detección**

Contraste de las propuestas con la estructura del repositorio,
la especificación y las decisiones arquitectónicas vigentes.

**Consecuencia**

Las propuestas no podían incorporarse directamente sin riesgo
de introducir inconsistencias técnicas o funcionales.

**Corrección**

Se rechazaron las propuestas incompatibles y se reforzó la revisión
previa a cualquier implementación.

**Capa de prevención**

- Consulta obligatoria de SPEC.md.
- Consulta de los ADR relacionados.
- Revisión de la estructura existente.
- Restricciones técnicas en .opencoderules.
- Pruebas automatizadas de regresión.

**Estado**

Controlado mediante revisión y restricciones de desarrollo.

### INC-03 — Documentación y contratos con información incorrecta

**Descripción**

Durante el desarrollo se identificaron propuestas de documentación
y contratos que contenían información incorrecta o que no representaban
fielmente el estado real del sistema.

**Detección**

Comparación de los documentos generados con los requisitos y la
implementación efectiva.

**Consecuencia**

Una documentación incorrecta podía transmitir una descripción
inexacta de las funcionalidades, decisiones o contratos de la API.

**Corrección**

Se revisó la documentación contra la implementación real y se
corrigieron las inconsistencias antes de considerar los documentos
como válidos.

**Capa de prevención**

- Contrato OpenAPI como referencia para los endpoints.
- Validación automática del contrato mediante Redocly.
- Revisión cruzada entre SPEC, ADR y código.
- Pruebas automatizadas.
- Aprobación humana antes de aceptar documentación.

**Estado**

Controlado mediante revisión documental y controles de calidad.

## 4. Análisis de causas

Los incidentes identificados comparten una causa transversal:
las respuestas generadas mediante IA pueden ser plausibles y
formalmente correctas sin representar necesariamente los requisitos
o el estado real del proyecto.

Se identifican tres riesgos principales:

1. Aceptar propuestas por su presentación formal sin comprobar que cumplan los criterios de la consigna.
2. Incorporar soluciones técnicamente razonables pero incompatibles con la arquitectura o el alcance definido.
3. Mantener documentos individualmente correctos que, al compararse, contengan contradicciones entre sí.

## 5. Medidas preventivas

### 5.1. Prevención documental

- Mantener SPEC.md como referencia funcional y técnica.
- Formalizar decisiones arquitectónicas mediante ADR.
- Documentar el contrato de API antes de implementar endpoints.
- Mantener las reglas de desarrollo actualizadas.

### 5.2. Prevención técnica

- Ejecutar pruebas automatizadas.
- Compilar los módulos Python.
- Validar OpenAPI mediante Redocly.
- Ejecutar controles mediante GitHub Actions.
- Impedir la integración de Pull Requests con CI fallido.

### 5.3. Control humano

- Revisar cada propuesta antes de implementarla.
- Comparar los cambios con la consigna.
- Verificar los resultados en el código y las pruebas.
- No declarar funcionalidades ni controles como completados sin evidencia reproducible.

## 6. Lecciones aprendidas

El uso de IA no elimina la necesidad de análisis, revisión ni
validación técnica.

Una propuesta generada debe considerarse una hipótesis de solución
hasta que se compruebe su correspondencia con el proyecto.

La calidad del resultado depende de mantener un proceso en el que
las decisiones, los cambios y los documentos sean revisados y
verificados por la responsable del desarrollo.

La automatización permite reducir verificaciones manuales repetitivas,
pero no reemplaza la revisión arquitectónica ni la aceptación funcional.

## 7. Evidencias

- `docs/auditoria/auditoria-sprint1.md`
- `docs/auditoria/auditoria-sprint2.md`
- `docs/auditoria/auditoria-sprint3.md`
- `SPEC.md`
- `docs/arquitectura/api-contracts.yaml`
- `docs/adr/`
- `.opencoderules`
- `.github/workflows/ci.yml`

## 8. Conclusión

Durante el cuatrimestre se incorporaron mecanismos de control para reducir el riesgo de aceptar propuestas incorrectas o incompatibles con el proyecto.

La responsabilidad sobre los requisitos, la arquitectura, la implementación y la aceptación de los entregables permaneció bajo control humano.

El proceso de desarrollo asistido por IA se considera válido cuando las propuestas se contrastan con la documentación, el código, las pruebas y las consignas académicas.