# 42. Notas al pie, definiciones y referencias

> [← Índice general](README.md) · Capítulo 42 de 63

Un documento técnico no solo se compone de párrafos: necesita notas, definiciones, abreviaturas, referencias cruzadas, citas y un índice. Markdown cubre una parte de forma estándar y el resto mediante extensiones. Este capítulo reúne las sintaxis y las diferencias que más problemas causan.

## 42.1 Notas al pie

### 42.1.1 Sintaxis por referencia

```markdown
Markdown permite separar el contenido de la presentación.[^1]

[^1]: Esta es la nota al pie.
```

La nota se numera automáticamente y se coloca al final del documento (o de la sección, según el renderizador).

### 42.1.2 Etiquetas con nombre

```markdown
CommonMark define el núcleo.[^commonmark]

[^commonmark]: <https://spec.commonmark.org/>
```

Las etiquetas con nombre son más legibles y estables que los números.

### 42.1.3 Notas en línea

Pandoc permite escribir la nota directamente:

```markdown
Esta es una nota en línea.^[Texto de la nota.]
```

No es sintaxis estándar: GitHub, GitLab y la mayoría de visores no la interpretan.

### 42.1.4 Notas con varios párrafos

```markdown
[^larga]: Primer párrafo.

    Segundo párrafo, indentado con cuatro espacios.

    ```bash
    código dentro de la nota
    ```
```

La indentación debe ser coherente; si el renderizador no la admite, la nota se corta.

### 42.1.5 Compatibilidad

| Plataforma | Notas al pie |
|---|---|
| Markdown original | No |
| CommonMark | No |
| GFM (GitHub) | Sí |
| Pandoc | Sí (referencia e inline) |
| kramdown | Sí |
| Markdown Extra | Sí |
| Markdown-it | Con plugin |
| Obsidian | Sí |

## 42.2 Listas de definiciones

```markdown
Markdown
: Lenguaje de marcado ligero.

CommonMark
: Especificación del núcleo de Markdown.
: Implementación de referencia en C.
```

| Plataforma | Soporte |
|---|---|
| Pandoc | Sí |
| kramdown | Sí |
| Markdown Extra | Sí |
| GFM | No |
| CommonMark | No |

Si el destino no las admite, usa una tabla de dos columnas o una lista con negritas.

## 42.3 Abreviaturas

```markdown
*[HTML]: HyperText Markup Language
*[CSS]: Cascading Style Sheets

HTML y CSS son estándares web.
```

El renderizador envuelve las coincidencias en `<abbr title="…">`. Es una extensión de Markdown Extra y kramdown; no está en GFM.

## 42.4 Enlaces de referencia

En lugar de repetir URLs:

```markdown
Consulta la [documentación de CommonMark][commonmark] y el [manual de Pandoc][pandoc].

[commonmark]: https://spec.commonmark.org/ "Especificación CommonMark"
[pandoc]: https://pandoc.org/MANUAL.html "Manual de Pandoc"
```

Variantes:

```markdown
[texto][]      <!-- usa el propio texto como etiqueta -->
[texto]        <!-- forma abreviada -->
```

Las etiquetas no distinguen mayúsculas de minúsculas y pueden definirse en cualquier parte del documento. Son útiles para mantener las URLs centralizadas y los párrafos legibles.

## 42.5 Anclas y enlaces internos

### 42.5.1 Generación automática

Los encabezados generan un identificador a partir del texto. El algoritmo varía:

- **GitHub**: minúsculas, elimina puntuación, sustituye espacios por guiones; conserva letras acentuadas. Si hay duplicados, añade `-1`, `-2`…
- **Pandoc**: minúsculas, elimina puntuación, espacios por guiones; puede añadir prefijo con `--id-prefix`.
- **kramdown**: genera IDs con `auto_ids: true`.
- **Otros**: pueden eliminar acentos o usar otra normalización.

Por eso un enlace `#cómo-funciona` puede funcionar en GitHub y fallar en otro renderizador.

### 42.5.2 IDs explícitos

Pandoc, kramdown y Markdown Extra permiten fijar el ID:

```markdown
## Cómo funciona {#como-funciona}
```

Así el enlace `[Cómo funciona](#como-funciona)` es estable aunque cambie el texto del encabezado.

En GitHub no se admiten `{#id}`; se puede usar un ancla HTML:

```markdown
<a id="como-funciona"></a>
## Cómo funciona
```

### 42.5.3 Buenas prácticas

- Usa enlaces relativos entre archivos (`../guia/intro.md`).
- Comprueba las anclas después de renombrar encabezados.
- Evita IDs que empiecen por números si el destino lo prohíbe.
- No dupliques IDs en la misma página.
- Codifica los caracteres especiales de la URL (`%20`, `%C3%A9`).

El capítulo [17](17-enlaces-internos.md) amplía la organización de enlaces.

## 42.6 Citas y bibliografía

Pandoc reconoce citas con claves de un archivo BibTeX/BibLaTeX:

```markdown
Como demuestra Doe [@doe2024], el formato es estable.

Varios estudios lo confirman [@doe2024; @roe2025].

Solo el año: [-@doe2024].

Con localizador: [@doe2024, pp. 33-35].
```

```bash
pandoc articulo.md -o articulo.pdf \
  --citeproc \
  --bibliography=referencias.bib \
  --csl=estilos/apa.csl
```

| Elemento | Función |
|---|---|
| `--citeproc` | Procesa las citas y genera la bibliografía |
| `--bibliography` | Archivo `.bib` o `.json` |
| `--csl` | Estilo de cita (APA, IEEE, Chicago…) |
| `--bibliography` repetido | Varias fuentes |

Sin `--citeproc`, las citas quedan como texto entre corchetes.

## 42.7 Índice de contenidos

| Método | Ejemplo | Contexto |
|---|---|---|
| Automático del visor | Botón “Índice” | GitHub, GitLab |
| Pandoc | `--toc` | HTML, PDF, DOCX, EPUB |
| kramdown | `* TOC` + `{:toc}` | Jekyll |
| markdown-toc | `<!-- toc -->` | Node.js |
| remark-toc | Plugin de remark | JavaScript |
| Manual | Lista de enlaces | Cualquier destino |

Para un índice manual, genera los enlaces a partir de los IDs reales, no de los títulos.

## 42.8 Numeración de secciones

- **Manual**: escribe `1.`, `1.1` en los títulos. Sencillo, pero se rompe al reordenar.
- **Automática**: `--number-sections` en Pandoc, numeración de LaTeX o del procesador de textos.
- **CSS**: contadores `counter-reset` y `counter-increment` para HTML.

En documentación colaborativa, la numeración automática evita errores, pero complica los enlaces si los IDs incluyen el número.

## 42.9 Glosarios e índices

Markdown no tiene un elemento de glosario ni de índice analítico. Alternativas:

- **Glosario como lista de definiciones** o tabla.
- **Índice alfabético manual** con enlaces a las secciones.
- **LaTeX** para índices analíticos (`\makeindex`, `\printindex`).
- **Buscador del sitio** para recuperar términos.

Si necesitas un índice analítico real, el destino PDF/LaTeX es más adecuado que HTML.

## 42.10 Accesibilidad

- Las notas al pie deben tener enlaces de ida y vuelta; comprueba que el renderizador los genera.
- Usa textos de enlace descriptivos (`[documentación de CommonMark]`, no `[aquí]`).
- No bases la información en el número de la nota.
- En tablas, evita notas que dependan de la posición.
- Los glosarios deben estar en orden lógico o alfabético y ser navegables.

## 42.11 Lista de comprobación

- [ ] Las notas tienen etiquetas únicas y definiciones completas.
- [ ] El renderizador de destino admite notas y definiciones.
- [ ] Los enlaces internos apuntan a IDs existentes.
- [ ] Las citas tienen bibliografía y estilo definidos.
- [ ] El índice se genera o se actualiza tras cambiar títulos.
- [ ] La numeración es coherente en todo el documento.

---

[← 41. Matemáticas y notación científica](41-matematicas-y-notacion-cientifica.md) · [Índice general](README.md) · [43. Cuadernos y publicación científica →](43-cuadernos-y-publicacion-cientifica.md)
