# 35. Exportación a EPUB

> [← Índice general](README.md) · Capítulo 35 de 63

EPUB es el formato abierto de libros electrónicos. Por dentro es una **carpeta comprimida** con capítulos en XHTML, CSS, imágenes, metadatos y un índice de navegación. Markdown encaja bien porque el texto ya está estructurado en capítulos y párrafos.

## 35.1 Anatomía de un EPUB

| Parte | Función |
|---|---|
| `mimetype` | Identifica el archivo como EPUB |
| `META-INF/container.xml` | Señala el archivo `.opf` |
| `content.opf` | Metadatos, manifiesto y orden de lectura |
| `nav.xhtml` | Índice de navegación (EPUB 3) |
| `*.xhtml` | Capítulos y secciones |
| `*.css` | Estilos |
| `images/`, `fonts/` | Recursos |

Un EPUB válido no es un ZIP con HTML: debe cumplir la especificación **EPUB 3** y declarar metadatos, orden de lectura y navegación.

- Especificación EPUB 3.3: <https://www.w3.org/TR/epub-33/>
- Accesibilidad EPUB: <https://www.w3.org/TR/epub-a11y-11/>

## 35.2 Conversión con Pandoc

```bash
pandoc manual.md -o manual.epub \
  --toc --toc-depth=2 \
  --epub-cover-image=img/portada.jpg \
  --epub-metadata=metadata.xml \
  --css=epub.css \
  --split-level=1 \
  --metadata title="Manual de usuario" \
  --metadata author="Equipo de documentación" \
  --metadata lang=es
```

| Opción | Efecto |
|---|---|
| `--epub-cover-image` | Portada |
| `--epub-metadata` | Metadatos adicionales en XML |
| `--epub-embed-font` | Embebe una fuente |
| `--css` | Hoja de estilo del libro |
| `--toc-depth` | Profundidad del índice |
| `--split-level` | Nivel de encabezado en el que se divide cada archivo |
| `--mathml` | Matemáticas como MathML |

## 35.3 Metadatos

`metadata.xml` sigue el esquema de Dublin Core:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/"
          xmlns:opf="http://www.idpf.org/2007/opf">
  <dc:title>Manual de usuario</dc:title>
  <dc:creator opf:role="aut">Equipo de documentación</dc:creator>
  <dc:language>es</dc:language>
  <dc:identifier id="pub-id">urn:uuid:12345678-1234-1234-1234-123456789abc</dc:identifier>
  <dc:date>2026-10-28</dc:date>
  <dc:publisher>Mi editorial</dc:publisher>
  <dc:rights>CC BY 4.0</dc:rights>
  <dc:description>Guía de referencia sobre Markdown.</dc:description>
  <meta property="dcterms:modified">2026-10-28T00:00:00Z</meta>
</metadata>
```

- `dc:identifier` debe ser único y estable; un UUID o un ISBN.
- `dc:language` usa etiquetas BCP 47 (`es`, `es-MX`, `en`).
- `dcterms:modified` es obligatorio en EPUB 3 y debe estar en UTC.
- La portada debe ser una imagen de alta resolución, sin texto pequeño.

## 35.4 CSS para lectores electrónicos

Los lectores aplican sus propias preferencias de fuente, tamaño y tema. El CSS debe ser **flexible**, no una maqueta fija.

```css
body {
  font-family: serif;
  line-height: 1.6;
  margin: 0;
  padding: 0;
}

h1, h2, h3 {
  line-height: 1.25;
  page-break-after: avoid;
  break-after: avoid;
}

p {
  margin: 0 0 0.8em;
  orphans: 2;
  widows: 2;
  text-align: justify;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-size: 0.85em;
}

img {
  max-width: 100%;
  height: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9em;
}
```

Recomendaciones:

- Usa unidades relativas (`em`, `%`), no píxeles fijos.
- Evita `position: fixed`, `vh`/`vw` y diseños de varias columnas.
- No dependas de `flex` o `grid` para la estructura principal.
- Define `page-break-before: always` en los títulos de capítulo si quieres que empiecen en página nueva.
- Prueba en modo claro y oscuro, con tamaño de fuente grande y con fuente del sistema.

## 35.5 Imágenes y diagramas

- **Portada**: JPG o PNG de alta resolución; ratio vertical habitual (por ejemplo, 1.6:1).
- **Ilustraciones**: PNG para capturas y diagramas con texto; JPG para fotografías.
- **SVG**: útil y ligero, pero el soporte varía entre lectores. Para máxima compatibilidad, exporta también PNG.
- **Mermaid**: pre-renderiza a SVG o PNG; el lector no ejecuta JavaScript.
- **Texto alternativo**: obligatorio para accesibilidad; Pandoc lo toma del `alt` de Markdown.

## 35.6 Matemáticas y código

- EPUB 3 admite **MathML**; Pandoc puede generarlo con `--mathml`.
- Algunos lectores renderizan mal MathML; para fórmulas complejas, valora imágenes de alta resolución con texto alternativo.
- El código debe usar `white-space: pre-wrap` para no desbordar en pantallas pequeñas.
- Evita líneas de más de 70 caracteres.
- El resaltado de sintaxis puede depender de CSS; comprueba que los colores tienen contraste en modo oscuro.

## 35.7 Validación y pruebas

| Herramienta | Uso |
|---|---|
| **EPUBCheck** | Valida la estructura y la especificación |
| **Kindle Previewer** | Simula la conversión y la lectura en Kindle |
| **Calibre** | Convierte, edita y previsualiza |
| **Thorium Reader** | Lector de referencia en escritorio |
| **Apple Books** | Prueba en macOS/iOS |
| **Lectores móviles** | Comprueba tamaño, reflejo y navegación |

```bash
# EPUBCheck (Java)
java -jar epubcheck.jar manual.epub
```

- EPUBCheck: <https://github.com/w3c/epubcheck>
- Calibre: <https://calibre-ebook.com/>
- Sigil: <https://sigil-ebook.com/>

## 35.8 Kindle y otras tiendas

- Amazon **Send to Kindle** acepta EPUB; la tienda convierte el archivo a su formato interno.
- KDP acepta EPUB y DOCX, pero revisa el resultado en Kindle Previewer antes de publicar.
- Apple Books, Kobo y Google Play Books tienen sus propios requisitos de metadatos, portada y derechos.
- No incluyas fuentes con licencia restrictiva sin comprobar que permiten su incrustación.

## 35.9 Accesibilidad

- Índice de navegación completo y jerárquico.
- Idioma declarado en el documento y en los fragmentos en otro idioma.
- Texto alternativo en todas las imágenes.
- Tablas con cabeceras y sin celdas vacías innecesarias.
- Orden de lectura lógico.
- Contraste suficiente y posibilidad de aumentar el tamaño del texto.
- Evita texto incrustado en imágenes.

## 35.10 Lista de comprobación

- [ ] Título, autor, idioma e identificador están definidos.
- [ ] La portada tiene resolución suficiente.
- [ ] El índice refleja la jerarquía real.
- [ ] El CSS funciona en pantallas pequeñas y en modo oscuro.
- [ ] Las imágenes tienen `alt` y no desbordan.
- [ ] Las fórmulas y los diagramas se ven correctamente.
- [ ] El EPUB pasa EPUBCheck.
- [ ] Se ha probado en al menos dos lectores distintos.

---

[← 34. Exportación a DOCX y ODT](34-exportacion-a-docx-y-odt.md) · [Índice general](README.md) · [36. Exportación a LaTeX →](36-exportacion-a-latex.md)
