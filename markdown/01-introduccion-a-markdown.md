# 1. Introducción a Markdown

> [← Índice general](README.md) · Capítulo 1 de 63

## 1.1 Qué es Markdown

**Markdown** es un **lenguaje de marcado ligero** que permite escribir texto con estructura (títulos, listas, énfasis, enlaces, código…) usando únicamente caracteres de texto plano. Ese texto se convierte después, mediante un programa, en HTML u otros formatos.

Definición técnica: Markdown es, a la vez, (1) una **sintaxis** de texto plano diseñada para ser legible tal cual y (2) una **herramienta de conversión** (el script original `Markdown.pl`) que la transforma en HTML. Hoy el término designa una *familia* de dialectos con un núcleo común (véanse [CommonMark](11-commonmark.md) y [GFM](10-github-flavored-markdown-gfm.md)).

```markdown
# Mi primer documento

Esto es un párrafo con **negrita**, *cursiva* y un [enlace](https://example.com).

- Elemento uno
- Elemento dos
```

HTML equivalente (simplificado):

```html
<h1>Mi primer documento</h1>
<p>Esto es un párrafo con <strong>negrita</strong>, <em>cursiva</em> y un <a href="https://example.com">enlace</a>.</p>
<ul>
  <li>Elemento uno</li>
  <li>Elemento dos</li>
</ul>
```

## 1.2 Características principales

- **Texto plano**: cualquier editor sirve; los archivos suelen usar extensión `.md` o `.markdown`.
- **Legible sin renderizar**: el propio texto fuente ya resulta comprensible.
- **Sintaxis pequeña**: se aprende en minutos.
- **Portable y versionable**: encaja con Git (diffs legibles).
- **Convertible**: a HTML, PDF, DOCX, EPUB, LaTeX, etc.
- **Extensible**: mediante HTML embebido y dialectos con extensiones.

## 1.3 Filosofía

El objetivo declarado por John Gruber es que un documento sea **publicable tal cual, como texto plano, sin parecer que está lleno de etiquetas o instrucciones de formato**. La sintaxis se inspira en convenciones del correo electrónico en texto plano (por ejemplo, `>` para citas o `*` para listas). Markdown **no pretende sustituir a HTML**: cubre únicamente las necesidades más comunes de escritura para la web.

## 1.4 Ventajas

| Ventaja | Explicación |
|---|---|
| Curva de aprendizaje baja | Pocas reglas, muy memorizables |
| Independencia de herramienta | Texto plano; sin formato propietario |
| Control de versiones | Diffs y merges limpios en Git |
| Interoperabilidad | Soportado en GitHub, GitLab, foros, editores, generadores de sitios |
| Centrado en el contenido | Se separa el contenido de su presentación |
| Longevidad | Un `.md` de hoy se podrá leer dentro de décadas |

## 1.5 Desventajas

- **No hay un único Markdown**: existen dialectos con diferencias (véase [sección 12](12-variantes-y-dialectos-de-markdown.md)).
- **Maquetación limitada**: no hay colores, columnas, tamaños de fuente, etc.
- **Funciones avanzadas dependientes de extensiones** (tablas, notas al pie, diagramas, fórmulas).
- **Ambigüedades históricas** en el Markdown original (anidación de listas, énfasis), resueltas en gran parte por CommonMark.
- **Tablas incómodas** de mantener a mano cuando son grandes.

## 1.6 Cuándo utilizar Markdown

- README, guías, manuales, wikis, ADR, changelogs.
- Notas personales y bases de conocimiento.
- Blogs técnicos y sitios de documentación (con generadores estáticos).
- Comentarios en issues, pull requests y foros.
- Contenido que debe versionarse y revisarse como código.

## 1.7 Cuándo NO utilizar Markdown

- **Maquetación editorial compleja** (libros con diseño, folletos): mejor LaTeX, InDesign o similar.
- **Documentos con control fino de formato** (informes con estilos corporativos estrictos, numeración legal automática).
- **Documentación de gran escala con requisitos de reutilización y semántica rica** (ahí pueden encajar mejor AsciiDoc, reStructuredText o DocBook/DITA).
- **Formularios o aplicaciones interactivas**: para eso hace falta HTML/JS o [MDX](29-mdx-creacion-de-paginas-web-con-markdown-y-componentes.md).
- **Edición colaborativa en tiempo real por usuarios no técnicos** (suele ser más cómodo un editor visual).

## 1.8 Markdown vs HTML

| Aspecto | Markdown | HTML |
|---|---|---|
| Propósito | Escribir texto estructurado de forma sencilla | Describir la estructura completa de una página web |
| Legibilidad del fuente | Muy alta | Media/baja (etiquetas) |
| Potencia | Limitada | Total |
| Estilos y scripts | No nativos | Sí (CSS, JS) |
| Relación | Se convierte a HTML | Es el destino habitual |

Markdown permite incrustar HTML como recurso de escape ([sección 13](13-html-dentro-de-markdown.md)).

## 1.9 Markdown vs procesadores de texto

| Aspecto | Markdown | Procesadores (Word, Writer…) |
|---|---|---|
| Modelo | Texto plano + marcas | WYSIWYG, formato binario/XML |
| Formato visual | Delegado al renderizador | Controlado directamente |
| Control de versiones | Excelente | Limitado (aunque existe seguimiento de cambios) |
| Compatibilidad | Cualquier editor | Depende del software |
| Colaboración no técnica | Más difícil | Más sencilla |

---

[Índice general](README.md) · [2. Historia de Markdown →](02-historia-de-markdown.md)
