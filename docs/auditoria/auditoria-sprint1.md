Auditoría crítica del uso de IA — Sprint 1

Proyecto: GanadApp
Repositorio: "IES9018/agustinagnz-proyecto-ganadero"
Sprint: 1
Período: agosto–septiembre 2026
Alcance: "SPEC.md", "docs/adr/ADR-001-stack-tecnologico.md" y ".opencoderules"

---

1. Objetivo de la auditoría

Esta auditoría tiene como objetivo documentar y evaluar críticamente el uso de Inteligencia Artificial durante la elaboración de los entregables correspondientes al Sprint 1 del proyecto GanadApp.

El análisis se concentra exclusivamente en el trabajo asistido por IA para:

- la especificación funcional "SPEC.md";
- la decisión arquitectónica "docs/adr/ADR-001-stack-tecnologico.md";
- el arnés de control de IA ".opencoderules".

El propósito no es demostrar que la IA produjo un resultado correcto de manera autónoma, sino verificar cómo fue utilizada, qué problemas o inconsistencias surgieron durante el proceso, cómo fueron detectados y qué mecanismos humanos se utilizaron para corregirlos y validar el resultado final.

---

2. Criterio de evaluación

El uso de IA se evaluó considerando cuatro aspectos principales:

1. Asistencia: qué tareas fueron delegadas a la IA.
2. Control: qué decisiones permanecieron bajo responsabilidad humana.
3. Verificación: cómo se comprobaron las propuestas generadas.
4. Corrección: qué modificaciones fueron necesarias antes de considerar los documentos como entregables válidos.

La IA se utilizó principalmente como herramienta de apoyo para redactar, estructurar, revisar y proponer alternativas. La decisión definitiva sobre el contenido del proyecto correspondió al autor del repositorio.

---

3. Entregables auditados

3.1. "SPEC.md"

La especificación establece el contexto de GanadApp, su propósito, los requisitos funcionales, los objetivos que quedan fuera del alcance y las restricciones generales del proyecto.

La IA fue utilizada como apoyo para:

- estructurar la especificación;
- transformar información del dominio en requisitos funcionales;
- organizar los requisitos mediante identificadores "RF-*";
- identificar y redactar los "Non-Goals";
- revisar la coherencia entre alcance, funcionalidades y decisiones técnicas;
- mejorar la redacción para que el documento pudiera funcionar como fuente de referencia para las etapas posteriores.

La revisión humana fue necesaria porque una propuesta generada por IA puede presentar funcionalidades plausibles que no necesariamente forman parte del alcance académico definido para el proyecto.

Por este motivo, los requisitos no fueron aceptados únicamente por haber sido propuestos por la IA. Se contrastaron con las decisiones previamente tomadas sobre GanadApp y con las consignas del trabajo práctico.

Resultado: el documento final contiene una especificación explícita del propósito, requisitos funcionales y límites del sistema.

Evidencia: "SPEC.md".

---

3.2. "docs/adr/ADR-001-stack-tecnologico.md"

El ADR documenta la decisión arquitectónica y tecnológica adoptada para el proyecto.

La IA fue utilizada para:

- proponer una estructura formal para el ADR;
- organizar el contexto y el problema arquitectónico;
- redactar la decisión;
- identificar alternativas;
- proponer criterios de comparación;
- estructurar consecuencias y riesgos;
- revisar la trazabilidad con otros documentos arquitectónicos.

En este documento se identificó uno de los principales puntos de revisión del trabajo asistido por IA: una primera versión necesitó ser mejorada para que la comparación de alternativas tuviera criterios objetivos y una justificación más verificable.

La corrección quedó reflejada posteriormente en el historial del repositorio mediante modificaciones específicamente orientadas a incorporar criterios ponderados y trazabilidad.

Esto constituye un ejemplo concreto del riesgo de aceptar directamente una respuesta generada por IA: una respuesta puede ser formalmente correcta y estar bien redactada, pero no necesariamente satisfacer con suficiente precisión los criterios de evaluación del trabajo.

La revisión humana permitió detectar esa insuficiencia y solicitar una reformulación del documento.

Evidencia de la evolución:

- "32d8e40" — versión inicial de la especificación, ADR y arnés de IA.
- "2db06b1" — mejora del ADR con criterios ponderados y trazabilidad.
- "b3fa800" — continuación de la mejora del ADR.
- Estado final de "docs/adr/ADR-001-stack-tecnologico.md".

Resultado: el ADR final presenta una decisión explícita, alternativas descartadas, criterios de selección ponderados, trazabilidad arquitectónica y consecuencias/riesgos.

---

3.3. ".opencoderules"

".opencoderules" constituye el mecanismo de gobierno utilizado para limitar el comportamiento del agente de IA durante las tareas de implementación posteriores.

La IA fue utilizada como apoyo para estructurar estas reglas a partir de las necesidades del proyecto.

El documento establece, entre otros aspectos:

- alcance permitido para el agente;
- archivos y directorios que puede modificar;
- documentación que puede consultar como contexto;
- estándares técnicos obligatorios;
- separación de responsabilidades;
- convenciones de nombres;
- prácticas prohibidas;
- restricciones frente a cambios arquitectónicos;
- prohibición de modificar documentación o decisiones arquitectónicas durante una tarea de implementación sin autorización.

Este documento es especialmente relevante para la auditoría porque representa la transición desde un uso abierto de IA hacia un uso gobernado mediante especificaciones y restricciones explícitas.

Resultado: el archivo dejó de funcionar como una instrucción genérica para una IA y pasó a constituir un conjunto de reglas específicas para el proyecto GanadApp.

Evidencia: ".opencoderules".

---

4. Hallazgos de la auditoría sobre el uso de IA

Hallazgo IA-01 — La primera propuesta no fue considerada una fuente de verdad

Durante el trabajo se comprobó que una respuesta generada por IA podía presentar una estructura aparentemente completa sin cumplir necesariamente todos los criterios específicos solicitados para el entregable.

El caso más claro se produjo en el ADR-001. La versión inicial fue posteriormente mejorada incorporando criterios ponderados y trazabilidad.

Esto demuestra que la IA fue utilizada como generador de propuestas y no como autoridad para determinar automáticamente la arquitectura del proyecto.

Riesgo identificado: aceptar una respuesta de IA por su apariencia formal sin verificarla contra la consigna y las decisiones del proyecto.

Medida correctiva: revisión humana de cada documento y sucesivas iteraciones hasta obtener una versión que cumpliera los criterios requeridos.

Estado: corregido.

---

Hallazgo IA-02 — Necesidad de controlar el alcance generado por la IA

La IA puede completar especificaciones con funcionalidades que resultan técnicamente razonables pero que no necesariamente pertenecen al alcance definido.

Este riesgo fue relevante durante la construcción de "SPEC.md", ya que la especificación debía representar exclusivamente el alcance acordado para GanadApp.

La utilización de "Non-Goals" permitió establecer explícitamente qué funcionalidades no forman parte del sistema y reducir la posibilidad de que una propuesta posterior de IA incorporara funcionalidades fuera del alcance.

Riesgo identificado: expansión automática del alcance por incorporación de funcionalidades sugeridas por la IA.

Medida correctiva: definición explícita de requisitos y "Non-Goals", junto con revisión humana de las propuestas.

Estado: controlado mediante la especificación.

---

Hallazgo IA-03 — Riesgo de inconsistencias entre documentos

La generación asistida por IA también presenta el riesgo de producir documentos individualmente correctos pero que, al compararse entre sí, contengan diferencias de criterio o decisiones que no estén suficientemente alineadas.

En un proyecto basado en SDD, "SPEC.md", el ADR y las reglas del agente no pueden analizarse como documentos independientes. Las decisiones establecidas en uno de ellos deben ser compatibles con los demás.

Por este motivo, la revisión no se limitó a corregir la redacción de cada archivo, sino que también se utilizó la comparación entre documentos como mecanismo de control.

Riesgo identificado: pérdida de coherencia global al generar documentos de manera independiente.

Medida correctiva: revisión cruzada entre especificación, decisión arquitectónica y reglas del agente.

Estado: controlado mediante revisión documental.

---

Hallazgo IA-04 — La IA requiere instrucciones específicas para producir resultados adecuados

Durante el desarrollo se comprobó que las respuestas de IA mejoraban cuando las instrucciones incluían:

- contexto concreto del proyecto;
- estructura real del repositorio;
- decisiones previamente adoptadas;
- restricciones explícitas;
- archivos que podían modificarse;
- archivos que no debían modificarse;
- formato esperado del resultado.

Este comportamiento justificó la creación de ".opencoderules".

La experiencia permitió comprobar que una instrucción genérica deja demasiado espacio para interpretaciones, mientras que un conjunto de reglas específicas reduce el margen de modificación no deseada.

Riesgo identificado: respuestas técnicamente plausibles pero incompatibles con las decisiones del proyecto.

Medida correctiva: creación de un arnés de IA con reglas explícitas y restricciones de alcance.

Estado: controlado.

---

5. Principales riesgos del uso de IA identificados

A partir de la experiencia del Sprint 1 se identificaron los siguientes riesgos:

5.1. Aceptación acrítica

Una respuesta puede presentar una redacción profesional y, aun así, no cumplir exactamente con una consigna.

Control: revisión contra requisitos verificables.

5.2. Alucinación o incorporación de información no definida

La IA puede completar espacios con información plausible que no haya sido establecida por el proyecto.

Control: utilizar la documentación del proyecto como fuente de contexto y validar cada decisión.

5.3. Expansión del alcance

La IA puede sugerir funcionalidades técnicamente razonables que no corresponden al alcance académico.

Control: "SPEC.md" y sus "Non-Goals".

5.4. Inconsistencia entre documentos

La IA puede generar documentos individualmente coherentes pero incompatibles entre sí.

Control: revisión cruzada entre SPEC, ADR y reglas del agente.

                 
6. Evaluación del arnés de IA

La creación de ".opencoderules" constituye una de las principales medidas de control obtenidas durante este Sprint.

Las reglas establecen explícitamente:

- qué documentación puede utilizarse como contexto;
- qué directorios puede modificar el agente;
- qué tipos de archivos puede trabajar;
- qué prácticas están prohibidas;
- qué decisiones arquitectónicas no puede modificar;
- qué separación de responsabilidades debe respetar;
- que no debe realizar cambios fuera del alcance autorizado.

Desde el punto de vista de la auditoría, esto representa un cambio importante respecto de un modelo de utilización de IA sin restricciones.

El agente deja de recibir únicamente instrucciones conversacionales y pasa a operar dentro de un marco documental previamente definido.

---

7. Conclusión

El uso de Inteligencia Artificial durante el Sprint 1 fue asistido y supervisado, no autónomo.

La IA aportó valor principalmente en tareas de estructuración, redacción, análisis, generación de alternativas y revisión documental. Sin embargo, el proceso demostró que sus primeras respuestas no deben considerarse automáticamente correctas.

El caso del ADR-001 resulta especialmente representativo: la versión inicial fue posteriormente revisada para incorporar criterios ponderados y mayor trazabilidad. Esto demuestra la necesidad de un ciclo de revisión humana incluso cuando la salida generada por IA presenta una estructura formalmente adecuada.

La experiencia también permitió identificar riesgos concretos asociados al uso de IA: aceptación acrítica, incorporación de información no definida, expansión del alcance e inconsistencias entre documentos.

Como respuesta a estos riesgos se establecieron mecanismos de control mediante "SPEC.md", "Non-Goals", el ADR y especialmente ".opencoderules".

La conclusión de esta auditoría es que la IA funcionó como una herramienta de asistencia dentro de un proceso de ingeniería de software dirigido por el autor. Las decisiones finales sobre alcance, arquitectura, restricciones y aceptación de los documentos permanecieron bajo control humano.

El resultado más importante del Sprint 1 no fue únicamente la generación de tres archivos, sino la definición de un modo de trabajo en el que las propuestas de IA deben ser contextualizadas, verificadas, corregidas y trazables antes de convertirse en artefactos oficiales del proyecto.

Rol de la IA: herramienta de apoyo para análisis, redacción, estructuración y revisión.

Principio adoptado:

«La IA propone; el desarrollador verifica, decide y responde por el resultado.»

Alcance cerrado: esta auditoría corresponde exclusivamente al uso de IA durante la elaboración de "SPEC.md", "ADR-001-stack-tecnologico.md" y ".opencoderules".
