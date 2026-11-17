# 24. Front Matter

> [← Índice general](README.md) · Capítulo 24 de 63

El **Front Matter** es un bloque de metadatos al inicio de un archivo Markdown. Lo leen generadores de sitios, gestores de notas y algunas plataformas para obtener título, fecha, autor, etiquetas, plantilla o estado editorial. No forma parte de Markdown: es una convención que cada herramienta interpreta a su manera.

## 24.1 Qué es y qué no es

Es:

- Un bloque delimitado al principio del archivo.
- Un conjunto de claves y valores en YAML, TOML o JSON.
- Metadatos que el renderizador puede usar o ignorar.

No es:

- Parte de CommonMark ni de GFM.
- Un estándar con campos obligatorios.
- Contenido visible en todos los destinos: GitHub muestra YAML como tabla, otros renderizadores lo ocultan o lo imprimen.

La misma clave puede significar cosas distintas en dos herramientas. `draft: true` en Jekyll y en Hugo excluye la página de la compilación, pero no necesariamente del sitio ya generado. `date` puede ser la fecha de publicación, la de modificación o solo un dato informativo.

## 24.2 YAML

El formato más extendido, delimitado por `---`:

```yaml
---
title: "Instalación en Linux"
description: "Requisitos, pasos y verificación."
date: 2026-10-28
tags:
  - markdown
  - documentación
draft: false
---
```

Reglas:

- El bloque debe empezar en la **primera línea** del archivo.
- Se cierra con `---` en una línea propia.
- La indentación es significante; usa espacios, no tabulaciones.
- Las cadenas con `:`, `#`, comillas o caracteres especiales se entrecomillan.
- Los valores vacíos se escriben `""` o `null`, según lo que espere la herramienta.

## 24.3 TOML

Hugo y algunas herramientas aceptan TOML, delimitado por `+++`:

```toml
+++
title = "Instalación en Linux"
date = 2026-10-28
tags = ["markdown", "documentación"]
draft = false
+++
```

TOML es más explícito con los tipos y evita algunas ambigüedades de YAML, pero está menos extendido en el ecosistema Markdown.

## 24.4 JSON

Hugo admite JSON con llaves `{` y `}` al inicio del archivo:

```json
{
  "title": "Instalación en Linux",
  "date": "2026-10-28",
  "tags": ["markdown", "documentación"],
  "draft": false
}
```

Es útil para generar metadatos desde un script, pero incómodo de editar a mano: no admite comentarios y exige comas y comillas correctas.

## 24.5 Campos habituales

| Campo | Uso | Notas |
|---|---|---|
| `title` | Título visible y `<title>` | No siempre coincide con el H1 |
| `description` | Resumen para buscadores y listados | 150-160 caracteres orientativos |
| `date` | Fecha de publicación | Formato ISO 8601 |
| `lastmod` / `updated` | Última modificación | Útil para sitemap |
| `tags` / `categories` | Clasificación | Listas, no cadenas separadas por comas |
| `draft` | Excluir de la compilación | Comportamiento variable |
| `weight` / `order` | Orden en la navegación | Entero |
| `slug` | Parte final de la URL | Estable |
| `layout` | Plantilla | Depende del generador |
| `aliases` | URLs antiguas | Redirecciones |
| `image` | Imagen social | Ruta o URL absoluta |
| `canonical` | URL preferida | Solo si hay duplicados |
| `toc` | Generar índice | Booleano o configuración |

No copies un conjunto de campos de otro proyecto sin comprobar que tu generador los usa. Un campo ignorado es peor que un campo ausente: da la impresión de que el metadato está aplicado.

## 24.6 Fechas y zonas horarias

Las fechas son la fuente más común de errores:

- **YAML convierte fechas sin comillas en objetos de fecha**, no en cadenas. Eso puede cambiar el formato al exportar.
- **Sin zona horaria**, la interpretación depende del servidor. Usa `2026-10-28T10:00:00Z` o un desplazamiento explícito (`+02:00`) cuando la hora importe.
- **Para una fecha sin hora**, `2026-10-28` suele ser suficiente, pero comprueba cómo la muestra el generador.
- **No uses formatos locales** (`28/10/2026`): son ambiguos y difíciles de ordenar.

En el sitemap y en los feeds, la fecha debe ser la de publicación o modificación real, no la de generación del sitio.

## 24.7 Front Matter y contenido

El H1 del cuerpo y el `title` del Front Matter pueden diferir:

- `title` alimenta la pestaña, el listado y las tarjetas sociales.
- El H1 es el encabezado visible de la página.

Si se duplican literalmente, el lector ve el mismo texto dos veces. Si difieren demasiado, el título de la pestaña no corresponde con la página. Una práctica habitual es un `title` algo más corto y un H1 más descriptivo.

```markdown
---
title: "Instalación en Linux"
description: "Requisitos, pasos y verificación para instalar la CLI."
---

# Instalar la CLI en Linux

...
```

## 24.8 Validación y esquemas

Un campo mal escrito (`descripton`, `tag`, `draf`) no produce error: el generador lo ignora. Para evitarlo:

1. **Define un esquema** de los campos permitidos y sus tipos.
2. **Valida en CI** antes de publicar.
3. **Fija valores** para estados (`draft`, `published`, `deprecated`).
4. **Comprueba fechas** y enlaces.
5. **Documenta** qué campos son obligatorios y cuáles opcionales.

Astro permite esquemas de colecciones; otros generadores tienen plugins o validadores propios. Si no existe, un script de validación es suficiente para empezar.

## 24.9 Seguridad

- **No cargues YAML de fuentes no confiables con un parser que permita etiquetas arbitrarias.** Un YAML malicioso puede instanciar objetos o ejecutar código en algunos lenguajes.
- **Escapa los valores** que se imprimen en HTML; el Front Matter no es una zona segura.
- **No guardes secretos** en el Front Matter: se publica con el contenido.
- **Revisa los campos que se usan en plantillas**; un valor inesperado puede romper el render o inyectar HTML.

## 24.10 Errores frecuentes

| Error | Efecto |
|---|---|
| Bloque que no empieza en la primera línea | Se muestra como contenido |
| Falta el delimitador de cierre | Todo el documento se interpreta como metadatos |
| Tabulaciones en YAML | Error de análisis |
| `:` sin comillas en un valor | El parser corta la cadena |
| Fechas locales | Orden incorrecto o ambigüedad |
| Campo desconocido | Se ignora silenciosamente |
| `tags` como cadena | Se trata como una sola etiqueta |
| Front Matter en un archivo que no lo admite | Aparece como texto |

## 24.11 Lista de comprobación

- [ ] El bloque empieza en la primera línea y está bien cerrado.
- [ ] El formato (YAML, TOML, JSON) es el que espera el generador.
- [ ] Los campos obligatorios están presentes y bien escritos.
- [ ] Las fechas usan ISO 8601 y la zona horaria es explícita si importa.
- [ ] Las cadenas con caracteres especiales están entrecomilladas.
- [ ] `tags` y `categories` son listas.
- [ ] El `title` y el H1 no se contradicen.
- [ ] Los campos se validan en CI.
- [ ] No hay secretos ni datos personales.
- [ ] El render final no muestra el bloque como contenido.

---

[← 23. ADR](23-adr.md) · [Índice general](README.md) · [25. Markdown y Git →](25-markdown-y-git.md)
