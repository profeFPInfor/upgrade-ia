# 57. FAQ

> [← Índice general](README.md) · Capítulo 57 de 63

## 57.1 Conceptos básicos

**¿Markdown es un lenguaje de programación?**
No. Es un **lenguaje de marcado ligero**: describe estructura y formato, pero no tiene variables, bucles, funciones ni ejecución. Los documentos Markdown se convierten a otro formato mediante un programa.

**¿Markdown es un lenguaje de marcado?**
Sí. Al igual que HTML, indica estructura (títulos, párrafos, listas, enlaces), pero con una sintaxis mucho más simple y legible.

**¿Markdown es un estándar?**
No hay un único estándar. El Markdown original es una descripción informal; **CommonMark** es una especificación formal del núcleo; **GFM** es una especificación de GitHub sobre CommonMark. Muchas funciones habituales son extensiones.

**¿Markdown y HTML son lo mismo?**
No. Markdown es una sintaxis de autoría; HTML es el lenguaje de estructura de la web. Markdown se convierte a HTML, pero no describe estilos, scripts ni una página completa.

**¿Qué diferencia hay entre Markdown y HTML?**
Markdown es más legible y breve; HTML es más potente y permite control total. Markdown está pensado para contenido; HTML para la estructura final de una página. Véase [1.8](01-introduccion-a-markdown.md#18-markdown-vs-html).

**¿Qué es CommonMark?**
Una especificación formal del núcleo de Markdown, con ejemplos y pruebas de conformidad. Es la base más portable para escribir Markdown. Véase [sección 11](11-commonmark.md).

**¿Qué es GFM?**
**GitHub Flavored Markdown**: un superconjunto estricto de CommonMark con tablas, listas de tareas, tachado, autolinks y filtro de HTML peligroso. GitHub añade además funciones de plataforma. Véase [sección 10](10-github-flavored-markdown-gfm.md).

**¿Qué Markdown utiliza GitHub?**
GFM, más funciones propias de github.com: alertas, Mermaid, matemáticas, menciones, referencias a issues, etc. No todas forman parte de la especificación GFM.

**¿Qué es un dialecto?**
Una variante de Markdown con reglas o extensiones propias. GFM, Kramdown, Python-Markdown y Obsidian Flavored Markdown son dialectos. Véase [sección 12](12-variantes-y-dialectos-de-markdown.md).

**¿Markdown es gratis?**
La sintaxis es libre y abierta; no hay que pagar por escribir Markdown. Algunos editores o servicios son de pago, pero existen alternativas libres.

**¿Quién creó Markdown?**
John Gruber, con contribuciones de Aaron Swartz, en 2004. Publicó la sintaxis y el script `Markdown.pl`.

**¿Markdown sirve para programar?**
No. Sirve para documentar código, escribir README, comentar decisiones y generar documentación. Para programar se usan lenguajes de programación.

## 57.2 Sintaxis y compatibilidad

**¿Cómo hago un título?**
Con `#` para H1, `##` para H2, hasta `######` para H6: `# Título`. Deja un espacio después de las almohadillas.

**¿Cómo pongo negrita y cursiva?**
Negrita: `**texto**`; cursiva: `*texto*`; ambas: `***texto***`.

**¿Cómo hago una tabla?**
Con filas separadas por `|` y una fila de separación `|---|---|`. Es GFM o una extensión; no CommonMark. Ejemplo en [sección 5](05-tablas.md).

**¿Cómo pongo una imagen?**
`![texto alternativo](ruta-o-url)`. El texto alternativo es obligatorio para accesibilidad. Ejemplo en [sección 18](18-imagenes-y-recursos-multimedia.md).

**¿Cómo enlazo a otra sección?**
`[texto](#ancla)`. El ancla suele ser el título en minúsculas, sin puntuación y con guiones. Si el renderizador cambia el ID, copia el ancla real. Véase [sección 17](17-enlaces-internos.md).

**¿Cómo escribo código?**
En línea, con backticks: `` `código` ``. En bloque, con tres backticks y el lenguaje:

````markdown
```python
print("Hola")
```
````

**¿Cómo hago una lista de tareas?**
`- [ ] pendiente` y `- [x] hecho`. Es GFM o una extensión; no CommonMark. Véase [sección 6](06-listas-de-tareas.md).

**¿Cómo pongo notas al pie?**
`Texto[^1]` y, en otra línea, `[^1]: Nota`. Es una extensión; no todos los renderizadores la admiten.

**¿Cómo escribo matemáticas?**
Con `$...$` en línea o `$$...$$` en bloque, siempre que el renderizador tenga MathJax o KaTeX. No es Markdown estándar.

**¿Puedo usar HTML dentro de Markdown?**
Sí, en muchos renderizadores, pero puede estar deshabilitado o sanitizado. No dependas de HTML para contenido esencial. Véase [sección 13](13-html-dentro-de-markdown.md).

**¿Puedo crear diagramas?**
Sí, con Mermaid si la plataforma lo soporta, o con una imagen SVG/PNG generada aparte. Mermaid no es parte de Markdown. Véanse [sección 14](14-mermaid.md) y [sección 29.9](29-mdx-creacion-de-paginas-web-con-markdown-y-componentes.md#299-mdx-y-mermaid).

**¿Qué es Mermaid?**
Una biblioteca de JavaScript que genera diagramas a partir de texto. Se integra en GitHub, GitLab, Obsidian, Docusaurus y otros, pero no es estándar.

**¿Por qué no se renderiza mi HTML?**
Puede estar deshabilitado por el parser, eliminado por el sanitizador o bloqueado por la plataforma. Revisa la configuración y la política de seguridad del destino.

**¿Por qué GitHub no muestra mi Mermaid?**
Comprueba que el bloque usa el lenguaje `mermaid`, que la sintaxis es válida y que el repositorio se muestra en una vista compatible. GitHub no renderiza Mermaid dentro de un archivo `.mdx` como si fuera MDX.

**¿Cómo hago un salto de línea?**
Para un nuevo párrafo, deja una línea en blanco. Para un salto duro dentro del párrafo, usa dos espacios al final o `\` (CommonMark).

**¿Cómo escapo caracteres especiales?**
Con una barra invertida: `\*`, `\_`, `\[`, `\]`, `\<`, `\>`, `\|`, `\{`, `\}`. En bloques de código no hace falta.

**¿Puedo usar tablas en CommonMark?**
No. CommonMark no incluye tablas; GFM y muchas extensiones sí. Si necesitas portabilidad, ofrece una lista equivalente.

**¿Cómo anido listas?**
Indenta 2–4 espacios respecto al marcador padre y mantén el mismo tipo de marcador. Deja una línea en blanco si el elemento contiene varios párrafos.

## 57.3 Herramientas y conversión

**¿Puedo convertir Markdown a PDF?**
Sí. Pandoc es la opción más completa; también existen `md-to-pdf`, navegadores y motores HTML/CSS. Véase [sección 31](31-conversion-de-markdown.md).

**¿Cómo convierto Markdown a DOCX?**
`pandoc README.md -o README.docx --reference-doc=plantilla.docx`. Revisa tablas, imágenes y estilos después de convertir.

**¿Qué editor Markdown debería utilizar?**
Depende del uso: VS Code para repositorios, Obsidian para notas, Typora para WYSIWYG, Zettlr para escritura académica, Vim/Emacs para terminal. Véase [sección 30](30-editores-markdown.md).

**¿Markdown funciona en Word?**
Word no interpreta Markdown de forma nativa. Puedes convertir a DOCX con Pandoc o abrir el texto y aplicar estilos manualmente.

**¿Cómo mantengo los enlaces sin romperse?**
Usa rutas relativas, evita cambios de nombres, comprueba con lychee o markdown-link-check y ejecuta la validación en CI.

**¿Qué es un linter?**
Una herramienta que analiza el documento y señala problemas de estilo o estructura. markdownlint es el más habitual para Markdown. Véase [sección 46](46-linting-y-validacion.md).

**¿Qué es un SSG?**
Un generador de sitios estáticos: convierte Markdown y plantillas en HTML durante el build. Ejemplos: Jekyll, Hugo, MkDocs, Astro, Docusaurus. Véase [sección 28](28-generadores-de-sitios-estaticos.md).

**¿Qué es Front Matter?**
Un bloque de metadatos al inicio del archivo, normalmente YAML, usado por SSG para título, fecha, etiquetas y otras propiedades. No es Markdown estándar. Véase [sección 24](24-front-matter.md).

**¿Qué es docs-as-code?**
Tratar la documentación como código: archivos en Git, revisión en pull requests, linting, pruebas y despliegue automatizado.

**¿Cómo versiono la documentación?**
Con etiquetas y ramas de Git, y con versionado del sitio (por ejemplo, `/v1/`, `/v2/`) cuando la herramienta lo permita. Mantén un changelog y marca lo obsoleto.

## 57.4 Documentación, MDX y web

**¿Markdown sirve para documentación profesional?**
Sí. Es el formato habitual de README, guías, manuales, documentación de API y sitios de documentación. Requiere estructura, revisión y herramientas de validación.

**¿Markdown sirve para documentar una API?**
Sí, para la parte narrativa y los ejemplos. Para la especificación formal de la API suele usarse OpenAPI/Swagger, y Markdown se integra con esas herramientas.

**¿Markdown sirve para una página web?**
Sí, con un generador de sitios estáticos o un framework. Para interactividad y componentes se puede usar MDX. Véase [sección 29](29-mdx-creacion-de-paginas-web-con-markdown-y-componentes.md).

**¿Qué diferencia hay entre Markdown y MDX?**
Markdown es texto con formato; MDX añade JSX, componentes, `import`/`export` y expresiones JavaScript. MDX necesita un compilador y un framework compatible. Véase [29.13](29-mdx-creacion-de-paginas-web-con-markdown-y-componentes.md#2913-mdx-frente-a-markdown).

**¿Debo usar `.md` o `.mdx`?**
`.md` si buscas portabilidad y contenido textual. `.mdx` si necesitas componentes, interactividad y tu herramienta lo soporta. No uses `.mdx` para contenido que deba verse en GitHub como página.

**¿Puedo usar React en Markdown?**
No en Markdown estándar. Puedes usar MDX o incluir HTML/JS en un sitio que lo permita, con las precauciones de seguridad.

**¿Qué es un componente?**
Una unidad reutilizable de interfaz (un botón, una tarjeta, una alerta) que recibe props y devuelve JSX. En MDX se inserta como `<Componente />`.

**¿Qué es un AST?**
El árbol de sintaxis abstracta: una representación estructurada del documento que usan parsers, linters y plugins para analizarlo y transformarlo.

**¿Qué es un parser?**
El analizador que convierte el texto en una estructura (AST). CommonMark, markdown-it, remark y Python-Markdown son parsers.

**¿Qué es un renderizador?**
El componente que convierte el AST o el texto parseado en HTML, PDF u otro formato. Un parser puede incluir su propio renderizador.

**¿Qué diferencia hay entre Markdown y AsciiDoc?**
AsciiDoc es más rico semánticamente (incluye, atributos, roles, referencias), pero más complejo. Markdown es más simple y extendido. Véase [sección 58](58-markdown-vs-otras-tecnologias.md).

**¿Qué diferencia hay entre Markdown y LaTeX?**
LaTeX ofrece control tipográfico y matemático muy superior; Markdown es más sencillo y legible. Para artículos científicos o libros, LaTeX suele ser mejor; para documentación web, Markdown.

## 57.5 Seguridad y accesibilidad

**¿Es seguro renderizar Markdown de usuarios?**
No sin precauciones. El Markdown puede contener HTML, enlaces peligrosos o imágenes de seguimiento. Desactiva HTML o sanitiza la salida y aplica una CSP. Véase [sección 48](48-seguridad.md).

**¿Qué es XSS?**
Cross-Site Scripting: inyección de código JavaScript que se ejecuta en el navegador de otra persona. Puede robar sesiones, modificar la página o redirigir a sitios maliciosos.

**¿Cómo hago mi Markdown accesible?**
Usa títulos jerárquicos, texto alternativo, enlaces descriptivos, tablas con encabezados, lenguaje claro y contraste suficiente. Véase [sección 47](47-accesibilidad.md).

**¿Cómo pongo texto alternativo?**
`![Descripción de la imagen](imagen.png)`. Si es decorativa, `![](imagen.png)` o, mejor, usa CSS. No empieces con "imagen de".

**¿Qué es WCAG?**
Las Web Content Accessibility Guidelines del W3C. La versión 2.2 define criterios como contraste, texto alternativo, navegación por teclado y estructura semántica.

**¿Puedo confiar en el HTML de un README?**
Si el README es tuyo, sí; si viene de terceros, trátalo como contenido no confiable. GitHub sanea, pero tu sitio puede no hacerlo.

**¿Qué es la sanitización?**
El proceso de eliminar etiquetas, atributos y protocolos peligrosos del HTML. Se hace con bibliotecas como DOMPurify o rehype-sanitize, no con expresiones regulares caseras.

**¿Cómo evito dependencias inseguras?**
Fija versiones, usa archivos de bloqueo, ejecuta auditorías, revisa plugins y acciones de CI, y desconfía de paquetes con nombres similares a los oficiales.

---

[← 56. Glosario](56-glosario.md) · [Índice general](README.md) · [58. Markdown vs otras tecnologías →](58-markdown-vs-otras-tecnologias.md)
