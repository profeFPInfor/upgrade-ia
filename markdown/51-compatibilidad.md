# 51. Compatibilidad

> [← Índice general](README.md) · Capítulo 51 de 63

Un mismo documento Markdown puede verse diferente en GitHub, GitLab, VS Code, Obsidian, Jekyll, MkDocs o un navegador. La causa no es que "Markdown esté roto", sino que cada herramienta implementa un **dialecto**, activa unas **extensiones** y aplica su propio **CSS**, su **sanitización** y sus **convenciones de enlaces**.

## 51.1 Por qué cambia el renderizado

| Factor | Efecto |
|---|---|
| **Parser** | CommonMark, GFM, markdown-it, Python-Markdown, Kramdown o Goldmark interpretan detalles de forma distinta |
| **Versión de la especificación** | Una versión antigua puede no admitir una construcción nueva |
| **Extensiones** | Tablas, notas al pie, matemáticas, Mermaid o admoniciones pueden estar activadas o no |
| **HTML permitido** | Algunos renderizadores lo permiten; otros lo eliminan o lo sanean |
| **Sanitización** | GitHub y GitLab eliminan scripts y atributos peligrosos |
| **CSS y tema** | Tipografía, anchos, colores, tablas y bloques de código cambian por completo |
| **Generación de IDs** | Las anclas pueden incluir acentos, guiones o sufijos numéricos distintos |
| **Resolución de enlaces** | Las rutas relativas se resuelven respecto al archivo, al repositorio o al sitio |
| **Front Matter** | Los SSG lo procesan; un visor genérico lo muestra como texto o tabla |
| **Resaltado de sintaxis** | Depende del highlighter y de los lenguajes registrados |
| **Contexto de salida** | No es lo mismo una página HTML que un PDF, un correo o una vista de terminal |

## 51.2 Núcleo común

La tabla siguiente resume el comportamiento **habitual**; la configuración concreta puede cambiar el resultado. Leyenda: **Sí** = soportado por defecto; **Ext.** = requiere extensión, plugin o configuración; **No** = no soportado; **Varía** = depende de la versión o del tema.

| Característica | Original | CommonMark | GFM | GitHub | GitLab | VS Code | Obsidian | Jekyll | MkDocs |
|---|---|---|---|---|---|---|---|---|---|
| Párrafos | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| Títulos ATX | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| Títulos Setext | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| Énfasis y negrita | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| Listas | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| Listas anidadas | Varía | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| Citas | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| Código en línea | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| Bloques de código | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| Enlaces | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| Imágenes | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| Enlaces de referencia | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| HTML embebido | Sí | Sí | Sí | Sí (saneado) | Sí (saneado) | Sí | Sí | Sí | Sí |
| Saltos duros | Varía | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| Escapes | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| Entidades HTML | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| Regla horizontal | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí |

## 51.3 Extensiones y funciones de plataforma

| Característica | Original | CommonMark | GFM (spec) | GitHub | GitLab | VS Code | Obsidian | Jekyll | MkDocs |
|---|---|---|---|---|---|---|---|---|---|
| Tablas | No | No | Sí | Sí | Sí | Sí | Sí | Sí | Ext. |
| Listas de tareas | No | No | Sí | Sí | Sí | Sí | Sí | No | Ext. |
| Tachado | No | No | Sí | Sí | Sí | Sí | Sí | Varía | Ext. |
| Autolinks extendidos | No | No | Sí | Sí | Sí | Sí | Sí | Varía | Ext. |
| Notas al pie | No | No | No | Sí | Sí | Varía | Sí | Ext. | Ext. |
| Listas de definiciones | No | No | No | No | Sí | Varía | Varía | Ext. | Ext. |
| Admoniciones / alertas | No | No | No | Sí | Sí | Ext. | Sí | Ext. | Ext. |
| Matemáticas | No | No | No | Sí | Sí | Sí | Sí | Ext. | Ext. |
| Mermaid | No | No | No | Sí | Sí | Ext. | Sí | Ext. | Ext. |
| Front Matter | No | No | No | No | Sí | Ext. | Sí | Sí | Sí |
| Índice automático | No | No | No | No | Sí | Ext. | Ext. | Ext. | Sí (tema) |
| Emojis `:shortcode:` | No | No | No | Sí | Sí | Ext. | Ext. | Ext. | Ext. |
| Menciones `@usuario` | No | No | No | Sí | Sí | No | No | No | No |
| Referencias `#123` | No | No | No | Sí | Sí | No | No | No | No |
| IDs de encabezado | No | No | No | Sí | Sí | Sí | Sí | Sí | Sí |
| `<details>` / `<summary>` | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| Resaltado de sintaxis | No | No | No | Sí | Sí | Sí | Sí | Ext. | Ext. |

> "GitHub" se refiere a github.com, no solo a la especificación GFM. "GitLab" incluye GitLab.com y las versiones autogestionadas, que pueden variar. "Jekyll" usa Kramdown por defecto, pero puede configurarse con GFM. "MkDocs" usa Python-Markdown y depende de las extensiones declaradas en `mkdocs.yml`.

## 51.4 Detalles por plataforma

### GitHub

- Usa **GFM**, definido como superconjunto de CommonMark, más funciones de la plataforma.
- Soporta tablas, listas de tareas, tachado, autolinks, notas al pie, matemáticas, Mermaid, alertas (`> [!NOTE]`), menciones y referencias a issues.
- **Sanea** el HTML: elimina scripts, manejadores de eventos y etiquetas peligrosas.
- Las rutas relativas se resuelven respecto al archivo dentro del repositorio.
- Un archivo `.mdx` **no se renderiza como MDX**: se muestra como texto o código; GitHub no compila JSX.
- Documentación: <https://docs.github.com/en/get-started/writing-on-github>

### GitLab

- Usa **GitLab Flavored Markdown**, inspirado en GFM pero con diferencias.
- Soporta tablas, listas de tareas, tachado, notas al pie, definiciones, alertas, Front Matter, TOC, matemáticas, Mermaid y referencias a issues/MRs.
- Sanea el HTML y aplica sus propias reglas de seguridad.
- Algunas funciones cambian entre versiones y ediciones (CE/EE).
- Documentación: <https://docs.gitlab.com/user/markdown/>

### Visual Studio Code

- La previsualización integrada usa **markdown-it** y extensiones propias; no es idéntica a GitHub.
- Opciones como `markdown.preview.breaks` alteran el tratamiento de los saltos de línea.
- Mermaid, matemáticas avanzadas y exportación suelen requerir extensiones.
- Es excelente para editar, pero conviene validar en el renderizador final.
- Documentación: <https://code.visualstudio.com/docs/languages/markdown>

### Obsidian

- Usa un dialecto propio con **wikilinks**, **embeds**, **callouts**, etiquetas y propiedades.
- Los enlaces `[[nota]]` y los callouts `> [!note]` no son Markdown estándar.
- Permite HTML y plugins de la comunidad, con los riesgos que ello implica.
- Es ideal para notas personales, no necesariamente para documentación portable.
- Ayuda: <https://help.obsidian.md/>

### Jekyll

- Generador de sitios estáticos en Ruby, usado por GitHub Pages.
- Por defecto utiliza **Kramdown**; se puede configurar `markdown: GFM` en `_config.yml`.
- Requiere Front Matter para procesar páginas y publicaciones.
- Las extensiones (Mermaid, matemáticas, admoniciones) dependen de plugins y del tema.
- Documentación: <https://jekyllrb.com/docs/configuration/markdown/>

### MkDocs

- Generador de documentación en Python; usa **Python-Markdown**.
- Las tablas, notas al pie, definiciones, admoniciones, matemáticas y Mermaid requieren extensiones o plugins.
- Material for MkDocs añade componentes y sintaxis propias (admoniciones, pestañas, botones).
- El tema controla la navegación, el índice y el aspecto.
- Documentación: <https://squidfunk.github.io/mkdocs-material/>

### CommonMark

- Define el núcleo estricto: párrafos, títulos, énfasis, listas, citas, código, enlaces, imágenes y HTML.
- **No** incluye tablas, listas de tareas, tachado, notas al pie ni Mermaid.
- Es la base más portable para contenido que debe funcionar en muchos sistemas.
- Especificación: <https://spec.commonmark.org/>

### Navegadores

- Un navegador **no interpreta Markdown**: recibe HTML ya renderizado.
- Las diferencias visuales provienen del CSS, las fuentes, el tamaño de ventana y las capacidades del navegador.
- HTML5 es un estándar independiente; no debe confundirse con Markdown.
- Especificación HTML: <https://html.spec.whatwg.org/>

### Otros renderizadores

| Herramienta | Base | Nota |
|---|---|---|
| **Hugo** | Goldmark | CommonMark + extensiones; configuración explícita |
| **Docusaurus** | MDX | Componentes React y plugins |
| **Astro** | MDX/Markdown | Integración oficial; contenido y componentes |
| **Pandoc** | Múltiples dialectos | Muy configurable; especifica `-f` |
| **markdown-it** | CommonMark + plugins | Usado por VS Code y muchas webs |
| **remark** | AST de Markdown | Ecosistema de plugins; base de MDX |
| **Kramdown** | Ruby | Usado por Jekyll; extensiones propias |

## 51.5 Estándar frente a extensión

| Característica | Dónde se define | ¿Estándar Markdown? | Nota |
|---|---|---|---|
| Títulos, listas, énfasis, enlaces, imágenes, citas, código | Markdown original / CommonMark | Sí (núcleo) | CommonMark formaliza el comportamiento |
| Tablas | GFM | No en CommonMark; sí en GFM | Muchas implementaciones las añaden |
| Listas de tareas | GFM | No en CommonMark; sí en GFM | GitHub y GitLab las muestran interactivas |
| Tachado | GFM | No en CommonMark; sí en GFM | `~~texto~~` |
| Autolinks de URLs | GFM | No en CommonMark; sí en GFM | CommonMark solo `<...>` |
| Notas al pie | Extensiones / GitHub | No | Variables según plataforma |
| Matemáticas | Extensiones / GitHub | No | MathJax, KaTeX o servicios |
| Mermaid | Proyecto independiente | No | Requiere soporte del renderizador |
| Alertas `> [!NOTE]` | GitHub | No | También adoptadas por otras plataformas |
| Front Matter | Convención de SSG | No | YAML al inicio del archivo |
| Wikilinks `[[...]]` | Obsidian y otros | No | No funcionan en GitHub |
| Callouts `> [!note]` | Obsidian | No | Sintaxis propia |
| Admoniciones | Docusaurus, MkDocs, otros | No | Sintaxis específica de cada herramienta |
| MDX | Proyecto MDX | No | Formato distinto, no Markdown estándar |

## 51.6 Cómo escribir Markdown portable

1. **Usa el núcleo CommonMark** para el contenido esencial.
2. **Evita HTML** salvo que sea imprescindible y esté permitido.
3. **No dependas de extensiones** para información crítica: si usas una tabla, ofrece una lista equivalente cuando la portabilidad sea prioritaria.
4. **Usa enlaces relativos** y comprueba cómo se resuelven en el destino.
5. **No confíes en los IDs automáticos** de los encabezados: si necesitas anclas estables, usa un ID explícito cuando la herramienta lo permita o mantén títulos estables.
6. **Especifica el lenguaje** en los bloques de código.
7. **Prueba en el renderizador final**, no solo en el editor.
8. **Documenta las extensiones** que usa el proyecto (Mermaid, matemáticas, alertas).
9. **Mantén el Front Matter solo si el SSG lo necesita**.
10. **Evita sintaxis específica de un editor** en documentos compartidos.

| Necesidad | Opción portable | Opción específica |
|---|---|---|
| Tabla | Lista de definiciones o tabla GFM con fallback | Tabla con extensiones del sitio |
| Aviso | Cita `>` con texto "Nota:" | Alerta `> [!NOTE]` o componente |
| Diagrama | Imagen SVG/PNG con `alt` | Bloque Mermaid |
| Fórmula | Imagen o código | `$...$` con MathJax/KaTeX |
| Índice | Lista de enlaces manual | Plugin de TOC |
| Metadatos | Texto al inicio | Front Matter YAML |

## 51.7 Cómo comprobar la compatibilidad

| Prueba | Herramienta |
|---|---|
| CommonMark estricto | <https://spec.commonmark.org/dingus/> |
| GFM | <https://github.github.com/gfm/> |
| Previsualización de GitHub | El propio repositorio o `grip` |
| Previsualización de GitLab | El propio proyecto o el editor de GitLab |
| Previsualización de VS Code | `Ctrl+Shift+V` |
| Previsualización de Obsidian | Modo lectura |
| Sitio final | Build local del SSG |
| HTML generado | Inspeccionar el DOM y el CSS |
| Enlaces | lychee, markdown-link-check |

---

[← 50. Errores frecuentes](50-errores-frecuentes.md) · [Índice general](README.md) · [52. Tabla de referencia rápida →](52-tabla-de-referencia-rapida.md)
