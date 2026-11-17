# 6. Listas de tareas

> [← Índice general](README.md) · Capítulo 6 de 63

Las listas de tareas son una extensión de **GFM** que convierte un elemento de lista en una casilla. Son cómodas para checklists de revisión y para el seguimiento de issues, pero no son un sistema de gestión de proyectos ni un formulario: el estado vive en el texto y no genera eventos, fechas ni responsables.

## 6.1 Sintaxis y reglas

```markdown
- [ ] Tarea pendiente
- [x] Tarea completada
```

- [ ] Tarea pendiente
- [x] Tarea completada

Reglas:

- El elemento debe empezar por `-`, `*` o `+`, seguido de un espacio.
- Después vienen `[ ]` (pendiente) o `[x]`/`[X]` (completada).
- Debe haber un espacio entre `]` y el texto; sin él, no se reconoce como tarea.
- La casilla afecta al elemento completo, no a una parte del texto.
- Se pueden anidar dentro de otras listas, con sangría de dos o cuatro espacios según el render.

```markdown
- [ ] Preparar la versión
  - [x] Actualizar el changelog
  - [ ] Revisar enlaces
  - [ ] Publicar
```

## 6.2 Dónde son interactivas

| Contexto | Comportamiento |
|---|---|
| Issue o pull request en GitHub | Casilla interactiva; el progreso se muestra en el listado |
| Archivo `.md` en el repositorio | Se renderiza, pero no se puede marcar desde la vista |
| Wiki | Renderizado; la edición es manual |
| Comentario de commit o revisión | Renderizado; sin interacción |
| Sitio estático | Solo apariencia; requiere JavaScript propio para cambiar el estado |
| PDF, DOCX, EPUB | Solo apariencia; el estado queda congelado |

La diferencia importante: marcar una casilla en un issue **edita el cuerpo del issue**. No es un dato estructurado que puedas consultar con una API como un campo booleano. Si necesitas seguimiento real, usa el sistema de issues, proyectos o una herramienta externa.

## 6.3 GitHub: progreso, conversión y plantillas

En issues y pull requests, GitHub cuenta las tareas completadas y muestra el progreso («2 de 5»). También permite convertir un elemento de la lista en un issue independiente desde el menú contextual de la casilla.

Las listas de tareas son habituales en:

- **Plantillas de pull request**: recuerdan las comprobaciones mínimas.
- **Plantillas de issue**: piden los datos necesarios para reproducir un error.
- **Seguimiento de un cambio**: agrupan los pasos de una migración.
- **Revisiones**: marcan lo que ya se comprobó.

```markdown
### Checklist de PR

- [ ] Tests añadidos o actualizados
- [ ] Documentación actualizada
- [ ] Changelog actualizado
- [ ] Sin avisos del linter
- [ ] Enlaces internos comprobados
```

Una lista demasiado larga se ignora. Si la plantilla tiene veinte casillas, la persona marcará las primeras y dejará el resto. Pide solo lo que bloquea la fusión o lo que evita una revisión incompleta.

## 6.4 Semántica y accesibilidad

En el HTML generado, una lista de tareas suele ser una lista normal con un `<input type="checkbox">` deshabilitado o decorativo. Eso implica:

- **No es un formulario enviable.** El estado no se guarda al marcar la casilla en un sitio estático.
- **El lector de pantalla anuncia la casilla** y su estado, pero no siempre el texto asociado si el HTML está mal construido.
- **El color no basta.** Si usas iconos o colores para indicar el estado, añade texto.
- **No uses la casilla como único contenido** de un elemento: el texto debe describir la tarea.
- **En documentos exportados**, la casilla puede convertirse en un carácter o perderse; comprueba el resultado.

El capítulo [47](47-accesibilidad.md) detalla las comprobaciones con lector de pantalla.

## 6.5 Compatibilidad

| Entorno | Soporte |
|---|---|
| GitHub, GitLab | Sí, con matices de interactividad |
| VS Code (vista previa) | Sí |
| Obsidian, Typora, Logseq | Sí |
| markdown-it | Solo con el plugin `markdown-it-task-lists` |
| Pandoc | Sí con la extensión `task_lists` |
| CommonMark puro | No; se ve `[ ]` como texto |
| Motores de PDF/DOCX | Depende de la extensión y la plantilla |

En un visor sin soporte, el texto literal `[ ]` aparece tal cual. No es un error grave, pero conviene saberlo si el documento se publica en varios destinos.

## 6.6 Cuándo no usarlas

Las listas de tareas no sustituyen a:

- **Un tablero de proyecto.** No hay columnas, prioridades ni fechas.
- **Un formulario.** No valida datos ni envía nada.
- **Un registro de auditoría.** Marcar una casilla no deja rastro de quién lo hizo.
- **Una lista de requisitos.** Un requisito completado no es lo mismo que un requisito verificado.

Tampoco conviene usarlas en documentación de referencia publicada: una casilla sin contexto parece una tarea pendiente del equipo, no una opción del producto. Si el objetivo es mostrar estados posibles, una tabla es más clara.

## 6.7 Alternativas

| Necesidad | Alternativa |
|---|---|
| Seguimiento con responsables | Issues, proyectos o herramienta dedicada |
| Estado de un proceso | Tabla con columnas de estado y fecha |
| Requisitos verificables | Lista con criterios de aceptación |
| Progreso visible en el sitio | Barra generada desde datos, no desde Markdown |
| Checklist imprimible | Casillas tipográficas (`☐`, `☑`) o tabla |

Las casillas tipográficas no son interactivas, pero se imprimen y se leen bien. Si el documento va a papel, suelen ser mejores que un `input` deshabilitado.

## 6.8 Lista de comprobación

- [ ] Cada tarea empieza por `- [ ]` o `- [x]` con un espacio después del corchete.
- [ ] El texto de la tarea describe una acción concreta.
- [ ] La lista no se usa como sustituto de un sistema de seguimiento.
- [ ] Las tareas anidadas tienen sangría consistente.
- [ ] El estado se entiende sin depender solo del color.
- [ ] La plantilla pide solo las comprobaciones que importan.
- [ ] Se comprobó el render en el destino final (GitHub, sitio, PDF).
- [ ] Las casillas interactivas se limitan a issues y pull requests.

---

[← 5. Tablas](05-tablas.md) · [Índice general](README.md) · [7. Código y documentación de software →](07-codigo-y-documentacion-de-software.md)
