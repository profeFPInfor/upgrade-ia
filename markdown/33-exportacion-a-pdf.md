# 33. Exportación a PDF

> [← Índice general](README.md) · Capítulo 33 de 63

PDF es el formato de distribución por excelencia para manuales, informes, libros y documentación que debe verse igual en cualquier dispositivo. Markdown no genera PDF directamente: hay que elegir un **motor** que convierta el documento y una **plantilla** que controle la tipografía.

## 33.1 Cuatro familias de motores

| Familia | Ejemplos | Ventajas | Limitaciones |
|---|---|---|---|
| **LaTeX** | `xelatex`, `lualatex`, `pdflatex`, ConTeXt | Tipografía, matemáticas, referencias, control de página | Instalación grande; errores de compilación |
| **HTML/CSS** | WeasyPrint, Prince, Chromium | Diseño web, CSS moderno, iteración rápida | Matemáticas complejas y paginación fina |
| **Tipografía programable** | Typst | Rápido, moderno, buena sintaxis | Ecosistema más joven |
| **Ofimática** | LibreOffice desde DOCX/ODT | Estilos corporativos y revisión | Conversión en dos pasos; ajustes manuales |

## 33.2 Pandoc + LaTeX

Es la ruta con mejor calidad tipográfica para texto técnico con fórmulas.

```bash
pandoc manual.md -o manual.pdf \
  --pdf-engine=xelatex \
  --toc --number-sections \
  -V documentclass=report \
  -V geometry:margin=2.5cm \
  -V mainfont="DejaVu Serif" \
  -V monofont="DejaVu Sans Mono" \
  -V lang=es \
  -V fontsize=11pt \
  -V linestretch=1.15
```

| Variable | Efecto |
|---|---|
| `documentclass` | `article`, `report`, `book`, `scrreprt`… |
| `geometry` | Márgenes (`margin=2.5cm`, `a4paper`) |
| `mainfont`, `monofont` | Fuentes con `xelatex` o `lualatex` |
| `lang` | Idioma (división silábica y comillas) |
| `fontsize` | `10pt`, `11pt`, `12pt` |
| `linestretch` | Interlineado (`1.15`, `1.5`) |
| `classoption` | Opciones de clase (`oneside`, `twocolumn`) |
| `toc-title` | Título del índice |

Motores:

- `xelatex`: Unicode y fuentes del sistema; recomendado para español, emoji y CJK (con la fuente adecuada).
- `lualatex`: similar, con Lua para personalización.
- `pdflatex`: rápido y compatible, pero limitado con Unicode.
- `context`: alternativa potente, menos habitual.

### 33.2.1 Portada, encabezados y saltos

```bash
pandoc manual.md -o manual.pdf \
  --include-in-header=cabecera.tex \
  --include-before-body=portada.tex \
  --include-after-body=colofon.tex
```

`cabecera.tex` puede cargar `fancyhdr`, `hyperref` o definir colores:

```latex
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead[L]{Manual de usuario}
\fancyhead[R]{\thepage}
```

Para forzar un salto de página, incluye LaTeX crudo en el Markdown:

```markdown
\newpage
```

Pandoc lo deja pasar al archivo `.tex`. Si necesitas un salto en DOCX, el mecanismo es distinto (véase el capítulo [34](34-exportacion-a-docx-y-odt.md)).

### 33.2.2 Código y tablas

```bash
# Resaltado con listings
pandoc manual.md -o manual.pdf --listings

# Con minted (requiere instalar pygments y compilar con --shell-escape)
pandoc manual.md -o manual.pdf \
  --pdf-engine=xelatex \
  --include-in-header=minted.tex
```

Pandoc convierte las tablas a `longtable` cuando pueden ocupar varias páginas. Para tablas muy anchas, reduce columnas, usa texto más corto o cambia a una lista de definiciones.

### 33.2.3 Imágenes y figuras

```markdown
![Diagrama de arquitectura](img/arquitectura.png){width=80%}
```

Con LaTeX, `width=80%` se traduce en un ancho relativo al texto. Para control en centímetros: `{width=12cm}`. Las imágenes deben tener resolución suficiente (al menos 150–300 ppp para impresión).

### 33.2.4 Matemáticas y referencias

Pandoc convierte `$...$` y `$$...$$` a LaTeX nativo. Para numerar y referenciar ecuaciones, figuras o tablas, usa un filtro como `pandoc-crossref`:

```bash
pandoc apuntes.md -o apuntes.pdf \
  --filter=pandoc-crossref \
  --number-sections
```

Para bibliografía:

```bash
pandoc articulo.md -o articulo.pdf \
  --citeproc --bibliography=referencias.bib --csl=estilo.csl
```

El capítulo [36](36-exportacion-a-latex.md) amplía las referencias cruzadas y las citas.

## 33.3 Pandoc + WeasyPrint (HTML/CSS)

WeasyPrint convierte HTML y CSS a PDF e implementa **CSS Paged Media**: márgenes, cabeceras, pies, numeración y saltos.

```bash
pandoc manual.md -o manual.pdf \
  --pdf-engine=weasyprint \
  --css=estilo-pdf.css \
  --toc
```

```css
@page {
  size: A4;
  margin: 2.2cm 2cm;
  @bottom-center {
    content: counter(page);
    font-size: .85rem;
    color: #666;
  }
}

@page :first {
  margin: 0;
  @bottom-center { content: none; }
}

h1 { break-before: page; }
h2, h3 { break-after: avoid; }
table, figure, pre { break-inside: avoid; }
p { orphans: 3; widows: 3; }
```

Cabeceras variables con `string-set`:

```css
h1 { string-set: capitulo content(); }
@page { @top-right { content: string(capitulo); } }
```

WeasyPrint no ejecuta JavaScript: Mermaid, KaTeX y resaltadores que dependen del navegador deben pre-renderizarse o generar HTML estático.

- Documentación: <https://doc.courtbouillon.org/weasyprint/stable/>
- Proyecto: <https://weasyprint.org/>

## 33.4 Chromium y md-to-pdf

La impresión del navegador reproduce el CSS de pantalla y admite `@media print`. Se puede automatizar con Chrome/Chromium en modo headless:

```bash
chrome --headless --disable-gpu \
  --print-to-pdf=manual.pdf \
  --no-pdf-header-footer \
  file:///ruta/manual.html
```

`md-to-pdf` envuelve este flujo para Markdown:

```bash
npx md-to-pdf README.md
npx md-to-pdf README.md --config-file=pdf-config.js
```

Ventajas: usa el mismo CSS que la web y renderiza Mermaid/KaTeX con JavaScript. Limitaciones: cabeceras y pies menos flexibles, dependencia de Chromium y resultados variables entre versiones.

- `md-to-pdf`: <https://github.com/simonhaenisch/md-to-pdf>

## 33.5 Typst

Pandoc 3.x puede usar **Typst** como motor:

```bash
pandoc manual.md -o manual.pdf --pdf-engine=typst
```

Typst es un sistema de composición moderno, rápido y con una sintaxis más sencilla que LaTeX. Su ecosistema de paquetes es más joven, pero cubre documentos técnicos, tablas y matemáticas.

- Typst: <https://typst.app/>
- Documentación: <https://typst.app/docs/>

## 33.6 LibreOffice y wkhtmltopdf

- **LibreOffice**: convierte DOCX u ODT a PDF con `soffice --headless --convert-to pdf manual.docx`. Útil si el flujo pasa por Word o si la organización exige plantillas corporativas.
- **wkhtmltopdf**: usa Qt WebKit; su mantenimiento es limitado y el renderizado CSS moderno es inconsistente. Para nuevos proyectos, prefiere Chromium o WeasyPrint.

## 33.7 Metadatos, enlaces y accesibilidad

- **Título y autor**: añade `title` y `author` en el Front Matter; Pandoc los pasa a `hyperref` en LaTeX.
- **Marcadores**: los encabezados generan marcadores en el PDF si el motor lo permite.
- **Enlaces internos**: comprueba que las anclas sobreviven a la conversión.
- **Idioma**: declara `lang` para que el lector active la voz y la división correctas.
- **PDF etiquetado**: la accesibilidad completa (orden de lectura, tablas etiquetadas) no es automática; requiere motores y flujos específicos.

### 33.7.1 PDF/UA

**PDF/UA** (ISO 14289) es la norma de accesibilidad para PDF. No basta con que el documento «se vea bien»: el archivo debe exponer su estructura para que un lector de pantalla pueda recorrerlo.

| Requisito | Qué implica |
|---|---|
| Documento etiquetado | El PDF contiene estructura lógica (títulos, párrafos, listas, tablas), no solo texto dibujado |
| Orden de lectura | El orden de los objetos coincide con el orden lógico |
| Idioma | El documento declara su idioma principal |
| Título | Los metadatos incluyen título y la opción de mostrarlo en la ventana |
| Texto alternativo | Figuras, fórmulas e imágenes tienen descripción |
| Tablas | Cabeceras identificadas y relaciones fila/columna |
| Marcadores | La navegación por secciones está disponible |
| Fuentes | Están incrustadas y con mapeo Unicode |
| Enlaces | Tienen texto o descripción comprensible |
| Color y contraste | El contenido cumple los criterios de legibilidad aplicables |

Cómo se consigue:

- **LaTeX:** el kernel reciente permite `\DocumentMetadata{...}` y el paquete `tagpdf` para generar estructura etiquetada. No es el comportamiento por defecto de una instalación antigua.
- **HTML → PDF:** algunos motores permiten generar PDF etiquetado; comprueba la versión y el resultado, porque el soporte varía.
- **Ofimática:** Word y LibreOffice tienen comprobadores de accesibilidad y exportación etiquetada, con resultados desiguales.
- **Pandoc solo:** la conversión a PDF no garantiza PDF/UA. Hay que elegir el motor y la configuración adecuados.

Validación:

1. **veraPDF** con el perfil PDF/UA, si está disponible en tu flujo.
2. **PAC** u otra herramienta de validación.
3. **Comprobador de accesibilidad** del editor de PDF.
4. **Prueba manual con lector de pantalla**: orden de lectura, tablas y figuras.
5. **Revisión del texto extraído**: si el orden es absurdo, la estructura no sirve.

Errores frecuentes: documento sin etiquetas, figuras sin texto alternativo, tablas sin cabeceras, idioma ausente, fuentes no incrustadas y páginas escaneadas sin OCR. Un PDF/UA técnicamente válido puede seguir siendo difícil de usar; la validación automática no sustituye la prueba con una persona.

### 33.7.2 Verificación antes de publicar

1. Abre el PDF en dos lectores distintos.
2. Comprueba el índice, los marcadores y los enlaces internos.
3. Copia texto de una tabla y de un bloque de código: ¿el orden tiene sentido?
4. Busca una palabra con tilde y otra con símbolo matemático.
5. Revisa los metadatos (título, autor, idioma).
6. Ejecuta el validador de accesibilidad si el documento lo requiere.
7. Prueba la navegación con teclado y, si es crítico, con lector de pantalla.

## 33.8 Problemas frecuentes

| Problema | Causa | Solución |
|---|---|---|
| `! Package fontspec Error` | Falta la fuente o el nombre no coincide | Instala la fuente o usa `DejaVu` |
| Caracteres `?` o cajas | `pdflatex` sin soporte Unicode | Cambia a `xelatex` o `lualatex` |
| `Overfull \hbox` | Línea o tabla demasiado ancha | Reescribe, reduce columnas o ajusta `\emergencystretch` |
| Página en blanco | Salto de sección o `\newpage` doble | Revisa los saltos y la clase de documento |
| Imagen gigante | Sin `width` y con muchos píxeles | Añade `{width=…}` o redimensiona |
| Enlaces rotos | Anclas duplicadas o renombradas | Verifica IDs antes de exportar |
| PDF enorme | Imágenes sin comprimir o fuentes embebidas | Optimiza imágenes y subconjuntos de fuentes |

## 33.9 Lista de comprobación

- [ ] El motor elegido soporta los caracteres del documento.
- [ ] Márgenes, tamaño de página y fuente están definidos.
- [ ] El índice y la numeración de secciones son correctos.
- [ ] Las tablas no desbordan y se parten donde deben.
- [ ] Las imágenes tienen resolución y tamaño adecuados.
- [ ] Los diagramas están pre-renderizados.
- [ ] Los enlaces internos y las referencias funcionan.
- [ ] El idioma y los metadatos están declarados.
- [ ] Si se exige PDF/UA, el documento está etiquetado y validado.
- [ ] Las tablas tienen cabeceras y las figuras, texto alternativo.
- [ ] El PDF se ha revisado en un lector real, no solo en el editor.

---

[← 32. Exportación a HTML](32-exportacion-a-html.md) · [Índice general](README.md) · [34. Exportación a DOCX y ODT →](34-exportacion-a-docx-y-odt.md)
