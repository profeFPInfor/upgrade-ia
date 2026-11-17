# 32. Exportación a HTML

> [← Índice general](README.md) · Capítulo 32 de 63

HTML es el destino **natural** de Markdown: el formato se diseñó para escribir texto que luego se convertía en HTML. Es también el paso intermedio de casi todas las demás exportaciones (PDF con CSS, EPUB, correo, sitios estáticos).

Este capítulo explica cómo generar HTML limpio, completo, autocontenido y accesible, y cómo integrarlo en un sitio o en una aplicación.

## 32.1 Dos salidas distintas

| Salida | Contenido | Uso |
|---|---|---|
| **Fragmento** | Solo el cuerpo convertido (`<h1>`, `<p>`…) | Insertar en una plantilla, CMS o componente |
| **Documento completo** | `<!DOCTYPE html>`, `<head>`, `<body>`, CSS… | Abrir directamente en el navegador o publicar |

En Pandoc, un fragmento es la opción por defecto; `-s` o `--standalone` genera el documento completo.

```bash
# Fragmento
pandoc README.md -f gfm -t html5 -o fragmento.html

# Documento completo con índice
pandoc README.md -f gfm -t html5 -s --toc -o README.html

# Documento autocontenido: CSS, imágenes y fuentes embebidas
pandoc README.md -f gfm -t html5 -s --embed-resources --standalone -o README.html
```

`--embed-resources` sustituye `--self-contained`, que está obsoleto. El resultado es un único archivo fácil de enviar por correo o publicar en un sitio sin dependencias.

## 32.2 Opciones útiles de Pandoc

| Opción | Efecto |
|---|---|
| `--toc` / `--toc-depth=N` | Índice lateral o inicial y profundidad |
| `--number-sections` | Numera títulos (`1`, `1.1`…) |
| `--section-divs` | Envuelve cada sección en `<section id="…">` |
| `--id-prefix=prefijo-` | Evita colisiones de IDs al incrustar varios documentos |
| `--shift-heading-level-by=N` | Sube o baja todos los niveles de encabezado |
| `--css=estilo.css` | Añade una hoja de estilo |
| `--template=plantilla.html` | Usa una plantilla propia |
| `--highlight-style=estilo` | Cambia el tema de resaltado de código |
| `--no-highlight` | Desactiva el resaltado |
| `--mathjax`, `--katex`, `--mathml` | Renderiza matemáticas en el navegador |
| `--wrap=none` | No parte las líneas del HTML generado |

Ejemplo con secciones, numeración y prefijo:

```bash
pandoc manual.md -f gfm -t html5 -s \
  --toc --toc-depth=3 --number-sections \
  --section-divs --id-prefix=manual- \
  --css=assets/manual.css \
  -o manual.html
```

## 32.3 Plantillas

Una plantilla HTML de Pandoc es un archivo con variables `$…$`:

```html
<!DOCTYPE html>
<html lang="$lang$">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>$title$</title>
  $for(css)$<link rel="stylesheet" href="$css$">$endfor$
</head>
<body>
  <header>
    <h1>$title$</h1>
    $if(subtitle)$<p class="subtitle">$subtitle$</p>$endif$
  </header>
  $if(toc)$<nav id="TOC" aria-label="Índice">$toc$</nav>$endif$
  <main>$body$</main>
  $for(include-after)$
  $include-after$
  $endfor$
</body>
</html>
```

Variables habituales: `$body$`, `$title$`, `$subtitle$`, `$author$`, `$date$`, `$lang$`, `$toc$`, `$css$`, `$header-includes$`. La lista completa está en el manual de Pandoc.

```bash
pandoc README.md -s --template=plantilla.html -o README.html
```

## 32.4 CSS y presentación

El HTML generado por Pandoc usa clases estándar (`sourceCode`, `code`, `footnotes`, `toc`, `table`…). Un CSS mínimo debe cubrir:

- **Tipografía**: familia, tamaño, interlineado y medida de línea (entre 60 y 75 caracteres).
- **Tablas**: `border-collapse`, cabeceras visibles y desplazamiento horizontal en pantallas pequeñas.
- **Código**: fuente monoespaciada, fondo, borde y `overflow-x: auto`.
- **Imágenes**: `max-width: 100%` y `height: auto`.
- **Enlaces**: color con contraste suficiente y subrayado.
- **Modo oscuro**: `@media (prefers-color-scheme: dark)` con variables CSS.

```css
:root { --texto: #1b1b1b; --fondo: #fff; --acento: #0b5cab; }
@media (prefers-color-scheme: dark) {
  :root { --texto: #eae8e3; --fondo: #111318; --acento: #93c2ff; }
}
body {
  max-width: 72ch;
  margin: 0 auto;
  padding: 2rem 1rem;
  background: var(--fondo);
  color: var(--texto);
  font: 1rem/1.7 system-ui, sans-serif;
}
pre, table { overflow-x: auto; }
img { max-width: 100%; height: auto; }
```

## 32.5 Resaltado de sintaxis y matemáticas

Pandoc genera HTML con clases para el resaltado (skylighting) y hojas de estilo integradas. Para cambiar el tema:

```bash
pandoc README.md -s --highlight-style=tango -o README.html
```

Temas disponibles: `pygments`, `tango`, `espresso`, `zenburn`, `kate`, `monochrome`, `breezedark`, `haddock`. También se puede generar un CSS propio:

```bash
pandoc --print-highlight-style=pygments > resaltado.css
```

Matemáticas:

```bash
pandoc apuntes.md -s --mathjax -o apuntes.html
pandoc apuntes.md -s --katex  -o apuntes.html
pandoc apuntes.md -s --mathml -o apuntes.html
```

- **MathJax**: más completo (LaTeX, MathML, AsciiMath), pero pesado.
- **KaTeX**: más rápido, subconjunto de LaTeX.
- **MathML**: nativo del navegador, sin JavaScript; soporte y calidad variables.

El capítulo [41](41-matematicas-y-notacion-cientifica.md) detalla la sintaxis y las diferencias.

## 32.6 HTML seguro

Markdown permite HTML crudo. Si el contenido viene de terceros, **no lo insertes sin sanitizar**:

- Pandoc incluye el HTML tal cual; no lo sanea.
- markdown-it y marked permiten desactivar HTML (`html: false`).
- DOMPurify elimina scripts, `on*` y URLs peligrosas en el navegador: <https://github.com/cure53/DOMPurify>.
- En un servidor, sanitiza también y aplica una **Content Security Policy**.

```javascript
import MarkdownIt from "markdown-it";
import DOMPurify from "dompurify";

const md = new MarkdownIt({ html: false, linkify: true });
const html = DOMPurify.sanitize(md.render(texto));
```

Riesgos típicos: `<script>`, `javascript:` en enlaces, `<iframe>` incrustados, imágenes de seguimiento y CSS que oculta contenido. Véase el capítulo [48](48-seguridad.md).

## 32.7 Otras herramientas

| Herramienta | Lenguaje | Uso |
|---|---|---|
| **markdown-it** | JavaScript | Renderizado extensible; plugins de anclas, notas y tablas |
| **marked** | JavaScript | Rápido y sencillo; CLI y API |
| **cmark** | C | Implementación de referencia de CommonMark |
| **cmark-gfm** | C | CommonMark + extensiones de GitHub |
| **Python-Markdown** | Python | Extensiones de tablas, notas, TOC y metadatos |
| **kramdown** | Ruby | Motor de Jekyll; IAL y atributos |
| **remark / rehype** | JavaScript | Pipeline de AST y plugins |

```bash
# markdown-it
npx markdown-it README.md -o README.html

# marked
npx marked -i README.md -o README.html

# cmark
cmark --to html README.md > README.html

# Python-Markdown
python -m markdown README.md > README.html

# kramdown
kramdown README.md > README.html
```

## 32.8 HTML dentro de generadores de sitios

Los generadores estáticos (Jekyll, Hugo, MkDocs, Docusaurus, Eleventy) convierten Markdown a HTML y añaden plantillas, navegación y búsqueda. En ellos:

- El **Front Matter** aporta título, fecha, plantilla y metadatos.
- Los enlaces internos deben apuntar a la URL final (`.html`, rutas limpias o *slugs*).
- Las extensiones del generador pueden cambiar la sintaxis (por ejemplo, *shortcodes* o *includes*).
- El HTML crudo puede estar deshabilitado por seguridad.

Véase el capítulo [28](28-generadores-de-sitios-estaticos.md).

## 32.9 Verificación

1. **Validez**: <https://validator.w3.org/>.
2. **Accesibilidad**: <https://pa11y.org/> o Lighthouse en las herramientas del navegador.
3. **Enlaces**: comprueba anclas y rutas relativas con un verificador.
4. **Rendimiento**: evita imágenes enormes y JavaScript innecesario.
5. **Sin JavaScript**: el contenido debe seguir siendo legible.

```bash
# Servir el resultado en local
python -m http.server 8000
```

## 32.10 Lista de comprobación

- [ ] ¿Fragmento o documento completo? Es una decisión consciente.
- [ ] El `<html>` declara el idioma (`lang="es"`).
- [ ] Hay `<meta charset="utf-8">` y `<meta name="viewport">`.
- [ ] El título de la página es descriptivo.
- [ ] Los encabezados no saltan niveles.
- [ ] Las tablas tienen cabeceras y no desbordan.
- [ ] Las imágenes tienen `alt` y dimensiones razonables.
- [ ] El HTML de terceros está sanitizado.
- [ ] El resultado se ve bien en claro, oscuro y móvil.
- [ ] Los enlaces internos y el índice funcionan.

---

[← 31. Conversión y exportación: panorama](31-conversion-de-markdown.md) · [Índice general](README.md) · [33. Exportación a PDF →](33-exportacion-a-pdf.md)
