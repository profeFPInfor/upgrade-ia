# 34. Exportación a DOCX y ODT

> [← Índice general](README.md) · Capítulo 34 de 63

DOCX (Office Open XML) y ODT (OpenDocument Text) son los formatos de los procesadores de texto. Se exportan cuando el documento debe **editarse con Word, LibreOffice o Google Docs**, revisarse con control de cambios o integrarse en un circuito administrativo.

Markdown sigue siendo la fuente; el DOCX es un **artefacto de entrega**. Mantener esa separación evita que el documento final se convierta en la única copia del contenido.

## 34.1 Conversión básica

```bash
# DOCX
pandoc manual.md -o manual.docx --toc --number-sections

# ODT
pandoc manual.md -o manual.odt --toc --number-sections
```

Sin plantilla, Pandoc aplica estilos genéricos. El resultado es correcto pero probablemente no coincide con la identidad visual de la organización.

## 34.2 Plantilla de referencia

La clave para un DOCX presentable es `--reference-doc`: un documento de Word cuyos **estilos** se copian al resultado.

```bash
# Generar una plantilla con los estilos por defecto de Pandoc
pandoc -o referencia.docx --print-default-data-file reference.docx

# Usarla
pandoc manual.md -o manual.docx \
  --reference-doc=referencia.docx \
  --toc --number-sections
```

Para ODT:

```bash
pandoc -o referencia.odt --print-default-data-file reference.odt
pandoc manual.md -o manual.odt --reference-doc=referencia.odt
```

### 34.2.1 Estilos que debes revisar

Abre la plantilla en Word o LibreOffice y ajusta los estilos que Pandoc utiliza:

| Estilo | Se aplica a |
|---|---|
| `Title` | Título del documento |
| `Subtitle` | Subtítulo |
| `Author`, `Date` | Metadatos |
| `Heading 1`…`Heading 6` | Encabezados |
| `Body Text` | Párrafos |
| `First Paragraph` | Primer párrafo tras un encabezado |
| `Block Text` | Citas |
| `Source Code` | Bloques de código |
| `Verbatim Char` | Código en línea |
| `Table` | Tablas |
| `Image Caption` | Leyendas de imagen |
| `Table Caption` | Leyendas de tabla |
| `Footnote Text` | Notas al pie |

Si un estilo no existe, Pandoc usa uno equivalente o el estilo predeterminado.

### 34.2.2 Tipografía y página

En la plantilla se definen también:

- Tamaño de página (A4 o Letter), márgenes y orientación.
- Fuente principal y monoespaciada.
- Encabezado y pie de página.
- Numeración de páginas.
- Interlineado y espaciado entre párrafos.
- Sangría de primera línea.

No cambies el **nombre** de los estilos: Pandoc los busca por nombre. Puedes cambiar su apariencia, no su identidad.

## 34.3 Estructura y contenido

### 34.3.1 Índice y numeración

`--toc` inserta un índice nativo. Word puede mostrarlo como campo que hay que actualizar (botón derecho → **Actualizar campo** o `F9`). `--number-sections` numera los encabezados según su nivel.

### 34.3.2 Saltos de página

Markdown no tiene saltos de página. En DOCX se puede insertar OpenXML crudo:

````markdown
```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```
````

La sintaxis `{=openxml}` es un bloque crudo de Pandoc. También se puede conseguir un salto con un estilo de párrafo que tenga “salto antes” configurado en la plantilla.

### 34.3.3 Imágenes

```markdown
![Diagrama de red](img/red.png){width=12cm}
![Logotipo](img/logo.png){width=4cm}
```

En DOCX, `width` y `height` aceptan unidades (`cm`, `mm`, `in`, `pt`, `%`). Sin dimensiones, la imagen se inserta a su tamaño natural y puede desbordar la página.

Para figuras con leyenda, el texto alternativo se convierte en el texto alternativo de la imagen; la leyenda visible se escribe como párrafo o se controla con la plantilla.

### 34.3.4 Tablas

Pandoc convierte las tablas GFM en tablas de Word. Limitaciones habituales:

- El ancho de columna se calcula a partir del contenido; puede requerir ajuste manual.
- Las tablas muy anchas se salen del margen.
- Las celdas con párrafos múltiples o listas funcionan, pero el resultado varía.
- No hay `colspan` ni `rowspan` en Markdown estándar.

Para documentos con tablas complejas, valora HTML + CSS y PDF, o diseña la tabla en Word y mantenla fuera del flujo Markdown.

### 34.3.5 Código

Los bloques con lenguaje se convierten en párrafos `Source Code` y conservan el resaltado si la plantilla define los estilos de caracteres. El código en línea usa `Verbatim Char`.

Para código largo:

- Divide las líneas a 80–100 caracteres.
- Evita tabuladores; usa espacios.
- Comprueba que la fuente monoespaciada está disponible en Word.
- Si el documento se imprime, usa un tamaño de 9–10 pt.

## 34.4 DOCX → Markdown

La dirección inversa es útil para recuperar contenido heredado:

```bash
pandoc informe.docx -t gfm \
  --extract-media=media \
  --wrap=none \
  -o informe.md
```

- `--extract-media=media` guarda las imágenes en una carpeta y ajusta las rutas.
- `--track-changes=accept|reject|all` decide qué hacer con los cambios registrados.
- Los comentarios, cuadros de texto, SmartArt y gráficos no se convierten en Markdown estándar.
- Las tablas complejas pueden quedar como HTML incrustado.

La conversión no es reversible: si vuelves a DOCX, los estilos pueden cambiar.

## 34.5 LibreOffice en la cadena de conversión

LibreOffice puede convertir entre DOCX, ODT y PDF sin interfaz gráfica:

```bash
soffice --headless --convert-to pdf manual.docx
soffice --headless --convert-to odt manual.docx
soffice --headless --convert-to docx manual.odt
```

Ventajas: gratuito, multiplataforma y respeta plantillas. Limitaciones: la conversión puede alterar saltos, fuentes o tablas; revisa siempre el resultado.

- LibreOffice: <https://www.libreoffice.org/>

## 34.6 Flujo de trabajo recomendado

1. **Markdown como fuente de verdad** en el repositorio.
2. **Plantilla DOCX/ODT versionada** con los estilos corporativos.
3. **Script de exportación** reproducible (`make docx`, tarea de CI o comando documentado).
4. **Revisión en Word/LibreOffice** con control de cambios.
5. **Incorporar correcciones al Markdown**, no al DOCX, si el documento va a seguir evolucionando.
6. **Generar de nuevo** el DOCX para la entrega final.

Este flujo evita la deriva entre versiones y permite revisar el contenido como código.

## 34.7 Accesibilidad

- Usa **estilos de encabezado** reales, no negritas ni tamaños manuales.
- Añade texto alternativo a todas las imágenes.
- Marca la fila de encabezado de las tablas.
- Declara el idioma del documento en la plantilla.
- Evita tablas usadas solo para maquetar.
- Comprueba el orden de lectura con un lector de pantalla o el comprobador de accesibilidad de Word.

## 34.8 Limitaciones que conviene aceptar

| Elemento | Resultado en DOCX/ODT |
|---|---|
| Columnas de página | No se generan desde Markdown; se definen en la plantilla |
| Encabezados por sección | Requieren secciones de Word; no se expresan en Markdown |
| Notas al final | Dependen del procesador y de la plantilla |
| Comentarios | No forman parte de Markdown |
| Control de cambios | Se pierde al convertir; no es un formato de revisión |
| Ecuaciones | Se convierten, pero la edición posterior puede ser limitada |
| Diagramas Mermaid | No se renderizan; pre-renderiza a imagen |
| Campos y referencias cruzadas | No se generan de forma nativa |

## 34.9 Lista de comprobación

- [ ] La plantilla de referencia existe y está versionada.
- [ ] Los estilos tienen los nombres que Pandoc espera.
- [ ] El índice se actualiza en Word/LibreOffice.
- [ ] Las imágenes tienen tamaño y texto alternativo.
- [ ] Las tablas caben en la página.
- [ ] El código usa una fuente monoespaciada legible.
- [ ] Los encabezados usan estilos, no formato manual.
- [ ] El documento se ha abierto en el programa de destino final.

---

[← 33. Exportación a PDF](33-exportacion-a-pdf.md) · [Índice general](README.md) · [35. Exportación a EPUB →](35-exportacion-a-epub.md)
