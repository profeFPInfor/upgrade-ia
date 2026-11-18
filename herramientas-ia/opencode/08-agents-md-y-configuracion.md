# OpenCode: agents.md y configuración

> **Estado:** pendiente de documentar.
> **Zona de trabajo:** este fichero. Si tu Issue es este apartado, **solo editas este fichero**; los índices y los README los actualiza el profesor.

## Qué debe contener

- Para qué sirve `AGENTS.md` y un ejemplo para este repositorio.
- El fichero de configuración: dónde está, el orden de prioridad y las claves principales.
- Cómo evitar escribir claves en el repositorio.


## Punto de partida (documentación oficial, consultada el 2026-11-18)

- `AGENTS.md` da guía permanente al proyecto; si no existe, OpenCode lee `CLAUDE.md`.
- La configuración es `opencode.json` o `opencode.jsonc`, con `$schema: https://opencode.ai/config.json`; los de carpetas más cercanas pisan a los lejanos.
- Las claves no van en el fichero: usa `{env:NOMBRE}` o `{file:ruta}`.
- No aparece documentado el comando `/init`: compruébalo.

> Esto es solo una pista para empezar: **compruébalo tú** en https://opencode.ai/docs/ con la versión que instales. Si ha cambiado, escribe lo nuevo.

*Cuando termines, borra los apartados «Qué debe contener» y «Punto de partida», y la nota de estado de arriba.*

## Contenido

*(Pendiente.)*

## Antes de abrir el pull request

- [ ] Los comandos se han probado y indican la versión.
- [ ] Las afirmaciones enlazan a una fuente primaria.
- [ ] No hay claves, tokens ni datos personales.
- [ ] Solo he modificado este fichero.
