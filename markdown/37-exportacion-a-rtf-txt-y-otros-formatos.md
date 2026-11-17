# 37. Exportación a RTF, TXT y otros formatos

> [← Índice general](README.md) · Capítulo 37 de 63

No todos los destinos necesitan un PDF o un libro electrónico. A veces el objetivo es **intercambiar** texto con un procesador de textos, **leerlo en el terminal**, **publicarlo en una wiki** o **alimentar otra herramienta**. Este capítulo cubre los formatos de texto que no tienen capítulo propio.

## 37.1 RTF

RTF (*Rich Text Format*) es un formato de intercambio con formato básico, legible por Word, LibreOffice y muchos editores.

```bash
pandoc README.md -t rtf -s -o README.rtf
```

Conserva negritas, cursivas, listas, tablas sencillas, enlaces e imágenes, pero su modelo es limitado:

- No hay estilos semánticos modernos ni herencia de estilos como en DOCX.
- Las tablas complejas y los diseños de página se pierden.
- Los caracteres no ASCII se codifican con escapes `\uN?`; el resultado depende de la fuente.
- No es un buen formato para revisión colaborativa.

Úsalo para intercambio puntual, no como formato de archivo ni como fuente de verdad.

## 37.2 Texto plano

```bash
pandoc README.md -t plain -o README.txt
pandoc README.md -t plain --wrap=none -o README.txt
pandoc README.md -t plain --wrap=auto --columns=80 -o README.txt
```

| Opción | Efecto |
|---|---|
| `--wrap=none` | No parte líneas |
| `--wrap=auto` | Ajusta al ancho indicado |
| `--wrap=preserve` | Respeta los saltos del original |
| `--columns=N` | Ancho de línea |
| `--reference-links` | Usa enlaces de referencia al final |

El texto plano pierde títulos, énfasis, enlaces y tablas. Es útil para:

- Índices y búsquedas.
- Documentos que se leen en terminal o en un correo sencillo.
- Entradas de sistemas que solo aceptan texto.
- Comparaciones de contenido con `diff`.

Si necesitas que los enlaces sigan siendo visibles, revisa la salida: algunos writers añaden las URLs entre paréntesis o al final.

## 37.3 Markdown normalizado

Convertir Markdown a Markdown parece redundante, pero sirve para **normalizar** el formato:

```bash
pandoc README.md -t gfm \
  --markdown-headings=atx \
  --wrap=none \
  -o README.normalizado.md
```

- `--markdown-headings=atx` fuerza `#` en lugar de subrayados.
- `--wrap=none` evita reflow.
- `-t gfm` limita la salida a GFM.
- `--reference-links` agrupa los enlaces al final.

Para formatear Markdown con un estilo consistente, también existen **Prettier** (<https://prettier.io/>) y **markdownlint** (<https://github.com/DavidAnson/markdownlint>). El capítulo [46](46-linting-y-validacion.md) cubre la validación.

## 37.4 Páginas de manual

Pandoc y cmark pueden generar páginas `man`:

```bash
pandoc README.md -t man -s -o README.1
cmark --to man README.md > README.1
man ./README.1
```

Aspectos prácticos:

- La sección 1 es para comandos de usuario; la 5, para formatos de archivo; la 7, para convenciones.
- El nombre del archivo debe coincidir con el comando (`mi-herramienta.1`).
- Los encabezados se convierten en secciones (`NAME`, `SYNOPSIS`, `DESCRIPTION`…).
- Las tablas y el HTML no se representan bien.

Para groff `ms`:

```bash
pandoc README.md -t ms -s -o README.ms
groff -ms -Tpdf README.ms > README.pdf
```

## 37.5 AsciiDoc y reStructuredText

| Destino | Comando | Ecosistema |
|---|---|---|
| **AsciiDoc** | `pandoc README.md -t asciidoc -s -o README.adoc` | Asciidoctor, Antora |
| **reStructuredText** | `pandoc README.md -t rst -s -o README.rst` | Sphinx, Docutils |
| **Org** | `pandoc README.md -t org -s -o README.org` | Emacs Org mode |
| **DocBook** | `pandoc README.md -t docbook5 -s -o README.xml` | Publicación técnica |
| **Typst** | `pandoc README.md -t typst -s -o README.typ` | Typst |

Estas conversiones son útiles para:

- Migrar documentación a Sphinx (Python) o Antora (AsciiDoc).
- Reutilizar contenido en un manual con DocBook.
- Editar en Emacs con Org mode.
- Integrar en una cadena Typst.

La sintaxis no es equivalente: las tablas, notas y bloques de código pueden requerir ajustes manuales. Revisa el resultado y no asumas un *round-trip* perfecto.

## 37.6 Formatos de wiki y foros

| Destino | Comando | Notas |
|---|---|---|
| **MediaWiki** | `pandoc README.md -t mediawiki -o README.wiki` | Plantillas y extensiones no se convierten |
| **DokuWiki** | `pandoc README.md -t dokuwiki -o README.txt` | Sintaxis propia |
| **XWiki** | `pandoc README.md -t xwiki -o README.xwiki` | Macros no portables |
| **ZimWiki** | `pandoc README.md -t zimwiki -o README.txt` | Diario personal |
| **Jira** | `pandoc README.md -t jira -o README.jira` | Markup de Jira |
| **BBCode** | `pandoc README.md -t bbcode -o README.bbcode` | Foros clásicos |
| **Textile** | `pandoc README.md -t textile -o README.textile` | Sistemas antiguos |

Advertencias:

- Las macros, plantillas y extensiones de cada wiki **no forman parte de Markdown**; se pierden o quedan como texto.
- Los enlaces internos pueden necesitar el prefijo o la sintaxis del wiki.
- Las tablas complejas suelen degradarse.
- Comprueba el resultado en el editor de la plataforma, no solo en el archivo.

## 37.7 Cuadernos y AST

| Destino | Comando | Uso |
|---|---|---|
| **Jupyter Notebook** | `pandoc README.md -t ipynb -o README.ipynb` | Cuadernos con celdas Markdown y código |
| **JSON (AST)** | `pandoc README.md -t json -o README.json` | Inspección, filtros y herramientas |
| **Native** | `pandoc README.md -t native` | Representación legible del AST |
| **HTML** | `pandoc README.md -t html5` | Paso intermedio |

El AST JSON es la base de los filtros de Pandoc y de muchas integraciones. Si desarrollas una herramienta, trabaja con el AST en lugar de manipular HTML con expresiones regulares.

## 37.8 Correo electrónico HTML

Markdown se usa mucho para redactar correos y boletines. El HTML resultante necesita estilos **en línea** porque muchos clientes de correo ignoran `<style>`:

```bash
pandoc boletin.md -t html5 -s --css=correo.css -o boletin.html
```

Después, herramientas como **Premailer** convierten el CSS en atributos `style`:

- Premailer: <https://premailer.io/>
- MJML: <https://mjml.io/> (componentes y compilación a HTML para correo)

Limitaciones del correo: sin JavaScript, soporte irregular de CSS, imágenes externas bloqueadas por defecto y anchos de 600 px habituales. Prueba en varios clientes.

## 37.9 Cómo elegir

| Necesidad | Formato |
|---|---|
| Intercambio con Word sin estilos complejos | RTF |
| Lectura en terminal o búsqueda | TXT |
| Normalizar el Markdown | Markdown |
| Documentación de comandos | man / ms |
| Ecosistema Sphinx | reStructuredText |
| Ecosistema Asciidoctor | AsciiDoc |
| Wiki corporativa | MediaWiki / XWiki / Jira |
| Cuaderno reproducible | ipynb |
| Herramienta propia | JSON AST |

## 37.10 Lista de comprobación

- [ ] El formato de destino admite las estructuras que necesitas.
- [ ] Los caracteres no ASCII se ven correctamente.
- [ ] Los enlaces siguen siendo útiles (o se han convertido en URLs visibles).
- [ ] Las tablas no se han degradado en exceso.
- [ ] El resultado se ha abierto en la herramienta de destino.
- [ ] El archivo generado no se edita a mano si se puede regenerar.

---

[← 36. Exportación a LaTeX](36-exportacion-a-latex.md) · [Índice general](README.md) · [38. Exportación a vídeo →](38-exportacion-a-video.md)
