# OpenCode

> Nota breve y provisional. La documentación completa se irá construyendo a través de **Issues** del repositorio; esto es solo el punto de partida.

## Apartados

Cada apartado es **un fichero**, y cada fichero se trabaja con **una Issue**: así nadie se pisa. **Núcleo** es lo imprescindible para el taller; **Ampliación**, lo que se aborda después.

| Apartado | Alcance | Estado |
|----------|---------|--------|
| [Qué es y versiones](01-que-es-y-versiones.md) | Núcleo | Pendiente |
| [Instalación y primeros pasos](02-instalacion.md) | Núcleo | Pendiente |
| [Modelos y proveedores](03-modelos-y-proveedores.md) | Núcleo | Pendiente |
| [Interfaz y atajos](04-interfaz-y-atajos.md) | Núcleo | Pendiente |
| [Comandos personalizados](05-comandos-personalizados.md) | Ampliación | Pendiente |
| [Agentes](06-agentes.md) | Núcleo | Pendiente |
| [Skills](07-skills.md) | Ampliación | Pendiente |
| [AGENTS.md y configuración](08-agents-md-y-configuracion.md) | Núcleo | Pendiente |
| [Permisos, seguridad y privacidad](09-permisos-seguridad-y-privacidad.md) | Núcleo | Pendiente |
| [Sesiones, contexto y ahorro de tokens](10-sesiones-contexto-y-tokens.md) | Núcleo | Pendiente |
| [Servidores MCP y plugins](11-mcp-y-plugins.md) | Ampliación | Pendiente |
| [Línea de comandos y automatización](12-cli-y-automatizacion.md) | Ampliación | Pendiente |
| [Solución de problemas](13-solucion-de-problemas.md) | Ampliación | Pendiente |
| [Uso en las fases del proceso](14-uso-en-el-proceso.md) | Núcleo | Pendiente |
| [Límites, costes y alternativas](15-limites-costes-y-alternativas.md) | Núcleo | Pendiente |
| [Fuentes](16-fuentes.md) | Núcleo | Pendiente |

> **Cómo se ha ordenado.** Los apartados salen de la documentación oficial (versión 2.x, consultada el 2026-11-18) y del título de un [curso en vídeo](https://www.youtube.com/watch?v=ZZq4TpNgnvg). Del vídeo solo se ha usado el título y un resumen público, **no su contenido**, y puede describir la versión 1.x. Quien documente un apartado debe contrastarlo con la documentación oficial; lo que no se pueda confirmar, no se escribe.

## Qué es

OpenCode es un agente de programación de código abierto. Se usa desde una interfaz de terminal, una aplicación de escritorio o una interfaz web. Es la herramienta con la que se trabajará en el taller.

## Lo que dice la documentación oficial

- **Proveedores de modelos:** tiene soporte integrado para muchos proveedores de LLM; se conectan desde la interfaz de terminal con `/connect`.
- **Se amplía con:** plugins, servidores MCP y comandos propios.
- **Instalación:** hay varias vías (script, gestores de paquetes y binarios para macOS, Windows y Linux). Los comandos exactos cambian entre versiones, así que consúltalos en la página oficial antes de instalar.
- **Interfaz web:** se arranca con `opencode pair`, que muestra un enlace de conexión de un solo uso que caduca a los 5 minutos.

## Pendiente de documentar

- Instalación paso a paso en el equipo de clase.
- Configuración de un proveedor gratuito (ver el tema LLMs gratuitos, con OpenRouter).
- Configuración del proyecto: reglas y contexto para el agente.
- Uso en cada fase del [proceso](../../proceso/).
- Límites y costes.

## Verificación pendiente

La página oficial describe OpenCode en una versión reciente (2.x); algunas guías antiguas se refieren a la 1.x y los comandos pueden diferir. Al documentar un comando, indica la versión con la que se probó.

## Fuentes

- [Documentación oficial de OpenCode](https://opencode.ai/docs/)
