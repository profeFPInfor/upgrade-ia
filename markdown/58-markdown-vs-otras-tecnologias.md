# 58. Markdown vs otras tecnologías

> [← Índice general](README.md) · Capítulo 58 de 63

No existe una tecnología universalmente mejor. La elección depende del **contenido**, el **público**, el **flujo de publicación** y el **ecosistema** del equipo.

## 58.1 Comparación general

| Tecnología | Facilidad | Potencia | Legibilidad | Extensibilidad | Documentación | Publicación | Soporte | Casos de uso |
|---|---|---|---|---|---|---|---|---|
| **Markdown** | Muy alta | Media-baja | Muy alta | Media | Excelente | Muy amplia | Muy amplio | README, notas, guías, blogs, docs |
| **HTML** | Media-baja | Muy alta | Baja | Muy alta | Excelente | Nativa en web | Universal | Páginas web, aplicaciones, maquetación |
| **AsciiDoc** | Media | Alta | Alta | Alta | Buena | Asciidoctor, GitHub, GitLab | Medio | Libros, manuales, documentación compleja |
| **reStructuredText** | Media-baja | Alta | Media | Alta | Buena | Sphinx, Docutils | Medio (Python) | Documentación de APIs y proyectos Python |
| **LaTeX** | Baja | Muy alta | Baja-media | Muy alta | Muy amplia | PDF, DVI, PS | Alto en academia | Artículos, tesis, libros, matemáticas |
| **MDX** | Media | Muy alta | Alta | Muy alta | Buena | Frameworks React | Alto en JS | Docs interactivas, blogs, landing pages |
| **Org Mode** | Media-baja | Alta | Alta | Muy alta | Buena | Emacs, Pandoc, HTML | Medio (Emacs) | Notas, tareas, investigación, publicación |

## 58.2 Markdown

**Qué es:** lenguaje de marcado ligero, legible en texto plano y ampliamente adoptado.

**Fortalezas:** simplicidad, portabilidad, ecosistema enorme, integración con Git, conversión a múltiples formatos.

**Limitaciones:** semántica limitada, dependencia de extensiones para tablas avanzadas, matemáticas o diagramas, y diferencias entre dialectos.

**Cuándo usarlo:** README, documentación de proyectos, notas, blogs técnicos, guías y contenido que debe versionarse y revisarse como código.

## 58.3 HTML

**Qué es:** lenguaje de marcado que describe la estructura y el contenido de las páginas web.

**Fortalezas:** control total, semántica rica, integración con CSS y JavaScript, estándar universal.

**Limitaciones:** verboso, menos legible para autores no técnicos, requiere disciplina para mantener la accesibilidad y la seguridad.

**Cuándo usarlo:** páginas web finales, aplicaciones, componentes de interfaz, contenido que necesita estructura o interactividad que Markdown no ofrece.

## 58.4 AsciiDoc

**Qué es:** lenguaje de marcado ligero con una sintaxis más rica que Markdown, procesado habitualmente por Asciidoctor.

**Fortalezas:** includes, atributos, roles, referencias cruzadas, tablas complejas, admoniciones, numeración y libros. Muy usado en documentación técnica de gran escala.

**Limitaciones:** menos extendido que Markdown, curva de aprendizaje mayor, ecosistema más pequeño.

**Cuándo usarlo:** manuales extensos, libros técnicos, documentación con reutilización intensiva y necesidades semánticas que Markdown no cubre bien.

- Sitio: <https://asciidoc.org/>
- Asciidoctor: <https://docs.asciidoctor.org/>

## 58.5 reStructuredText

**Qué es:** lenguaje de marcado usado por Docutils y Sphinx, muy habitual en el ecosistema Python.

**Fortalezas:** roles y directivas, referencias cruzadas, generación de documentación de API, indexación y extensiones potentes.

**Limitaciones:** sintaxis más difícil de leer que Markdown, adopción fuera de Python menor, configuración más compleja.

**Cuándo usarlo:** documentación de proyectos Python, APIs con Sphinx, documentación que necesita referencias cruzadas y estructura formal.

- Documentación: <https://docutils.sourceforge.io/rst.html>

## 58.6 LaTeX

**Qué es:** sistema de composición tipográfica basado en TeX, orientado a documentos de alta calidad.

**Fortalezas:** control tipográfico excepcional, matemáticas, bibliografía, referencias cruzadas, estabilidad para documentos largos.

**Limitaciones:** curva de aprendizaje alta, sintaxis verbosa, compilación lenta, difícil de integrar en flujos web sin herramientas adicionales.

**Cuándo usarlo:** artículos científicos, tesis, libros, documentos con fórmulas complejas y requisitos de impresión.

- Sitio: <https://www.latex-project.org/>

## 58.7 MDX

**Qué es:** formato que combina Markdown con JSX y módulos ESM; se compila a JavaScript y se integra en frameworks React.

**Fortalezas:** contenido legible con componentes interactivos, reutilización, documentación viva, integración con el ecosistema JavaScript.

**Limitaciones:** dependencia de un compilador y un framework, menor portabilidad, riesgos de seguridad si el contenido no es de confianza, curva de aprendizaje.

**Cuándo usarlo:** documentación interactiva, blogs técnicos, landing pages, design systems y sitios donde los ejemplos deben ejecutarse o actualizarse con componentes.

- Sitio: <https://mdxjs.com/>

## 58.8 Org Mode

**Qué es:** modo de Emacs para notas, tareas, agendas, captura y publicación. Usa una sintaxis propia basada en encabezados y palabras clave.

**Fortalezas:** organización jerárquica, TODOs, tablas, bloques de código, *literate programming*, exportación a HTML/LaTeX/PDF y automatización.

**Limitaciones:** ligado a Emacs, sintaxis específica, ecosistema más pequeño y menor interoperabilidad con herramientas web.

**Cuándo usarlo:** gestión personal del conocimiento, investigación, planificación y documentos que se benefician de la integración con Emacs.

- Sitio: <https://orgmode.org/>

## 58.9 Cómo elegir

| Si necesitas… | Considera… |
|---|---|
| Máxima portabilidad y simplicidad | Markdown |
| Control total de una página web | HTML + CSS/JS |
| Documentación técnica extensa con reutilización | AsciiDoc o reStructuredText |
| Matemáticas y tipografía de calidad | LaTeX |
| Componentes interactivos en documentación | MDX |
| Notas y planificación integradas en Emacs | Org Mode |

---

[← 57. FAQ](57-faq.md) · [Índice general](README.md) · [59. Recomendaciones finales →](59-recomendaciones-finales.md)
