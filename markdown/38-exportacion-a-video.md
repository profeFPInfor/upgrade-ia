# 38. Exportación a vídeo

> [← Índice general](README.md) · Capítulo 38 de 63

Markdown **no se exporta a vídeo** con un comando equivalente a `pandoc -o video.mp4`. El vídeo se produce a partir de lo que el documento muestra: una página renderizada, una demo de terminal, una animación de diagramas o una presentación. Markdown actúa como **guion y fuente de verdad**; la grabación es un paso posterior.

Este capítulo explica qué formatos usar, cómo grabarlos, cómo comprimirlos y cómo incrustarlos en documentación sin arruinar el rendimiento ni la accesibilidad.

## 38.1 Qué se puede convertir en vídeo

| Origen | Herramienta típica | Resultado |
|---|---|---|
| Página web renderizada | OBS, captura de pantalla | Tutorial navegando por la documentación |
| Terminal | asciinema, VHS, Terminalizer | Demo de comandos |
| Diagramas animados | Manim, Motion Canvas, Remotion | Explicación visual |
| Diapositivas | PowerPoint, OBS, grabador de pantalla | Charla o clase |
| Capturas de interfaz | ScreenToGif, LICEcap, Peek | GIF de un flujo corto |
| Fragmento de una grabación | ffmpeg | Recorte, compresión y conversión |

## 38.2 Formatos: GIF, MP4 y WebM

| Formato | Ventajas | Limitaciones | Uso recomendado |
|---|---|---|---|
| **GIF** | Se reproduce en todas partes, sin controles | 256 colores, sin audio, archivos grandes | Demos muy cortas (<10 s) en README |
| **MP4 (H.264/AAC)** | Compatibilidad amplia, buen tamaño, audio | Códec con patentes en algunos contextos | Vídeo principal en web y documentación |
| **WebM (VP9/Opus)** | Buena compresión, abierto | Soporte algo menor en navegadores antiguos | Fuente alternativa junto a MP4 |
| **AV1** | Compresión superior | Codificación más lenta y soporte irregular | Archivos grandes, cuando el destino lo admite |

La estrategia habitual es ofrecer **MP4 y WebM** con `<video>` y dejar un **GIF** solo para casos donde no se puede usar HTML.

## 38.3 Grabar la pantalla

| Herramienta | Plataforma | Notas |
|---|---|---|
| **OBS Studio** | Windows, macOS, Linux | Gratuito, potente, grabación de ventana o región |
| **ScreenToGif** | Windows | Editor de frames; exporta GIF, APNG y MP4 |
| **LICEcap** | Windows, macOS | GIF sencillo de una región |
| **Peek** | Linux | GIF/MP4 de una región |
| **Captura del sistema** | macOS (`Cmd` + `Shift` + `5`), Windows (`Win` + `G`) | Rápida, sin edición avanzada |

Consejos de grabación:

1. **Prepara el escenario**: cierra notificaciones, usa una ventana limpia y un tamaño estable.
2. **Graba a 30 fps** salvo que necesites movimiento rápido; 60 fps multiplica el peso.
3. **Usa 1280×720 o 1920×1080**; evita escalar después.
4. **Guioniza**: qué se va a mostrar, qué se escribe y cuánto dura.
5. **Graba sin audio** si no hay narración; añade música o voz en la edición.
6. **No muestres datos personales**: blurrea correos, tokens, rutas privadas y nombres.

## 38.4 Grabar la terminal

### 38.4.1 asciinema

```bash
# Instalar y grabar
asciinema rec demo.cast

# Reproducir
asciinema play demo.cast

# Convertir a GIF con agg
agg demo.cast demo.gif
```

`asciinema` guarda una transcripción ligera y reproducible; `agg` la convierte en GIF o vídeo. Ventaja: el texto es nítido y el archivo `.cast` se puede versionar.

- asciinema: <https://asciinema.org/>
- Documentación: <https://docs.asciinema.org/>
- agg: <https://github.com/asciinema/agg>

### 38.4.2 VHS

VHS graba terminales a partir de un guion `.tape`:

```text
Output demo.gif
Set FontSize 18
Set Width 1200
Set Height 600
Set Theme "Dracula"

Type "echo 'Hola, Markdown'"
Enter
Sleep 1s
Type "pandoc README.md -o README.html"
Enter
Sleep 2s
```

```bash
vhs demo.tape
```

Ventaja: la demo es **reproducible** y se regenera con el código. Ideal para documentación que cambia.

- VHS: <https://github.com/charmbracelet/vhs>

### 38.4.3 Terminalizer

```bash
npm install -g terminalizer
terminalizer record demo
terminalizer render demo
```

Genera GIF o vídeo a partir de una grabación de terminal. Menos reproducible que VHS, pero cómodo para demos puntuales.

- Terminalizer: <https://github.com/faressoft/terminalizer>

## 38.5 Animar diagramas

- **Manim**: animaciones matemáticas y explicaciones técnicas; <https://www.manim.community/>.
- **Motion Canvas**: animaciones programadas con TypeScript; <https://motioncanvas.io/>.
- **Remotion**: vídeo con React; <https://www.remotion.dev/>.
- **Mermaid CLI**: genera SVG, PNG y PDF, **no vídeo**; para animar hay que crear una secuencia de imágenes o usar otra herramienta.

Flujo típico:

```text
guion → animación → render de frames → ffmpeg → MP4/WebM
```

Manim, por ejemplo, renderiza una escena a MP4:

```bash
manim -pql escena.py MiEscena
```

`-ql` produce baja calidad para previsualizar; `-qh` alta calidad para la versión final.

## 38.6 Convertir y comprimir con ffmpeg

`ffmpeg` es la navaja suiza de la conversión de vídeo: <https://ffmpeg.org/>.

### 38.6.1 MP4 compatible

```bash
ffmpeg -i entrada.mov \
  -c:v libx264 -preset medium -crf 23 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  -c:a aac -b:a 128k \
  salida.mp4
```

- `-crf 23` equilibra calidad y tamaño (menor valor, más calidad).
- `-pix_fmt yuv420p` maximiza compatibilidad.
- `+faststart` permite reproducir antes de descargar todo.
- `-an` elimina el audio.

### 38.6.2 WebM

```bash
ffmpeg -i entrada.mp4 \
  -c:v libvpx-vp9 -crf 32 -b:v 0 \
  -c:a libopus -b:a 96k \
  salida.webm
```

### 38.6.3 Recortar, escalar y acelerar

```bash
# Del segundo 5 al 20
ffmpeg -ss 00:00:05 -to 00:00:20 -i entrada.mp4 -c copy recorte.mp4

# Escalar a 1280 px de ancho
ffmpeg -i entrada.mp4 -vf "scale=1280:-2" salida.mp4

# Doble velocidad (vídeo y audio)
ffmpeg -i entrada.mp4 \
  -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" \
  -map "[v]" -map "[a]" rapido.mp4
```

### 38.6.4 GIF con paleta

Un GIF directo pierde calidad y pesa demasiado. Genera una paleta óptima:

```bash
ffmpeg -i entrada.mp4 \
  -vf "fps=15,scale=960:-1:flags=lanczos,palettegen" paleta.png

ffmpeg -i entrada.mp4 -i paleta.png \
  -lavfi "fps=15,scale=960:-1:flags=lanczos[x];[x][1:v]paletteuse" \
  -loop 0 salida.gif
```

Para reducir aún más el peso:

- Baja a 10–12 fps.
- Reduce el ancho a 640–800 px.
- Recorta la duración a 5–10 s.
- Optimiza con `gifsicle`: <https://www.lcdf.org/gifsicle/>.

### 38.6.5 Miniatura y subtítulos

```bash
# Miniatura en el segundo 2
ffmpeg -ss 00:00:02 -i salida.mp4 -frames:v 1 miniatura.png

# Incrustar subtítulos WebVTT en MP4
ffmpeg -i salida.mp4 -i subtitulos.vtt -c copy -c:s mov_text salida-con-subtitulos.mp4
```

## 38.7 Incrustar vídeo en Markdown

### 38.7.1 HTML5

```html
<video controls muted loop playsinline
       preload="metadata"
       poster="img/demo-miniatura.png"
       width="800">
  <source src="video/demo.webm" type="video/webm">
  <source src="video/demo.mp4" type="video/mp4">
  <track kind="captions" src="video/demo.vtt"
         srclang="es" label="Español" default>
  Tu navegador no admite vídeo HTML5.
  <a href="video/demo.mp4">Descargar el vídeo</a>.
</video>
```

- `controls`: controles nativos; no los ocultes.
- `muted` y `loop`: útil para demos decorativas; no las inicies con sonido.
- `playsinline`: evita pantalla completa automática en iOS.
- `poster`: imagen antes de reproducir.
- `preload="metadata"`: no descarga todo el archivo.
- `<track>`: subtítulos y descripciones.
- El texto de respaldo y el enlace son imprescindibles.

### 38.7.2 GIF

```markdown
![Demo de la instalación](img/instalacion.gif)
```

Ventaja: funciona en cualquier visor de Markdown. Desventaja: peso y falta de controles.

### 38.7.3 Miniatura enlazada

Para vídeos largos, aloja el archivo en una plataforma y enlaza una miniatura:

```markdown
[![Ver la demo en vídeo](img/miniatura.png)](https://www.youtube.com/watch?v=ID_DEL_VIDEO)
```

No inventes un ID: usa la URL real del vídeo publicado.

## 38.8 Limitaciones por plataforma

| Plataforma | Comportamiento |
|---|---|
| **GitHub** | El HTML se sanea; `<video>` no se reproduce en README. Los vídeos adjuntos en issues, PR y discusiones sí se pueden subir. Para README, usa GIF o un enlace. |
| **GitLab** | Admite adjuntos multimedia; comprueba la sintaxis y el tamaño máximo. |
| **VS Code** | La vista previa puede no reproducir vídeo; el HTML se muestra de forma limitada. |
| **Sitios estáticos** | Depende del HTML permitido y del CSS del tema. |
| **PDF/DOCX/EPUB** | El vídeo no se reproduce; solo se conserva una imagen o un enlace. |

Por eso el vídeo **nunca debe ser la única fuente de una información crítica**: añade una transcripción o unos pasos en texto.

## 38.9 Accesibilidad

- **Subtítulos** para todo audio con voz (WCAG 1.2.2).
- **Transcripción** con los pasos y la información relevante.
- **Audiodescripción** si lo visual es imprescindible (WCAG 1.2.3/1.2.5).
- No inicies el vídeo automáticamente con sonido.
- Respeta `prefers-reduced-motion`: evita animaciones que parpadean o se mueven sin control.
- Contraste suficiente y texto grande en la grabación.
- No pongas información solo en el color.
- Ofrece una versión en texto de los comandos que aparecen.

```css
@media (prefers-reduced-motion: reduce) {
  video[autoplay] { display: none; }
}
```

## 38.10 Flujo de trabajo recomendado

1. **Escribe el guion en Markdown**: pasos, comandos y resultado esperado.
2. **Prepara el entorno**: ventana limpia, datos ficticios, fuente legible.
3. **Graba** con OBS, asciinema o VHS.
4. **Edita**: recorta, acelera las pausas y añade subtítulos.
5. **Comprime** a MP4/WebM; genera GIF solo si hace falta.
6. **Incrusta** con `<video>`, GIF o miniatura enlazada.
7. **Añade** subtítulos, transcripción y texto alternativo.
8. **Verifica** en el destino real y en móvil.

## 38.11 Lista de comprobación

- [ ] El vídeo tiene un objetivo claro y dura lo necesario.
- [ ] No contiene datos personales ni secretos.
- [ ] Se entiende sin audio o tiene subtítulos.
- [ ] El archivo está comprimido y no bloquea la página.
- [ ] Hay una alternativa en texto.
- [ ] El formato se reproduce en el destino previsto.
- [ ] La miniatura y el texto alternativo son descriptivos.
- [ ] La licencia de música, fuentes e imágenes permite su uso.

---

[← 37. Exportación a RTF, TXT y otros formatos](37-exportacion-a-rtf-txt-y-otros-formatos.md) · [Índice general](README.md) · [39. Exportación a presentaciones →](39-exportacion-a-presentaciones.md)
