# 10. GitHub Flavored Markdown (GFM)

> [← Índice general](README.md) · Capítulo 10 de 63

## 10.1 Qué es

**GFM** es el dialecto de Markdown que usa GitHub. Su especificación formal es un **superconjunto estricto de CommonMark**: todo documento CommonMark válido es GFM válido, y GFM añade extensiones. Especificación: <https://github.github.com/gfm/>.

> GitHub además añade **características propias de la plataforma** que *no* están en la especificación GFM (menciones, referencias a issues, alertas, Mermaid, emojis, etc.). Conviene distinguirlas.

| Característica | Original | CommonMark | GFM (spec) | github.com |
|---|---|---|---|---|
| Especificación formal | No | Sí | Sí (sobre CommonMark) | Sí + extras |
| Tablas | No | No | **Sí** | Sí |
| Listas de tareas | No | No | **Sí** | Sí (interactivas) |
| Tachado | No | No | **Sí** | Sí |
| Autoenlaces extendidos (`www.`, `https://`) | No | No | **Sí** | Sí |
| Filtrado de HTML peligroso (*tagfilter*) | No | No | **Sí** | Sí |
| Menciones `@usuario` | No | No | No | **Sí** |
| Referencias `#123` | No | No | No | **Sí** |
| Alertas `> [!NOTE]` | No | No | No | **Sí** |
| Mermaid | No | No | No | **Sí** |
| Matemáticas `$...$` | No | No | No | **Sí** |
| Notas al pie `[^1]` | No | No | No | **Sí** |

## 10.2 Extensiones de la especificación GFM

| Característica | Ejemplo | ¿En la spec GFM? |
|---|---|---|
| Tablas | `\| a \| b \|` | Sí |
| Listas de tareas | `- [x] hecho` | Sí |
| Tachado | `~~texto~~` | Sí |
| Autolinks extendidos | `www.example.com`, `https://…`, correos | Sí |
| Filtro de etiquetas HTML (*tagfilter*) | Escapa `<script>`, `<iframe>`, etc. | Sí |

## 10.3 Características de GitHub (no parte de la spec)

| Característica | Sintaxis | Notas |
|---|---|---|
| Menciones | `@usuario`, `@org/equipo` | Notifica a la persona |
| Referencias a issues/PR | `#123`, `usuario/repo#123` | Se enlazan automáticamente |
| Referencias a commits | SHA (7+ caracteres) | Se enlazan automáticamente |
| Alertas (*admonitions*) | `> [!NOTE]` | Ver abajo |
| Diagramas | ` ```mermaid ` | Ver [sección 15](15-mermaid-en-github.md) |
| Fórmulas matemáticas | `$a^2+b^2=c^2$` y `$$ … $$` | Basadas en LaTeX/MathJax |
| Emojis | `:rocket:` | *Shortcodes* |
| Notas al pie | `texto[^1]` + `[^1]: nota` | Soportadas por GitHub |
| Colores | `` `#ff0000` `` | Muestra muestra de color |
| Secciones plegables | `<details>` | HTML |
| Enlace permanente a líneas de código | URL con `#L10-L20` | Previsualización en comentarios |

Otras referencias útiles: `GH-123` (identificador de issue), palabras clave como `closes #12`, `fixes #12` o `resolves #12` (cierran el issue al fusionar el PR) y SHA de commits de 7 o más caracteres.

**Notas al pie y matemáticas** (extensiones de GitHub):

```markdown
Texto con una nota al pie.[^1]

[^1]: Contenido de la nota.

Fórmula en línea: $E = mc^2$

$$
\int_0^1 x^2\,dx = \frac{1}{3}
$$
```

Bloques con lenguajes especiales que GitHub renderiza de forma particular: `mermaid`, `math`, `geojson`, `topojson` y `stl`.

**Secciones plegables:**

```markdown
<details>
<summary>Ver más</summary>

Contenido oculto. Deja una línea en blanco después de `<summary>` para poder usar Markdown dentro.

</details>
```

**Alertas** (sintaxis vigente en GitHub; **no estándar**):

```markdown
> [!NOTE]
> Información útil que los usuarios deberían conocer.

> [!TIP]
> Consejo para hacer las cosas mejor.

> [!IMPORTANT]
> Información clave para lograr el objetivo.

> [!WARNING]
> Contenido urgente que requiere atención inmediata.

> [!CAUTION]
> Riesgos o consecuencias negativas de una acción.
```

Fuera de GitHub (y plataformas que la hayan adoptado, como GitLab o Obsidian con su propio formato) se verán como una cita normal con el texto `[!NOTE]`.

## 10.4 HTML en GFM

GFM permite HTML, pero **filtra** algunas etiquetas peligrosas (`<title>`, `<textarea>`, `<style>`, `<xmp>`, `<iframe>`, `<noembed>`, `<noframes>`, `<script>`, `<plaintext>`) y GitHub **sanea** el resultado final (elimina scripts, manejadores de eventos, etc.).

## 10.5 Compatibilidad

GFM está ampliamente soportado (GitLab, Bitbucket con matices, VS Code, markdown-it con plugins, `cmark-gfm`, Goldmark con extensiones, remark con `remark-gfm`). Las características de plataforma, no.

## 10.6 Documentación oficial

- Especificación GFM: <https://github.github.com/gfm/>
- Sintaxis básica de escritura y formato: <https://docs.github.com/es/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax>
- Sintaxis avanzada (tablas, secciones plegables, alertas…): <https://docs.github.com/es/get-started/writing-on-github/working-with-advanced-formatting>
- Referencias y enlaces automáticos: <https://docs.github.com/es/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls>

---

[← 9. Documentación técnica con Markdown](09-documentacion-tecnica-con-markdown.md) · [Índice general](README.md) · [11. CommonMark →](11-commonmark.md)
