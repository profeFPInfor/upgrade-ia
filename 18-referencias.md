---
title: "18 · Referencias, glosario y verificación"
description: "Fuentes consultadas, glosario de términos y checklist de verificación periódica de la documentación."
doc_id: "18"
version: "1.0.0"
last_updated: "2026-11-18"
status: "borrador-revisable"
audience: ["todos"]
tags: ["referencias", "fuentes", "glosario", "verificación"]
prev: "17-futuro.md"
next: null
---

# 18 · Referencias

[← 17 · Futuro](17-futuro.md) · [README](README.md)

---

## 1. Cómo se han usado las fuentes

La información sobre Antigravity procede de **búsquedas web realizadas el 18 de noviembre de 2026**. Se ha dado prioridad a documentación oficial, entradas de blog de Google, informes de investigadores de seguridad con divulgación coordinada y *codelabs* de Google. Las páginas de terceros (guías, reseñas, agregadores) se han usado como apoyo y se ha contrastado lo posible entre varias.

**Limitaciones de esta bibliografía:**

- No se ha accedido a todas las páginas de la documentación oficial; varias afirmaciones de configuración (rutas, nombres de ajustes) proceden de extractos y de guías de terceros y **deben verificarse** en la versión que uses.
- Los datos de planes, cuotas, modelos y versiones son volátiles. Se indica la fecha de consulta.
- La información sobre herramientas distintas de Antigravity (capítulo 07) se basa en conocimiento general y **no se ha reverificado fuente por fuente** en esta redacción.

## 2. Fuentes principales

### 2.1 Oficiales de Google

| Fuente | Uso en la documentación |
|---|---|
| Sitio de Antigravity (`antigravity.google`) y su documentación: inicio, planes, modelos, descargas | Superficies, planes, modelos, ajustes, artifacts, navegador, sandbox, MCP, Skills, plugins |
| Documentación de la CLI: sandbox | Sandbox nativo por sistema operativo (macOS y Windows) |
| Blog de desarrolladores de Google: “Build with Google Antigravity, our new agentic development platform” | Concepto de plataforma agent-first, Editor y Manager |
| Codelabs de Google: “Command and control: Orchestrate app development with Gemini and MCP” | MCP, Skills en la CLI, estructura de directorios de configuración |
| Codelabs de Google: “Agentic UI automation with Antigravity” | Skills, MCP multimodal, navegador |
| Codelabs de Google: “Supercharge Code Quality: AI-Assisted Code Review with Antigravity CLI and SDK” | Revisión de código con CLI y SDK |
| Entrada de la comunidad de Google AI en DEV: “Building an agentic PR reviewer with Antigravity SDK” | Patrón de workflow de GitHub Actions para revisión de PRs |

### 2.2 Cobertura de prensa y análisis

| Fuente | Uso |
|---|---|
| VentureBeat, “Google Antigravity introduces agent-first architecture for asynchronous, verifiable coding workflows” (18 nov 2025) | Presentación del producto, Editor y Manager |
| Wikipedia, “Google Antigravity” | Cronología, modos de autonomía, incidentes, soporte de modelos |
| Charla de AI Engineer Code 2025, “Defying Gravity” | Tres superficies y filosofía de producto |
| Guías de terceros sobre Antigravity 2.0 (por ejemplo, de Lilach Bullock, danicat.dev, networkershome, fastero, aimadetools) | Superficies, versiones, planes y modelos a noviembre de 2026; algunas difieren en detalles (por ejemplo, lenguajes soportados por el SDK) |
| Firecrawl, “Antigravity skills” | Rutas de Skills por superficie |
| Iceberg Lakehouse, “Context: Google Antigravity” | Tipos de artifacts y pilares de contexto |

### 2.3 Seguridad

| Fuente | Tema |
|---|---|
| PromptArmor, “Google Antigravity exfiltrates data” | Inyección indirecta y exfiltración vía subagente de navegador |
| Mindgard, “Google Antigravity persistent code execution vulnerability” | Persistencia y ejecución de código desde el workspace |
| Pillar Security, “Prompt injection leads to RCE and sandbox escape in Antigravity” (20 abr 2026) | Inyección en el tool de búsqueda de ficheros, evasión de modo estricto |
| Cloud Security Alliance, nota de investigación sobre la cadena de ejecución (21 abr 2026) | Análisis complementario (marcado por su autor como investigación asistida y no oficial) |
| TechRadar y CyberScoop | Cobertura de hallazgos |
| Agentpedia, “Antigravity security guide” | Ajustes de endurecimiento sugeridos (fuente de terceros; verificar) |

### 2.4 Integraciones

| Fuente | Tema |
|---|---|
| Documentación de CodeRabbit para Antigravity | Plugin de revisión con `gh` |
| Material sobre el servidor MCP oficial de GitHub y revisión acotada de PRs | Solo lectura, herramientas limitadas, permisos mínimos |
| Estándar *Model Context Protocol* | Arquitectura MCP |
| Estándar *Agent Skills* | Formato de Skills |

## 3. Glosario

| Término | Definición |
|---|---|
| Agent harness | Bucle de ejecución del agente: modelo, herramientas, permisos, contexto y artifacts |
| Agent Manager | Vista o superficie de orquestación de varios agentes y revisión de sus resultados |
| Agent-first | Paradigma en el que las superficies existen para el agente y el humano dirige y revisa |
| Artifact | Entregable verificable del agente: plan, lista de tareas, walkthrough, captura, grabación |
| `agy` | Comando de la CLI de Antigravity |
| Browser subagent | Agente especializado en controlar el navegador |
| Context engineering | Disciplina de decidir qué información recibe el agente, cuándo y cómo |
| Hook | Lógica determinista ejecutada en eventos del ciclo del agente |
| Inyección indirecta de instrucciones | Contenido no confiable leído por el agente que contiene órdenes dirigidas a él |
| MCP | Model Context Protocol: estándar para conectar agentes con herramientas y datos externos |
| Plugin | Paquete que agrupa Skills, MCP, reglas, hooks y agentes |
| Projects | Agrupación de carpetas de trabajo en la App |
| RAG | Generación aumentada por recuperación de información |
| Regla | Instrucción siempre presente o por patrón |
| Sandbox | Entorno restringido de ejecución de comandos |
| Skill | Paquete de procedimiento cargado bajo demanda, con `SKILL.md` |
| Subagente | Agente creado por otro para una subtarea |
| Worktree | Copia de trabajo aislada de Git para trabajo en paralelo |
| Workflow | Secuencia repetible invocada por el usuario |
| Turbo | Modo de ejecución de terminal sin aprobaciones |

## 4. Checklist de verificación periódica

Ejecutar cada trimestre y tras cualquier anuncio mayor de producto.

### 4.1 Producto

- [ ] ¿Siguen vigentes los nombres de superficies y la separación App/IDE?
- [ ] ¿Cambió el catálogo de modelos y su disponibilidad por plan?
- [ ] ¿Cambiaron cuotas, planes o precios?
- [ ] ¿El SDK sigue en preview? ¿Cambió su API?
- [ ] ¿Cambiaron las rutas de configuración de Skills, MCP y plugins?
- [ ] ¿El IDE independiente cubre ya el acceso empresarial?

### 4.2 Seguridad

- [ ] ¿Hay nuevas divulgaciones o avisos de seguridad?
- [ ] ¿Cambiaron los valores por defecto de políticas de terminal y artifacts?
- [ ] ¿Mejoró o cambió el sandbox por sistema operativo?
- [ ] ¿La configuración aprobada de la organización sigue siendo válida?

### 4.3 Integración

- [ ] ¿Las acciones de GitHub de terceros siguen fijadas y auditadas?
- [ ] ¿Los servidores MCP aprobados mantienen versión y propietario?
- [ ] ¿Se rotaron los tokens de servicio?

### 4.4 Contenido de esta documentación

- [ ] Actualizar `last_updated` y `version` en los capítulos modificados.
- [ ] Revisar los avisos `Verificar` de cada capítulo.
- [ ] Validar enlaces relativos y diagramas Mermaid.
- [ ] Reverificar el capítulo 07 con fuentes actuales de cada herramienta.

## 5. Cómo citar esta documentación

```text
Equipo de Plataforma de Ingeniería. "Antigravity IDE: documentación técnica y de adopción",
versión 1.0.0, 18 de noviembre de 2026. Repositorio interno, carpeta docs/.
```

## 6. Aviso final

Esta documentación describe un producto en evolución rápida. Las afirmaciones se han redactado con cautela y señalan lo que debe verificarse. Ante cualquier discrepancia entre este texto y la documentación oficial vigente, **prevalece la documentación oficial**; abre una *issue* para corregir el capítulo afectado.

---

[← 17 · Futuro](17-futuro.md) · [README](README.md)
