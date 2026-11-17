# 56. Glosario

> [← Índice general](README.md) · Capítulo 56 de 63

Glosario alfabético de términos usados en el documento. Las definiciones son breves; para profundizar, consulta la sección correspondiente.

## 56.1 Cómo usar y mantener el glosario

- **Una definición por término**, en una o dos frases.
- **La primera aparición enlaza al glosario**; las siguientes no necesitan repetirlo.
- **El término va en negrita**, seguido de una raya y la definición.
- **Los sinónimos se remiten** al término principal («*front matter*, véase Front Matter»).
- **Las referencias cruzadas** apuntan al capítulo donde se desarrolla el concepto.
- **Se revisa al añadir capítulos**: un término nuevo sin definición deja un hueco.

Un glosario que define todo se convierte en un diccionario; uno que define solo lo ambiguo es más útil. Prioriza los términos que el lector puede interpretar de forma distinta según su experiencia.

## 56.2 Términos A-F

**Abreviatura** — Extensión de Markdown que permite definir el significado de un término y mostrarlo al pasar el ratón. No forma parte de CommonMark.

**Admonición** - Bloque destacado para notas, avisos o peligros. Cada herramienta usa su propia sintaxis (Docusaurus `:::note`, MkDocs `!!! note`, Obsidian `> [!note]`).

**Agente** - Sistema que usa un modelo de lenguaje para ejecutar tareas con herramientas y fuentes de datos. En documentación, conviene darle instrucciones explícitas y limitar sus permisos (capítulo [61](61-markdown-e-inteligencia-artificial.md)).

**Alucinación** - Respuesta de un modelo que parece plausible pero es falsa o no está respaldada por una fuente. Se mitiga verificando datos y enlaces.

**Ancla (anchor)** — Identificador de un encabezado o elemento que permite enlazar directamente a una sección. El ID lo genera el renderizador y puede variar entre plataformas.

**AST (Abstract Syntax Tree)** — Árbol de sintaxis abstracta. Representación estructurada del documento que usan los parsers, linters y plugins para analizar y transformar el contenido.

**ATX** — Estilo de encabezado que usa almohadillas (`#`, `##`, etc.). Es el más común y el que recomienda CommonMark.

**Backtick** — Acento grave (`` ` ``). Se usa para código en línea y para delimitar bloques de código.

**Badge** — Insignia gráfica que se muestra en un README o página. Normalmente es una imagen enlazada a un servicio (CI, licencia, versión).

**Blockquote** — Cita o bloque indentado. Se escribe con `>` al inicio de la línea.

**BOM (Byte Order Mark)** — Marca de orden de bytes al inicio de un archivo. Puede interferir con el Front Matter o con el primer encabezado; se recomienda UTF-8 sin BOM.

**Callout** - Bloque de aviso o nota. En Obsidian se escribe `> [!note]`; en otras herramientas recibe nombres como *admonition*.

**Canonical** - URL preferida de una página cuando existen duplicados. Se declara con `<link rel="canonical">` y debe coincidir con el sitemap y los enlaces internos (capítulo [63](63-publicacion-y-distribucion.md)).

**Changelog** - Registro legible de los cambios notables de cada versión. No es el historial de commits (capítulo [22](22-changelog.md)).

**CommonMark** — Especificación formal del núcleo de Markdown, con una suite de pruebas y varias implementaciones de referencia. No incluye tablas, tareas ni Mermaid.

**Dialecto** — Variante de Markdown con reglas o extensiones propias. Ejemplos: GFM, Kramdown, Python-Markdown, Obsidian Flavored Markdown.

**Diátaxis** — Marco de documentación que distingue tutoriales, guías prácticas, referencia y explicación. No es un estándar formal, sino una guía de diseño.

**Docs-as-code** — Práctica de tratar la documentación como código: archivos en Git, revisión mediante pull requests, linting y CI.

**DOM (Document Object Model)** — Representación en memoria de un documento HTML que el navegador manipula mediante JavaScript. Insertar HTML no confiable en el DOM puede provocar XSS.

**Énfasis** — Cursiva (`*texto*`) o negrita (`**texto**`). En Markdown también se usan guiones bajos, con matices.

**Emoji shortcode** — Código textual como `:smile:` que algunas plataformas convierten en un emoji. No es estándar.

**Entidad HTML** — Secuencia como `&copy;` o `&amp;` que representa un carácter. Se interpreta en HTML y en muchos renderizadores Markdown.

**Escape** — Uso de una barra invertida (`\`) para que un carácter especial se muestre literalmente: `\*` produce `*`.

**Extensión** - Función añadida al núcleo de Markdown por un parser, un plugin o una plataforma. No debe presentarse como parte del estándar.

**Feed** - Archivo RSS o Atom que permite seguir las novedades de un sitio sin visitarlo. Se descubre con `<link rel="alternate">` en el `<head>` (capítulo [63](63-publicacion-y-distribucion.md)).

**Fenced code block** — Bloque de código delimitado por tres o más backticks (o tildes). Permite indicar el lenguaje para el resaltado.

**Front Matter** — Bloque de metadatos, normalmente YAML, al inicio de un archivo y delimitado por `---`. Es una convención de generadores de sitios, no parte de Markdown.

## 56.3 Términos G-M

**GFM (GitHub Flavored Markdown)** — Dialecto de GitHub definido como superconjunto estricto de CommonMark. Añade tablas, listas de tareas, tachado, autolinks y *tagfilter*.

**Hard line break** - Salto de línea forzado dentro de un párrafo. Se consigue con dos espacios al final de la línea o con una barra invertida final (CommonMark).

**hreflang** - Atributo que indica la lengua y, opcionalmente, la región de una página. En un sitio multilingüe, las variantes deben enlazarse de forma recíproca (capítulo [45](45-internacionalizacion-y-escritura-multilingue.md)).

**HTML (HyperText Markup Language)** — Lenguaje de marcado que describe la estructura de las páginas web. Markdown se convierte a HTML, pero no es HTML.

**Indented code block** — Bloque de código creado con una sangría de cuatro espacios. Es menos explícito que el bloque con fences.

**Inline** - Elemento que forma parte de una línea de texto: énfasis, código, enlace, imagen, etc.

**JSON-LD** - Formato de datos estructurados basado en JSON que se inserta en un `<script type="application/ld+json">` para describir la página con vocabulario de schema.org (capítulo [63](63-publicacion-y-distribucion.md)).

**Kramdown** — Parser de Markdown en Ruby, usado por Jekyll por defecto. Tiene extensiones propias y un comportamiento específico.

**LaTeX** — Sistema de composición tipográfica de alta calidad, muy usado en matemáticas, ciencia y libros. No es Markdown, aunque se puede generar desde él.

**Linter** — Herramienta que analiza el texto y señala problemas de estilo, estructura o sintaxis. Ejemplos: markdownlint, remark-lint, Vale.

**Link reference definition** - Definición reutilizable de un enlace: `[id]: https://example.com`. Permite usar `[texto][id]` varias veces.

**llms.txt** - Convención de archivo Markdown en la raíz de un sitio con un resumen y enlaces curados para modelos de lenguaje. No es un estándar ni sustituye a `robots.txt` (capítulo [61](61-markdown-e-inteligencia-artificial.md)).

**Markdown** — Lenguaje de marcado ligero creado por John Gruber en 2004 para escribir texto estructurado de forma legible y convertirlo a HTML.

**Markdown-it** - Parser y renderizador de Markdown en JavaScript, compatible con CommonMark y extensible mediante plugins.

**MCP (Model Context Protocol)** - Protocolo abierto para conectar un modelo con herramientas y fuentes de datos. Un servidor MCP puede exponer recursos y herramientas; Markdown suele ser el formato de los recursos textuales (capítulo [61](61-markdown-e-inteligencia-artificial.md)).

**MDX** — Formato que combina Markdown con JSX y módulos ESM. Se compila a JavaScript y se usa en frameworks React. No es Markdown estándar.

**Mermaid** — Biblioteca de JavaScript que genera diagramas a partir de texto. No forma parte de Markdown ni de CommonMark; las plataformas la integran como extensión.

**Metadatos** — Información sobre el documento (título, autor, fecha, etiquetas, borrador). En Markdown suele expresarse con Front Matter.

## 56.4 Términos N-Z

**OpenAPI** - Especificación para describir APIs HTTP en YAML o JSON. Permite generar referencia interactiva y validar el contrato (capítulo [20](20-documentacion-de-apis.md)).

**Org Mode** — Modo de Emacs para notas, tareas, agendas y publicación. Tiene su propia sintaxis y no es Markdown.

**Parser** — Analizador que convierte el texto de entrada en una estructura (normalmente un AST) para que el renderer o los plugins la procesen.

**Pandoc** - Conversor universal de documentos que lee y escribe Markdown, HTML, PDF, DOCX, EPUB, LaTeX y muchos otros formatos.

**PDF/UA** - Norma ISO 14289 de accesibilidad para PDF. Exige documento etiquetado, orden de lectura lógico, idioma, texto alternativo y tablas con cabeceras. No se obtiene solo por exportar (capítulo [33](33-exportacion-a-pdf.md)).

**Prettier** - Formateador de código que también formatea Markdown. No valida semántica; normaliza el estilo.

**RAG (Retrieval-Augmented Generation)** - Técnica que recupera fragmentos de un corpus y los pasa a un modelo para responder con contexto. La estructura de Markdown influye en la calidad de la recuperación (capítulo [61](61-markdown-e-inteligencia-artificial.md)).

**Renderer** — Componente que convierte el AST o el texto parseado en HTML, PDF u otro formato de salida.

**reStructuredText (reST)** — Lenguaje de marcado usado por Docutils y Sphinx, muy habitual en documentación de Python. Tiene roles, directivas y referencias cruzadas.

**Sanitización** — Proceso de eliminar etiquetas, atributos, protocolos o contenido peligroso de HTML antes de insertarlo en una página.

**SemVer (Semantic Versioning)** - Esquema de versiones `MAJOR.MINOR.PATCH` con reglas para comunicar cambios incompatibles, nuevas funciones y correcciones.

**SEO (Search Engine Optimization)** - Conjunto de decisiones editoriales y técnicas para que el contenido sea encontrable y comprensible para los buscadores. No garantiza posiciones (capítulo [63](63-publicacion-y-distribucion.md)).

**Setext** - Estilo de encabezado que subraya el texto con `=` (H1) o `-` (H2). Solo admite dos niveles.

**Sitemap** - Archivo XML que enumera las URLs que se desea rastrear, con fecha de modificación. Se declara en `robots.txt` (capítulo [63](63-publicacion-y-distribucion.md)).

**Slug** — Versión simplificada de un título que se usa como identificador o ancla. Puede eliminar acentos, puntuación y espacios.

**Soft line break** — Salto de línea que el renderizador puede convertir en un espacio. En la mayoría de implementaciones, un salto simple no crea un nuevo párrafo.

**SSG (Static Site Generator)** — Generador de sitios estáticos. Convierte Markdown y plantillas en HTML durante el build. Ejemplos: Jekyll, Hugo, MkDocs, Astro, Docusaurus.

**Syntax highlighting** — Resaltado de sintaxis en bloques de código. Depende del lenguaje indicado y del highlighter del renderizador.

**Tabla** — Estructura de filas y columnas. En Markdown no forma parte de CommonMark; GFM y muchas extensiones la añaden.

**Thematic break** — Línea horizontal que separa secciones. Se escribe con `---`, `***` o `___`.

**TOC (Table of Contents)** - Tabla de contenidos o índice. Puede ser manual (lista de enlaces) o generada por una extensión o un SSG.

**Token** - Unidad mínima de texto que procesa un modelo de lenguaje. La longitud del contexto se mide en tokens, no en palabras o caracteres.

**UTF-8** — Codificación Unicode que puede representar prácticamente todos los caracteres. Es la codificación recomendada para Markdown.

**WCAG (Web Content Accessibility Guidelines)** — Pautas del W3C para hacer el contenido web accesible. La versión 2.2 es una recomendación estable.

**Wiki link** — Enlace con doble corchete (`[[nota]]`), típico de Obsidian, Logseq y algunas wikis. No es Markdown estándar.

**WYSIWYG** — *What You See Is What You Get*: el editor muestra el resultado final mientras se escribe. Typora y MarkText son ejemplos.

**XSS (Cross-Site Scripting)** — Ataque que consiste en inyectar código JavaScript en una página vista por otras personas. El HTML y el MDX no confiables son vectores habituales.

**YAML** — Formato de serialización legible usado en Front Matter y archivos de configuración. No es Markdown, aunque convive con él.

---

[← 55. Recursos y documentación oficial](55-recursos-y-documentacion-oficial.md) · [Índice general](README.md) · [57. FAQ →](57-faq.md)
