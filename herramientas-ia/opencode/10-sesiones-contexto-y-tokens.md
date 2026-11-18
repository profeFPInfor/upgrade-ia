# OpenCode: sesiones, contexto y ahorro de tokens

> **Estado:** pendiente de documentar.
> **Zona de trabajo:** este fichero. Si tu Issue es este apartado, **solo editas este fichero**; los índices y los README los actualiza el profesor.

## Qué debe contener

- Qué es una sesión y cómo se gestionan.
- Qué es el contexto, qué es un token y por qué importa para el coste y los límites.
- Técnicas para gastar menos, **midiendo el efecto** si puedes.


## Punto de partida (documentación oficial, consultada el 2026-11-18)

- La compactación sustituye la conversación antigua por un resumen y **pierde detalle**; es automática por defecto (`compaction.auto`).
- Se pueden ajustar `keep.tokens` (15 000 por defecto) y `buffer` (15 %), o usar un modelo más barato para los resúmenes.
- La compactación no libera lo que ocupan las instrucciones fijas y las herramientas: cada servidor MCP que añades consume contexto.
- En la documentación consultada **no se explica cómo ver el gasto de tokens**: compruébalo.

> Esto es solo una pista para empezar: **compruébalo tú** en https://opencode.ai/docs/ con la versión que instales. Si ha cambiado, escribe lo nuevo.

*Cuando termines, borra los apartados «Qué debe contener» y «Punto de partida», y la nota de estado de arriba.*

## Contenido

*(Pendiente.)*

## Antes de abrir el pull request

- [ ] Los comandos se han probado y indican la versión.
- [ ] Las afirmaciones enlazan a una fuente primaria.
- [ ] No hay claves, tokens ni datos personales.
- [ ] Solo he modificado este fichero.
