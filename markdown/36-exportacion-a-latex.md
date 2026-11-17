# 36. Exportación a LaTeX

> [← Índice general](README.md) · Capítulo 36 de 63

LaTeX es un sistema de composición tipográfica de alta calidad, estándar en matemáticas, física, ingeniería y publicaciones académicas. Exportar Markdown a LaTeX permite escribir en un formato sencillo y aprovechar después el control fino de LaTeX: fórmulas, referencias cruzadas, bibliografía, teoremas y estilo editorial.

## 36.1 Cuándo exportar a LaTeX

- Artículos, tesis y memorias con muchas fórmulas.
- Documentos que deben integrarse en una plantilla LaTeX existente.
- Publicaciones que exigen clases o paquetes concretos.
- Presentaciones con **Beamer**.
- Libros con control de página, índices y numeración.

Si solo necesitas un PDF corriente, suele ser más directo usar Pandoc + `xelatex` (capítulo [33](33-exportacion-a-pdf.md)). Exportar a `.tex` tiene sentido cuando vas a **editar o integrar** el LaTeX.

## 36.2 Conversión básica

```bash
# Documento compilable
pandoc README.md -t latex -s -o README.tex

# Con numeración y código con listings
pandoc README.md -t latex -s --number-sections --listings -o README.tex

# Con clase de libro y división por capítulos
pandoc manual.md -t latex -s \
  --top-level-division=chapter \
  -V documentclass=book \
  -o manual.tex
```

| Opción | Efecto |
|---|---|
| `-s`, `--standalone` | Añade preámbulo y `\begin{document}` |
| `--number-sections` | Numera secciones |
| `--listings` | Usa `listings` para el código |
| `--top-level-division` | `section`, `chapter` o `part` |
| `-V documentclass=…` | Clase de documento |
| `--include-in-header` | Paquetes y configuración |
| `--include-before-body` | Portada o páginas iniciales |
| `--include-after-body` | Anexos o colofón |
| `--template` | Plantilla completa |

## 36.3 Estructura del archivo generado

Un `.tex` mínimo generado por Pandoc contiene:

```latex
\documentclass{article}
\usepackage{amsmath,amssymb}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{longtable,booktabs}
\usepackage{xcolor}
\usepackage{listings}

\title{Manual de usuario}
\author{Equipo de documentación}
\date{2026-10-28}

\begin{document}
\maketitle
\tableofcontents

\section{Introducción}\label{introducción}

Texto con \textbf{negrita} y \emph{cursiva}.

\end{document}
```

Los encabezados se convierten en `\section`, `\subsection` o `\chapter` según `--top-level-division` y el nivel del encabezado.

## 36.4 Matemáticas

Markdown con `$...$` y `$$...$$` se traduce directamente a matemáticas de LaTeX:

```markdown
La energía de una partícula es $E = mc^2$.

$$
\int_{0}^{1} x^2 \, dx = \frac{1}{3}
$$
```

```latex
La energía de una partícula es \(E = mc^2\).

\[
\int_{0}^{1} x^2 \, dx = \frac{1}{3}
\]
```

Para entornos con alineación, usa LaTeX crudo:

````markdown
```{=latex}
\begin{align}
  a &= b + c \\
  d &= e + f
\end{align}
```
````

El capítulo [41](41-matematicas-y-notacion-cientifica.md) cubre la sintaxis matemática y su compatibilidad.

## 36.5 Referencias cruzadas

Pandoc convierte los enlaces internos a referencias de LaTeX. Para figuras, tablas y ecuaciones numeradas, el filtro `pandoc-crossref` añade etiquetas y referencias:

```markdown
![Diagrama](figura.png){#fig:arquitectura width=80%}

Como muestra la @fig:arquitectura, el flujo es lineal.
```

```bash
pandoc documento.md -o documento.pdf \
  --filter=pandoc-crossref \
  --number-sections
```

En LaTeX puro, las etiquetas se escriben así:

```latex
\begin{figure}
  \centering
  \includegraphics[width=0.8\textwidth]{figura.png}
  \caption{Diagrama de arquitectura}
  \label{fig:arquitectura}
\end{figure}

Como muestra la figura~\ref{fig:arquitectura}, el flujo es lineal.
```

- `pandoc-crossref`: <https://github.com/lierdakil/pandoc-crossref>

## 36.6 Bibliografía y citas

Pandoc puede procesar citas con `--citeproc` y un archivo BibTeX/BibLaTeX:

```bash
pandoc articulo.md -o articulo.pdf \
  --citeproc \
  --bibliography=referencias.bib \
  --csl=estilos/apa.csl
```

O delegar en LaTeX:

```bash
pandoc articulo.md -t latex -s \
  --natbib \
  --bibliography=referencias.bib \
  -o articulo.tex

latexmk -pdf articulo.tex
```

| Modo | Ventaja | Requisito |
|---|---|---|
| `--citeproc` | Funciona con cualquier writer; estilos CSL | `pandoc` + archivo `.csl` |
| `--natbib` | Integración con BibTeX clásico | `bibtex` |
| `--biblatex` | BibLaTeX y `biber` | `biber` |

Los estilos CSL están en <https://github.com/citation-style-language/styles>.

## 36.7 Código

### 36.7.1 listings

```bash
pandoc manual.md -t latex -s --listings -o manual.tex
```

`listings` es estable y no requiere compilar con `--shell-escape`. Se configura con `\lstset` en la cabecera.

### 36.7.2 minted

`minted` usa Pygments y produce un resaltado más moderno, pero requiere `pygments` y compilar con `-shell-escape`:

```latex
\usepackage{minted}
```

```bash
pandoc manual.md -t latex -s \
  --pdf-engine=xelatex \
  --include-in-header=minted.tex \
  -o manual.pdf
```

`minted.tex` puede contener:

```latex
\usepackage{minted}
\setminted{fontsize=\small, breaklines=true}
```

## 36.8 Tablas e imágenes

- Pandoc usa `longtable` para tablas que pueden partirse entre páginas.
- `booktabs` mejora las líneas horizontales.
- Las tablas muy anchas requieren `tabularx`, `landscape` o rediseño.
- Las imágenes se incluyen con `\includegraphics`; usa `width=0.8\textwidth` o centímetros.
- Para figuras flotantes, escribe el entorno `figure` en LaTeX crudo o usa un filtro.

## 36.9 Plantillas y preámbulo

Para controlar paquetes, colores y estilo:

```bash
pandoc manual.md -t latex -s \
  --include-in-header=preambulo.tex \
  --template=plantilla.tex \
  -o manual.tex
```

`preambulo.tex`:

```latex
\usepackage[spanish]{babel}
\usepackage{fontspec}
\setmainfont{TeX Gyre Pagella}
\setmonofont{TeX Gyre DejaVu Sans Mono}
\usepackage{microtype}
\usepackage{fancyhdr}
\pagestyle{fancy}
```

Con `xelatex` o `lualatex` puedes usar las fuentes instaladas en el sistema; con `pdflatex`, solo las que tengan codificación adecuada.

## 36.10 Compilación

```bash
# Una pasada
xelatex manual.tex

# Referencias, índice y bibliografía
latexmk -xelatex manual.tex

# Limpiar auxiliares
latexmk -c
```

LaTeX necesita varias pasadas para resolver referencias, índices y bibliografía. `latexmk` automatiza el proceso.

## 36.11 Problemas frecuentes

| Error | Causa | Solución |
|---|---|---|
| `Unicode character not set up` | `pdflatex` con Unicode | Usa `xelatex` o `lualatex` |
| `File not found` | Ruta de imagen o paquete | Revisa `\graphicspath` y la instalación |
| `Missing $ inserted` | `_` o `^` fuera de matemáticas | Escapa (`\_`) o usa modo matemático |
| `Undefined control sequence` | Paquete no cargado | Añade `\usepackage` |
| `Too many unprocessed floats` | Demasiadas figuras flotantes | Usa `[H]`, `\clearpage` o menos flotantes |
| `Overfull \hbox` | Línea o tabla ancha | Reescribe o ajusta |
| Bibliografía vacía | Falta compilar BibTeX/Biber | Ejecuta la cadena completa |

## 36.12 Beamer

Para diapositivas:

```bash
pandoc charla.md -t beamer -s -o charla.tex
pandoc charla.md -t beamer -s --pdf-engine=xelatex -o charla.pdf
```

En Markdown, cada encabezado de nivel 1 o 2 puede convertirse en una diapositiva según la plantilla. Usa `--slide-level=2` para controlar la división.

```markdown
---
title: "Introducción a Markdown"
author: "Equipo"
---

# Markdown

## Qué es

Texto...

## Sintaxis

- Títulos
- Listas
```

El capítulo [39](39-exportacion-a-presentaciones.md) compara Beamer con otras herramientas de presentaciones.

## 36.13 Lista de comprobación

- [ ] El documento compila sin errores.
- [ ] Las fuentes incluyen todos los glifos necesarios.
- [ ] Las referencias cruzadas apuntan a etiquetas existentes.
- [ ] La bibliografía se genera y ordena correctamente.
- [ ] Las tablas y figuras caben en la página.
- [ ] El código se resalta y no desborda.
- [ ] El índice y los marcadores del PDF son correctos.
- [ ] El `.tex` está versionado junto al Markdown.

---

[← 35. Exportación a EPUB](35-exportacion-a-epub.md) · [Índice general](README.md) · [37. Exportación a RTF, TXT y otros formatos →](37-exportacion-a-rtf-txt-y-otros-formatos.md)
