# 39. Exportación a presentaciones

> [← Índice general](README.md) · Capítulo 39 de 63

Markdown también sirve para preparar **diapositivas**: se escribe el contenido en texto plano y la herramienta se encarga del diseño, la navegación y la exportación a HTML, PDF o PPTX. Es una forma cómoda de mantener charlas versionadas y reutilizar material de la documentación.

## 39.1 Herramientas principales

| Herramienta | Entrada | Salidas | Enfoque |
|---|---|---|---|
| **Marp** | Markdown + Front Matter | HTML, PDF, PPTX, imágenes | Sencillo, basado en CSS |
| **Slidev** | Markdown + Vue | HTML, PDF, PPTX | Presentaciones web interactivas |
| **reveal.js** | Markdown o HTML | HTML | Navegación y temas web |
| **Pandoc** | Markdown | reveal.js, PPTX, Beamer | Conversión desde el mismo documento |
| **Beamer** | Markdown → LaTeX | PDF | Académico y matemático |
| **presenterm** | Markdown | Terminal | Charlas en terminal |

## 39.2 Marp

Marp convierte Markdown en diapositivas. El Front Matter activa el modo presentación:

```markdown
---
marp: true
theme: default
paginate: true
---

# Introducción a Markdown

## Qué es

Texto plano con estructura.

---

## Sintaxis

- Títulos
- Listas
- Enlaces
```

Las diapositivas se separan con `---`. Instalación y uso:

```bash
npm install -g @marp-team/marp-cli

marp slides.md -o slides.html
marp slides.md -o slides.pdf
marp slides.md -o slides.pptx
marp slides.md --images png
```

Opciones útiles:

| Opción | Efecto |
|---|---|
| `--html` | Permite HTML dentro de las diapositivas |
| `--pdf` | Exporta a PDF |
| `--pptx` | Exporta a PowerPoint |
| `--images png` | Genera una imagen por diapositiva |
| `--theme tema.css` | Usa un tema propio |
| `--allow-local-files` | Permite imágenes locales |

Notas del presentador:

```markdown
## Diapositiva

Contenido visible.

<!-- Nota solo para quien presenta. -->
```

- Marp: <https://marp.app/>
- CLI: <https://github.com/marp-team/marp-cli>

## 39.3 Slidev

Slidev está pensado para presentaciones web con componentes Vue, resaltado de código y modo presentador.

```bash
npm init slidev
npm run dev
npm run build
npx slidev export --format pdf
```

Estructura:

````markdown
---
theme: default
title: Introducción a Markdown
highlighter: shiki
---

# Introducción a Markdown

---

## Código

```python
def saludo(nombre):
    return f"Hola, {nombre}"
```
````

Características:

- **Layouts** (`cover`, `center`, `two-cols`…).
- **Resaltado de código** con Shiki y animaciones por líneas.
- **Modo presentador** con notas y vista previa.
- **Componentes Vue** para interactividad.
- Exportación a PDF, PPTX o imágenes (según versión y plugins).

- Slidev: <https://sli.dev/>

## 39.4 reveal.js con Pandoc

```bash
pandoc charla.md -t revealjs -s \
  --slide-level=2 \
  -V theme=white \
  -V transition=slide \
  -o charla.html
```

| Opción | Efecto |
|---|---|
| `-t revealjs` | Genera una presentación reveal.js |
| `--slide-level=2` | Nivel de encabezado que crea diapositivas |
| `-V theme=…` | Tema (`white`, `black`, `league`, `beige`, `sky`, `night`, `serif`, `simple`, `solarized`, `moon`, `dracula`…) |
| `-V transition=…` | Transición (`none`, `fade`, `slide`, `convex`, `concave`, `zoom`) |
| `-V controls=true` | Muestra controles |
| `-V progress=true` | Barra de progreso |

Separación vertical y notas:

```markdown
## Diapositiva

Contenido.

--

### Subdiapositiva

Más contenido.

::: notes
Esto solo lo ve el presentador.
:::
```

- reveal.js: <https://revealjs.com/>
- Documentación de Pandoc: <https://pandoc.org/MANUAL.html#slide-shows>

## 39.5 PowerPoint con Pandoc

```bash
pandoc charla.md -t pptx -o charla.pptx \
  --reference-doc=plantilla.pptx \
  --slide-level=2
```

- Cada encabezado del nivel indicado crea una diapositiva.
- La plantilla PPTX define fuentes, colores y diseños.
- Las notas del presentador se pueden incluir con bloques de notas.
- Las animaciones y transiciones complejas no se generan desde Markdown.

## 39.6 Beamer

```bash
pandoc charla.md -t beamer -s --pdf-engine=xelatex -o charla.pdf
```

Beamer es la opción académica habitual: matemáticas, teoremas, referencias y plantillas institucionales. Requiere LaTeX y una plantilla adecuada. Véase el capítulo [36](36-exportacion-a-latex.md).

## 39.7 presenterm

Para charlas en terminal:

```bash
presenterm charla.md
```

Presenta Markdown con resaltado de código y navegación por teclado. Útil para demos técnicas en vivo, no para audiencias que esperan diapositivas tradicionales.

- presenterm: <https://github.com/mfontanini/presenterm>

## 39.8 Diseño de diapositivas

1. **Una idea por diapositiva**: si necesita dos, divide.
2. **Poco texto**: la diapositiva acompaña, no sustituye a la explicación.
3. **Código legible**: 12–16 líneas como máximo y fuente grande.
4. **Contraste**: comprueba el proyector y el modo claro/oscuro.
5. **Imágenes con `alt`**: también en presentaciones.
6. **Números de diapositiva**: ayudan a las preguntas.
7. **Notas del presentador**: guion, no párrafos para leer.
8. **Consistencia**: mismos márgenes, tipografía y colores.

## 39.9 Exportar a PDF y a vídeo

- **PDF**: formato de respaldo y de distribución; conserva el diseño y funciona sin conexión.
- **PPTX**: útil si la organización exige PowerPoint editable.
- **HTML**: mantiene interactividad, enlaces y animaciones.
- **Vídeo**: graba la presentación con OBS o exporta desde PowerPoint; añade subtítulos (capítulo [38](38-exportacion-a-video.md)).

## 39.10 Problemas frecuentes

| Problema | Causa | Solución |
|---|---|---|
| El código se sale de la diapositiva | Líneas largas o fuente grande | Acorta el código y usa `font-size` menor |
| Las imágenes no aparecen | Rutas relativas al directorio de ejecución | Usa rutas desde la raíz o `--allow-local-files` |
| El PDF pierde animaciones | El formato PDF es estático | Exporta HTML o graba vídeo |
| Las notas no se ven | La herramienta no las exporta a PPTX | Revisa la compatibilidad de notas |
| Fuentes distintas | La fuente no está instalada en el destino | Usa fuentes web o incrusta |
| Texto ilegible en el proyector | Poco contraste o tamaño pequeño | Aumenta tamaño y contraste |

## 39.11 Lista de comprobación

- [ ] Cada diapositiva tiene una idea principal.
- [ ] El texto se lee desde el fondo de la sala.
- [ ] El código cabe y tiene resaltado legible.
- [ ] Las imágenes tienen texto alternativo y buena resolución.
- [ ] Hay versión PDF de respaldo.
- [ ] Las notas del presentador están escritas.
- [ ] Los enlaces funcionan en la versión HTML.
- [ ] Se ha probado en el equipo y el proyector reales.

---

[← 38. Exportación a vídeo](38-exportacion-a-video.md) · [Índice general](README.md) · [40. Exportación a imágenes y otros destinos →](40-exportacion-a-imagenes-y-otros-destinos.md)
