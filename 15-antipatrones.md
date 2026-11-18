---
title: "15 · Antipatrones"
description: "Errores frecuentes al adoptar IDEs agénticos y Antigravity, con síntomas, causas y correcciones."
doc_id: "15"
version: "1.0.0"
last_updated: "2026-11-18"
status: "borrador-revisable"
audience: ["ingeniería", "tech leads", "seguridad"]
tags: ["antipatrones", "errores", "riesgos", "calidad"]
prev: "14-buenas-practicas.md"
next: "16-limitaciones.md"
---

# 15 · Antipatrones

[← 14 · Buenas prácticas](14-buenas-practicas.md) · [README](README.md) · [Siguiente: 16 · Limitaciones →](16-limitaciones.md)

---

Cada antipatrón se presenta con **síntoma**, **por qué ocurre**, **consecuencia** y **corrección**. Se agrupan por área.

## 1. Seguridad y permisos

### 1.1 Autonomía total en la máquina personal

- **Síntoma**: política de ejecución sin aprobación activada “para ir más rápido”, en un portátil con datos, claves y sesiones.
- **Por qué**: la fricción de aprobar cada comando es real y molesta.
- **Consecuencia**: un comando mal formado o una inyección tiene efecto inmediato. Se ha informado de un caso en el que una petición de limpiar caché derivó en un borrado irrecuperable de una unidad entera.
- **Corrección**: reglas `deny` explícitas, sandbox, aprobación solo para lo sensible; autonomía total únicamente en contenedor o VM desechable.

### 1.2 Confiar en la política de ejecución como control de acceso a datos

- **Síntoma**: “el agente no puede leer `.env` porque requiere aprobación”.
- **Por qué**: se confunde control de comandos con control de datos.
- **Consecuencia**: el agente puede acceder a contenido por rutas alternativas (se ha demostrado eludir políticas imprimiendo ficheros con comandos permitidos).
- **Corrección**: no tener secretos reales en el entorno del agente; aislamiento a nivel de sistema operativo o contenedor.

### 1.3 Navegación abierta con secretos al alcance

- **Síntoma**: el subagente de navegador puede visitar cualquier dominio mientras el workspace contiene credenciales.
- **Consecuencia**: una página con instrucciones ocultas puede inducir el envío de datos a un destino del atacante, como se ha demostrado con inyección indirecta.
- **Corrección**: lista de permitidos, perfil separado, agentes separados para investigación web e implementación.

### 1.4 Abrir repositorios no confiables con permisos habituales

- **Síntoma**: clonar y abrir un repositorio desconocido “para ver qué hace” con la configuración normal.
- **Consecuencia**: ficheros del repositorio pueden contener instrucciones o configuración maliciosa; se han demostrado puertas traseras persistentes mediante contenido del workspace.
- **Corrección**: nivel 0 de autonomía, contenedor, y no confiar en el workspace sin revisarlo.

### 1.5 Servidores MCP y plugins sin auditar

- **Síntoma**: instalar servidores del directorio “porque tienen muchas estrellas”.
- **Consecuencia**: código ejecutado con tus credenciales; descripciones de herramientas con instrucciones ocultas.
- **Corrección**: lista aprobada, versión fijada, revisión del código y de los metadatos, mínimo privilegio.

### 1.6 Token personal con permisos excesivos

- **Síntoma**: PAT clásico con acceso a toda la organización pegado en la configuración.
- **Consecuencia**: cualquier fallo del agente o del servidor MCP afecta a todo.
- **Corrección**: tokens de grano fino por repositorio, cuentas de servicio, caducidad corta.

## 2. Delegación y proceso

### 2.1 El prompt vago

- **Síntoma**: “Arregla el rendimiento”, “limpia este módulo”.
- **Consecuencia**: el agente decide el alcance; PRs enormes e incomprensibles.
- **Corrección**: objetivo observable, restricciones y criterios de aceptación ejecutables.

### 2.2 Saltarse el plan

- **Síntoma**: lanzar tareas amplias sin revisar el plan.
- **Consecuencia**: el malentendido se descubre tras horas de ejecución y cientos de líneas.
- **Corrección**: plan previo obligatorio en tareas no triviales; comentar y ajustar.

### 2.3 La tarea gigante

- **Síntoma**: “Migra todo el monolito a microservicios”.
- **Consecuencia**: derivas, contexto saturado, resultados irrevisables.
- **Corrección**: descomponer en tareas de un PR; usar agentes de investigación y de implementación separados.

### 2.4 Demasiados agentes en paralelo

- **Síntoma**: diez agentes activos y una persona revisando.
- **Consecuencia**: aprobación por inercia, defectos escapados, cuello de botella en revisión.
- **Corrección**: limitar agentes por persona a la capacidad real de revisión.

### 2.5 Mezclar objetivos en una conversación

- **Síntoma**: “y ya de paso, arregla también…”.
- **Consecuencia**: contexto contaminado, cambios no relacionados en el mismo diff.
- **Corrección**: una tarea, una conversación, un PR.

## 3. Verificación y calidad

### 3.1 Creer el walkthrough

- **Síntoma**: aprobar porque el resumen del agente dice que todo pasó.
- **Consecuencia**: el resumen puede ser optimista, incompleto o erróneo.
- **Corrección**: revisar el diff, ejecutar CI independiente y contrastar capturas con los criterios.

### 3.2 Tests que no prueban nada

- **Síntoma**: cobertura alta con aserciones triviales; tests que se ajustan para pasar.
- **Consecuencia**: falsa seguridad.
- **Corrección**: mutation testing, revisión de aserciones, prohibir modificar tests existentes sin justificación.

### 3.3 Verificación solo del camino feliz

- **Síntoma**: grabación que muestra únicamente el caso exitoso.
- **Corrección**: criterios que incluyan errores, bordes, accesibilidad y consola.

### 3.4 Sin CI como puerta final

- **Síntoma**: merge basado solo en lo que el agente ejecutó localmente.
- **Corrección**: checks obligatorios en ramas protegidas.

## 4. Contexto y configuración

### 4.1 Reglas gigantes

- **Síntoma**: fichero de reglas de miles de palabras con procedimientos, historia y opiniones.
- **Consecuencia**: contexto saturado y reglas contradictorias que el agente ignora parcialmente.
- **Corrección**: reglas cortas; procedimientos como Skills; documentación enlazada.

### 4.2 Skills con descripción vaga o “todoterreno”

- **Síntoma**: nombre y descripción genéricos.
- **Consecuencia**: no se activan, o lo hacen fuera de lugar.
- **Corrección**: descripción con qué, cuándo y cuándo no; una responsabilidad por Skill.

### 4.3 Documentación obsoleta o contradictoria

- **Síntoma**: ADR antiguas sin marcar, README con comandos que ya no funcionan.
- **Consecuencia**: el agente aplica decisiones caducadas con total convicción.
- **Corrección**: propietarios, fechas, estado de vigencia y limpieza periódica.

### 4.4 Memoria persistente sin supervisión

- **Síntoma**: nadie revisa lo que el agente “aprende”.
- **Consecuencia**: fija decisiones erróneas o antiguas y las propaga a futuras tareas.
- **Corrección**: revisión periódica y normas críticas en reglas versionadas, no en memoria implícita.

### 4.5 Demasiadas herramientas MCP activas

- **Síntoma**: decenas de servidores habilitados “por si acaso”.
- **Consecuencia**: peor selección de herramientas, más coste de contexto y mayor superficie de ataque.
- **Corrección**: activar por proyecto solo lo necesario; plugins por rol.

### 4.6 Configuración solo en el equipo de cada persona

- **Síntoma**: cada desarrollador con reglas, Skills y MCP propios.
- **Consecuencia**: resultados inconsistentes, imposibilidad de auditar.
- **Corrección**: configuración en el repositorio y plugin corporativo.

## 5. Organización

### 5.1 Medir productividad por líneas generadas

- **Consecuencia**: incentiva volumen sobre calidad.
- **Corrección**: medir aceptación, defectos escapados, tiempo de revisión y ciclo completo.

### 5.2 Adopción sin formación ni gobierno

- **Consecuencia**: nivel 0 de madurez de forma permanente, riesgos sin control.
- **Corrección**: formación breve obligatoria, propietarios y revisión trimestral.

### 5.3 Estandarizar en una sola herramienta sin salida

- **Consecuencia**: dependencia de un proveedor en un mercado muy cambiante (modelos retirados, cuotas, cambios de producto).
- **Corrección**: contexto portátil con estándares abiertos y reevaluación periódica.

### 5.4 Revisión de PRs de agente igual que las humanas

- **Consecuencia**: errores de patrón distintos (plausible pero incorrecto) pasan desapercibidos.
- **Corrección**: checklist específica y atención a dependencias, tests modificados y cambios fuera de alcance.

### 5.5 Sustituir la formación de junior por agentes

- **Consecuencia**: pérdida de la capacidad de revisión futura.
- **Corrección**: usar agentes como herramienta de aprendizaje con revisión guiada, no como sustituto del criterio.

## 6. Tabla resumen

| # | Antipatrón | Riesgo | Control clave |
|---|---|---|---|
| 1.1 | Autonomía total local | Alto | Sandbox, deny, entorno desechable |
| 1.2 | Política = control de datos | Alto | Sin secretos en el entorno |
| 1.3 | Navegación abierta | Alto | Lista de permitidos |
| 1.4 | Repos no confiables | Alto | Nivel 0 en contenedor |
| 1.5 | MCP sin auditar | Alto | Lista aprobada |
| 2.1 | Prompt vago | Medio | Plantilla de delegación |
| 2.2 | Sin plan | Medio | Plan obligatorio |
| 3.1 | Creer el walkthrough | Alto | CI y revisión del diff |
| 3.2 | Tests vacíos | Medio | Mutation testing |
| 4.1 | Reglas gigantes | Medio | Reglas cortas + Skills |
| 4.4 | Memoria sin revisar | Medio | Revisión periódica |
| 5.1 | Medir líneas | Medio | Métricas de calidad |

## 7. Autoevaluación rápida

Si respondes “sí” a tres o más, tu adopción necesita revisión:

- [ ] ¿El agente corre con aprobación desactivada en tu máquina de trabajo?
- [ ] ¿Hay secretos reales en el workspace donde se usa el navegador del agente?
- [ ] ¿Se aprueban planes y PRs sin leerlos?
- [ ] ¿Nadie revisa la memoria persistente o las Skills de terceros?
- [ ] ¿El merge depende solo del resumen del agente?
- [ ] ¿Cada persona tiene su propia configuración sin versionar?

---

[← 14 · Buenas prácticas](14-buenas-practicas.md) · [README](README.md) · [Siguiente: 16 · Limitaciones →](16-limitaciones.md)
