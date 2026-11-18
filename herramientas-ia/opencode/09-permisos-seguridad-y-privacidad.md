# OpenCode: permisos, seguridad y privacidad

> **Estado:** pendiente de documentar.
> **Zona de trabajo:** este fichero. Si tu Issue es este apartado, **solo editas este fichero**; los índices y los README los actualiza el profesor.

## Qué debe contener

- Cómo funcionan los permisos y una configuración prudente para clase.
- Qué riesgos tiene dar acceso al terminal y a los ficheros a un agente.
- **Privacidad:** qué datos salen del equipo según el modelo elegido y qué no se debe pegar nunca (claves, datos personales, material que no puedas compartir).


## Punto de partida (documentación oficial, consultada el 2026-11-18)

- Una regla tiene `action`, `resource` y `effect` (`allow`, `ask`, `deny`); **gana la última que coincida**; sin regla se pregunta.
- Por defecto casi todo está permitido, salvo leer ficheros `.env`, que pregunta; el acceso a directorios externos (`external_directory`) también está permitido por defecto.
- `shell` actúa con los permisos de tu usuario del sistema: conviene una lista corta de comandos permitidos.
- Algunos modelos gratuitos **pueden usar los datos para entrenar** o retenerlos; en los de pago, la retención va de 0 a 55 días según el proveedor.

> Esto es solo una pista para empezar: **compruébalo tú** en https://opencode.ai/docs/ con la versión que instales. Si ha cambiado, escribe lo nuevo.

*Cuando termines, borra los apartados «Qué debe contener» y «Punto de partida», y la nota de estado de arriba.*

## Contenido

*(Pendiente.)*

## Antes de abrir el pull request

- [ ] Los comandos se han probado y indican la versión.
- [ ] Las afirmaciones enlazan a una fuente primaria.
- [ ] No hay claves, tokens ni datos personales.
- [ ] Solo he modificado este fichero.
