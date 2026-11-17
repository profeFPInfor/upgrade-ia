# 40. Exportación a imágenes y otros destinos

> [← Índice general](README.md) · Capítulo 40 de 63

Además de documentos, Markdown alimenta **diagramas, capturas, wikis y plataformas de documentación**. Este capítulo cubre la exportación a imágenes y los destinos que no encajan en los capítulos anteriores.

## 40.1 Imágenes: SVG, PNG, JPEG y WebP

| Formato | Cuándo usarlo | Ventajas | Limitaciones |
|---|---|---|---|
| **SVG** | Diagramas, iconos, logotipos | Escalable, texto nítido, ligero | Soporte variable; puede incluir scripts |
| **PNG** | Capturas, diagramas con transparencia | Sin pérdida, transparencia | Archivos grandes |
| **JPEG** | Fotografías | Compresión eficiente | Sin transparencia; artefactos |
| **WebP** | Web moderna | Buena compresión y transparencia | Compatibilidad algo menor |

Para documentación técnica, **SVG** es la primera opción en diagramas y **PNG** en capturas. Si el destino no admite SVG (algunos lectores de EPUB o visores antiguos), exporta también PNG.

## 40.2 Diagramas como código

### 40.2.1 Mermaid CLI

```bash
npm install -g @mermaid-js/mermaid-cli

mmdc -i diagrama.mmd -o diagrama.svg
mmdc -i diagrama.mmd -o diagrama.png -w 1600 -b transparent
mmdc -i diagrama.mmd -o diagrama.pdf
```

| Opción | Efecto |
|---|---|
| `-w`, `-H` | Ancho y alto |
| `-b` | Color de fondo (`transparent`, `white`, `#ffffff`) |
| `-t` | Tema (`default`, `dark`, `forest`, `neutral`) |
| `-s` | Escala (por ejemplo, `-s 2` para alta densidad) |
| `-c` | Archivo de configuración |

- Mermaid CLI: <https://github.com/mermaid-js/mermaid-cli>

### 40.2.2 PlantUML

```bash
java -jar plantuml.jar diagrama.puml -tsvg
java -jar plantuml.jar diagrama.puml -tpng
```

- PlantUML: <https://plantuml.com/>

### 40.2.3 Graphviz

```bash
dot -Tsvg diagrama.dot -o diagrama.svg
dot -Tpng -Gdpi=200 diagrama.dot -o diagrama.png
```

- Graphviz: <https://graphviz.org/>

### 40.2.4 D2

```bash
d2 diagrama.d2 diagrama.svg
d2 --theme=200 diagrama.d2 diagrama.png
```

- D2: <https://d2lang.com/>

### 40.2.5 Diagramas dibujados

- **draw.io / diagrams.net**: exporta SVG/PNG y guarda el fuente `.drawio`.
- **Excalidraw**: estilo dibujado a mano; exporta PNG/SVG.
- **Inkscape**: edición vectorial; exporta PNG con `--export-type=png`.
- **Figma**: diseño colaborativo; exporta PNG/SVG/PDF.

Consejo: guarda siempre el **archivo fuente** del diagrama junto a la imagen exportada. Así se puede corregir sin redibujarlo.

## 40.3 Capturas de pantalla automatizadas

Para documentación que cambia con frecuencia, automatiza las capturas:

```bash
# shot-scraper (Python)
shot-scraper https://ejemplo.com -o captura.png

# Con espera y tamaño de ventana
shot-scraper https://ejemplo.com -o captura.png --wait 2000 --width 1280 --height 800
```

- `shot-scraper`: <https://github.com/simonw/shot-scraper>

Con Playwright o Puppeteer puedes capturar secciones concretas y generar varias imágenes en un script:

```javascript
await page.screenshot({ path: "captura.png", fullPage: true });
```

Ventajas: capturas reproducibles y actualizadas en CI. Limitaciones: requieren navegador y credenciales si la página es privada.

## 40.4 Convertir y optimizar imágenes

```bash
# Redimensionar y convertir a WebP
magick entrada.png -resize 1200x -strip -quality 85 salida.webp

# Convertir SVG a PNG
rsvg-convert -w 1600 diagrama.svg -o diagrama.png

# Inkscape
inkscape diagrama.svg --export-type=png --export-filename=diagrama.png
```

- ImageMagick: <https://imagemagick.org/>
- librsvg (`rsvg-convert`): <https://gitlab.gnome.org/GNOME/librsvg>
- Inkscape: <https://inkscape.org/>

Buenas prácticas:

- Exporta al **doble de resolución** si la imagen se verá en pantallas de alta densidad.
- Elimina metadatos (`-strip`) antes de publicar.
- Usa nombres descriptivos y sin espacios.
- No reescales una captura hacia arriba: pierde nitidez.

## 40.5 Incrustar imágenes en Markdown

```markdown
![Diagrama de arquitectura](img/arquitectura.svg)
```

Con HTML para controlar tamaño y tema:

```html
<img src="img/arquitectura.svg" alt="Diagrama de arquitectura"
     width="800" loading="lazy">
```

En Pandoc se pueden usar atributos:

```markdown
![Diagrama](img/arquitectura.svg){width=80%}
```

Recomendaciones:

- El texto alternativo describe **qué muestra** la imagen, no “imagen” ni el nombre del archivo.
- No incluyas texto importante solo dentro de la imagen.
- Para diagramas, añade una descripción textual o una tabla equivalente.
- En SVG, usa `<title>` y `<desc>`; muchos lectores los aprovechan.

## 40.6 Notion

Notion importa Markdown y conserva títulos, listas, tablas, código y enlaces. Limitaciones:

- Las bases de datos, relaciones y vistas no existen en Markdown.
- Los enlaces tipo wiki (`[[nota]]`) no se convierten en relaciones de Notion.
- Las imágenes locales deben subirse o incluirse en la importación.
- El HTML incrustado puede ignorarse.
- La exportación de Notion a Markdown pierde parte de la estructura y los colores.

Flujo recomendado: Markdown como fuente, importación puntual y revisión manual de la estructura.

## 40.7 Confluence

Confluence usa un formato propio (storage format) basado en XHTML. Herramientas como `mark` convierten Markdown a ese formato:

```bash
mark -f documento.md
```

- `mark`: <https://github.com/kovetskiy/mark>

Limitaciones: macros, paneles y layouts de Confluence no se generan desde Markdown; las tablas y los attachments requieren revisión.

## 40.8 Wikis, foros y plataformas

| Destino | Entrada | Notas |
|---|---|---|
| **MediaWiki** | `pandoc -t mediawiki` | Plantillas y extensiones no portables |
| **Discourse** | Markdown | Soporte amplio; algunas extensiones propias |
| **Reddit** | Markdown | Subconjunto; tablas y HTML limitados |
| **GitHub Discussions** | GFM | Igual que issues/PR |
| **Jira** | `pandoc -t jira` | Markup propio |
| **Notion** | Importación | Bases de datos no portables |
| **Confluence** | `mark` / storage format | Macros específicas |
| **GitBook / ReadMe** | Markdown + configuración | Estructura propia (sumarios, navegación) |

En todos los casos, comprueba el resultado **en la plataforma**, no solo en el archivo generado.

## 40.9 Documentación como producto

Si el destino es un portal de documentación (GitBook, ReadMe, Docusaurus, MkDocs), Markdown es la entrada, pero el portal añade:

- Navegación y jerarquía.
- Búsqueda.
- Versionado.
- Componentes interactivos.
- Analítica.

Conviene mantener el contenido en Markdown estándar y aislar las extensiones del portal en la capa de presentación. Así se puede migrar de herramienta sin reescribir el texto.

## 40.10 Lista de comprobación

- [ ] El formato de imagen es el adecuado para el destino.
- [ ] La imagen tiene resolución suficiente y no pesa de más.
- [ ] Existe el archivo fuente del diagrama.
- [ ] El texto alternativo es descriptivo.
- [ ] Las capturas no muestran datos personales.
- [ ] El destino admite las estructuras utilizadas.
- [ ] Se ha revisado el resultado en la plataforma final.

---

[← 39. Exportación a presentaciones](39-exportacion-a-presentaciones.md) · [Índice general](README.md) · [41. Matemáticas y notación científica →](41-matematicas-y-notacion-cientifica.md)
