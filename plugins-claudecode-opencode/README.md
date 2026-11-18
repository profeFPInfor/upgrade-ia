# Volcar plugins de Claude Code a OpenCode

> **Entorno objetivo:** OpenCode **2.0.x** (V2). La API de plugins de V2 está en beta y puede cambiar.
>
> Fecha de la investigación: octubre de 2026. Ambos ecosistemas cambian muy rápido; conviene revisar las fuentes antes de aplicar nada.

---

## Índice

1. [Qué es un plugin de Claude Code](#1-qué-es-un-plugin-de-claude-code)
2. [Estructura, manifiesto y variables](#2-estructura-manifiesto-y-variables)
3. [Distribución: marketplaces e instalación](#3-distribución-marketplaces-e-instalación)
4. [Catálogo y uso real de componentes](#4-catálogo-y-uso-real-de-componentes)
5. [OpenCode V2: cómo se extiende y su sistema de plugins](#5-opencode-v2-cómo-se-extiende-y-su-sistema-de-plugins)
6. [Matriz de compatibilidad por componente](#6-matriz-de-compatibilidad-por-componente)
7. [Cómo evaluar un plugin antes de volcarlo](#7-cómo-evaluar-un-plugin-antes-de-volcarlo)
8. [Procedimiento general de volcado](#8-procedimiento-general-de-volcado)
9. [Recetas de conversión por componente](#9-recetas-de-conversión-por-componente)
10. [Conversión automática](#10-conversión-automática)
11. [Verificación y problemas habituales](#11-verificación-y-problemas-habituales)
12. [Fuentes](#12-fuentes)
- [Apéndice A — `claude2opencode.py`](#apéndice-a--claude2opencodepy)
- [Apéndice B — `hooks-adapter.template.js`](#apéndice-b--hooks-adaptertemplatejs)

---

## 1. Qué es un plugin de Claude Code

Un plugin de Claude Code es un **directorio autocontenido que empaqueta varias piezas de configuración** para que se puedan compartir entre proyectos y equipos. No es código que se ejecuta "dentro" de Claude Code (como sí ocurre con los plugins de OpenCode), sino sobre todo **ficheros declarativos** (Markdown y JSON) más algunos scripts auxiliares.

Componentes que puede incluir un plugin:

| Componente | Qué hace | Formato |
|---|---|---|
| **Skills** | Instrucciones reutilizables que el modelo carga bajo demanda según la tarea; también generan atajos `/nombre` | Carpeta con `SKILL.md` (frontmatter YAML + Markdown) y ficheros de apoyo |
| **Commands** (slash commands) | Plantillas de prompt que el usuario lanza con `/comando` | Ficheros `.md` en `commands/`. Hoy se consideran formato *legacy*: Claude Code los ha unificado con las skills |
| **Agents** (subagentes) | Asistentes especializados con su propio prompt de sistema, herramientas y modelo | Ficheros `.md` con frontmatter en `agents/` |
| **Hooks** | Manejadores que se disparan en eventos del ciclo de vida (antes/después de usar una herramienta, al enviar un prompt, al iniciar sesión, al parar…) | `hooks/hooks.json` + scripts (shell, Python…) |
| **MCP servers** | Conectan el agente con herramientas y servicios externos mediante Model Context Protocol | `.mcp.json` |
| **LSP servers** | Inteligencia de código (diagnósticos, ir a definición, referencias) | `.lsp.json`, inline en `plugin.json` o en la entrada del marketplace |
| **Monitors** | Procesos en segundo plano que vigilan logs o estados externos y avisan al agente | `monitors/monitors.json` |
| **Output styles** | Cambian el estilo/tono de las respuestas | Directorio de estilos |

**Idea clave para la migración:** las skills, commands y agents son Markdown → se portan con poco esfuerzo. Los MCP son un estándar abierto → se portan cambiando el formato de configuración. Los hooks son scripts atados a eventos de Claude Code → necesitan un adaptador o reescritura.

---

## 2. Estructura, manifiesto y variables

```text
mi-plugin/
├── .claude-plugin/
│   └── plugin.json      # Manifiesto. Solo el manifiesto va aquí dentro
├── skills/
│   └── mi-skill/
│       ├── SKILL.md
│       └── scripts/     # opcional
├── commands/            # slash commands (legacy)
├── agents/              # subagentes
├── hooks/
│   └── hooks.json
├── .mcp.json            # servidores MCP
├── .lsp.json            # servidores LSP
└── README.md
```

Ejemplo de `plugin.json`:

```json
{
  "name": "mi-plugin",
  "version": "1.0.0",
  "description": "Descripción breve",
  "author": { "name": "Autor" },
  "commands": "./custom/commands/",
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./hooks.json",
  "mcpServers": "./.mcp.json",
  "lspServers": "./.lsp.json",
  "userConfig": { "apiKey": { "type": "string", "title": "API key" } }
}
```

Las rutas personalizadas (`commands`, `agents`, `skills`…) son opcionales: si no aparecen, Claude Code busca las carpetas por defecto. Un plugin puede incluso no tener `plugin.json` (los *skill-bundles* del marketplace oficial se declaran directamente en `marketplace.json`).

### Variables y convenciones propias de Claude Code

Son lo primero que se rompe al llevar un plugin a otra herramienta:

| Elemento | Qué es | En OpenCode |
|---|---|---|
| `${CLAUDE_PLUGIN_ROOT}` | Ruta absoluta del plugin instalado. Muy usada en hooks, MCP y scripts | No existe: sustituir por la ruta real donde dejes los ficheros |
| `${CLAUDE_SKILL_DIR}` | Carpeta de la skill en ejecución | No existe: sustituir por la ruta de la skill instalada |
| `${CLAUDE_PLUGIN_DATA}` | Carpeta persistente de datos del plugin | No existe: crear una carpeta y usar su ruta |
| `userConfig` | Valores que Claude Code pide al instalar el plugin | No existe: fijarlos a mano (variables de entorno o editando ficheros) |
| `/plugin:comando`, `plugin:agente` | Espacio de nombres de los componentes de un plugin | `/plugin/comando` (subcarpeta) y el nombre del agente sin prefijo |
| `arguments: nombre` + `$nombre` | Argumentos con nombre en comandos | Solo hay posicionales: `$1`, `$2`… |
| `@fichero` en comandos | Incluye el contenido de un fichero | No se expande en plantillas de OpenCode |
| `allowed-tools` | Preautoriza herramientas | No existe: se controla con los permisos del agente |

---

## 3. Distribución: marketplaces e instalación

- Los plugins se distribuyen mediante **marketplaces**: repositorios git con un `.claude-plugin/marketplace.json` que lista plugins (con su carpeta o un repositorio externo).
- Marketplace oficial: **`anthropics/claude-plugins-official`**, con `plugins/` (mantenidos por Anthropic) y `external_plugins/` (partners y comunidad).
- Instalación desde Claude Code:

```bash
/plugin marketplace add <owner/repo>
/plugin install <plugin>@<marketplace>
/plugin                 # interfaz: Discover, instalados, etc.
claude --plugin-dir ./mi-plugin   # cargar un plugin local para probarlo
```

- **Ámbitos**: `user` (`~/.claude/settings.json`), `project` (`.claude/settings.json`), `local` (`.claude/settings.local.json`) y `managed` (empresa).
- **Seguridad**: un plugin puede incluir scripts y servidores MCP arbitrarios. Hay que confiar en él antes de instalarlo… y antes de volcarlo a otra herramienta.

> 💡 Para volcar un plugin **no hace falta tener Claude Code**: basta con clonar el repositorio del marketplace o del plugin y trabajar sobre su carpeta.

---

## 4. Catálogo y uso real de componentes

### 4.1 Plugins oficiales más conocidos (como referencia)

| Plugin | Para qué sirve | Componentes |
|---|---|---|
| frontend-design | Guía de diseño visual para interfaces | Skill |
| feature-dev | Flujo guiado de desarrollo de funcionalidades | Comando + 3 agentes |
| code-review / pr-review-toolkit | Revisión de PR con varios agentes | Comando + agentes |
| commit-commands | Commit, push y PR en un comando | Comandos |
| security-guidance | Avisos de patrones inseguros | Hooks + scripts Python |
| explanatory / learning-output-style | Modos educativos | Hook `SessionStart` |
| `*-lsp` (typescript, pyright, gopls…) | Inteligencia de código | LSP declarado en el marketplace |
| Integraciones (playwright, github, linear…) | Servicios externos | Servidor MCP |

### 4.2 Qué componentes se usan en la práctica

Recuento sobre las **54 carpetas de plugins** del repositorio oficial (octubre de 2026):

| Componente | Plugins que lo usan | Dificultad de volcado |
|---|---|---|
| Skills | 19 | 🟢 Trivial |
| Servidores MCP | 14 | 🟢 Fácil |
| Commands | 14 | 🟡 Fácil con ajustes |
| Agents | 9 | 🟡 Fácil con ajustes |
| Hooks | 7 | 🔴 Adaptador o reescritura |
| LSP | 12 (declarados en el marketplace) | ⚪ Innecesario en OpenCode |

**Conclusión:** la gran mayoría de plugins se componen de piezas fáciles de volcar. Los hooks son la excepción y conviene tratarlos aparte.

---

## 5. OpenCode V2: cómo se extiende y su sistema de plugins

OpenCode (proyecto de código abierto de Anomaly) es un agente de programación con interfaz de terminal, escritorio, web y extensión de IDE. La versión 2.0 unifica todo sobre un único servidor local. A diferencia de Claude Code, **no tiene un formato de "paquete" que agrupe** skills + agentes + comandos + hooks: cada pieza se configura por separado.

> ⚠️ **La palabra "plugin" significa cosas distintas.** En Claude Code es un paquete de configuración; en OpenCode es **código JS/TS que se ejecuta dentro de OpenCode**. Por eso un plugin de Claude Code no se "instala" en OpenCode: se **descompone** y cada pieza va a su sitio.

### 5.1 Dónde va cada pieza en V2

| Pieza | Proyecto | Global | Alternativa en `opencode.jsonc` |
|---|---|---|---|
| Skills | `.opencode/skills/`, **`.claude/skills/`**, `.agents/skills/` | `~/.config/opencode/skills/`, **`~/.claude/skills/`**, `~/.agents/skills/` | `"skills": ["./ruta", "https://catalogo/"]` |
| Commands | `.opencode/commands/*.md` | `~/.config/opencode/commands/*.md` | `"commands": { ... }` |
| Agents | `.opencode/agents/*.md` | `~/.config/opencode/agents/*.md` | `"agents": { ... }` |
| MCP | — | — | `"mcp": { "servers": { ... } }` o `opencode mcp add` |
| Plugins (código) | `.opencode/plugins/*.ts` o `*.js` | `~/.config/opencode/plugins/` | `"plugins": [ ... ]` |
| Instrucciones | `AGENTS.md` (y `CLAUDE.md` por compatibilidad) | — | — |

En Windows, `~` es `%USERPROFILE%`.

Notas importantes de V2:

- **Subcarpetas = nombres compuestos.** `.opencode/commands/team/review.md` → `/team/review`; `.opencode/agents/team/reviewer.md` → agente `team/reviewer`. Sirve para imitar el prefijo de plugin de Claude Code.
- **Las skills también aparecen como comandos `/id`** (se puede desactivar con `slash: false`).
- **Recarga en caliente:** cambios en commands, skills y plugins locales se aplican sin reiniciar.
- **Proyecto abierto:** las rutas de proyecto solo se cargan si OpenCode tiene una carpeta de proyecto abierta. Sin ella, hay que usar las rutas globales.

### 5.2 Diferencias V2 respecto a V1 que afectan a la migración

| Tema | V1 | V2 |
|---|---|---|
| Plugins | Clave `plugin`, exporta funciones con hooks | Clave **`plugins`**, objeto `{ id, setup }` (normalmente envuelto en `Plugin.define`) |
| Agentes | Clave `agent`, campos `tools`, `permission`, `prompt`, `temperature` | Clave **`agents`**, `permissions` como **array ordenado de reglas** `{action, resource, effect}`, `system`, `steps` |
| Comandos | Clave `command`, `subtask` | Clave **`commands`**, **`subagent`** (`subtask` queda como alias obsoleto) |
| MCP | `mcp.<nombre>` con `enabled` | **`mcp.servers.<nombre>`** con `disabled` |
| Compatibilidad | — | **Los plugins de V1 no funcionan en V2** (tampoco las capas comunitarias de compatibilidad con Claude Code hechas para V1) |

### 5.3 La API de plugins de V2 está en movimiento

Al revisar los paquetes publicados de `@opencode-ai/plugin` se ven diferencias con la documentación:

| Aspecto | Documentación V2 | Paquetes publicados (beta / dev) |
|---|---|---|
| Importación | `@opencode-ai/plugin/v2` | Varía: entrada principal o `/v2/promise` según la versión |
| Hook de contexto de sesión | `ctx.session.hook("request")` | `ctx.session.hook("context")` |
| Hook al enviar el usuario un mensaje | — | `ctx.session.hook("prompt")` |
| Hooks de herramientas | `ctx.tool.hook("execute.before" / "execute.after")` | Igual |

Dos consecuencias prácticas:

1. `Plugin.define` es una función identidad: un plugin puede exportar directamente `export default { id, setup }` **sin importar nada**, lo que evita depender de la versión del paquete.
2. Conviene registrar los hooks de sesión de forma defensiva (probar ambos nombres). El adaptador del apéndice B ya lo hace.

### 5.4 Nombres de herramientas (para traducir agentes, permisos y hooks)

| Claude Code | OpenCode V2 (acción de permiso) |
|---|---|
| `Bash` | `shell` |
| `Edit`, `Write`, `MultiEdit`, `NotebookEdit` | `edit` |
| `Read` | `read` |
| `Grep` | `grep` |
| `Glob` | `glob` |
| `WebFetch` | `webfetch` |
| `WebSearch` | `websearch` |
| `Task` / `Agent` (lanzar subagentes) | `subagent` |
| `Skill` | `skill` |
| Herramienta MCP `mcp__servidor__tool` | `servidor_tool` |

Agentes integrados de V2: **build** y **plan** (primarios), **general** y **explore** (subagentes).

### 5.5 El sistema de plugins de OpenCode

Un plugin de OpenCode es un **módulo JavaScript o TypeScript que se ejecuta dentro del propio proceso de OpenCode**. No es un paquete de ficheros de configuración como en Claude Code, sino código con acceso a la configuración y al ciclo de vida de las sesiones. Un plugin puede:

- **Transformar** la configuración: agentes, catálogo de modelos, comandos, integraciones, referencias, skills y herramientas (añadir, cambiar o quitar).
- **Interceptar** operaciones en vivo: peticiones al modelo y ejecución de herramientas.
- **Llamar** a parte del cliente de OpenCode: crear sesiones, enviar mensajes, lanzar comandos, suscribirse a eventos.

Es, por tanto, bastante más potente que un plugin de Claude Code, pero también más frágil: depende de una API que en V2 todavía es beta.

### 5.6 Cómo se cargan

**Desde la configuración** (`opencode.jsonc`), con una lista ordenada en `plugins`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    "opencode-acme-plugin@1.2.0",          // paquete npm con versión
    "@acme/opencode-plugin",               // paquete con ámbito
    "./plugins/local.ts",                  // ruta local (relativa al fichero de config)
    { "package": "./plugins/reviewer.ts",  // forma objeto: pasa opciones
      "options": { "agent": "reviewer", "strict": true } }
  ]
}
```

- Las opciones llegan sin tocar al plugin como `ctx.options`; el plugin es quien las valida.
- Las entradas de todos los ficheros de configuración se acumulan (de menor a mayor precedencia), no se sustituyen.

**Por descubrimiento local**, sin tocar la configuración:

- `.opencode/plugins/` (proyecto) y `~/.config/opencode/plugins/` (global).
- Se cargan los `.ts` y `.js` que estén directamente ahí, y las subcarpetas que sean un paquete (con `exports`, `module`, `main` o un `index.ts`/`index.js`).
- Una carpeta `plugins/` junto al `opencode.json` de la raíz **no** se descubre: hay que moverla a `.opencode/` o declararla en `plugins`.

**Activar y desactivar** por el `id` del plugin:

```jsonc
{ "plugins": ["./plugins/reviewer.ts", "-acme.reviewer", "-opencode.provider.*", "opencode.provider.openai"] }
```

`-id` desactiva, `*` equivale a todos y `prefijo.*` a un grupo. Las directivas se aplican en orden, así que una entrada posterior puede reactivar lo que otra desactivó (incluidos plugins internos de OpenCode).

**Dependencias:**

- Los paquetes npm se instalan solos en una caché aislada, **sin ejecutar scripts de instalación**.
- Los ficheros locales **no** instalan dependencias: hay que hacerlo a mano en un `package.json` visible desde el plugin (por ejemplo `cd .opencode && bun add <paquete>`).
- Los cambios en ficheros vigilados recargan el plugin en caliente; si cambias la versión de un paquete npm, reinicia OpenCode.

### 5.7 Anatomía de un plugin V2

```ts
// .opencode/plugins/reviewer.ts
import { Plugin } from "@opencode-ai/plugin/v2"   // ver aviso de la sección 5.3

export default Plugin.define({
  id: "acme.reviewer",                 // identificador único
  setup: async (ctx) => {              // se ejecuta cada vez que el plugin se activa
    await ctx.agent.transform((agents) => {
      agents.update("reviewer", (agent) => {
        agent.description = String(ctx.options.description ?? "Revisa regresiones")
        agent.mode = "subagent"
      })
    })
    const timer = setInterval(() => {}, 60_000)
    return () => clearInterval(timer)  // limpieza opcional al desactivar/recargar/cerrar
  },
})
```

- El módulo exporta **por defecto** un objeto con `id` y `setup`.
- En `setup` se registra todo lo que el plugin hace; no se debe quedar esperando indefinidamente.
- Los hooks registrados se liberan solos al recargar; la función de limpieza es para recursos propios (temporizadores, conexiones, procesos).
- Hay una variante con la librería **Effect** (`effect` en lugar de `setup`) para quien trabaje con ese ecosistema.

### 5.8 El contexto (`ctx`)

| Capacidad | Para qué sirve |
|---|---|
| `ctx.agent` | Listar y transformar agentes |
| `ctx.catalog` | Proveedores y modelos; cambiar el modelo por defecto |
| `ctx.command` | Listar y transformar comandos |
| `ctx.skill` | Listar skills y añadir fuentes |
| `ctx.reference` | Añadir o quitar referencias (documentación de contexto) |
| `ctx.integration` | Integraciones y sus conexiones |
| `ctx.tool` | Añadir herramientas e interceptar su ejecución |
| `ctx.session` | Crear sesiones, enviar mensajes, lanzar comandos, interrumpir; hooks de sesión |
| `ctx.aisdk` | Interceptar el SDK y el modelo de lenguaje que se usan |
| `ctx.event` | Suscribirse al flujo de eventos del servidor |
| `ctx.plugin` | Ver qué plugins están activos |
| `ctx.options` | Opciones pasadas desde la configuración (solo lectura) |

Los paquetes beta publicados exponen además `mcp`, `permission`, `shell`, `storage`, `vcs`, `websearch`, `worktree` y `location` (directorio de trabajo), aún sin documentar.

### 5.9 Tipos de hooks

**Hooks de transformación** — cambian cómo está configurado OpenCode. Se pueden volver a aplicar con `reload()` sin reiniciar (por ejemplo, para refrescar una lista de modelos remota):

| Transformación | Operaciones |
|---|---|
| `agent.transform` | `list`, `get`, `default`, `update`, `remove` |
| `catalog.transform` | Proveedores y modelos: `list`, `get`, `update`, `remove`; modelo por defecto: `get`, `set` |
| `command.transform` | `list`, `get`, `update`, `remove` |
| `integration.transform` | Integraciones y métodos: `list`, `get`, `update`, `remove` |
| `reference.transform` | `add`, `remove`, `list` |
| `skill.transform` | `source`, `list` |
| `tool.transform` | `add` |

**Hooks de ejecución** — interceptan operaciones en vivo y pueden modificar ciertos campos:

| Hook | Qué permite cambiar | Equivalente aproximado en Claude Code |
|---|---|---|
| `tool.hook("execute.before")` | La entrada de la herramienta; lanzar un error la bloquea | `PreToolUse` |
| `tool.hook("execute.after")` | El resultado de la herramienta | `PostToolUse` |
| `session.hook("request")` (docs) / `"context"` (paquetes beta) | Prompt de sistema, mensajes y herramientas antes de llamar al modelo | `SessionStart` / `UserPromptSubmit` con contexto |
| `session.hook("prompt")` (paquetes beta) | El mensaje del usuario | `UserPromptSubmit` |
| `session.hook("model.request" / "http.request" / "http.response" / "retry")` (paquetes beta) | Cabeceras, petición HTTP, respuesta, reintentos | — |
| `aisdk.hook("sdk" / "language")` | El SDK o el modelo de lenguaje | — |

Los hooks se ejecutan en orden de registro y cada uno ve los cambios del anterior. **Si un hook falla, falla la operación que intercepta**, así que deben ser rápidos y capturar sus propios errores.

### 5.10 Ejemplos típicos

**Añadir una herramienta:**

```js
export default {
  id: "acme.greeting",
  setup: async (ctx) => {
    await ctx.tool.transform((tools) => {
      tools.add({
        name: "greeting",
        description: "Crea un saludo",
        jsonSchema: { type: "object", properties: { name: { type: "string" } }, required: ["name"] },
        execute: async ({ name }) => ({ content: [{ type: "text", text: `¡Hola, ${name}!` }] }),
      })
    })
  },
}
```

**Añadir un comando:**

```js
export default {
  id: "acme.review-command",
  setup: async (ctx) => {
    await ctx.command.transform((commands) => {
      commands.update("review", (c) => {
        c.description = "Revisa los cambios actuales"
        c.template = "Revisa los cambios actuales buscando errores y tests que falten."
      })
    })
  },
}
```

**Fijar el modelo por defecto:**

```js
export default {
  id: "acme.default-model",
  setup: async (ctx) => {
    await ctx.catalog.transform((catalog) => catalog.model.default.set("anthropic", "claude-sonnet-4-5"))
  },
}
```

> Estos ejemplos exportan el objeto directamente en lugar de usar `Plugin.define`: es equivalente y evita depender de la ruta de importación del paquete, que cambia entre versiones (sección 5.3). En los paquetes beta, la declaración de una herramienta usa `input` para el esquema en lugar de `jsonSchema`: comprueba los tipos de tu versión.

### 5.11 Publicar y comprobar un plugin

- Un plugin publicado en npm usa la misma exportación por defecto. Manifiesto mínimo: `"type": "module"`, `"exports"` apuntando al fichero del plugin y `@opencode-ai/plugin` en `dependencies`, con una versión compatible con tu OpenCode.
- Para ver qué plugins están activos: `opencode api get /api/plugin` (en algunas instalaciones el binario se llama `opencode2`).
- Si un plugin no aparece, el registro del servidor indica el error; un plugin que falla no impide cargar los demás.

### 5.12 Plugins de V1 (para comparar)

En V1 un plugin era una función que devolvía un objeto de hooks con nombres como `tool.execute.before`, `shell.env` o `experimental.session.compacting`, y podía añadir herramientas con `tool()`. Se declaraban en la clave `plugin` y los paquetes npm se instalaban con Bun al arrancar. **No son compatibles con V2**: hay que reescribirlos con `{ id, setup }`.

### 5.13 Plugins de Claude Code frente a plugins de OpenCode

| Aspecto | Claude Code | OpenCode V2 |
|---|---|---|
| Qué es | Paquete de ficheros (Markdown, JSON, scripts) | Módulo JS/TS que se ejecuta dentro de OpenCode |
| Contenido | Skills, comandos, agentes, hooks, MCP, LSP… | Código que registra transformaciones y hooks |
| Hooks | Scripts externos por evento, con JSON por stdin y *exit codes* | Funciones JS dentro del proceso |
| Instalación | Marketplaces (`/plugin install`) | npm o ficheros en `plugins/` |
| Espacio de nombres | `plugin:componente` automático | Ninguno; `id` único por plugin |
| Estabilidad | Formato estable y documentado | API beta en V2 |
| Riesgo | Scripts y MCP arbitrarios | Código arbitrario con acceso a todo OpenCode |

En la práctica, al volcar un plugin de Claude Code **solo los hooks acaban convertidos en un plugin de OpenCode**. Skills, comandos, agentes y MCP tienen su propio sitio en la configuración y no necesitan código.

---

## 6. Matriz de compatibilidad por componente

| Componente Claude Code | Equivalente OpenCode V2 | Esfuerzo | Notas |
|---|---|---|---|
| **Skill** (`SKILL.md`) | Skill nativa | 🟢 Ninguno | OpenCode lee `.claude/skills/` tal cual. V2 interpreta `name`, `description`, `slash` y `metadata.opencode/*`. Sin `description` la skill no se anuncia al modelo |
| **Command** | Command nativo | 🟡 Ligero | `$ARGUMENTS`, `$1…` y `` !`cmd` `` funcionan igual. Cambian `@fichero`, `allowed-tools`, `argument-hint`, argumentos con nombre y `model` |
| **Agent** | Agent con `mode: subagent` | 🟡 Ligero | `tools` → reglas `permissions`; alias de modelo → eliminar o ID completo; `maxTurns` → `steps` |
| **Comando que orquesta agentes** | Command + herramienta `subagent` | 🟡 Medio | Revisar menciones a *Task* y a nombres con prefijo de plugin |
| **Hook `PreToolUse`** | Plugin V2: `ctx.tool.hook("execute.before")` | 🔴 Adaptador | Lanzar un error bloquea la herramienta |
| **Hook `PostToolUse`** | Plugin V2: `ctx.tool.hook("execute.after")` | 🔴 Adaptador | Se puede añadir texto al resultado que verá el modelo |
| **Hook `UserPromptSubmit`** | Plugin V2: `ctx.session.hook("prompt")` | 🔴 Adaptador | Puede bloquear o añadir contexto al mensaje |
| **Hook `SessionStart`** | Plugin V2: hook de contexto de sesión | 🔴 Adaptador | Inyectar texto en `system` |
| **Hooks `Stop`, `SubagentStop`, `PreCompact`, `Notification`, `PermissionRequest`…** | — | 🔴 Reescritura | Sin equivalente directo; valorar caso a caso |
| **Hooks de tipo `prompt`, `agent`, `http`** | — | 🔴 Reescritura | Solo los de tipo `command` se adaptan |
| **MCP** (`.mcp.json`) | `mcp.servers` | 🟢 Ligero | Cambia el formato (ver receta 9.4) |
| **LSP** | LSP integrado | ⚪ Innecesario | OpenCode detecta y arranca servidores LSP |
| **Output style** | Agente primario con su prompt, o hook `SessionStart` adaptado | 🟡 Ligero | |
| **Monitor** | Plugin V2 con tarea en segundo plano | 🔴 Reescritura | |
| **`CLAUDE.md`** | `AGENTS.md` | 🟢 | OpenCode también lee `CLAUDE.md` |

---

## 7. Cómo evaluar un plugin antes de volcarlo

### 7.1 Lista de comprobación

| # | Pregunta | Cómo comprobarlo | Si la respuesta es mala |
|---|---|---|---|
| 1 | ¿La licencia permite usarlo fuera de Claude? | `LICENSE`, campo `license` del manifiesto o del `SKILL.md` | Si es propietaria o lo prohíbe, **no se vuelca** |
| 2 | ¿Qué componentes tiene? | Listar carpetas y claves de `plugin.json` | Cada componente tiene su receta (sección 9) |
| 3 | ¿Depende de herramientas exclusivas de Claude? | Buscar menciones a artefactos, `present_files`, `SendUserFile`, *Workflow*, memoria, extensiones de Claude, `claude -p` | Si son el núcleo del plugin, no compensa |
| 4 | ¿Qué hooks usa y de qué tipo? | `hooks/hooks.json` | Solo `PreToolUse`, `PostToolUse`, `UserPromptSubmit` y `SessionStart` de tipo `command` se adaptan |
| 5 | ¿Qué necesita el sistema? | Comandos de hooks y MCP: `bash`, `python3`, `node`, `bun`, `uvx`, `docker`… | En Windows, `bash`/`sh` exigen Git Bash |
| 6 | ¿Qué ejecuta y a dónde se conecta? | Leer scripts y URLs de MCP | Si no te fías, no lo vuelques |

### 7.2 Clasificación rápida

| Si el plugin tiene… | Resultado esperado |
|---|---|
| Solo skills y/o MCP | 🟢 Funciona casi igual |
| Commands y agents | 🟡 Funciona tras convertir el frontmatter |
| Hooks soportados por el adaptador | 🟡 Funciona con el adaptador (API beta) |
| Hooks `Stop`/`PreCompact`, de tipo `prompt`/`agent`/`http`, o módulos propios | 🔴 Funcionalidad parcial: el resto del plugin sí se puede volcar |
| Dependencia fuerte de herramientas exclusivas de Claude | ⚪ No compensa |

---

## 8. Procedimiento general de volcado

```text
1. Obtener  →  2. Evaluar  →  3. Convertir  →  4. Instalar  →  5. Configurar  →  6. Verificar
```

1. **Obtener el plugin.** Clona el repositorio del marketplace o del plugin (`git clone …`). Si lo tienes instalado en Claude Code, sus ficheros también están en la caché de plugins dentro de `~/.claude/plugins/`.
2. **Evaluarlo** con la lista de la sección 7.
3. **Convertir** cada componente con las recetas de la sección 9, a mano o con el conversor de la sección 10.
4. **Instalar** en uno de estos destinos:
   - Global: `~/.config/opencode/` → disponible en todos los proyectos.
   - Proyecto: `<proyecto>/.opencode/` → solo en ese proyecto (y se puede versionar con git).
5. **Configurar** lo que no se instala copiando ficheros: servidores MCP, permisos, variables de entorno que antes pedía `userConfig`.
6. **Verificar** con las pruebas de la sección 11.

Estructura final en el destino:

```text
~/.config/opencode/                (o <proyecto>/.opencode/)
├── skills/<skill>/SKILL.md
├── commands/<plugin>/<comando>.md   → /<plugin>/<comando>
├── agents/<agente>.md
├── plugins/claude-hooks-<plugin>.js  (solo si había hooks)
├── claude-plugins/<plugin>/          copia del original: scripts, datos, informe
└── opencode.jsonc                    MCP y permisos
```

La carpeta `claude-plugins/` no la lee OpenCode: solo sirve para que los scripts referenciados por `${CLAUDE_PLUGIN_ROOT}` tengan una ruta fija.

---

## 9. Recetas de conversión por componente

### 9.1 Skills

1. Copia la carpeta completa (con `SKILL.md` y sus ficheros) a `skills/<nombre>/`.
2. Sustituye `${CLAUDE_SKILL_DIR}` y `${CLAUDE_PLUGIN_ROOT}` por rutas reales.
3. Ajusta el frontmatter si hace falta:

| Claude Code | OpenCode V2 |
|---|---|
| `user-invocable: false` | `slash: false` |
| `disable-model-invocation: true` | `metadata:` → `opencode/autoinvoke: "false"` |
| `allowed-tools`, `disallowed-tools` | Sin efecto; usar permisos del agente |

4. Si el texto habla de herramientas de Claude (*Bash tool*, *Read tool*, panel *Preview*…), añade una nota de traducción al principio o en un fichero aparte que el `SKILL.md` mencione.

### 9.2 Commands

```markdown
<!-- Claude Code: commands/check.md -->
---
description: Revisa un sistema
argument-hint: <system>
arguments: system
allowed-tools: Bash(git status:*)
model: sonnet
---
Revisa legacy/$system. Contexto: !`git status`. Lee @docs/guia.md
Después ejecuta /mi-plugin:informe
```

```markdown
<!-- OpenCode V2: commands/mi-plugin/check.md  →  /mi-plugin/check -->
---
description: "Revisa un sistema"
---
Revisa legacy/$1. Contexto: !`git status`. Lee !`cat docs/guia.md`
Después ejecuta /mi-plugin/informe
```

Reglas:

- Conserva `description`. Mantén `model` solo si tiene formato `proveedor/modelo`.
- Elimina `allowed-tools`, `argument-hint`, `disable-model-invocation`, `hide-from-slash-command-tool`.
- Argumentos con nombre → `$1`, `$2`… (en OpenCode el último posicional recoge el resto del texto).
- `@fichero` → `` !`cat fichero` `` (o `type` en Windows) o pedir al usuario que adjunte el fichero. Los bloques `` !`…` `` se ejecutan sin pasar por los permisos: úsalos solo con comandos de confianza.
- `/plugin:comando` → `/plugin/comando`; `plugin:agente` → `agente`.
- Opcional: `agent: <id>` para ejecutarlo con un agente concreto y `subagent: true` para que corra en segundo plano.

### 9.3 Agents

```markdown
<!-- Claude Code: agents/code-explorer.md -->
---
name: code-explorer
description: Analiza el código existente…
tools: Glob, Grep, LS, Read, WebFetch, WebSearch
model: sonnet
color: yellow
maxTurns: 40
---
(prompt)
```

```markdown
<!-- OpenCode V2: agents/code-explorer.md -->
---
description: "Analiza el código existente…"
mode: "subagent"
color: "warning"
steps: 40
permissions:
  - action: "edit"
    resource: "*"
    effect: "deny"
  - action: "shell"
    resource: "*"
    effect: "deny"
  - action: "subagent"
    resource: "*"
    effect: "deny"
---
(mismo prompt)
```

Reglas:

- El ID del agente sale del nombre del fichero; `name` sobra.
- `tools` (lista blanca en Claude) → reglas `deny` para las acciones que **no** estén en la lista (`edit`, `shell`, `webfetch`, `websearch`, `subagent`).
- `model: sonnet/opus/haiku/inherit` → eliminar (hereda el modelo de la sesión) o poner `proveedor/modelo`.
- `color`: nombres → valores de V2 (`success`, `warning`, `error`, `info`, `accent`, `secondary`) o un hex.
- `maxTurns` → `steps`. Campos sin equivalente: `effort`, `initialPrompt`, `permissionMode`, `hooks`, `mcpServers`, `skills`.
- Si dos plugins traen agentes con el mismo nombre, el segundo reemplaza al primero: renombra uno.

### 9.4 Servidores MCP

| Claude Code (`.mcp.json`) | OpenCode V2 (`opencode.jsonc`) |
|---|---|
| Raíz `mcpServers` o servidores directamente en la raíz | `mcp.servers` |
| `command` + `args` | `"type": "local"`, `command` como **un solo array** |
| `env` | `environment` |
| `"type": "http"` + `url` | `"type": "remote"` + `url` |
| `"type": "sse"` | No soportado: V2 solo usa Streamable HTTP |
| `headers` | `headers` |
| `${VARIABLE}` | `{env:VARIABLE}` |
| `${CLAUDE_PLUGIN_ROOT}` | Ruta real |

```jsonc
// Claude Code
{ "mcpServers": {
    "terraform": { "command": "docker", "args": ["run", "-i", "--rm", "-e", "TFE_TOKEN=${TFE_TOKEN}", "hashicorp/terraform-mcp-server:0.4.0"] },
    "linear": { "type": "http", "url": "https://mcp.linear.app/mcp" }
} }

// OpenCode V2
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": { "servers": {
    "terraform": { "type": "local", "command": ["docker", "run", "-i", "--rm", "-e", "TFE_TOKEN={env:TFE_TOKEN}", "hashicorp/terraform-mcp-server:0.4.0"] },
    "linear": { "type": "remote", "url": "https://mcp.linear.app/mcp" }
  } }
}
```

Alternativa por línea de comandos (añade `--global` para todos los proyectos):

```bash
opencode mcp add linear --url https://mcp.linear.app/mcp
opencode mcp add terraform -- docker run -i --rm -e TFE_TOKEN={env:TFE_TOKEN} hashicorp/terraform-mcp-server:0.4.0
opencode mcp auth linear      # si el servidor usa OAuth
```

### 9.5 Hooks

Hay dos caminos:

**A. Adaptador genérico (recomendado para empezar).** Un plugin de OpenCode que ejecuta los **scripts originales** del hook con el mismo protocolo que Claude Code: JSON por la entrada estándar, *exit code* 2 para bloquear, y respuesta JSON (`decision`, `hookSpecificOutput.permissionDecision`, `hookSpecificOutput.additionalContext`). Así no hay que reescribir la lógica. El código completo está en el **apéndice B** y el conversor lo genera para cada plugin.

| Evento Claude Code | Cómo lo traduce el adaptador |
|---|---|
| `PreToolUse` | `tool.hook("execute.before")`; si el script bloquea, lanza un error y la herramienta no se ejecuta |
| `PostToolUse` | `tool.hook("execute.after")`; el contexto o motivo devuelto se añade al resultado de la herramienta |
| `UserPromptSubmit` | `session.hook("prompt")`; puede bloquear el mensaje o añadirle contexto |
| `SessionStart` | Hook de contexto de sesión; el texto se inyecta en el prompt de sistema una vez por sesión |
| `matcher` y campo `if` | Se respetan, traduciendo los nombres de herramienta de OpenCode a los de Claude |
| `async` / `asyncRewake` | Se lanza en segundo plano sin esperar resultado |
| Resto de eventos | Se ignoran y se informa de ellos |

Limitaciones: la API de plugins de V2 es beta; en Windows los hooks que empiezan por `bash` o `sh` necesitan Git Bash; los hooks de tipo `prompt`, `agent` o `http` no se adaptan.

**B. Reescritura nativa.** Para hooks no soportados o cuando se quiere rendimiento, se reescribe la lógica como plugin V2:

```ts
// .opencode/plugins/guard.ts — equivalente nativo de un PreToolUse que bloquea
export default {
  id: "local.guard",
  setup: async (ctx) => {
    await ctx.tool.hook("execute.before", (event) => {
      const cmd = String((event.input as any)?.command ?? "")
      if (cmd.includes("rm -rf")) throw new Error("Comando bloqueado")
    })
  },
}
```

### 9.6 Output styles

- **Sin código:** crea un agente primario (`mode: primary`) cuyo cuerpo sea el texto del estilo. Se selecciona con Tab en OpenCode.
- **Con el adaptador:** muchos estilos se implementan como hook `SessionStart` que devuelve `additionalContext`; el adaptador los inyecta tal cual.

### 9.7 LSP, monitores y `userConfig`

- **LSP:** OpenCode trae LSP integrado; normalmente basta con tener instalado el servidor del lenguaje.
- **Monitores:** reescribir como plugin V2 con una tarea en segundo plano iniciada en `setup` (y devolver una función de limpieza).
- **`userConfig`:** fija los valores a mano. Si el plugin los usaba como variables de entorno, defínelas en tu sistema o en `environment` del servidor MCP.

---

## 10. Conversión automática

El **apéndice A** contiene `claude2opencode.py`, un conversor que aplica todas las recetas anteriores. Solo necesita Python 3.8 o superior (sin dependencias).

### 10.1 Uso

1. Copia el código del apéndice A en `claude2opencode.py` y el del apéndice B en `hooks-adapter.template.js`, **en la misma carpeta**.
2. Ejecuta:

```bash
# Global (todos los proyectos)
python claude2opencode.py ruta/al/plugin

# Solo un proyecto
python claude2opencode.py ruta/al/plugin --dest ruta/al/proyecto/.opencode
```

3. Lee el informe que imprime (también se guarda en `claude-plugins/<plugin>/CONVERSION.md`). Tiene tres apartados: lo convertido, los avisos y lo que queda **pendiente a mano** (por ejemplo, registrar los servidores MCP con los comandos `opencode mcp add` que propone).

Para volcar un marketplace entero, basta con un bucle:

```bash
git clone --depth 1 https://github.com/anthropics/claude-plugins-official
for p in claude-plugins-official/plugins/*; do python claude2opencode.py "$p"; done
```

### 10.2 Qué hace

| Componente | Acción |
|---|---|
| Skills | Copia, sustituye variables, ajusta `slash`/`autoinvoke`, avisa de lo que no tiene efecto |
| Commands | Convierte frontmatter, argumentos con nombre, prefijos `/plugin:`; avisa de `@fichero` y de menciones a *Task* |
| Agents | Convierte `tools` en reglas `deny`, modelo, color, `maxTurns`; avisa de colisiones |
| MCP | Genera `mcp.jsonc` y los comandos `opencode mcp add` equivalentes |
| Hooks | Genera `plugins/claude-hooks-<plugin>.js` con el adaptador; informa de eventos no soportados |
| LSP, monitores, `userConfig`, módulos propios | Los lista como pendientes |

### 10.3 Hasta dónde se ha probado

- El conversor se ha ejecutado sobre **las 54 carpetas de plugins del marketplace oficial** sin errores, con y sin PyYAML instalado (mismo resultado). Todo el frontmatter generado es YAML válido y no queda ningún `${CLAUDE_PLUGIN_ROOT}` sin sustituir en los `.md` ni en los adaptadores; los scripts y ejemplos que traen las skills se copian sin tocar.
- El adaptador de hooks se ha probado con un **contexto simulado** de OpenCode: bloqueo con *exit code* 2, `matcher`, campo `if`, contexto añadido tras editar, `UserPromptSubmit` y `SessionStart` (incluido el hook real de `explanatory-output-style`).
- **No se ha probado dentro de una instalación real de OpenCode 2.0.** Por eso conviene seguir la verificación de la sección 11 después del primer volcado.
- No convierte plugins de LSP declarados solo en `marketplace.json`, ni hooks `Stop`/`PreCompact`/etc.

---

## 11. Verificación y problemas habituales

### 11.1 Pruebas tras volcar un plugin

| Prueba | Resultado esperado |
|---|---|
| Escribir `/` en el cuadro de mensaje | Aparecen los comandos `/<plugin>/…` y las skills |
| Escribir `@` | Aparecen los subagentes convertidos |
| `opencode mcp list` | Los servidores MCP aparecen como `connected` (o piden autenticación) |
| Pedir una tarea que encaje con una skill | El agente la carga por su cuenta |
| Con hooks: abrir OpenCode con `CLAUDE_HOOKS_DEBUG=1` | El registro muestra `hook registrado: …` y la salida de cada script |
| Con hooks: provocar el caso que el hook debe bloquear | La herramienta falla con el mensaje del hook |

### 11.2 Problemas habituales

| Síntoma | Causa probable | Solución |
|---|---|---|
| No aparece una skill | Ruta incorrecta, `SKILL.md` con otro nombre o sin `description` | `…/skills/<nombre>/SKILL.md`, en mayúsculas, con `description` |
| No aparecen los ficheros de proyecto | OpenCode no tiene la carpeta del proyecto abierta | Abrir la carpeta o instalar en global |
| Skill o agente duplicado | La misma pieza en `~/.claude/` y en `~/.config/opencode/` | Dejar solo una copia |
| Pide permiso al leer ficheros de una skill global | Están fuera del proyecto | Reglas `external_directory` y `read` para `~/.config/opencode/*` en `agents.build.permissions` |
| Un comando no encuentra un fichero | Usaba `@fichero` | Receta 9.2 |
| Un hook no hace nada | Evento no soportado, API distinta o falta `bash`/`python3` | Activar `CLAUDE_HOOKS_DEBUG=1` y revisar el registro |
| Error al cargar un plugin JS/TS | Importa un paquete o una ruta que tu versión no tiene | Exportar `{ id, setup }` sin importar `@opencode-ai/plugin` |
| Un MCP no conecta | Transporte SSE o variable de entorno sin definir | Buscar URL Streamable HTTP; definir la variable |

---

## 12. Fuentes

**Claude Code**
- [Claude Code — Create plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code — Plugins reference](https://code.claude.com/docs/en/plugins-reference)
- [anthropics/claude-plugins-official (GitHub)](https://github.com/anthropics/claude-plugins-official)
- [Plugins oficiales en el repo de Claude Code](https://upd.dev/anthropics/claude-code/src/branch/main/plugins)
- [Claude Code plugins development guide — fast.io](https://fast.io/resources/claude-code-plugins-development-guide.md)

**OpenCode V2**
- [OpenCode V2 — Plugins](https://v2.opencode.ai/build/plugins.md)
- [OpenCode V2 — Agents](https://v2.opencode.ai/agents.md)
- [OpenCode V2 — Skills](https://v2.opencode.ai/skills)
- [OpenCode V2 — Commands](https://opencode.ai/v2/docs/commands/)
- [OpenCode V2 — MCP servers](https://opencode.ai/v2/docs/mcp-servers/)
- [OpenCode V2 — Permissions](https://v2.opencode.ai/permissions.md)
- [OpenCode 2.0 Beta: one backend, three interfaces — byteiota](https://byteiota.com/opencode-2-beta-unified-ai-coding-agent/)
- Paquete npm `@opencode-ai/plugin` (versiones `beta` y `dev`, revisadas en octubre de 2026)

**OpenCode V1 y compatibilidad**
- [OpenCode V1 — Agent Skills](https://opencode.ai/docs/skills)
- [OpenCode V1 — Plugins](https://opencode.ai/docs/plugins.md)
- [Skills y comandos de Claude Code en OpenCode — Hora de Codar](https://horadecodar.com.br/skills-claude-code-opencode/)

---

## Apéndice A — `claude2opencode.py`

Guárdalo como `claude2opencode.py` en la misma carpeta que el apéndice B.

```python
#!/usr/bin/env python3
"""claude2opencode.py - Vuelca un plugin de Claude Code a OpenCode V2.

Uso:
    python claude2opencode.py <carpeta-del-plugin> [--dest DESTINO]

DESTINO por defecto: ~/.config/opencode (instalacion global).
Para un solo proyecto: --dest <proyecto>/.opencode

Genera, dentro de DESTINO:
    skills/<skill>/                    skills (casi sin cambios)
    commands/<plugin>/<comando>.md     comandos  -> /<plugin>/<comando>
    agents/<agente>.md                 subagentes
    plugins/claude-hooks-<plugin>.js   adaptador de hooks (si el plugin tiene hooks)
    claude-plugins/<plugin>/           copia del plugin original (scripts, datos...)
                                       + CONVERSION.md (informe) + mcp.jsonc (si hay MCP)

Solo usa la biblioteca estandar de Python 3.8+. Si PyYAML esta instalado, lo usa.
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "hooks-adapter.template.js"

# Herramienta de Claude Code -> accion de permiso de OpenCode V2 que se puede denegar
ACTIONS = {
    "edit": {"Edit", "Write", "MultiEdit", "NotebookEdit"},
    "shell": {"Bash"},
    "webfetch": {"WebFetch"},
    "websearch": {"WebSearch"},
    "subagent": {"Task", "Agent"},
}
MODEL_ALIASES = {"inherit", "sonnet", "opus", "haiku", "default"}
COLORS = {
    "red": "error", "green": "success", "yellow": "warning", "orange": "warning",
    "blue": "info", "cyan": "info", "purple": "accent", "pink": "accent",
    "magenta": "accent", "gray": "secondary", "grey": "secondary",
}
SUPPORTED_HOOKS = {"PreToolUse", "PostToolUse", "UserPromptSubmit", "SessionStart"}


# ---------------------------------------------------------------- frontmatter
def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] == '"':
        try:
            return json.loads(v)
        except ValueError:
            return v[1:-1]
    if len(v) >= 2 and v[0] == v[-1] == "'":
        return v[1:-1].replace("''", "'")
    return v


def mini_yaml(raw):
    """Parser minimo para el frontmatter habitual (claves planas, listas, bloques | y >)."""
    data, lines, i = {}, raw.splitlines(), 0
    while i < len(lines):
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", lines[i])
        i += 1
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val[:1] in ("|", ">") and val.rstrip("+-") in ("|", ">"):
            block = []
            while i < len(lines) and (lines[i][:1] in (" ", "\t") or not lines[i].strip()):
                block.append(lines[i])
                i += 1
            ind = min((len(b) - len(b.lstrip()) for b in block if b.strip()), default=0)
            data[key] = ("\n" if val[0] == "|" else " ").join(b[ind:] for b in block).strip()
        elif val == "":
            items = []
            while i < len(lines) and re.match(r"^\s+-\s", lines[i]):
                items.append(unquote(lines[i].strip()[2:]))
                i += 1
            data[key] = items
        elif val.startswith("[") and val.endswith("]"):
            data[key] = [unquote(x) for x in val[1:-1].split(",") if x.strip()]
        else:
            while i < len(lines) and lines[i][:1] in (" ", "\t") and lines[i].strip():
                val += " " + lines[i].strip()
                i += 1
            data[key] = unquote(val)
    return data


def split_fm(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---[ \t]*\r?\n?(.*)$", text, re.S)
    if not m:
        return None, {}, text
    raw, body = m.groups()
    try:
        import yaml  # opcional

        data = yaml.safe_load(raw)
        if isinstance(data, dict):
            return raw, data, body
    except Exception:
        pass
    return raw, mini_yaml(raw), body


def dump_fm(d):
    out = ["---"]
    for k, v in d.items():
        if isinstance(v, list):
            out.append(f"{k}:")
            for it in v:
                if isinstance(it, dict):
                    for n, (kk, vv) in enumerate(it.items()):
                        out.append(f"  {'- ' if n == 0 else '  '}{kk}: {json.dumps(vv, ensure_ascii=False)}")
                else:
                    out.append(f"  - {json.dumps(it, ensure_ascii=False)}")
        else:
            out.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    out.append("---")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- conversor
class Converter:
    def __init__(self, src, dest):
        self.src = src.resolve()
        self.dest = dest.expanduser().resolve()
        manifest = self.src / ".claude-plugin" / "plugin.json"
        self.manifest = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else {}
        self.name = self.manifest.get("name") or self.src.name
        self.root = self.dest / "claude-plugins" / self.name
        self.data = self.dest / "claude-plugins" / f"{self.name}-data"
        self.report = {"ok": [], "warn": [], "manual": []}
        self.agent_names, self.skill_names = [], []

    # -- utilidades
    def ok(self, msg):
        self.report["ok"].append(msg)

    def warn(self, msg):
        self.report["warn"].append(msg)

    def manual(self, msg):
        self.report["manual"].append(msg)

    def component_paths(self, key, default):
        """Rutas de un componente: carpeta por defecto + las declaradas en plugin.json."""
        found = []
        if (self.src / default).exists():
            found.append(self.src / default)
        val = self.manifest.get(key)
        for p in ([val] if isinstance(val, str) else val if isinstance(val, list) else []):
            path = (self.src / p).resolve()
            if path.exists() and path not in found:
                found.append(path)
        return found

    def rewrite(self, text, skill_dir=None):
        text = text.replace("${CLAUDE_PLUGIN_ROOT}", self.root.as_posix())
        text = text.replace("${CLAUDE_PLUGIN_DATA}", self.data.as_posix())
        if skill_dir is not None:
            text = text.replace("${CLAUDE_SKILL_DIR}", skill_dir.as_posix())
        n = re.escape(self.name)
        text = re.sub(rf"/{n}:([A-Za-z0-9_.-]+)", rf"/{self.name}/\1", text)  # /plugin:cmd -> /plugin/cmd
        text = re.sub(rf"(?<![\w/]){n}:([A-Za-z0-9_.-]+)", r"\1", text)  # plugin:agente -> agente
        return text

    # -- pasos
    def copy_root(self):
        if self.root.exists():
            shutil.rmtree(self.root)
        shutil.copytree(self.src, self.root, ignore=shutil.ignore_patterns(".git"))
        self.data.mkdir(parents=True, exist_ok=True)

    def skills(self):
        for base in self.component_paths("skills", "skills"):
            dirs = [base] if (base / "SKILL.md").exists() else [d for d in sorted(base.iterdir()) if (d / "SKILL.md").exists()]
            for d in dirs:
                target = self.dest / "skills" / d.name
                if target.exists():
                    self.warn(f"La skill `{d.name}` ya existia en destino y se ha reemplazado")
                    shutil.rmtree(target)
                shutil.copytree(d, target)
                for f in target.rglob("*.md"):
                    f.write_text(self.rewrite(f.read_text(encoding="utf-8"), target), encoding="utf-8")
                self.patch_skill(target / "SKILL.md")
                self.skill_names.append(d.name)
                self.ok(f"Skill `{d.name}` -> `skills/{d.name}/`")

    def patch_skill(self, path):
        text = path.read_text(encoding="utf-8")
        raw, fm, body = split_fm(text)
        if raw is None:
            self.warn(f"`{path.parent.name}/SKILL.md` no tiene frontmatter: OpenCode no la anunciara al modelo")
            return
        extra = []
        if str(fm.get("user-invocable", "")).lower() == "false":
            extra.append("slash: false")
        if str(fm.get("disable-model-invocation", "")).lower() == "true":
            if "metadata" in fm:
                self.warn(f"Skill `{path.parent.name}`: anade a mano `opencode/autoinvoke: \"false\"` en `metadata`")
            else:
                extra.append('metadata:\n  opencode/autoinvoke: "false"')
        if not fm.get("description"):
            self.warn(f"Skill `{path.parent.name}` sin `description`: OpenCode V2 no la anunciara al modelo")
        for k in ("allowed-tools", "disallowed-tools", "tools"):
            if k in fm:
                self.warn(f"Skill `{path.parent.name}`: `{k}` no tiene efecto en OpenCode (usa permisos del agente)")
        if extra:
            path.write_text(f"---\n{raw}\n" + "\n".join(extra) + f"\n---\n{body}", encoding="utf-8")

    def commands(self):
        for base in self.component_paths("commands", "commands"):
            files = [base] if base.is_file() else sorted(base.rglob("*.md"))
            for f in files:
                rel = f.name if base.is_file() else f.relative_to(base).as_posix()
                raw, fm, body = split_fm(f.read_text(encoding="utf-8"))
                out = {}
                if fm.get("description"):
                    out["description"] = str(fm["description"])
                model = str(fm.get("model", "")).strip()
                if model and "/" in model:
                    out["model"] = model
                elif model:
                    self.warn(f"Comando `{rel}`: modelo `{model}` eliminado (usa `proveedor/modelo` si quieres fijarlo)")
                args = fm.get("arguments")
                if args:
                    names = args if isinstance(args, list) else re.split(r"[,\s]+", str(args).strip())
                    for idx, an in enumerate([a for a in names if a], 1):
                        body = re.sub(rf"\${re.escape(str(an))}(?![A-Za-z0-9_])", f"${idx}", body)
                    self.warn(f"Comando `{rel}`: argumentos con nombre {names} pasados a $1, $2... (el ultimo recoge el resto)")
                if "allowed-tools" in fm:
                    self.warn(f"Comando `{rel}`: `allowed-tools` eliminado (en OpenCode lo controlan los permisos del agente)")
                if re.search(r"(?<![\w`'\"/])@[\w${}.-]*[/.][\w${}./-]+", body):
                    self.warn(f"Comando `{rel}`: usa referencias `@fichero`, que OpenCode no expande en plantillas")
                if re.search(r"\bTask tool\b|\bTask\(|subagent_type", body):
                    self.warn(f"Comando `{rel}`: menciona la herramienta Task; en OpenCode es la herramienta `subagent`")
                target = self.dest / "commands" / self.name / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(dump_fm(out) + "\n" + self.rewrite(body).lstrip("\n"), encoding="utf-8")
                self.ok(f"Comando `{rel}` -> `/{self.name}/{rel[:-3]}`")

    def agents(self):
        for base in self.component_paths("agents", "agents"):
            files = [base] if base.is_file() else sorted(base.rglob("*.md"))
            for f in files:
                raw, fm, body = split_fm(f.read_text(encoding="utf-8"))
                name = str(fm.get("name") or f.stem)
                out = {"description": str(fm.get("description", "")).strip(), "mode": "subagent"}
                model = str(fm.get("model", "")).strip()
                if model and "/" in model:
                    out["model"] = model
                elif model and model not in MODEL_ALIASES:
                    self.warn(f"Agente `{name}`: modelo `{model}` eliminado (hereda el de la sesion)")
                color = str(fm.get("color", "")).strip().lower()
                if color:
                    out["color"] = color if color.startswith("#") else COLORS.get(color, "accent")
                if str(fm.get("maxTurns", "")).isdigit():
                    out["steps"] = int(fm["maxTurns"])
                tools = fm.get("tools")
                if tools:
                    listed = tools if isinstance(tools, list) else str(tools).split(",")
                    listed = {re.sub(r"\(.*$", "", str(t)).strip() for t in listed}
                    deny = [a for a, names in ACTIONS.items() if not (listed & names)]
                    if deny:
                        out["permissions"] = [{"action": a, "resource": "*", "effect": "deny"} for a in deny]
                for k in ("effort", "initialPrompt", "permissionMode", "hooks", "mcpServers", "skills", "disallowedTools"):
                    if k in fm:
                        self.warn(f"Agente `{name}`: campo `{k}` sin equivalente, eliminado")
                target = self.dest / "agents" / f"{name}.md"
                if target.exists():
                    self.warn(f"El agente `{name}` ya existia en destino y se ha reemplazado")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(dump_fm(out) + "\n" + self.rewrite(body).lstrip("\n"), encoding="utf-8")
                self.agent_names.append(name)
                self.ok(f"Agente `{name}` -> `agents/{name}.md`" + (f" (deniega: {', '.join(d['action'] for d in out.get('permissions', []))})" if out.get("permissions") else ""))

    def load_json_component(self, key, default_file):
        val = self.manifest.get(key)
        if isinstance(val, dict):
            return val
        path = self.src / (val if isinstance(val, str) else default_file)
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return None

    def mcp(self):
        cfg = self.load_json_component("mcpServers", ".mcp.json")
        if not cfg:
            return
        servers = cfg.get("mcpServers", cfg)
        out, cli = {}, []
        scope = "" if self.dest.name == ".opencode" else " --global"

        def env_ref(s):
            s = self.rewrite(str(s))
            return re.sub(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}", r"{env:\1}", s)

        for sname, s in servers.items():
            kind = s.get("type", "stdio" if "command" in s else "http")
            if kind == "stdio":
                cmd = [env_ref(s["command"])] + [env_ref(a) for a in s.get("args", [])]
                entry = {"type": "local", "command": cmd}
                if s.get("env"):
                    entry["environment"] = {k: env_ref(v) for k, v in s["env"].items()}
                if s.get("cwd"):
                    entry["cwd"] = env_ref(s["cwd"])
                envs = "".join(f" --env '{k}={v}'" for k, v in entry.get("environment", {}).items())
                cli.append(f"opencode mcp add {sname}{scope}{envs} -- " + " ".join(json.dumps(c) if " " in c else c for c in cmd))
            else:
                entry = {"type": "remote", "url": env_ref(s["url"])}
                if s.get("headers"):
                    entry["headers"] = {k: env_ref(v) for k, v in s["headers"].items()}
                if kind == "sse":
                    self.warn(f"MCP `{sname}` usa SSE; OpenCode V2 solo habla Streamable HTTP. Comprueba si el servidor ofrece una URL /mcp")
                hdrs = "".join(f" --header '{k}={v}'" for k, v in entry.get("headers", {}).items())
                cli.append(f"opencode mcp add {sname}{scope} --url '{entry['url']}'{hdrs}")
            out[sname] = entry
        snippet = {"$schema": "https://opencode.ai/config.json", "mcp": {"servers": out}}
        (self.root / "mcp.jsonc").write_text(
            "// Fusiona este bloque en tu opencode.jsonc o usa los comandos `opencode mcp add` de CONVERSION.md\n"
            + json.dumps(snippet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        self.manual(f"Registrar {len(out)} servidor(es) MCP: ver `mcp.jsonc` o los comandos de abajo")
        for c in cli:
            self.manual(f"`{c}`")

    def hooks(self):
        hooks_file = self.load_json_component("hooks", "hooks/hooks.json")
        if not hooks_file:
            return
        hooks = hooks_file.get("hooks", hooks_file)
        for ev in hooks:
            if ev not in SUPPORTED_HOOKS:
                self.manual(f"Hook `{ev}` sin equivalente en el adaptador: revisar a mano o descartar")
        usable = {k: v for k, v in hooks.items() if k in SUPPORTED_HOOKS}
        for groups in usable.values():
            for g in groups:
                for h in g.get("hooks", []):
                    if h.get("type", "command") != "command":
                        self.manual(f"Hook de tipo `{h.get('type')}` no soportado: reescribir a mano")
                    if "command" in h:
                        h["command"] = h["command"].replace("${CLAUDE_PLUGIN_ROOT}", self.root.as_posix())
                        h["command"] = h["command"].replace("${CLAUDE_PLUGIN_DATA}", self.data.as_posix())
                        if re.match(r"\s*(bash|sh)\b", h["command"]):
                            self.warn("Hay hooks que se lanzan con `bash`/`sh`: en Windows necesitan Git Bash en el PATH")
        if "modules" in hooks_file:
            self.manual("El plugin carga modulos propios de Claude Code (`modules`): no se pueden volcar")
        if not usable:
            return
        if not TEMPLATE.exists():
            self.manual(f"Falta `{TEMPLATE.name}` junto al script: no se ha generado el adaptador de hooks")
            return
        js = TEMPLATE.read_text(encoding="utf-8")
        js = js.replace("__PLUGIN_NAME_JSON__", json.dumps(self.name)).replace("__PLUGIN_NAME__", self.name)
        js = js.replace("__PLUGIN_ROOT_JSON__", json.dumps(self.root.as_posix()))
        js = js.replace("__HOOKS_JSON__", json.dumps(usable, indent=2, ensure_ascii=False))
        target = self.dest / "plugins" / f"claude-hooks-{self.name}.js"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(js, encoding="utf-8")
        self.ok(f"Hooks {sorted(usable)} -> `plugins/{target.name}` (adaptador, API beta de V2)")

    def misc(self):
        if self.load_json_component("lspServers", ".lsp.json"):
            self.manual("Servidores LSP: OpenCode trae LSP integrado; normalmente no hace falta nada")
        for key, label in (("outputStyles", "Output styles"), ("monitors", "Monitors")):
            if self.manifest.get(key) or (self.src / key.replace("outputStyles", "output-styles")).exists():
                self.manual(f"{label}: sin equivalente directo (output style -> agente primario con ese prompt)")
        if self.manifest.get("userConfig"):
            keys = ", ".join(self.manifest["userConfig"])
            self.manual(f"`userConfig` ({keys}): los valores que pide Claude Code al instalar no existen en OpenCode")

    def write_report(self):
        lines = [f"# Conversion de `{self.name}` a OpenCode V2", "", f"Origen: `{self.src}`", f"Destino: `{self.dest}`", ""]
        for key, title in (("ok", "Convertido"), ("warn", "Avisos"), ("manual", "Pendiente / a mano")):
            items = list(dict.fromkeys(self.report[key]))
            if items:
                lines += [f"## {title}", ""] + [f"- {i}" for i in items] + [""]
        (self.root / "CONVERSION.md").write_text("\n".join(lines), encoding="utf-8")
        return "\n".join(lines)

    def run(self):
        self.copy_root()
        self.skills()
        self.commands()
        self.agents()
        self.mcp()
        self.hooks()
        self.misc()
        return self.write_report()


def main():
    ap = argparse.ArgumentParser(description="Vuelca un plugin de Claude Code a OpenCode V2")
    ap.add_argument("plugin", type=Path, help="carpeta del plugin (la que contiene .claude-plugin/)")
    ap.add_argument("--dest", type=Path, default=Path.home() / ".config" / "opencode",
                    help="destino: ~/.config/opencode (global, por defecto) o <proyecto>/.opencode")
    args = ap.parse_args()
    if not args.plugin.is_dir():
        sys.exit(f"No existe la carpeta: {args.plugin}")
    print(Converter(args.plugin, args.dest).run())


if __name__ == "__main__":
    main()
```

---

## Apéndice B — `hooks-adapter.template.js`

Guárdalo como `hooks-adapter.template.js` junto a `claude2opencode.py`. El conversor rellena los marcadores `__…__` para cada plugin y lo deja en `plugins/claude-hooks-<plugin>.js`.

```js
// Adaptador de hooks de Claude Code -> OpenCode V2. Generado por claude2opencode.py.
// Plugin de origen: __PLUGIN_NAME__
//
// Ejecuta los scripts de hooks ORIGINALES del plugin con el mismo protocolo que
// Claude Code (JSON por stdin, exit code 2 = bloquear, hookSpecificOutput...).
// Eventos soportados: PreToolUse, PostToolUse, UserPromptSubmit, SessionStart.
// El resto (Stop, PreCompact, Notification...) se ignora.
// Depuración: define la variable de entorno CLAUDE_HOOKS_DEBUG=1 antes de abrir OpenCode.
import { spawn } from "node:child_process"

const PLUGIN = __PLUGIN_NAME_JSON__
const ROOT = __PLUGIN_ROOT_JSON__
const HOOKS = __HOOKS_JSON__
const DEBUG = !!process.env.CLAUDE_HOOKS_DEBUG
const log = (...a) => DEBUG && console.error(`[claude-hooks:${PLUGIN}]`, ...a)

// Nombres de herramienta de OpenCode -> Claude Code (los hooks filtran por estos)
const TOOL_NAMES = {
  bash: "Bash", shell: "Bash", read: "Read", write: "Write", edit: "Edit",
  multiedit: "MultiEdit", patch: "Edit", apply_patch: "Edit", glob: "Glob",
  grep: "Grep", list: "LS", ls: "LS", webfetch: "WebFetch", websearch: "WebSearch",
  task: "Task", subagent: "Task", skill: "Skill", todowrite: "TodoWrite",
  question: "AskUserQuestion",
}
const claudeTool = (name) => TOOL_NAMES[String(name).toLowerCase()] ?? String(name)

// filePath -> file_path, oldString -> old_string... (Claude Code usa snake_case)
const snake = (obj) =>
  obj && typeof obj === "object" && !Array.isArray(obj)
    ? Object.fromEntries(Object.entries(obj).map(([k, v]) => [k.replace(/[A-Z]/g, (c) => "_" + c.toLowerCase()), v]))
    : obj

const globRe = (p) =>
  new RegExp("^" + p.replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*/g, ".*").replace(/\?/g, ".") + "$", "s")

// Campo "if" de Claude Code, p. ej. "Bash(git push *)"
function passesIf(rule, tool, input) {
  if (!rule) return true
  const m = /^([\w-]+)(?:\((.*)\))?$/s.exec(String(rule).trim())
  if (!m) return true
  if (m[1] !== tool) return false
  if (m[2] === undefined) return true
  const target = input?.command ?? input?.file_path ?? input?.path ?? input?.url ?? ""
  return globRe(m[2]).test(String(target))
}

function matches(group, tool) {
  const mt = group.matcher
  if (!mt || mt === "*" || tool === undefined) return true
  try {
    return new RegExp("^(?:" + mt + ")$").test(tool)
  } catch {
    return mt === tool
  }
}

function run(command, payload, timeoutSec) {
  return new Promise((resolve) => {
    let stdout = ""
    let stderr = ""
    const child = spawn(command, {
      shell: true,
      cwd: payload.cwd,
      env: { ...process.env, CLAUDE_PLUGIN_ROOT: ROOT, CLAUDE_PROJECT_DIR: payload.cwd },
    })
    const timer = setTimeout(() => child.kill(), (timeoutSec ?? 60) * 1000)
    child.stdout.on("data", (d) => (stdout += d))
    child.stderr.on("data", (d) => (stderr += d))
    child.on("error", (e) => {
      clearTimeout(timer)
      resolve({ code: -1, stdout, stderr: String(e) })
    })
    child.on("close", (code) => {
      clearTimeout(timer)
      resolve({ code, stdout, stderr })
    })
    child.stdin.on("error", () => {})
    child.stdin.end(JSON.stringify(payload))
  })
}

// Ejecuta los hooks de un evento. Devuelve { block, reason, context[] }
async function fire(event, payload, tool, input) {
  const out = { block: false, reason: "", context: [] }
  for (const group of HOOKS[event] ?? []) {
    if (!matches(group, tool)) continue
    for (const h of group.hooks ?? []) {
      if (h.type && h.type !== "command") continue
      if (!passesIf(h.if, tool, input)) continue
      const pending = run(h.command, payload, h.timeout)
      if (h.async || h.asyncRewake) continue // en segundo plano, sin esperar resultado
      const r = await pending
      log(event, tool ?? "", "-> exit", r.code, r.stderr.trim().slice(0, 200))
      if (r.code === 2) {
        out.block = true
        out.reason += r.stderr.trim() + "\n"
        continue
      }
      if (r.code !== 0) continue
      let json
      try {
        json = JSON.parse(r.stdout)
      } catch {}
      if (json && typeof json === "object") {
        const hs = json.hookSpecificOutput ?? {}
        if (json.decision === "block" || hs.permissionDecision === "deny") {
          out.block = true
          out.reason += (json.reason ?? hs.permissionDecisionReason ?? "") + "\n"
        }
        if (hs.additionalContext) out.context.push(String(hs.additionalContext))
      } else if (r.stdout.trim() && (event === "SessionStart" || event === "UserPromptSubmit")) {
        out.context.push(r.stdout.trim())
      }
    }
  }
  return out
}

export default {
  id: "claude-hooks." + PLUGIN,
  setup: async (ctx) => {
    const cwd = () => ctx.location?.directory ?? process.cwd()
    const base = (sessionID, name) => ({ session_id: sessionID, cwd: cwd(), hook_event_name: name, transcript_path: "" })
    const marker = `<hook-context plugin="${PLUGIN}">`
    const sessionStart = new Map()

    const hook = async (domain, name, cb) => {
      try {
        await domain.hook(name, cb)
        log("hook registrado:", name)
        return true
      } catch (e) {
        log("hook no disponible:", name, String(e))
        return false
      }
    }

    if (HOOKS.PreToolUse)
      await hook(ctx.tool, "execute.before", async (e) => {
        const tool = claudeTool(e.tool)
        const input = snake(e.input)
        const r = await fire("PreToolUse", { ...base(e.sessionID, "PreToolUse"), tool_name: tool, tool_input: input }, tool, input)
        if (r.block) throw new Error(`[${PLUGIN}] ${r.reason.trim() || "Acción bloqueada por un hook"}`)
      })

    if (HOOKS.PostToolUse)
      await hook(ctx.tool, "execute.after", async (e) => {
        if (e.status && e.status !== "completed") return
        const tool = claudeTool(e.tool)
        const input = snake(e.input)
        const r = await fire(
          "PostToolUse",
          { ...base(e.sessionID, "PostToolUse"), tool_name: tool, tool_input: input, tool_response: e.result ?? e.output },
          tool,
          input,
        )
        const note = [r.reason, ...r.context].map((s) => s.trim()).filter(Boolean).join("\n")
        if (!note) return
        const text = `\n\n${marker}\n${note}\n</hook-context>`
        if (e.result && typeof e.result === "object") {
          const c = e.result.content
          e.result = { ...e.result, content: Array.isArray(c) ? [...c, { type: "text", text }] : (c ?? "") + text }
        } else if (typeof e.output === "string") {
          e.output += text
        }
      })

    if (HOOKS.UserPromptSubmit)
      await hook(ctx.session, "prompt", async (e) => {
        if (!e.prompt || typeof e.prompt.text !== "string") return
        const r = await fire("UserPromptSubmit", { ...base(e.sessionID, "UserPromptSubmit"), prompt: e.prompt.text })
        if (r.block) throw new Error(`[${PLUGIN}] ${r.reason.trim() || "Mensaje bloqueado por un hook"}`)
        if (r.context.length) e.prompt.text += `\n\n${marker}\n${r.context.join("\n\n")}\n</hook-context>`
      })

    if (HOOKS.SessionStart) {
      // El nombre del hook de contexto cambia entre versiones de V2 ("context" o "request")
      const inject = async (e) => {
        if (!Array.isArray(e.system)) return
        if (e.system.some((p) => typeof p?.text === "string" && p.text.startsWith(marker))) return
        if (!sessionStart.has(e.sessionID)) {
          const r = await fire("SessionStart", { ...base(e.sessionID, "SessionStart"), source: "startup" })
          sessionStart.set(e.sessionID, r.context.join("\n\n"))
        }
        const text = sessionStart.get(e.sessionID)
        if (text) e.system.push({ type: "text", text: `${marker}\n${text}\n</hook-context>` })
      }
      await hook(ctx.session, "context", inject)
      await hook(ctx.session, "request", inject)
    }

    const unsupported = Object.keys(HOOKS).filter(
      (k) => !["PreToolUse", "PostToolUse", "UserPromptSubmit", "SessionStart"].includes(k),
    )
    if (unsupported.length) log("eventos sin equivalente (ignorados):", unsupported.join(", "))
  },
}
```
