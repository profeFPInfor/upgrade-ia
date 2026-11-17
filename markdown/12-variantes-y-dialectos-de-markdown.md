# 12. Variantes y dialectos de Markdown

> [← Índice general](README.md) · Capítulo 12 de 63

«Markdown» designa hoy una familia de lenguajes, no un único formato. Todos comparten un núcleo de sintaxis, pero difieren en tablas, notas al pie, matemáticas, atributos, metadatos y en cómo tratan los casos ambiguos. Escribir sin saber en qué dialecto se va a renderizar es la causa más común de documentos que «se ven mal» en otra plataforma.

## 12.1 Por qué hay tantas variantes

1. **El Markdown original no se especificó formalmente.** Gruber publicó la sintaxis y una implementación de referencia, pero dejó abiertos muchos detalles.
2. **Cada implementación resolvió las ambigüedades a su manera.** Qué es un párrafo, cuándo empieza una lista o cómo se anida el énfasis admite más de una respuesta razonable.
3. **Las necesidades añadieron extensiones.** Tablas, notas al pie, citas bibliográficas, matemáticas, diagramas y componentes no caben en el núcleo.
4. **Las plataformas añadieron funciones propias.** Menciones, alertas, casillas interactivas o *wikilinks* dependen del producto, no del lenguaje.
5. **La seguridad obligó a filtrar.** Un mismo HTML embebido se acepta en un sitio propio y se elimina en un repositorio público.

El resultado es un **núcleo común** relativamente estable y una periferia muy variable. El capítulo [11](11-commonmark.md) explica cómo CommonMark fijó ese núcleo; el [10](10-github-flavored-markdown-gfm.md), qué añade GFM.

## 12.2 Tabla comparativa

| Implementación | Características | Uso | Compatibilidad |
|---|---|---|---|
| Original Markdown | Sintaxis base de Gruber; HTML en bloque; sin especificación formal | Histórico; referencia de la sintaxis | Base de todos; comportamientos ambiguos |
| CommonMark | Especificación formal y suite de pruebas; sin tablas ni extensiones | Base de muchas herramientas modernas | Alta; núcleo común |
| GFM | CommonMark + tablas, tachado, tareas, autolinks y *tagfilter* | GitHub, GitLab (variante propia), muchas herramientas | Alta; extensiones no universales |
| Markdown Extra | Tablas, notas al pie, listas de definición, atributos y abreviaturas | Ecosistema PHP y algunos CMS | Media; sintaxis propia en parte |
| MultiMarkdown | Metadatos, tablas, citas, referencias cruzadas, notas y CriticMarkup | Escritura académica y exportación a LaTeX | Media |
| Pandoc Markdown | Extensiones numerosas y configurables: citas, matemáticas, divs, tablas de rejilla | Conversión entre formatos | Media; muy rico, poco portable |
| kramdown | Superconjunto con atributos, tablas, notas y TOC | Jekyll (por defecto histórico) | Parcial |
| Python-Markdown | Extensible mediante extensiones: tablas, TOC, admoniciones | MkDocs y proyectos Python | Depende de las extensiones activadas |
| markdown-it | Cumple CommonMark; plugins para casi todo | Aplicaciones JavaScript y vista previa de VS Code | Alta + plugins |
| remark / unified | Parser basado en AST con plugins (`remark-gfm`, etc.) | Docusaurus, MDX, Gatsby, Astro | Alta + plugins |
| GitLab Flavored Markdown (GLFM) | Basado en CommonMark; diagramas, alertas y tablas propias | GitLab | Específica de plataforma |
| MDX | Markdown + JSX/JavaScript | Sitios y documentación con React | **No** es Markdown estándar |
| R Markdown / Quarto | Markdown con código ejecutable embebido | Ciencia de datos e informes reproducibles | Específica de herramienta |
| Obsidian Flavored | Wikilinks `[[ ]]`, *callouts* y *embeds* | Notas personales | Específica de la aplicación |

Las filas no son categorías excluyentes: un proyecto puede usar CommonMark como base, activar extensiones de GFM y añadir plugins propios. Lo importante es saber **qué conjunto** está activo.

## 12.3 Cuatro familias

| Familia | Ejemplos | Riesgo principal |
|---|---|---|
| Especificaciones | CommonMark, GFM | Extensiones que parecen estándar y no lo son |
| Plataformas | GitHub, GitLab, Obsidian | Funciones que solo existen en ese producto |
| Herramientas | Pandoc, kramdown, Python-Markdown | Opciones distintas según la versión y la configuración |
| Formatos derivados | MDX, R Markdown, Quarto | Ya no son Markdown: añaden un lenguaje de programación |

Un documento portable se queda en la primera familia y, dentro de ella, en el subconjunto que comparten CommonMark y GFM. Todo lo demás exige una decisión consciente y una prueba en el destino.

## 12.4 El subconjunto portable

Estas funciones suelen funcionar en casi todos los renderizadores modernos:

- Títulos ATX (`#` a `######`).
- Párrafos, énfasis con `*` o `_`, negrita con `**` o `__`.
- Listas ordenadas y no ordenadas con sangría consistente.
- Citas con `>`.
- Enlaces e imágenes con sintaxis inline.
- Código inline y bloques cercados con tres acentos graves.
- Líneas horizontales con `---`.
- HTML básico, si la plataforma no lo filtra.

Fuera del subconjunto quedan, entre otras: tablas, notas al pie, listas de tareas, tachado, matemáticas, diagramas Mermaid, atributos `{.clase}`, metadatos y *wikilinks*. Algunas son tan habituales que parece que siempre están; no es así.

## 12.5 Cómo elegir un dialecto

| Pregunta | Decisión |
|---|---|
| ¿Dónde se va a leer? | GitHub, sitio propio, PDF, aplicación de notas |
| ¿Quién lo va a mantener? | Personas con distintos editores o un equipo único |
| ¿Necesitas tablas y tareas? | GFM o una extensión equivalente |
| ¿Necesitas matemáticas? | KaTeX/MathJax o Pandoc, según el destino |
| ¿Necesitas componentes? | MDX, con el coste de un lenguaje más |
| ¿Necesitas citas académicas? | Pandoc o Quarto |
| ¿Necesitas máxima portabilidad? | CommonMark + GFM básico |

La decisión no es solo técnica: un dialecto con muchas extensiones ata el corpus a una herramienta. Si el documento debe durar años, el subconjunto portable envejece mejor.

## 12.6 Cómo detectar el dialecto

Cuando heredas un repositorio, no supongas qué renderizador usa. Busca:

1. **Archivos de configuración:** `.markdownlint.*`, `_config.yml`, `mkdocs.yml`, `docusaurus.config.js`, `.pandoc/`.
2. **Extensiones en los archivos:** tablas, notas al pie, bloques `mermaid`, `{:.clase}`.
3. **El HTML generado:** etiquetas, clases y atributos revelan el motor.
4. **La documentación del proyecto:** versión del generador y plugins.
5. **Pruebas:** renderiza un documento con las funciones dudosas y compara.

No confíes solo en el editor: la vista previa de VS Code, Obsidian o Typora puede aceptar sintaxis que el sitio publicado rechaza.

## 12.7 Migrar entre dialectos

1. **Inventario de funciones** usadas y en qué archivos.
2. **Matriz de destino:** qué acepta el nuevo renderizador.
3. **Conversión automática** con Pandoc u otra herramienta, sabiendo que no es perfecta.
4. **Revisión manual** de tablas, notas y enlaces.
5. **Prueba de render** en el destino real, no solo en local.
6. **Documenta las diferencias** para quien escriba después.

Las migraciones más costosas no son las de sintaxis, sino las de **semántica**: un `[[enlace]]` de Obsidian no es un enlace Markdown, y un *callout* no tiene equivalente universal. Convierte esos elementos a HTML o a texto antes de migrar, o acepta que se perderán.

## 12.8 Errores frecuentes

| Error | Consecuencia |
|---|---|
| Suponer que GFM es «Markdown estándar» | Tablas y tareas fallan en CommonMark |
| Usar sintaxis de Obsidian en un sitio público | Wikilinks y callouts se ven como texto |
| Mezclar dialectos en el mismo corpus | Render distinto según la página |
| Confiar en la vista previa del editor | El sitio publicado usa otro motor |
| No fijar la versión del generador | Una actualización cambia el render |
| Documentar solo la sintaxis, no el dialecto | Quien llega nuevo no sabe qué está permitido |

## 12.9 Lista de comprobación

- [ ] Está documentado qué dialecto y qué extensiones usa el proyecto.
- [ ] La versión del generador está fijada.
- [ ] El contenido crítico usa el subconjunto portable.
- [ ] Las extensiones están justificadas y probadas en el destino.
- [ ] La vista previa del editor no se confunde con el render final.
- [ ] Las migraciones revisan tablas, notas, enlaces y metadatos.
- [ ] Hay una prueba de render en CI o en el flujo de publicación.
- [ ] Quien escribe sabe dónde consultar las diferencias.

---

[← 11. CommonMark](11-commonmark.md) · [Índice general](README.md) · [13. HTML dentro de Markdown →](13-html-dentro-de-markdown.md)
