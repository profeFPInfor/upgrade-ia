# 44. Bases de conocimiento personal

> [← Índice general](README.md) · Capítulo 44 de 63

Markdown es la base de muchas herramientas de **gestión del conocimiento personal** (PKM): Obsidian, Logseq, Foam, Zettlr o Joplin. La promesa es atractiva: notas en texto plano, enlazadas entre sí, sin depender de una base de datos propietaria. La realidad incluye extensiones y convenciones que conviene conocer para no perder portabilidad.

## 44.1 Por qué Markdown

- **Texto plano**: legible dentro de décadas.
- **Portable**: se abre con cualquier editor.
- **Versionable**: Git y diffs legibles.
- **Enlazable**: cada nota es un archivo con una ruta estable.
- **Extensible**: metadatos, enlaces wiki, plugins.

El riesgo es adoptar sintaxis que solo entiende una aplicación. Cuanto más cerca esté la nota de Markdown estándar, más fácil será migrarla.

## 44.2 Obsidian

Obsidian trabaja sobre una **bóveda** (una carpeta con archivos `.md`).

| Elemento | Sintaxis |
|---|---|
| Enlace wiki | `[[Nombre de la nota]]` |
| Enlace con alias | `[[Nombre|texto visible]]` |
| Enlace a encabezado | `[[Nombre#Sección]]` |
| Enlace a bloque | `[[Nombre#^id]]` |
| Imagen incrustada | `![[imagen.png]]` |
| Etiqueta | `#proyecto/markdown` |
| Propiedades | Front Matter YAML |
| Callout | `> [!note]` |

```markdown
---
title: "Markdown"
tags: [markdown, documentación]
aliases: [MD]
created: 2026-10-28
---

# Markdown

Enlaza con [[CommonMark]] y [[GFM]].

> [!warning] Compatibilidad
> Los enlaces wiki no son Markdown estándar.
```

- Obsidian: <https://obsidian.md/>
- Documentación: <https://help.obsidian.md/>

### 44.2.1 Plugins y funciones no portables

- **Dataview**: consultas sobre el Front Matter; no funciona fuera de Obsidian.
- **Templater**: plantillas con lógica.
- **Canvas**: tableros en JSON.
- **Graph view**: visualización de enlaces.
- **Publish/Sync**: servicios de pago.

Los plugins pueden ejecutar código y acceder a la bóveda: instala solo los que conozcas y revisa sus permisos.

## 44.3 Logseq

Logseq es un **outliner** basado en bloques y diarios.

- `[[página]]` crea enlaces.
- `((referencia))` enlaza bloques.
- `TODO`, `DOING`, `DONE` gestionan tareas.
- Las consultas (`query`) filtran bloques.
- Los diarios (`journals/`) organizan por fecha.

```markdown
- Idea principal
  - Detalle con enlace a [[Markdown]]
  - Tarea TODO revisar #documentación
```

- Logseq: <https://logseq.com/>

Ventaja: captura rápida y pensamiento no lineal. Limitación: la estructura de bloques y las consultas no son Markdown estándar.

## 44.4 Otras herramientas

| Herramienta | Enfoque |
|---|---|
| **Foam** | PKM en VS Code con enlaces wiki |
| **Zettlr** | Editor académico con citas y Zettelkasten |
| **Joplin** | Notas sincronizadas y cifrado |
| **Notion** | Bloques y bases de datos (no es Markdown nativo) |
| **Silverbullet** | Wiki personal en Markdown |
| **Vim/Neovim + plugins** | Control total del texto |

- Foam: <https://foambubble.github.io/foam/>
- Zettlr: <https://www.zettlr.com/>
- Joplin: <https://joplinapp.org/>

## 44.5 Método Zettelkasten

Principios que encajan bien con Markdown:

1. **Notas atómicas**: una idea por nota.
2. **Identificadores estables**: nombre o fecha (`202610281200 Idea`).
3. **Enlaces explícitos**: explica por qué se enlazan dos notas.
4. **Notas de índice (MOC)**: mapas de contenido que agrupan temas.
5. **Revisión**: las notas se refinan con el tiempo.
6. **Referencias**: cita la fuente y guarda la fecha de lectura.

La estructura de carpetas importa menos que los enlaces y la disciplina de revisión.

## 44.6 Front Matter para notas

```yaml
---
title: "CommonMark"
aliases: [CommonMark, especificación CommonMark]
tags: [markdown, estándares]
status: evergreen
created: 2026-10-28
updated: 2026-10-28
source: "https://spec.commonmark.org/"
---
```

- `title`: título legible.
- `aliases`: variantes para enlaces.
- `tags`: clasificación.
- `status`: `seed`, `growing`, `evergreen`.
- `created` / `updated`: fechas ISO 8601.
- `source`: procedencia.

Mantén las claves en minúsculas y sé consistente: las consultas y plantillas dependen de ello.

## 44.7 Enlaces wiki frente a enlaces estándar

| Aspecto | `[[Nota]]` | `[texto](nota.md)` |
|---|---|---|
| Portabilidad | Baja | Alta |
| Renombrado | La herramienta lo actualiza | Hay que actualizar la ruta |
| Anclas | `[[Nota#Sección]]` | `nota.md#sección` |
| Imágenes | `![[imagen.png]]` | `![alt](imagen.png)` |
| GitHub | No lo interpreta | Sí |

Para publicar fuera de la herramienta, convierte los enlaces wiki:

```bash
obsidian-export boveda salida
```

- obsidian-export: <https://github.com/zoni/obsidian-export>

## 44.8 Publicar una base de conocimiento

| Destino | Herramienta |
|---|---|
| **Sitio estático** | Quartz, MkDocs, Hugo, Astro |
| **GitHub Pages** | Exportar a Markdown estándar y generar |
| **Obsidian Publish** | Servicio oficial (de pago) |
| **Wiki interna** | MediaWiki, Confluence, BookStack |
| **PDF/EPUB** | Pandoc |

- Quartz: <https://quartz.jzhao.xyz/>

Antes de publicar, revisa enlaces privados, nombres de clientes, rutas locales y metadatos personales.

## 44.9 Sincronización y copias

- **Git**: historial y diffs; ideal para texto, pero requiere disciplina.
- **Syncthing**: sincronización entre dispositivos: <https://syncthing.net/>.
- **Nube**: cómoda, pero puede generar conflictos si se edita sin conexión.
- **Copias de seguridad**: no confundas sincronización con respaldo.

En Git, excluye archivos de estado y caché:

```gitignore
.obsidian/workspace.json
.obsidian/cache
.trash/
```

## 44.10 Callouts entre plataformas

| Plataforma | Sintaxis |
|---|---|
| Obsidian | `> [!note]` |
| GitHub | `> [!NOTE]` |
| MkDocs Material | `!!! note` |
| Docusaurus | `:::note` |
| Pandoc | `::: {.note}` |

No hay un estándar común. Si el documento va a vivir en varias plataformas, usa una cita normal (`>`) o una tabla, que funcionan en todas.

## 44.11 Accesibilidad y privacidad

- Usa encabezados jerárquicos, no negritas como títulos.
- Escribe texto alternativo en las imágenes.
- Evita enlaces con texto vacío o “aquí”.
- Revisa que los plugins no envíen datos a servicios externos.
- Cifra las notas sensibles o guárdalas en un almacén aparte.

## 44.12 Lista de comprobación

- [ ] Las notas son archivos `.md` legibles sin la aplicación.
- [ ] Los enlaces wiki tienen equivalente estándar o se convierten al publicar.
- [ ] El Front Matter es consistente.
- [ ] Hay copias de seguridad además de la sincronización.
- [ ] Los plugins están revisados y actualizados.
- [ ] La publicación no expone información privada.

---

[← 43. Cuadernos y publicación científica](43-cuadernos-y-publicacion-cientifica.md) · [Índice general](README.md) · [45. Internacionalización y escritura multilingüe →](45-internacionalizacion-y-escritura-multilingue.md)
