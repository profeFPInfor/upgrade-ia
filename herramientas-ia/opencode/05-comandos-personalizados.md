# OpenCode: comandos personalizados

> **Estado:** pendiente de documentar.
> **Zona de trabajo:** este fichero. Si tu Issue es este apartado, **solo editas este fichero**; los índices y los README los actualiza el profesor.

## Qué debe contener

- Qué es un comando personalizado y cuándo compensa crear uno.
- Dónde se guardan, qué lleva la cabecera y cómo se pasan argumentos.
- Un ejemplo completo que funcione, con aviso de seguridad sobre `!`.


## Punto de partida (documentación oficial, consultada el 2026-11-18)

- Se guardan en `.opencode/commands/` (proyecto) o `~/.config/opencode/commands/` (global), como `.md`; las subcarpetas dan nombres como `/equipo/revisar`.
- Argumentos con `$ARGUMENTS` y `$1`, `$2`…; la salida de un comando se inserta con `` !`comando` ``.
- Esos bloques de terminal **se ejecutan fuera de los permisos del agente**: nunca con argumentos no fiables.

> Esto es solo una pista para empezar: **compruébalo tú** en https://opencode.ai/docs/ con la versión que instales. Si ha cambiado, escribe lo nuevo.

*Cuando termines, borra los apartados «Qué debe contener» y «Punto de partida», y la nota de estado de arriba.*

## Contenido

*(Pendiente.)*

## Antes de abrir el pull request

- [ ] Los comandos se han probado y indican la versión.
- [ ] Las afirmaciones enlazan a una fuente primaria.
- [ ] No hay claves, tokens ni datos personales.
- [ ] Solo he modificado este fichero.
