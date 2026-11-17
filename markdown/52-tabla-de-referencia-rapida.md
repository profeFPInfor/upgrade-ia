# 52. Tabla de referencia rápida

> [← Índice general](README.md) · Capítulo 52 de 63

Esta *cheat sheet* reúne la sintaxis más importante. La columna **Notas** indica si la característica pertenece al núcleo, a GFM, a una extensión o a una plataforma concreta.

| Elemento | Sintaxis | Resultado | Notas |
|---|---|---|---|
| Título H1 | `# Título` | Título grande | Un H1 por documento |
| Título H2 | `## Título` | Subtítulo | Nivel 2 |
| Título H3–H6 | `### Título` … `###### Título` | Subtítulos | No saltar niveles |
| Título Setext | `Título` + línea `=====` | H1 | Solo H1/H2; menos usado |
| Título Setext H2 | `Título` + línea `-----` | H2 | Cuidado: `---` también es regla horizontal |
| Párrafo | Texto separado por una línea en blanco | Párrafo | Una línea en blanco entre bloques |
| Negrita | `**texto**` | **texto** | También `__texto__` |
| Cursiva | `*texto*` | *texto* | También `_texto_` |
| Negrita y cursiva | `***texto***` | ***texto*** | Combinación |
| Tachado | `~~texto~~` | ~~texto~~ | GFM; no CommonMark |
| Resaltado | `==texto==` | ==texto== | Extensión; no estándar |
| Superíndice | `^texto^` | ^texto^ | Extensión |
| Subíndice | `~texto~` | ~texto~ | Extensión; puede confundirse con tachado |
| Código en línea | Un backtick de apertura y otro de cierre | `código` | Para backticks internos, usa más backticks |
| Código con backticks | Dos backticks de apertura y cierre | Código con un backtick interno | Delimita con dos backticks |
| Bloque de código | Tres backticks, lenguaje, código y cierre | Bloque resaltado | Indica el lenguaje |
| Bloque indentado | Cuatro espacios al inicio | Bloque de código | Alternativa; menos explícita |
| Cita | `> texto` | Cita | Puede contener Markdown |
| Cita anidada | `>> texto` | Cita anidada | Añade un nivel |
| Lista no ordenada | `- elemento` | Viñeta | También `*` y `+` |
| Lista ordenada | `1. elemento` | Lista numerada | Los números se renumeran |
| Lista anidada | Sangría de 2–4 espacios | Subnivel | Sé consistente |
| Lista de tareas | `- [x] hecho` | ☑ hecho | GFM o extensión |
| Lista de definiciones | `Término` + línea `: definición` | Definición | Extensión |
| Tabla | `\| A \| B \|` + `\|---\|---\|` | Tabla de dos columnas | GFM o extensión |
| Alineación de tabla | `:---`, `:---:`, `---:` | Izquierda, centro, derecha | En la fila separadora |
| Regla horizontal | `---` | Línea horizontal | Deja línea en blanco antes |
| Enlace | `[texto](https://example.com)` | [texto](https://example.com) | Texto descriptivo |
| Enlace con título | `[texto](https://example.com "Título")` | Enlace con tooltip | El título es opcional |
| Enlace de referencia | `[texto][id]` + `[id]: https://example.com` | Enlace | Útil para repetir URLs |
| Referencia colapsada | `[texto][]` + `[texto]: https://example.com` | Enlace | El texto es el identificador |
| Autoenlace | `<https://example.com>` | <https://example.com> | CommonMark; no en MDX 2 |
| URL desnuda | `https://example.com` | Enlace automático | GFM o extensión |
| Correo | `<persona@example.com>` | <persona@example.com> | Genera `mailto:` |
| Imagen | `![alt](imagen.png)` | Imagen | `alt` obligatorio |
| Imagen con título | `![alt](imagen.png "Título")` | Imagen con tooltip | Título opcional |
| Imagen de referencia | `![alt][id]` + `[id]: imagen.png` | Imagen | Útil para repetir |
| Imagen enlazada | `[![alt](imagen.png)](https://example.com)` | Imagen clicable | Enlace alrededor de la imagen |
| Nota al pie | `Texto[^1]` + `[^1]: nota` | Nota al pie | Extensión |
| Abreviatura | `*[HTML]: HyperText Markup Language` | Abreviatura | Extensión |
| Índice | `[TOC]` o plugin | Índice | Extensión o herramienta |
| Front Matter | `---` + YAML + `---` | Metadatos | Convención de SSG |
| HTML en línea | `<kbd>Ctrl</kbd>` | <kbd>Ctrl</kbd> | Permitido según parser |
| HTML en bloque | `<div>...</div>` | Bloque HTML | Cuidado con líneas en blanco |
| Comentario HTML | `<!-- comentario -->` | Oculto | No en MDX 2 |
| Salto duro | Dos espacios al final de la línea | Salto de línea | Poco visible en el fuente |
| Salto duro alternativo | `\` al final de la línea | Salto de línea | CommonMark |
| Escape | `\*texto\*` | Asteriscos literales | Muestra el carácter literal |
| Entidad HTML | `&copy;` | © | Útil para caracteres especiales |
| Emoji | `:smile:` | 😄 | GitHub o extensión |
| Mención | `@usuario` | @usuario | GitHub/GitLab |
| Referencia a issue | `#123` | #123 | GitHub/GitLab |
| Alerta | `> [!NOTE]` + `> texto` | Aviso | GitHub; no estándar |
| Sección plegable | `<details><summary>Título</summary>Texto</details>` | Sección plegable | HTML |
| Mermaid | Bloque con lenguaje `mermaid` | Diagrama | Extensión o plataforma |
| Matemáticas en línea | `$a^2+b^2=c^2$` | Fórmula | Extensión |
| Matemáticas en bloque | `$$ ... $$` | Fórmula | Extensión |
| Bloque diff | Bloque con lenguaje `diff` | Cambios resaltados | GitHub o extensión |
| Tecla | `<kbd>Ctrl</kbd>` | <kbd>Ctrl</kbd> | HTML |
| Badge | `![badge](https://img.shields.io/...)` | Insignia | Imagen remota |
| Ancla | `[Ir](#seccion)` | Enlace interno | ID generado por el renderizador |
| ID explícito | `## Título {#id}` | Encabezado con ID | Extensión; no estándar |
| Comentario MDX | `{/* comentario */}` | Oculto | MDX |
| Expresión MDX | `{1 + 1}` | 2 | MDX |
| Import MDX | `import { X } from './X'` | Módulo importado | MDX/ESM |
| Export MDX | `export const meta = {}` | Metadatos | MDX/ESM |
| Componente MDX | `<Boton>Texto</Boton>` | Componente | MDX/JSX |
| Líneas resaltadas | Bloque con `{1,3}` tras el lenguaje | Código resaltado | Extensiones como rehype-pretty-code |

> Las funciones marcadas como extensión **no forman parte de CommonMark**. Si el documento debe ser portable, proporciona una alternativa en texto o una imagen.

---

[← 51. Compatibilidad](51-compatibilidad.md) · [Índice general](README.md) · [53. Ejemplo de documento Markdown profesional →](53-ejemplo-de-documento-markdown-profesional.md)
