# 31. Conversión y exportación: panorama

> [← Índice general](README.md) · Capítulo 31 de 63

Markdown es un formato de **origen**, casi nunca el formato final. Un conversor transforma el texto en HTML, PDF, DOCX, EPUB, LaTeX, vídeo u otros destinos. La calidad del resultado depende de tres factores: el **parser** (qué dialecto entiende), las **extensiones** activadas y la **plantilla o motor de destino**.

Este capítulo ofrece el mapa general. Cada formato tiene su propio capítulo, con comandos, herramientas, limitaciones y listas de comprobación.

## 31.1 Mapa de exportación

| Destino | Capítulo | Herramientas habituales | Caso de uso |
|---|---|---|---|
| **HTML** | [32](32-exportacion-a-html.md) | Pandoc, markdown-it, marked, cmark | Web, documentación, correo |
| **PDF** | [33](33-exportacion-a-pdf.md) | Pandoc + LaTeX, WeasyPrint, Typst, Chromium | Manuales, informes, libros |
| **DOCX / ODT** | [34](34-exportacion-a-docx-y-odt.md) | Pandoc, LibreOffice | Documentos de oficina editables |
| **EPUB** | [35](35-exportacion-a-epub.md) | Pandoc, Calibre, Sigil | Libros electrónicos |
| **LaTeX** | [36](36-exportacion-a-latex.md) | Pandoc, filtros Lua | Artículos, tesis, matemáticas |
| **RTF, TXT y otros** | [37](37-exportacion-a-rtf-txt-y-otros-formatos.md) | Pandoc, cmark | Intercambio, terminal, wikis |
| **Vídeo** | [38](38-exportacion-a-video.md) | OBS, ffmpeg, asciinema, VHS | Demos, tutoriales, GIF |
| **Presentaciones** | [39](39-exportacion-a-presentaciones.md) | Marp, Slidev, reveal.js, Pandoc | Charlas y formación |
| **Imágenes** | [40](40-exportacion-a-imagenes-y-otros-destinos.md) | Mermaid CLI, PlantUML, Graphviz | Diagramas y capturas |

## 31.2 El pipeline de conversión

Todo conversor sigue un proceso común:

```text
texto Markdown
   │  parser (CommonMark, GFM, Pandoc Markdown…)
   ▼
árbol de sintaxis abstracta (AST)
   │  transformaciones y filtros
   ▼
writer o renderizador (HTML, LaTeX, DOCX…)
   │  plantilla, hoja de estilo, metadatos
   ▼
documento final
```

Consecuencias prácticas:

- **El dialecto importa**: una tabla GFM puede no interpretarse con un parser CommonMark estricto.
- **El AST pierde información**: dos documentos con el mismo HTML pueden tener estructuras distintas.
- **La plantilla manda**: el mismo HTML produce PDF, EPUB o DOCX muy diferentes según el CSS o la plantilla.
- **La conversión no suele ser reversible**: DOCX → Markdown → DOCX cambia estilos, numeración y metadatos.

## 31.3 Pandoc: el conversor de referencia

**Pandoc** lee y escribe decenas de formatos, admite plantillas, filtros, metadatos, citas y referencias cruzadas. Está escrito en Haskell y se distribuye como binario para Windows, macOS y Linux.

- Sitio oficial: <https://pandoc.org/>
- Manual: <https://pandoc.org/MANUAL.html>
- Descargas: <https://pandoc.org/installing.html>

### 31.3.1 Estructura de una orden

```bash
pandoc ENTRADA.md \
  -f gfm \                    # formato de lectura
  -t html5 \                  # formato de escritura
  -s \                        # documento completo
  --toc \                     # tabla de contenidos
  -o SALIDA.html
```

| Opción | Efecto |
|---|---|
| `-f`, `--from` | Formato de entrada (`gfm`, `commonmark`, `markdown`, `docx`…) |
| `-t`, `--to` | Formato de salida (`html5`, `pdf`, `docx`, `epub`, `latex`…) |
| `-o`, `--output` | Archivo de salida; si se omite, escribe en la salida estándar |
| `-s`, `--standalone` | Documento completo con cabecera y pie |
| `--toc`, `--toc-depth=N` | Índice y profundidad máxima |
| `--number-sections` | Numera las secciones |
| `--template=ARCHIVO` | Plantilla personalizada |
| `--metadata CLAVE=VALOR` | Metadatos del documento |
| `--resource-path=RUTAS` | Dónde buscar imágenes y recursos |
| `--embed-resources` | Embebe CSS, imágenes y fuentes en HTML |
| `--citeproc` | Procesa citas y bibliografía |
| `--lua-filter=ARCHIVO` | Transforma el AST con Lua |
| `--verbose` | Muestra información de diagnóstico |

### 31.3.2 Metadatos

Pandoc lee el Front Matter YAML:

```yaml
---
title: "Manual de usuario"
subtitle: "Versión 2.1"
author: "Equipo de documentación"
date: "2026-10-28"
lang: es
---
```

También se pueden pasar por línea de comandos:

```bash
pandoc README.md -o README.pdf \
  --metadata title="Manual" \
  --metadata author="Equipo" \
  --metadata lang=es
```

`lang` afecta a la división silábica, a las comillas tipográficas y a la etiqueta `lang` del HTML. En LaTeX se traduce en el paquete de idioma correspondiente.

### 31.3.3 Varios archivos y recursos

```bash
pandoc docs/00-intro.md docs/01-instalacion.md docs/02-uso.md \
  -o manual.pdf --toc --resource-path=.:docs
```

`--resource-path` indica dónde buscar imágenes. Para proyectos grandes conviene un script de composición o un documento maestro que incluya los demás.

### 31.3.4 Filtros

Los **filtros** modifican el AST antes de escribir:

- **Lua**: `--lua-filter=figuras.lua`; no requiere instalar nada más.
- **Ejecutables**: `--filter=pandoc-crossref`; leen y escriben JSON.
- **Filtros integrados**: `--citeproc` para bibliografía.

Los filtros son código: trátalos como cualquier dependencia y revísalos antes de ejecutarlos sobre contenido de terceros.

### 31.3.5 Limitaciones

- No todos los dialectos se interpretan igual: especifica `-f gfm`, `-f commonmark` o el formato adecuado.
- Las extensiones (notas al pie, definiciones, matemáticas) deben estar activadas en el lector correspondiente.
- La conversión **no es bidireccional sin pérdidas**.
- La salida PDF depende de fuentes y paquetes instalados.
- Algunos writers no admiten todas las estructuras (por ejemplo, RTF y ciertos tipos de tablas o notas).

## 31.4 Cómo elegir el destino

| Necesidad | Destino recomendado | Por qué |
|---|---|---|
| Publicar en web con diseño propio | HTML + CSS | Control total y carga rápida |
| Documento imprimible con fórmulas | PDF vía LaTeX | Tipografía y matemáticas de calidad |
| Documento editable por terceros | DOCX u ODT | Formatos de oficina estándar |
| Libro para lectores electrónicos | EPUB | Texto reflowable y metadatos |
| Integrarse en un proyecto LaTeX | LaTeX | Control fino y ecosistema académico |
| Demo de terminal o tutorial | Vídeo/GIF | Muestra interacción real |
| Charla o clase | Presentaciones | Diapositivas navegables |
| Diagrama o captura | SVG/PNG | Se incrusta en cualquier documento |

## 31.5 Criterios de calidad

1. **Fidelidad estructural**: títulos, listas y tablas conservan su jerarquía.
2. **Tipografía**: fuentes con glifos para todos los caracteres, interlineado y márgenes correctos.
3. **Accesibilidad**: jerarquía de encabezados, texto alternativo, tablas con cabeceras y enlaces descriptivos.
4. **Navegación**: índice, anclas, enlaces internos y paginación funcionan.
5. **Mantenibilidad**: plantillas, estilos y scripts versionados junto al contenido.
6. **Reproducibilidad**: la misma orden produce el mismo resultado en otra máquina.

## 31.6 Errores frecuentes al exportar

| Síntoma | Causa probable | Solución |
|---|---|---|
| Acentos o emoji rotos en PDF | Fuente sin glifos o motor `pdflatex` | Usa `xelatex`/`lualatex` y una fuente Unicode |
| Tablas desbordadas | Ancho fijo o contenido largo | CSS con `overflow`, tablas simples o `longtable` |
| Imágenes que no aparecen | Ruta relativa incorrecta | `--resource-path` o rutas desde la raíz |
| Diagramas Mermaid como código | El conversor no los renderiza | Pre-renderiza a SVG/PNG |
| Índice vacío | Encabezados no jerárquicos o `--toc` ausente | Corrige niveles y añade `--toc` |
| Estilos distintos en DOCX | Plantilla de referencia ausente | `--reference-doc` |
| Saltos de página imprevistos | Márgenes o estilos del destino | Ajusta CSS, plantilla o LaTeX |
| Enlaces internos rotos | Anclas renumeradas o IDs distintos | Verifica IDs y usa enlaces relativos |

## 31.7 Lista de comprobación antes de exportar

- [ ] El Markdown valida (sin vallas sin cerrar ni tablas mal formadas).
- [ ] El dialecto de entrada está especificado.
- [ ] Los encabezados siguen una jerarquía coherente.
- [ ] Las imágenes existen, tienen `alt` y un tamaño razonable.
- [ ] Los diagramas están pre-renderizados si el destino no los soporta.
- [ ] Los metadatos (título, autor, idioma, fecha) están completos.
- [ ] La plantilla o el CSS está versionado.
- [ ] El resultado se ha revisado en el formato final, no solo en el editor.
- [ ] Los enlaces y el índice funcionan en el archivo exportado.

---

[← 30. Editores Markdown](30-editores-markdown.md) · [Índice general](README.md) · [32. Exportación a HTML →](32-exportacion-a-html.md)
