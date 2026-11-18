# Sistema de Skills para LLM: Guía de Arquitectura, Ciclo de Vida y Gobernanza de Riesgos

**Versión del documento:** 1.0  
**Clasificación:** Documentación técnica de referencia interna  
**Audiencia:** Desarrolladores, arquitectos de software, responsables de seguridad, equipos de gobernanza y cumplimiento  
**Estado:** Aprobado para uso como marco de referencia organizativo


## Índice

**Bloque I: Fundamentos y Contexto**
1. [Propósito, Alcance y Audiencia](#1-propósito-alcance-y-audiencia)
2. [Arquitectura del Sistema de Skills](#2-arquitectura-del-sistema-de-skills)
3. [Ciclo de Vida de una Skill](#3-ciclo-de-vida-de-una-skill)

**Bloque II: Guías Prácticas de Uso**
4. [Guía de Inicio Rápido y Creación de Skills](#4-guía-de-inicio-rápido-y-creación-de-skills)
5. [Guía de Evaluación y Validación de Skills](#5-guía-de-evaluación-y-validación-de-skills)

**Bloque III: Límites, Riesgos y Gobernanza**
6. [¿Qué Ocurre Sin Límites? Escenarios de Ausencia de Restricciones](#6-qué-ocurre-sin-límites-escenarios-de-ausencia-de-restricciones)
7. [Riesgos de Seguridad y Cadena de Suministro](#7-riesgos-de-seguridad-y-cadena-de-suministro)
8. [Auditoría, Trazabilidad y Rendición de Cuentas](#8-auditoría-trazabilidad-y-rendición-de-cuentas)
9. [Marco de Gobernanza y Confianza por Niveles](#9-marco-de-gobernanza-y-confianza-por-niveles)
10. [Consideraciones Éticas y de Responsabilidad](#10-consideraciones-éticas-y-de-responsabilidad)
11. [Cumplimiento Normativo y Estándares](#11-cumplimiento-normativo-y-estándares)

**Bloque IV: Referencia Técnica**
12. [Referencia de la Especificación `SKILL.md`](#12-referencia-de-la-especificación-skillmd)
13. [Referencia de Herramientas y Permisos](#13-referencia-de-herramientas-y-permisos)

**Bloque V: Preguntas Abiertas y Agenda de Investigación**
14. [Desafíos Abiertos en el Ecosistema de Skills](#14-desafíos-abiertos-en-el-ecosistema-de-skills)
15. [Preguntas Guía para la Reflexión Futura](#15-preguntas-guía-para-la-reflexión-futura)

**Bloque VI: Apéndices y Soporte**
16. [Glosario y Referencias](#16-glosario-y-referencias)
17. [Registro de Cambios de la Documentación](#17-registro-de-cambios-de-la-documentación)

**Conclusiones y Recomendaciones**


## Bloque I: Fundamentos y Contexto

### 1. Propósito, Alcance y Audiencia

#### 1.1 Propósito

Este documento establece el marco técnico y de gobernanza para el diseño, despliegue y operación de **skills** en sistemas basados en Grandes Modelos de Lenguaje (LLM). Su finalidad es doble: por un lado, servir como guía práctica para equipos de ingeniería que construyen y mantienen skills; por otro, actuar como referencia normativa interna para la gestión de riesgos, la auditoría y la toma de decisiones por parte de comités de seguridad y cumplimiento.

La premisa central es que **la gobernanza y los límites no son un añadido posterior al diseño de una skill, sino una dimensión constitutiva de su arquitectura**. Un ecosistema de skills sin controles de cantidad, permisos y revisión no es un ecosistema más libre: es un ecosistema estructuralmente inseguro, degradado y opaco, como evidencian los datos empíricos disponibles.

#### 1.2 Alcance

El documento cubre el ciclo de vida completo de una skill: autoría, revisión, publicación, despliegue, monitorización y retirada. Aborda tanto las skills de instrucciones puras (Markdown) como las skills que incorporan código ejecutable (`scripts/`), y analiza su relación con el Model Context Protocol (MCP). Se extiende a los riesgos de seguridad, los marcos normativos aplicables y los desafíos abiertos del ecosistema.

**Queda fuera del alcance:** la implementación concreta de infraestructura de ejecución (sandboxes, contenedores), los detalles de facturación de proveedores de LLM, y la formación pedagógica de desarrolladores en lenguajes específicos. Tampoco se prescribe un proveedor de LLM ni un mercado de skills concreto; el marco es deliberadamente agnóstico en ese sentido.

#### 1.3 Audiencia

| Rol | Uso principal del documento |
|---|---|
| **Desarrolladores de skills** | Especificación del formato `SKILL.md`, patrones de diseño seguro, listas de verificación previas al despliegue |
| **Arquitectos de software** | Modelo de capas, integración con MCP, diseño de sistemas de descubrimiento y ejecución |
| **Responsables de seguridad (CISO, AppSec)** | Taxonomía de riesgos, controles de cadena de suministro, procedimientos de auditoría |
| **Equipos de gobernanza y cumplimiento** | Mapeo a EU AI Act, ISO/IEC 42001 y NIST AI RMF; evidencia documental para certificaciones |
| **Comités de seguridad de IA** | Criterios para la aprobación de skills, modelos de confianza por niveles, gestión de incidentes |

#### 1.4 Definición operativa de “skill”

En el contexto de este documento, una **skill** es una carpeta autocontenida que incluye, como mínimo, un archivo `SKILL.md` en su raíz. Ese archivo contiene metadatos en formato YAML (frontmatter) e instrucciones procedurales en Markdown. Opcionalmente, la carpeta puede incluir subdirectorios como `scripts/` (código ejecutable), `references/` (documentación de apoyo) y `assets/` (plantillas y recursos). El agente descubre la skill mediante una descripción compacta, carga las instrucciones completas cuando la tarea coincide con esa descripción, y ejecuta los recursos asociados solo cuando las instrucciones lo requieren.

Este diseño se conoce como **divulgación progresiva** (*progressive disclosure*): el agente no consume el costo completo en tokens de cada skill en cada turno, sino que paga un “peaje” mínimo de metadatos (del orden de 100 tokens por skill) y solo profundiza cuando es necesario. La especificación abierta, publicada en agentskills.io, define un formato portable que múltiples plataformas (Claude, Codex, ChatGPT, entre otras) han adoptado.

#### 1.5 Relación entre skills y MCP

Skills y MCP no son tecnologías competidoras; operan en capas diferentes. **MCP (Model Context Protocol) conecta al modelo con herramientas y fuentes de datos externas**, exponiendo funciones invocables y recursos. **Una skill enseña al agente *cómo* utilizar esas herramientas para completar un flujo de trabajo reconocible.** En palabras de Anthropic, “MCP conecta a Claude con herramientas de terceros, y las skills le enseñan a Claude cómo usarlas bien”. Un servidor MCP proporciona información en vivo y acciones controladas; una skill proporciona la secuencia procedural, las condiciones de activación y el contexto organizativo para combinar esas acciones de manera efectiva.

OWASP resume la distinción con una fórmula concisa: **MCP = cómo el modelo habla con las herramientas; AST10 (el marco de riesgos de skills) = qué hacen realmente esas herramientas**. Por tanto, la seguridad de una skill no se agota en la seguridad del servidor MCP que invoca: la skill puede orquestar múltiples herramientas, persistir instrucciones en memoria y alterar el comportamiento del agente de formas que un servidor MCP aislado no controla.

### 2. Arquitectura del Sistema de Skills

#### 2.1 Modelo de capas y divulgación progresiva

La arquitectura de skills se organiza en **tres niveles de carga**, diseñados para minimizar el consumo de contexto y maximizar la escalabilidad del ecosistema:

**Nivel 1 — Metadatos (aproximadamente 100 tokens por skill).** Al inicio de cada ejecución, el agente recibe únicamente el `name` y la `description` de cada skill disponible. Este índice compacto permite al modelo decidir, en una fase de descubrimiento, qué skill es potencialmente relevante para la tarea solicitada. La `description` funciona, por tanto, como un **contrato de activación**: no es una etiqueta decorativa, sino el texto contra el que el agente compara la intención del usuario.

**Nivel 2 — Instrucciones completas (`SKILL.md` body).** Cuando el agente determina que una skill es relevante, carga el cuerpo completo del archivo Markdown. La especificación recomienda que este cuerpo no supere los 5,000 tokens, aunque el límite no es una restricción técnica dura, sino una guía de diseño. Un cuerpo excesivamente largo compite por el presupuesto de contexto y puede desplazar información crítica de la tarea.

**Nivel 3 — Recursos empaquetados (`scripts/`, `references/`, `assets/`).** Los archivos auxiliares se cargan o ejecutan solo cuando las instrucciones del Nivel 2 lo indican explícitamente. Un script se ejecuta a través del shell del agente; su salida entra en la ventana de contexto, pero **el modelo no lee el código que ejecuta** —esa es una responsabilidad del revisor humano. Este detalle arquitectónico es crucial: la seguridad de una skill no puede depender de que el modelo “inspeccione” el código en tiempo de ejecución, porque no lo hace.

**Diagrama conceptual (descripción textual):**

```
┌─────────────────────────────────────────────────────────────┐
│  AGENTE (ventana de contexto)                                │
│                                                              │
│  [Índice de metadatos]                                       │
│   skill-A: description (~100 tokens)                         │
│   skill-B: description (~100 tokens)                         │
│   skill-C: description (~100 tokens)                         │
│            │                                                 │
│            ▼  (la tarea coincide con skill-B)                │
│  [SKILL.md body cargado]                                     │
│   Instrucciones procedurales (< 5,000 tokens recomendados)   │
│            │                                                 │
│            ▼  (las instrucciones apuntan a un script)        │
│  [scripts/run.py ejecutado en el shell]                      │
│   → salida devuelta al contexto                              │
│   (el código no se carga en el contexto)                     │
└─────────────────────────────────────────────────────────────┘
```

#### 2.2 Estructura de directorios

La especificación abierta define una estructura mínima y flexible:

```
skill-name/
├── SKILL.md          # Obligatorio: frontmatter YAML + instrucciones Markdown
├── scripts/          # Opcional: código ejecutable (Python, shell, etc.)
├── references/       # Opcional: documentación de apoyo, esquemas, guías
├── assets/           # Opcional: plantillas, recursos, ficheros de datos
└── ...               # Cualquier otro archivo o subdirectorio
```

Solo `SKILL.md` es obligatorio. Los tres subdirectorios son convenciones, no reglas de la especificación, y el formato permite explícitamente cualquier otro archivo. Esta libertad de diseño es conveniente para la expresividad, pero **constituye un vector de riesgo para la revisión**: una skill puede contener un binario, una imagen, un paquete de Python o un script de shell sin extensión, y el formato no marca ninguno de estos elementos como sospechoso por sí mismo.

#### 2.3 Cómo el agente descubre, carga y ejecuta una skill

El flujo operativo es el siguiente:

1. **Descubrimiento:** El agente recibe el índice de metadatos de todas las skills instaladas o disponibles en el entorno. En entornos con miles de skills, este índice se gestiona mediante un router o un mecanismo de selección que puede ser el propio LLM o un componente separado.
2. **Coincidencia semántica:** Cuando el usuario plantea una tarea, el agente compara la intención de la solicitud con las `description` del índice. Si ninguna descripción coincide, la skill no se activa.
3. **Carga del cuerpo:** Si hay coincidencia, el agente carga el `SKILL.md` completo y sigue las instrucciones procedurales.
4. **Ejecución de recursos:** Si las instrucciones indican ejecutar un script o leer un archivo de referencia, el agente realiza esa acción a través de las herramientas habilitadas (shell, lectura de archivos, etc.).
5. **Persistencia potencial:** Algunas skills pueden escribir en archivos de memoria del agente (`MEMORY.md`, `SOUL.md`), lo que introduce riesgos de persistencia más allá de la sesión inmediata.

#### 2.4 Consecuencias arquitectónicas y trade-offs

El modelo de divulgación progresiva resuelve el problema de escalabilidad del contexto, pero crea una **asimetría de información** estructural: el agente y el usuario ven la `description` y el cuerpo del `SKILL.md`, pero el código de los scripts se ejecuta con los permisos del agente sin ser leído por el modelo. El revisor humano es el único punto de control capaz de inspeccionar ese código antes de la ejecución. Si la revisión es superficial o inexistente, la divulgación progresiva se convierte en una **opacidad progresiva**.

Además, la flexibilidad del formato —que permite cualquier archivo adicional— significa que el perímetro de ataque de una skill no está definido por su estructura declarada, sino por el contenido real de todos sus archivos. Un revisor que solo lee el `SKILL.md` y no examina `scripts/` y `references/` está auditando una fracción del artefacto.

### 3. Ciclo de Vida de una Skill

El ciclo de vida que se propone a continuación está diseñado para que cada transición entre fases tenga un **criterio de salida verificable** y un **rol responsable identificable**. La ausencia de cualquiera de estas fases es, en sí misma, un indicador de riesgo.

#### 3.1 Fases del ciclo de vida

| Fase | Objetivo | Criterio de salida | Rol responsable |
|---|---|---|---|
| **Autoría** | Producir una skill con propósito claro, descripción precisa y permisos mínimos | `SKILL.md` válido según especificación; `description` revisada como contrato de activación; inventario de scripts y dependencias | Desarrollador de la skill |
| **Revisión** | Verificar seguridad, corrección y adecuación al propósito declarado | Lista de verificación de riesgo completada; análisis estático y manual de scripts; prueba en sandbox superada | Revisor de seguridad / segundo ingeniero |
| **Publicación** | Registrar la skill con procedencia, versión y hash de contenido | Entrada en el catálogo interno con metadatos de autoría, fecha, versión y nivel de confianza | Responsable del catálogo / plataforma |
| **Despliegue** | Habilitar la skill en el entorno de producción con los permisos aprobados | Configuración de `allowed-tools` y permisos de sistema coherente con la revisión; registro de auditoría activo | Arquitecto de plataforma / SRE |
| **Monitorización** | Detectar deriva, incidentes y degradación del comportamiento | Métricas de uso, alertas de permisos anómalos, revisión periódica de actualizaciones | Equipo de operaciones / seguridad |
| **Retirada** | Desactivar la skill sin dejar dependencias huérfanas ni riesgos residuales | Revocación de permisos, eliminación de artefactos de memoria persistente, comunicación a dependientes | Responsable del catálogo / seguridad |

#### 3.2 Roles y responsabilidades en detalle

**Desarrollador de la skill.** No solo escribe el código; declara el **propósito** de la skill y justifica cada permiso solicitado. La `description` debe reflejar fielmente lo que la skill hace y cuándo debe activarse, sin ambigüedades que puedan llevar a activaciones no deseadas.

**Revisor de seguridad.** Su función no es reescribir la skill, sino **verificar que el comportamiento del código coincide con el propósito declarado** y que no existen patrones de riesgo no justificados. Debe inspeccionar todos los archivos, no solo el `SKILL.md`.

**Comité de gobernanza (cuando aplique).** Para skills de alto impacto (acceso a datos sensibles, capacidad de escritura en sistemas, invocación de herramientas de red), la aprobación puede requerir una instancia colegiada. La composición y funciones de este comité se detallan en la Sección 9.

**Operaciones y monitorización.** La publicación no es el final del ciclo. Las skills que dependen de APIs externas pueden degradarse, las actualizaciones pueden introducir cambios no revisados, y el comportamiento del agente puede derivar con el uso prolongado. La monitorización debe incluir la **frescura** de la skill (¿sigue siendo válida la API que invoca?) y la **deriva de comportamiento** (¿sigue ejecutándose dentro del propósito declarado?).


## Bloque II: Guías Prácticas de Uso

### 4. Guía de Inicio Rápido y Creación de Skills

#### 4.1 Anatomía de una skill mínima funcional

Una skill mínima requiere únicamente un archivo `SKILL.md` con dos campos obligatorios en el frontmatter: `name` y `description`. El `name` debe cumplir restricciones estrictas: entre 1 y 64 caracteres, letras minúsculas, dígitos y guiones, sin guiones al inicio o al final, sin guiones consecutivos, y debe coincidir con el nombre del directorio padre. La `description` tiene entre 1 y 1,024 caracteres y es el texto contra el que el agente compara la tarea del usuario.

**Ejemplo de `SKILL.md` mínimo válido:**

```yaml
---
name: release-notes
description: >
  Drafts release notes from merged pull requests in the house format.
  Use when the user asks for release notes, a changelog entry, or a
  summary of what shipped.
---

# Release Notes

1. List merged pull requests since the last tag.
2. Group them under Added, Changed, Fixed, and Security.
3. Write one plain sentence per change. Link the pull request.
```

Este ejemplo, adaptado de la especificación, muestra una `description` que responde a dos preguntas: **qué hace** (“Drafts release notes...”) y **cuándo debe usarse** (“Use when the user asks...”). La segunda parte es tan importante como la primera: sin ella, el agente no tiene un criterio claro para activar la skill frente a alternativas.

#### 4.2 La `description` como contrato de activación

La `description` no es documentación para humanos; es el **único texto que el agente utiliza en la fase de descubrimiento** para decidir si carga la skill. Una descripción mal formulada produce uno de dos fallos: **infraactivación** (la skill nunca se selecciona porque la descripción no coincide con las formulaciones reales de los usuarios) o **sobreactivación** (la skill se selecciona para tareas para las que no fue diseñada, con consecuencias potencialmente graves si la skill tiene permisos elevados).

| Tipo de descripción | Ejemplo | Problema |
|---|---|---|
| **Demasiado vaga** | “Ayuda con documentos.” | No especifica qué tipo de documentos, qué operaciones ni cuándo usarla. El agente no puede distinguirla de otras skills genéricas. |
| **Demasiado amplia** | “Procesa cualquier archivo, ejecuta scripts y gestiona APIs externas.” | Atrae activaciones para tareas heterogéneas; combinada con permisos amplios, crea un riesgo de “permisos de Dios”. |
| **Bien formulada** | “Extrae tablas de PDFs escaneados y las exporta a CSV. Úsala cuando el usuario proporcione un PDF con tablas y solicite datos estructurados.” | Delimita el dominio de entrada, la operación y la condición de activación. |
| **Bien formulada (con límites)** | “Consulta la API de facturación para obtener el estado de una suscripción. No modifica datos. Úsala solo en consultas de solo lectura sobre suscripciones.” | Explicita lo que la skill *no* hace, reduciendo el riesgo de activación en contextos de escritura. |

**Regla de diseño:** la `description` debe ser **suficientemente específica para excluir** los casos en los que la skill no debe usarse, y **suficientemente clara para incluir** los casos en los que sí debe usarse. Una prueba útil es formular tres tareas que *no* deberían activar la skill y verificar que la descripción no las cubre.

#### 4.3 Pasos para crear una skill mínima

1. **Definir el propósito y los límites.** Escribir en una frase qué problema resuelve la skill y qué *no* hace.
2. **Redactar la `description`** con la estructura “qué hace + cuándo usarla + qué no hace”.
3. **Crear el directorio** con el nombre en minúsculas y guiones, coincidente con el campo `name`.
4. **Escribir el `SKILL.md`** con frontmatter YAML y un cuerpo Markdown que contenga instrucciones numeradas y verificables.
5. **Declarar `allowed-tools`** si la skill requiere herramientas específicas; si no se declara, la skill hereda el conjunto de herramientas del agente, lo que puede ser excesivo.
6. **Añadir scripts solo si son necesarios**, y documentar en el cuerpo cuándo deben ejecutarse y qué salida se espera.
7. **Probar en sandbox** con tareas que deberían activar la skill y tareas que no deberían hacerlo.

### 5. Guía de Evaluación y Validación de Skills

#### 5.1 Protocolo verificable antes del despliegue

La validación de una skill no puede limitarse a comprobar que el archivo se carga sin errores. Debe verificar que **el comportamiento del artefacto coincide con el propósito declarado** y que los riesgos están identificados y mitigados. El protocolo propuesto consta de cinco etapas:

**Etapa 1 — Validación estructural.** Verificar que el frontmatter es YAML válido, que `name` y `description` cumplen las restricciones de la especificación, que el `name` coincide con el directorio, y que no hay caracteres invisibles o de dirección en el nombre de la carpeta. Herramientas como `skills-ref` pueden automatizar parte de esta validación, aunque su propio README advierte que es una implementación de referencia, no de producción.

**Etapa 2 — Análisis de contenido.** Inspeccionar **todos** los archivos de la skill, no solo el `SKILL.md`. Identificar scripts ejecutables, dependencias externas, URLs de red, referencias a credenciales y cualquier operación de lectura o escritura sobre el sistema de archivos.

**Etapa 3 — Prueba en sandbox.** Ejecutar la skill en un entorno aislado con permisos restringidos, utilizando un conjunto de tareas de prueba que cubra: (a) activaciones correctas, (b) no activaciones correctas, (c) activaciones límite o ambiguas, y (d) intentos de manipulación que deberían ser rechazados. La salida del script debe compararse con la salida esperada según el propósito declarado.

**Etapa 4 — Evaluación de riesgo basada en indicadores.** Aplicar la lista de verificación de la Sección 5.2. Cualquier indicador marcado como “alto” requiere justificación explícita y, en su caso, aprobación del comité de gobernanza.

**Etapa 5 — Registro de la decisión.** Documentar qué se revisó, qué se encontró, qué se aceptó como riesgo residual y con qué condiciones. Este registro es la evidencia de diligencia debida que los marcos normativos exigirán más adelante (Sección 11).

#### 5.2 Lista de verificación de riesgo

La siguiente lista se basa en los indicadores empíricos identificados en estudios a gran escala sobre skills reales. El 26.1% de las skills analizadas en una muestra de 31,132 presentaba al menos una vulnerabilidad, con 13.3% de patrones de exfiltración de datos y 11.8% de escalada de privilegios. Las skills que incluyen scripts ejecutables tienen **2.12 veces más probabilidades** de contener vulnerabilidades que las skills de solo instrucciones (OR = 2.12).

**Indicadores estructurales y de contenido:**

- [ ] **¿La skill incluye scripts ejecutables?** Si sí, el nivel de escrutinio debe aumentar proporcionalmente. Un script ejecutado por el agente corre con los permisos del agente y su código no es leído por el modelo.
- [ ] **¿El `SKILL.md` contiene instrucciones que manipulan las directivas del agente o intentan anular salvaguardas?** Patrones de inyección de prompts en el manifiesto pueden secuestrar las directivas centrales del agente.
- [ ] **¿La skill hace referencia a servidores MCP o herramientas externas?** Cada servidor MCP invocado amplía la superficie de ataque; verificar que la referencia es necesaria y que el servidor está en el inventario aprobado.
- [ ] **¿Hay URLs, direcciones IP o dominios en el código o en las instrucciones?** La exfiltración de datos requiere un canal de salida; una URL no justificada es una señal de alerta.
- [ ] **¿Se incrustan credenciales, tokens o claves de API en el código o en archivos de referencia?** Las credenciales incrustadas son un riesgo de filtración y un indicador de malas prácticas.
- [ ] **¿La skill escribe en archivos de memoria del agente (`MEMORY.md`, `SOUL.md`) o en archivos de configuración persistentes?** La persistencia permite que una skill maliciosa sobreviva a su desinstalación y afecte sesiones futuras.
- [ ] **¿La skill lee o escribe fuera de su propio directorio?** El alcance del sistema de archivos debe estar delimitado y justificado.
- [ ] **¿La skill requiere permisos de red, de ejecución de shell o de escalada de privilegios?** Estos permisos deben estar declarados en `allowed-tools` y aprobados explícitamente.

**Indicadores de comportamiento (prueba en sandbox):**

- [ ] **¿La salida del script coincide con lo que la `description` promete?** Una discrepancia entre el propósito declarado y el comportamiento observado es un fallo crítico, independientemente de si el comportamiento es malicioso o simplemente erróneo.
- [ ] **¿La skill intenta acceder a recursos no mencionados en sus instrucciones?** Por ejemplo, leer variables de entorno, listar directorios del usuario o conectarse a servicios no declarados.
- [ ] **¿La skill modifica su propio código o el de otras skills durante la ejecución?** La automodificación es un vector de persistencia y de evasión de revisiones.
- [ ] **¿La skill funciona de manera diferente en la primera ejecución que en ejecuciones posteriores?** El comportamiento dependiente del estado puede indicar memoria oculta o “shadow features” —funcionalidades ocultas al usuario—; un estudio encontró que el 73.2% de las skills maliciosas implementaba shadow features.

**Criterio de decisión:** si algún indicador de la categoría “estructural y de contenido” está marcado y no existe una justificación documentada y aprobada, la skill **no debe desplegarse**. Si un indicador de comportamiento falla en sandbox, la skill debe devolverse al autor con hallazgos concretos.


## Bloque III: Límites, Riesgos y Gobernanza

### 6. ¿Qué Ocurre Sin Límites? Escenarios de Ausencia de Restricciones

Este apartado analiza las tres dimensiones de “sin límite” que definen los fallos estructurales del ecosistema de skills. No son escenarios hipotéticos: son patrones observados en datos empíricos de mercados públicos y estudios de seguridad a gran escala.

#### 6.1 Sin límite de cantidad: la explosión del ecosistema y el impuesto de descubrimiento

El crecimiento del número de skills ha sido explosivo. Un análisis cuantitativo de 40,285 skills publicadas en un mercado público documentó un crecimiento de **2,179 a 40,285 skills en 20 días**, lo que representa un factor de **18.5×** y una tasa media de crecimiento del **15.7% diario**. Un solo día (25 de enero de 2026) contribuyó con 8,857 skills, el 23.2% del corpus total, y la semana centrada en esa fecha concentró el 47.8% de todas las publicaciones. Este patrón de crecimiento en ráfagas, sincronizado con picos de atención pública (medidos, por ejemplo, por el historial de estrellas de GitHub de aplicaciones de skills), indica que el volumen no refleja necesariamente una diversificación de capacidades, sino una **reacción de la comunidad ante un estímulo de atención**.

La consecuencia más inmediata es la **redundancia masiva**. El **46.3% de las skills comparte un nombre normalizado con al menos otra publicación**, y el análisis de embeddings semánticos sugiere que la redundancia real a nivel de intención es aún mayor. La duplicación no es un fenómeno marginal: los grupos de 10 a 49 repeticiones contribuyen con el 8.8% del corpus, y algunos nombres aparecen más de 100 veces, lo que es consistente con la republicación automatizada o basada en plantillas.

Este exceso de oferta genera un **impuesto de descubrimiento**: encontrar una skill de alta calidad requiere filtrar cientos de listados duplicados o de baja calidad (“skills zombi”), lo que fragmenta las señales de retroalimentación (instalaciones, valoraciones) y hace casi imposible que las mejores implementaciones se distingan del ruido. El volumen del mercado **sobrestima sustancialmente la diversidad real de capacidades**, y el coste de esa sobrestimación lo paga cada usuario que intenta seleccionar una skill.

La dimensión de calidad agrava el problema. Las skills generadas automáticamente tienden a aportar poco valor diferencial frente a las curadas por humanos: reproducen procedimientos genéricos, carecen de contexto organizativo específico y a menudo son variaciones superficiales de un mismo patrón. El ecosistema no solo es redundante; es **homogéneo en intención** y **pobre en profundidad**.

#### 6.2 Sin límite de permisos: “permisos de Dios” y escalada silenciosa

La segunda dimensión de ausencia de límites es la concesión de permisos excesivos. En el análisis del ecosistema, un **9% de las skills** presentaba lo que la literatura denomina “permisos de Dios” (*god-mode permissions*): acceso amplio al sistema de archivos, ejecución de shell sin restricciones, capacidad de red sin delimitación o combinaciones de las tres. El 39% de las skills superaba el nivel de riesgo seguro, incluyendo un 9% clasificado como crítico.

El problema no es únicamente que existan skills con permisos amplios, sino que **la arquitectura de permisos no está alineada con el propósito declarado**. Una skill que “resume páginas web” puede solicitar permisos de escritura en el sistema de archivos o de ejecución de comandos del shell porque el formato no impone una correspondencia entre la `description` y los permisos solicitados. El usuario que instala la skill ve una descripción inocua; el agente ejecuta el código con los permisos que la skill ha solicitado (o con los permisos por defecto del entorno, que con frecuencia son amplios).

Los datos empíricos confirman la prevalencia de este desajuste: el **11.8% de las skills** presenta patrones de escalada de privilegios, y las skills con scripts ejecutables tienen **2.12 veces más probabilidades** de contener vulnerabilidades que las skills de solo instrucciones. La escalada no requiere una vulnerabilidad sofisticada: basta con que una skill incluya un script que lea variables de entorno, acceda a archivos de configuración o invoque comandos del sistema más allá de lo que su `description` sugiere.

#### 6.3 Sin límite de revisión: la campaña ClawHavoc y la infiltración a escala

La tercera dimensión es la ausencia de revisión obligatoria antes de la publicación. El caso más documentado es la **campaña ClawHavoc (enero de 2026)** , en la que **1,184 skills maliciosas** fueron infiltradas en el mercado ClawHub a través de **12 cuentas de editor**, todas compartiendo una misma IP de comando y control (`91.92.242[.]30`). Las skills maliciosas suplantaban nombres de alta demanda (“Google”, “Solana wallet tracker”, “YouTube Summarize Pro”, “Polymarket Trader”) y entregaban el *Atomic Stealer* (AMOS), un malware dirigido a billeteras de criptomonedas, claves SSH y credenciales del navegador en macOS. Cinco de las siete skills más descargadas de ClawHub en el pico de la infección eran malware confirmado.

La lección de ClawHavoc no es solo que existan actores maliciosos, sino que **la ausencia de revisión convierte el mercado en un canal de distribución de malware de bajo coste y alto impacto**. Tres líneas de Markdown en un archivo `SKILL.md` fueron suficientes para exfiltrar claves SSH. Un estudio de medición en USENIX Security 2026 analizó 98,380 skills en mercados públicos y confirmó 157 skills maliciosas que portaban 632 vulnerabilidades (promedio de 4.03 por skill); el **73.2% de las skills maliciosas implementaba shadow features** ocultas al usuario, y el **54.1% se remontaba a un único clúster de editores**. La concentración de la autoría maliciosa sugiere que una parte significativa del riesgo es **automatizable y repetible**, no el producto de actores aislados.

#### 6.4 Consecuencias sistémicas

Las tres dimensiones de ausencia de límites convergen en un conjunto de fallos sistémicos que ninguna mitigación individual puede resolver por completo:

**La seguridad como problema de cadena de suministro.** Una skill no es un artefacto aislado; es un nodo en una cadena que incluye al autor, los scripts, las dependencias (explícitas e implícitas), los servidores MCP que invoca y las actualizaciones posteriores. El ecosistema de skills reproduce los patrones de riesgo del software de código abierto, pero sin los mecanismos de gobernanza que la industria del software ha desarrollado durante décadas (firmas de paquetes, lockfiles, auditorías de dependencias). OWASP describe el ecosistema como “un problema de dependencias sin lockfile”.

**La opacidad de la divulgación progresiva.** El diseño que hace escalable al ecosistema —cargar solo lo necesario, ejecutar scripts sin que el modelo los lea— también hace que el comportamiento real de una skill sea opaco para el agente y para el usuario. La revisión humana es el único mecanismo que puede cerrar esa brecha, y es precisamente el mecanismo que la ausencia de límites elimina o degrada.

**La degradación del ecosistema por “skills zombi”.** La redundancia y la baja calidad no son solo un problema de experiencia de usuario; **expulsan a las skills de calidad del mercado**. Cuando el coste de descubrimiento es alto y las señales de calidad están fragmentadas, los autores de skills bien curadas tienen menos incentivos para publicar y mantener sus artefactos. El resultado es un equilibrio de bajo esfuerzo: muchas skills genéricas, pocas skills profundas, y una confianza erosionada en todo el ecosistema.

**El valor diferencial de la curaduría humana.** Las skills generadas automáticamente aportan poco valor frente a las curadas por humanos porque carecen de lo que hace útil a una skill: **conocimiento procedural específico del contexto**, decisiones de diseño justificadas, y límites explícitos. Un procedimiento genérico que el modelo ya podría inferir sin la skill no justifica el coste de contexto, el riesgo de seguridad ni la deuda de mantenimiento. La curaduría humana no es un lujo; es la fuente del valor diferencial de una skill frente a la capacidad base del modelo.

### 7. Riesgos de Seguridad y Cadena de Suministro

#### 7.1 La skill como código ejecutable: el modelo de amenaza

El modelo de amenaza de una skill debe partir de una premisa incómoda: **una skill es código ejecutable con los permisos del agente**, no un documento pasivo. Los scripts incluidos en `scripts/` se ejecutan en el shell del agente, y su salida entra en el contexto; el modelo no inspecciona el código, solo consume el resultado. Esto significa que la superficie de ataque de una skill incluye tanto su contenido declarativo (instrucciones que pueden contener inyección de prompts) como su contenido ejecutable (scripts que pueden realizar operaciones arbitrarias).

OWASP ha sistematizado los riesgos en el **Agentic Skills Top 10 (AST10)** , que documenta las diez clases de riesgo más críticas en skills para agentes de IA. La Tabla 7.1 presenta una síntesis de las clases principales y su relevancia para este documento.

**Tabla 7.1 — Clases de riesgo del OWASP AST10 (síntesis)**

| ID | Clase de riesgo | Descripción operativa |
|---|---|---|
| **AST01** | Skills maliciosas | Skills publicadas con intención hostil, con payload en código o en prosa |
| **AST02** | Compromiso de cadena de suministro | Dependencias, actualizaciones o editores comprometidos que introducen código malicioso en skills legítimas |
| **AST03** | Skills con permisos excesivos | Skills que solicitan o reciben más permisos de los necesarios para su propósito declarado |
| **AST04** | Metadatos inseguros | Descripciones, nombres o campos de frontmatter que facilitan suplantación, ambigüedad o activación no deseada |
| **AST05** | Instrucciones externas no confiables | Skills que incorporan contenido de fuentes no verificadas (URLs, APIs) susceptible de inyección |
| **AST06** | Aislamiento débil | Ejecución de skills en entornos sin sandbox o con aislamiento insuficiente |
| **AST07** | Deriva de actualizaciones | Cambios posteriores a la revisión que alteran el comportamiento de la skill sin un nuevo proceso de aprobación |
| **AST08** | Escaneo deficiente | Ausencia o insuficiencia de análisis estático y dinámico antes del despliegue |

#### 7.2 Vectores de ataque documentados

**Inyección indirecta de prompts.** El `SKILL.md` puede contener instrucciones que secuestran las directivas del agente, forzándolo a ignorar salvaguardas y obedecer instrucciones ocultas del atacante. La inyección no requiere código: tres líneas de Markdown fueron suficientes para exfiltrar claves SSH en el caso documentado por Snyk.

**Escalada de privilegios.** Una skill con permisos amplios puede realizar operaciones que el usuario nunca aprobó explícitamente. El 11.8% de las skills analizadas presentaba patrones de escalada de privilegios. La escalada puede ser intencionada (malware) o inadvertida (una skill que necesita escribir un archivo temporal y solicita permisos de escritura en todo el sistema).

**Exfiltración de datos.** El 13.3% de las skills presentaba patrones de exfiltración de datos. Los canales de salida incluyen URLs en scripts, llamadas a APIs externas, escritura en archivos compartidos y persistencia en memoria del agente que luego se sincroniza con servicios externos.

**Fallos en cascada y “radio de explosión” (*blast radius*).** El radio de explosión de una skill es el **alcance de recursos, datos y capacidades accesibles si la skill es comprometida**. En un agente, el radio de explosión combina los permisos del *service principal* (los scopes de API concedidos), las fuentes de conocimiento configuradas (sitios de SharePoint, bases de datos, archivos) y la configuración del blueprint (qué acciones puede ejecutar el agente). Una skill que combina acceso amplio a datos con capacidad de comunicación externa y ejecución de código tiene un radio de explosión máximo. El concepto de “tríada letal” —datos privados, contenido no confiable y comunicación externa— captura la combinación de factores que hace que una skill sea especialmente peligrosa.

**Persistencia y envenenamiento de memoria.** Las skills pueden escribir en `MEMORY.md` o `SOUL.md`, inyectando contexto malicioso que el agente recuperará y ejecutará en sesiones futuras. Esto permite que una skill maliciosa sobreviva a su desinstalación y afecte el comportamiento del agente de forma indefinida. La “degradación cognitiva” es una variante más sutil: una skill que se ejecuta repetidamente puede inundar la ventana de contexto, agotar al planificador o escribir contenido alucinado en la memoria, sin que ninguna escritura individual parezca maliciosa en una revisión puntual.

### 8. Auditoría, Trazabilidad y Rendición de Cuentas

#### 8.1 Qué debe registrarse

La trazabilidad de una skill debe permitir responder, para cualquier incidente, **qué ocurrió, cuándo, con qué artefacto y bajo qué decisión humana**. El registro mínimo incluye:

| Categoría | Elementos a registrar |
|---|---|
| **Identidad de la skill** | Nombre, versión, hash de contenido de todos los archivos, autor, fecha de publicación, nivel de confianza asignado |
| **Contexto de ejecución** | Prompt del usuario, índice de skills presentado al agente, skill seleccionada, versión cargada, herramientas habilitadas |
| **Invocaciones de herramientas** | Herramienta invocada, parámetros, resultado, duración, código de salida |
| **Decisiones de validación** | Lista de verificación completada, hallazgos, riesgos residuales aceptados, revisor responsable, aprobaciones |
| **Eventos de ciclo de vida** | Publicación, actualización, cambio de permisos, retirada, revocación |
| **Incidentes y anomalías** | Alertas de permisos, comportamiento fuera del propósito declarado, intentos de acceso denegados |

#### 8.2 Durante cuánto tiempo y cómo se investiga un incidente

La retención debe ser **proporcional al riesgo de la skill y a los requisitos regulatorios aplicables**. Para skills de alto impacto, un período mínimo de 12 meses es coherente con las obligaciones de documentación técnica y registro de eventos de sistemas de alto riesgo en el EU AI Act (Artículos 11-13 y 12). Para skills de bajo impacto, períodos más cortos pueden ser aceptables, pero nunca inferiores al ciclo de revisión de la skill.

La investigación de un incidente sigue una secuencia de atribución: **¿el fallo provino del modelo, del prompt, de la skill o de la revisión humana?** Sin trazabilidad, esta pregunta es irresoluble. Un modelo puede alucinar una llamada a una herramienta; un prompt malicioso puede inducir una acción no deseada; una skill puede ejecutar código que hace algo distinto de lo declarado; una revisión humana puede haber aprobado un artefacto sin inspeccionar un script. Cada una de estas causas requiere una mitigación diferente, y confundirlas conduce a correcciones ineficaces. **La trazabilidad es lo que convierte un incidente en aprendizaje organizativo** en lugar de en una recaída periódica.

### 9. Marco de Gobernanza y Confianza por Niveles

#### 9.1 Propuesta de modelo graduado

Se propone un modelo de **cuatro niveles de confianza** que mapea la procedencia y el nivel de verificación de una skill a las capacidades de despliegue permitidas. El principio rector es que **el nivel de confianza no se autodeclara: se gana mediante evidencia verificable y se degrada automáticamente si las condiciones cambian**.

| Nivel | Designación | Requisitos de evidencia | Capacidades permitidas | Restricciones |
|---|---|---|---|---|
| **N0** | *Sandboxed* | Sin revisión; solo artefacto bruto | Ejecución en sandbox aislado, sin acceso a red, sin credenciales, sin persistencia | Solo para pruebas locales; no desplegable en producción |
| **N1** | *Revisado por la comunidad* | Lista de verificación básica completada; análisis estático sin hallazgos críticos; procedencia declarada | Lectura de archivos del proyecto, herramientas de solo lectura (`Read`, `Grep`, `Glob`), sin red | Sin escritura fuera del directorio de la skill; sin ejecución de shell arbitraria |
| **N2** | *Vetado por la organización* | Revisión de seguridad completa; prueba en sandbox superada; permisos justificados y aprobados por el responsable de seguridad | Herramientas de lectura y escritura delimitadas; ejecución de scripts específicos aprobados; red restringida a dominios allowlisted | Monitorización obligatoria; revisión periódica de actualizaciones; `allowed-tools` explícito |
| **N3** | *Certificado por el proveedor* | Auditoría externa o certificación equivalente; cumplimiento de AST10 verificado; trazabilidad completa; acuerdo de nivel de servicio de seguridad | Conjunto completo de herramientas aprobadas para el caso de uso; acceso a datos sensibles según política; integración con MCP aprobados | Recertificación anual; notificación obligatoria de cambios; plan de respuesta a incidentes |

**Justificación del modelo.** Un esquema de cuatro niveles equilibra granularidad y operatividad. Menos niveles no distinguen entre una skill simplemente “revisada” y una “certificada”, lo que difumina la responsabilidad y dificulta la asignación de capacidades. Más niveles introducirían complejidad administrativa sin una ganancia proporcional de seguridad. La transición entre niveles debe ser **explícita y documentada**, y el descenso de nivel debe ser automático ante eventos como una actualización no revisada, un incidente de seguridad o una deriva de comportamiento detectada.

#### 9.2 Comité de Gobernanza de Seguridad de IA

Para las decisiones de nivel N2 y N3, se propone un **Comité de Gobernanza de Seguridad de IA** con composición cross-funcional y derechos de decisión claros. La literatura sobre comités de gobernanza de IA identifica la necesidad de órganos que resuelvan decisiones que los equipos de producto no pueden tomar por sí solos, incluyendo la aprobación o rechazo de usos de alto impacto, la resolución de desacuerdos entre funciones y la revisión de incidentes materiales.

**Composición propuesta:**

| Rol | Contribución principal |
|---|---|
| **Presidencia (CISO o delegado)** | Autoridad final sobre decisiones de seguridad; escalado de incidentes críticos |
| **Arquitectura de IA** | Evaluación técnica de la arquitectura de la skill, integración con MCP y modelo de permisos |
| **Seguridad de aplicaciones (AppSec)** | Análisis de código, revisión de scripts, evaluación de vectores de ataque |
| **Cumplimiento y privacidad** | Mapeo a EU AI Act, ISO 42001, NIST AI RMF; evaluación de impacto en privacidad |
| **Legal** | Responsabilidad, términos de licencia, obligaciones contractuales |
| **Representante de producto/negocio** | Justificación del caso de uso, aceptación del riesgo residual |
| **Operaciones/SRE** | Capacidad de monitorización, respuesta a incidentes, viabilidad de sandbox |

**Funciones del comité:** (a) aprobar o rechazar skills de nivel N2 y N3; (b) definir y revisar la política de niveles de confianza; (c) revisar incidentes materiales y identificar debilidades sistémicas; (d) aprobar excepciones temporales con fecha de caducidad; (e) mantener el registro de decisiones y su justificación. Las decisiones deben ser **colegiadas y documentadas**, con voto de calidad de la presidencia en caso de empate.

### 10. Consideraciones Éticas y de Responsabilidad

#### 10.1 Sesgos y transparencia

Las skills heredan los sesgos de sus autores y de los datos o procedimientos que codifican. Una skill de selección de candidatos, de priorización de clientes o de evaluación de riesgos puede incorporar criterios discriminatorios de forma inadvertida. La gobernanza debe incluir **revisiones de sesgo** para skills que afecten a personas, y la `description` debe declarar el propósito de manera que los usuarios puedan identificar cuándo una skill está tomando decisiones con impacto significativo.

La transparencia tiene dos dimensiones: **transparencia hacia el usuario** (que sepa qué skill se está ejecutando y con qué permisos) y **transparencia del artefacto** (que la `description` refleje fielmente lo que la skill hace). La opacidad de la divulgación progresiva no exime de la obligación de transparencia: el hecho de que el agente no lea el código no significa que el usuario no tenga derecho a saber qué código se ejecuta en su nombre.

#### 10.2 Límites de la autonomía delegada

La autonomía de un agente que ejecuta skills debe ser **proporcional a la reversibilidad de las acciones y al radio de explosión**. Las acciones irreversibles (envío de comunicaciones externas, modificación de registros financieros, eliminación de datos) requieren supervisión humana explícita, independientemente del nivel de confianza de la skill. La regla de diseño es: **cuanto mayor es el impacto potencial, menor debe ser el grado de autonomía no supervisada**.

#### 10.3 Responsabilidad legal y ética

La responsabilidad por el daño causado por una skill no recae exclusivamente en el modelo. Se distribuye entre el **autor** (que diseñó el artefacto), el **revisor** (que lo aprobó), la **organización** (que lo desplegó y definió sus permisos) y el **proveedor de la plataforma** (que facilitó su distribución). La documentación de cada fase del ciclo de vida —incluyendo las decisiones de aprobación y los riesgos residuales aceptados— es el mecanismo que permite **atribuir responsabilidades de forma fundamentada** y demostrar diligencia debida ante una investigación o un procedimiento regulatorio.

### 11. Cumplimiento Normativo y Estándares

#### 11.1 Mapeo a marcos regulatorios

Los tres marcos de referencia —EU AI Act, ISO/IEC 42001 y NIST AI RMF— abordan el mismo ciclo de vida de gestión de riesgos con diferentes pesos legales y estructuras de evidencia. La documentación generada por el ciclo de vida de una skill puede servir como evidencia para los tres si se diseña con la granularidad adecuada.

**Tabla 11.1 — Correspondencia entre controles del ciclo de vida de skills y marcos normativos**

| Área de control | EU AI Act | NIST AI RMF | ISO/IEC 42001 |
|---|---|---|---|
| **Gestión de riesgos** | Artículo 9 — sistema de gestión de riesgos durante todo el ciclo de vida | *Govern* + *Map* | Cláusula 6.1 / Anexo A.4 |
| **Documentación técnica** | Artículos 11-13 — documentación técnica (Anexo IV), registro de eventos, instrucciones de uso | *Map* + *Measure* | Anexo A.6 / Anexo A.8 |
| **Supervisión humana** | Artículo 14 — medidas de supervisión humana | *Manage* | Anexo A.9 |
| **Monitorización poscomercialización** | Artículo 72 — monitorización; Artículo 73 — notificación de incidentes graves | *Manage* + *Measure* | Anexo A.10 / evaluación de desempeño |
| **Gobernanza de terceros** | Artículo 15 — precisión, robustez y ciberseguridad (para sistemas de alto riesgo) | *Govern* | Anexo A.10 (relaciones con terceros) |

La documentación que satisface el Anexo IV del EU AI Act cubre la mayor parte de lo que NIST e ISO solicitan, con una reformateo ligero. Por tanto, **una organización que documenta rigurosamente el ciclo de vida de sus skills no está produciendo tres conjuntos de evidencia separados, sino un único cuerpo de evidencia que se traduce a los formatos que cada marco requiere**.

#### 11.2 La documentación como evidencia de cumplimiento

Para que la documentación sea aceptable como evidencia, debe cumplir tres condiciones: **trazabilidad** (cada decisión está vinculada a un artefacto, una fecha y un responsable), **verificabilidad** (los criterios de aprobación son explícitos y las pruebas son reproducibles) y **actualización** (la documentación refleja el estado real de la skill, incluyendo sus actualizaciones y su nivel de confianza vigente). Un registro de decisiones incompleto o desactualizado es peor que la ausencia de registro, porque crea una falsa sensación de diligencia.


## Bloque IV: Referencia Técnica

### 12. Referencia de la Especificación `SKILL.md`

#### 12.1 Campos del frontmatter YAML

La especificación abierta define **dos campos obligatorios** y **cuatro campos opcionales** en el frontmatter de `SKILL.md`.

| Campo | Obligatorio | Tipo / restricciones | Función |
|---|---|---|---|
| `name` | Sí | 1-64 caracteres; minúsculas, dígitos y guiones; sin guiones al inicio/final; sin guiones consecutivos; debe coincidir con el nombre del directorio padre | Identificador de la skill |
| `description` | Sí | 1-1,024 caracteres; no vacío | Texto de coincidencia para la activación; contrato de activación |
| `license` | No | Nombre corto de licencia o referencia a archivo de licencia | Términos legales |
| `compatibility` | No | 1-500 caracteres si está presente | Requisitos de entorno (paquetes, red) |
| `metadata` | No | Mapa de claves y valores de cadena | Propiedades específicas del cliente (autor, versión) |
| `allowed-tools` | No | Cadena separada por espacios; marcado como experimental | Herramientas que la skill solicita preaprobadas |

**Restricciones adicionales de plataforma.** Anthropic añade que `name` y `description` no pueden contener etiquetas XML, y que `name` no puede contener las palabras reservadas “anthropic” o “claude”. Claude Code añade campos propios (`when_to_use`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`, `context`, `agent`, `paths`, `shell`, `hooks`), pero **fuera de Claude Code solo se aceptan los seis campos de la especificación**; cargar una skill con campos extra en claude.ai o en la API de Skills falla con un error de “clave inesperada”.

#### 12.2 Ejemplo de `SKILL.md` con permisos mínimos

```yaml
---
name: csv-column-stats
description: >
  Computes descriptive statistics (count, mean, median, min, max) for a
  numeric column in a CSV file. Use only when the user provides a local
  CSV and asks for column-level statistics. Does not modify the file
  and does not access the network.
allowed-tools: Read Grep
---

# CSV Column Statistics

1. Read the CSV header to identify column names.
2. If the user has not specified a column, ask for clarification.
3. Use the bundled `scripts/stats.py` with the column name as the only
   argument. The script reads the file locally and prints a JSON object
   with the five statistics.
4. Return the JSON object to the user without reformatting.
```

En este ejemplo, `allowed-tools: Read Grep` restringe la skill a herramientas de solo lectura. La `description` declara explícitamente lo que la skill **no** hace (“Does not modify the file and does not access the network”), lo que reduce el riesgo de activación en contextos de escritura o de red.

#### 12.3 Reglas de privilegio mínimo

1. **Declarar `allowed-tools` siempre que sea posible.** Si no se declara, la skill hereda el conjunto de herramientas del agente, que puede ser significativamente más amplio de lo necesario.
2. **Preferir herramientas de solo lectura** (`Read`, `Grep`, `Glob`) sobre herramientas de escritura o ejecución.
3. **Restringir `Bash` sin justificación.** La ejecución de shell es la herramienta de mayor riesgo; cada uso debe estar justificado por el propósito declarado y revisado en el código del script.
4. **Delimitar el alcance del sistema de archivos** mediante rutas específicas o patrones glob cuando la plataforma lo permita.
5. **No incrustar credenciales** en el `SKILL.md`, en los scripts ni en los archivos de referencia. Las credenciales deben obtenerse de un gestor de secretos en tiempo de ejecución, y la skill debe declarar esa dependencia.
6. **Revisar las actualizaciones como nuevas publicaciones.** Un cambio en una skill, por pequeño que parezca, invalida la revisión anterior y requiere una nueva evaluación de riesgo.

### 13. Referencia de Herramientas y Permisos

La siguiente tabla proporciona una guía de niveles de riesgo y reglas recomendadas para las herramientas que una skill puede invocar. La clasificación es orientativa y debe adaptarse al entorno concreto de cada organización.

| Herramienta / capacidad | Nivel de riesgo | Regla recomendada |
|---|---|---|
| `Read` (lectura de archivos) | Bajo-Medio | Permitir por defecto con alcance delimitado al directorio del proyecto; auditar lecturas fuera del alcance |
| `Grep` (búsqueda de texto) | Bajo | Permitir por defecto; el riesgo reside en la exposición de contenido sensible en los resultados, no en la operación en sí |
| `Glob` (listado de archivos) | Bajo | Permitir por defecto; mismo criterio que `Grep` respecto a la información expuesta |
| `WebFetch` / acceso HTTP | Medio-Alto | Restringir a dominios allowlisted; justificar cada dominio; monitorizar el volumen y los destinos de las peticiones |
| `Bash` / shell genérico | Alto | Restringir por defecto; permitir solo comandos específicos aprobados; revisar cada script que invoque shell |
| `Write` / `Edit` (escritura) | Medio-Alto | Delimitar a rutas específicas; requerir justificación; evitar escritura en archivos de configuración o de memoria del agente |
| `MCP tool` (invocación de servidor MCP) | Variable | Evaluar el servidor MCP como un artefacto independiente; verificar que la skill no amplía los permisos del servidor |
| Acceso a variables de entorno | Alto | Denegar por defecto; permitir solo variables explícitamente declaradas y no sensibles |
| Persistencia en `MEMORY.md` / `SOUL.md` | Crítico | Denegar por defecto; cualquier persistencia requiere aprobación del comité y un mecanismo de caducidad |


## Bloque V: Preguntas Abiertas y Agenda de Investigación

### 14. Desafíos Abiertos en el Ecosistema de Skills

La literatura identifica **siete desafíos abiertos** que estructuran la agenda de investigación del ecosistema de skills: construcción, composición, evaluación, portabilidad, gobernanza, seguridad y alineación. Para cada uno se plantea la pregunta clave que permanece sin resolver.

| Desafío | Pregunta clave sin resolver |
|---|---|
| **Construcción** | ¿Cómo se pueden construir skills que capturen conocimiento procedural profundo y específico del contexto, en lugar de reproducir procedimientos genéricos que el modelo ya podría inferir? |
| **Composición** | ¿Cómo se pueden componer múltiples skills de forma segura y predecible, sin que la interacción entre ellas genere comportamientos emergentes no deseados o amplifique el radio de explosión? |
| **Evaluación** | ¿Qué métricas y metodologías permiten evaluar de forma reproducible la calidad, la seguridad y la utilidad real de una skill, más allá de las señales superficiales de instalaciones o descargas? |
| **Portabilidad** | ¿Cómo se puede garantizar que una skill funcione de manera consistente en diferentes plataformas y versiones de modelos, cuando los clientes implementan de forma divergente los campos opcionales y las extensiones propietarias? |
| **Gobernanza** | ¿Qué modelo de gobernanza distribuye de forma justa y eficaz la responsabilidad entre autores, revisores, plataformas y organizaciones desplegadoras, sin crear cuellos de botella que frenen la innovación? |
| **Seguridad** | ¿Cómo se puede pasar de un modelo de revisión puntual a un modelo de **garantía continua** que detecte la deriva de comportamiento, las actualizaciones maliciosas y las vulnerabilidades latentes a lo largo de todo el ciclo de vida? |
| **Alineación** | ¿Cómo se asegura que las skills, como capa intermedia entre el modelo y el mundo, operen de acuerdo con los valores y las intenciones de los usuarios y las organizaciones, incluso cuando el modelo subyacente cambia o se actualiza? |

La seguridad es el desafío que condiciona a todos los demás: sin un modelo de garantía continua, la construcción, la composición y la portabilidad se construyen sobre una base vulnerable. La alineación, por su parte, es el desafío más profundo, porque afecta a la legitimidad misma del ecosistema: una skill técnicamente segura pero alineada con valores equivocados sigue siendo un riesgo.

### 15. Preguntas Guía para la Reflexión Futura

Este documento debe revisarse periódicamente. Las siguientes preguntas están diseñadas para estructurar esa revisión y detectar desviaciones antes de que se conviertan en incidentes.

- **¿Estamos auditando el código de cada skill o delegando la seguridad al modelo?** El modelo no lee el código que ejecuta; la auditoría humana es insustituible. Si la respuesta es “delegamos en el modelo”, la organización ha transferido una responsabilidad que el modelo no puede asumir.
- **¿Qué métricas de frescura exigimos a las skills que dependen de APIs externas?** Una skill que invoca una API que ha cambiado puede fallar silenciosamente o, peor, ejecutar una acción incorrecta. ¿Tenemos un *freshness SLO* medible, con detección de cambios, evaluación de impacto y ventana de actualización?
- **¿Cómo evoluciona el equilibrio entre autonomía y supervisión humana?** A medida que las skills se vuelven más capaces, la tentación de reducir la supervisión aumenta. ¿Estamos ajustando los umbrales de autonomía en función del radio de explosión y la reversibilidad, o los estamos relajando por conveniencia operativa?
- **¿Estamos midiendo la diversidad real del ecosistema o solo su volumen?** Un mercado con 40,000 skills y un 46.3% de duplicados no es un mercado diverso. ¿Qué métricas de unicidad, profundidad y valor diferencial estamos utilizando?
- **¿La revisión de skills está integrada en el ciclo de desarrollo o es un trámite separado?** Si la revisión se percibe como un obstáculo externo, se degradará. Si está integrada en el flujo de trabajo, puede convertirse en una práctica de ingeniería.
- **¿Qué ocurre cuando una skill certificada se degrada?** ¿Tenemos un mecanismo automático de degradación del nivel de confianza y de revocación de permisos, o dependemos de que alguien lo detecte manualmente?


## Bloque VI: Apéndices y Soporte

### 16. Glosario y Referencias

#### 16.1 Glosario

| Término | Definición |
|---|---|
| **Progressive disclosure (divulgación progresiva)** | Arquitectura de carga en tres niveles que minimiza el consumo de contexto: metadatos compactos al inicio, instrucciones completas al activarse la skill, recursos solo cuando se necesitan |
| **`SKILL.md`** | Archivo raíz de una skill; contiene frontmatter YAML con metadatos e instrucciones Markdown |
| **`allowed-tools`** | Campo opcional del frontmatter que declara las herramientas que la skill solicita preaprobadas |
| **MCP (Model Context Protocol)** | Protocolo abierto que conecta aplicaciones LLM con fuentes de datos y herramientas externas; las skills enseñan al agente *cómo* usar esas herramientas |
| **AST10 (OWASP Agentic Skills Top 10)** | Primer marco integral de riesgos de seguridad para skills de agentes de IA, con diez clases de riesgo documentadas |
| **Blast radius (radio de explosión)** | Alcance de recursos, datos y capacidades accesibles si una skill o un agente es comprometido |
| **Shadow features** | Funcionalidades ocultas al usuario que una skill ejecuta sin declararlas en su descripción o instrucciones visibles |
| **Skills zombi** | Listados duplicados, de baja calidad o abandonados que saturan el mercado y dificultan el descubrimiento de skills útiles |

#### 16.2 Referencias y marcos citados

- **EU AI Act** — Reglamento (UE) 2024/1689. Artículos 9 (gestión de riesgos), 11-13 (documentación técnica y registro), 14 (supervisión humana), 72-73 (monitorización poscomercialización e incidentes).
- **ISO/IEC 42001** — Sistema de gestión de inteligencia artificial. Cláusula 6.1 y Anexos A.4, A.6, A.8, A.9, A.10.
- **NIST AI Risk Management Framework (AI RMF 1.0)** — Funciones *Govern*, *Map*, *Measure*, *Manage*.
- **OWASP Agentic Skills Top 10 (AST10)** — Marco de riesgos de seguridad para skills de agentes; versión 1.0 publicada en agosto de 2026.
- **Agent Skills Specification** — Especificación abierta del formato `SKILL.md`, disponible en agentskills.io.
- **ClawHavoc (enero de 2026)** — Campaña de infiltración de 1,184 skills maliciosas en el mercado ClawHub.
- **Agent Skills in the Wild (Liu et al., arXiv:2601.10338)** — Estudio empírico de 31,132 skills; 26.1% con al menos una vulnerabilidad.
- **Agent Skills Ecosystem: A Quantitative Analysis (arXiv:2602.08004)** — Análisis de 40,285 skills; crecimiento 18.5× en 20 días y 46.3% de duplicados.

### 17. Registro de Cambios de la Documentación

| Versión | Fecha | Cambios principales | Autor |
|---|---|---|---|
| 1.0 | 18 de noviembre de 2026 | Versión inicial completa. Cubre los 17 apartados, modelo de gobernanza por niveles, listas de verificación y mapeo normativo. |  |


## Conclusiones y Recomendaciones

### Mensajes clave

**1. La gobernanza no es un freno al ecosistema; es su condición de posibilidad.** Los datos de ClawHavoc, el 26.1% de skills con vulnerabilidades y el 46.3% de duplicados no describen un ecosistema “libre”, sino un ecosistema **degradado por la ausencia de límites**. Sin controles de cantidad, permisos y revisión, el volumen de skills crece mientras su calidad y su seguridad se deterioran. La gobernanza es lo que permite que las skills de calidad se distingan y sobrevivan.

**2. La `description` es el punto de control más crítico y el más descuidado.** Es el único texto que el agente utiliza para decidir si activa una skill, y sin embargo se redacta con frecuencia como documentación decorativa. Una `description` que no delimita el propósito y los límites de la skill es un fallo de seguridad, no un detalle de estilo.

**3. La divulgación progresiva crea una opacidad estructural que solo la revisión humana puede cerrar.** El modelo no lee el código que ejecuta. La seguridad de una skill depende de que un revisor humano inspeccione todos sus archivos antes del despliegue. Delegar esa función al modelo es transferirle una responsabilidad que no puede asumir.

**4. La trazabilidad es la infraestructura de la rendición de cuentas.** Sin registros de decisiones, prompts, invocaciones y resultados, es imposible determinar si un fallo provino del modelo, del prompt, de la skill o de la revisión. La trazabilidad convierte los incidentes en aprendizaje en lugar de en recaídas.

**5. El modelo de confianza por niveles debe ser explícito, verificable y degradable.** La confianza no se autodeclara: se gana con evidencia y se pierde cuando las condiciones cambian. Un esquema de cuatro niveles (sandboxed → comunidad → organización → proveedor) con transiciones documentadas y degradación automática es más operativo que un sistema binario de “aprobado/rechazado”.

### Próximos pasos recomendados para la organización

1. **Adoptar formalmente este documento** como marco de referencia para el ciclo de vida de skills, asignando un responsable de su mantenimiento y revisión periódica.
2. **Constituir el Comité de Gobernanza de Seguridad de IA** con la composición propuesta, o adaptarlo a la estructura organizativa existente, asegurando que tenga autoridad real de decisión sobre skills de nivel N2 y N3.
3. **Implementar el registro de trazabilidad** para todas las skills en producción, comenzando por las de mayor radio de explosión.
4. **Ejecutar una auditoría de las skills ya desplegadas** utilizando la lista de verificación de la Sección 5.2, priorizando aquellas con scripts ejecutables y permisos de red o de escritura.
5. **Establecer un *freshness SLO*** para las skills que dependen de APIs externas, con métricas de detección de cambios, evaluación de impacto y ventana de actualización.
6. **Revisar este documento anualmente** y siempre que ocurra un incidente material, utilizando las preguntas guía de la Sección 15 como estructura de la revisión.

La conclusión final es que **el ecosistema de skills ya no es un experimento**: es una capa de infraestructura para agentes de IA, con decenas de miles de artefactos en circulación y un historial documentado de ataques a escala. Tratarlo como infraestructura —con los controles, la trazabilidad y la gobernanza que la infraestructura exige— es la única vía para que su promesa de reutilización y especialización se realice sin reproducir los fallos que la ausencia de límites ya ha demostrado.
```
