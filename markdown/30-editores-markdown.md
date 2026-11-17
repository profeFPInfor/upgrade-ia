# 30. Editores Markdown

> [← Índice general](README.md) · Capítulo 30 de 63

Un editor Markdown no cambia la sintaxis del lenguaje, pero sí influye en la **experiencia de escritura**, la **previsualización**, el **soporte de extensiones**, el **linting**, la **gestión de archivos** y la **exportación**. La elección depende del uso: documentación de software, notas personales, escritura académica o edición rápida en terminal.

## 30.1 Criterios para elegir un editor

| Criterio | Preguntas útiles |
|---|---|
| Modelo de edición | ¿Se escribe Markdown puro, con previsualización lateral o en modo WYSIWYG? |
| Extensiones | ¿Admite tablas GFM, notas al pie, matemáticas, Mermaid, Front Matter? |
| Ecosistema | ¿Tiene plugins, correctores, linting, integración con Git? |
| Plataformas | ¿Se necesita Windows, macOS, Linux, móvil o web? |
| Licencia y coste | ¿Software libre, gratuito o de pago? ¿Uso comercial permitido? |
| Portabilidad | ¿Los archivos son `.md` estándar o usan un dialecto propietario? |
| Rendimiento | ¿Aguanta proyectos grandes, búsquedas y grafos de notas? |
| Exportación | ¿PDF, HTML, DOCX, EPUB, LaTeX? ¿Con plantillas? |
| Accesibilidad | ¿Navegación por teclado, lector de pantalla, contraste? |

## 30.2 Comparativa general

| Editor | Tipo | Licencia / precio | Plataformas | Previsualización | Extensibilidad | Punto fuerte | Limitación principal |
|---|---|---|---|---|---|---|---|
| **Visual Studio Code** | Editor de código | MIT (código) | Windows, macOS, Linux, web | Lateral integrada | Muy alta (extensiones) | Ecosistema y Git | Configuración para docs avanzadas |
| **Obsidian** | Base de conocimiento | Propietario; gratis para uso personal | Windows, macOS, Linux, iOS, Android | En vivo / fuente | Alta (plugins y temas) | Enlaces, backlinks y grafo | Dialecto propio; no es estándar |
| **Typora** | Editor WYSIWYG | De pago | Windows, macOS, Linux | WYSIWYG | Media | Escritura sin distracciones | Cerrado y sin plugins potentes |
| **MarkText** | Editor WYSIWYG | MIT | Windows, macOS, Linux | WYSIWYG / fuente | Baja | Sencillo y ligero | Desarrollo poco activo |
| **Zettlr** | Escritura académica | GPL-3.0 | Windows, macOS, Linux | En vivo | Media | Citas, Zotero y exportación | Curva de aprendizaje |
| **Vim / Neovim** | Editor modal | Vim / Apache-2.0 | Multiplataforma | Plugins | Muy alta | Velocidad y control | Configuración manual |
| **Emacs** | Editor extensible | GPL-3.0 | Multiplataforma | `markdown-mode` | Muy alta | Org Mode y personalización | Curva muy pronunciada |
| **Zed** | Editor colaborativo | GPL-3.0 | macOS, Linux (Windows en desarrollo) | Integrada | Media | Rendimiento y colaboración | Ecosistema joven |
| **JetBrains IDEs** | IDE | Propietario (freemium) | Multiplataforma | Integrada | Alta | Integración con el código | Pesado para solo Markdown |
| **Ghostwriter** | Escritura sin distracciones | GPL-3.0 | Windows, Linux | En vivo | Baja | Enfoque y simplicidad | Funciones limitadas |
| **iA Writer** | Escritura | De pago | macOS, iOS, Windows | WYSIWYG | Baja | Tipografía y enfoque | Coste y ecosistema cerrado |
| **Logseq** | Outliner / PKM | AGPL-3.0 | Multiplataforma | En vivo | Alta | Notas enlazadas y diarios | No es un editor de docs clásico |
| **Joplin** | Notas | AGPL-3.0 | Multiplataforma | Markdown / WYSIWYG | Media | Sincronización y cifrado | Interfaz menos pulida |

> La licencia y el precio pueden cambiar. Comprueba siempre la página oficial y, si el uso es comercial, revisa las condiciones concretas.

## 30.3 Visual Studio Code

**Qué es:** editor de código gratuito y de código abierto desarrollado por Microsoft, basado en Electron. Es una de las opciones más usadas para documentación *docs-as-code* porque integra edición, Git, terminal, tareas y extensiones en un solo entorno.

**Uso básico con Markdown:**

- Abrir un `.md` y pulsar `Ctrl+Shift+V` (Windows/Linux) o `Cmd+Shift+V` (macOS) para la previsualización.
- `Ctrl+K V` abre la previsualización al lado.
- El esquema del documento (*Outline*) muestra la jerarquía de títulos.
- La paleta de comandos permite "Markdown: Open Preview to the Side".

**Extensiones habituales:**

| Extensión | Para qué sirve |
|---|---|
| Markdown All in One | Atajos, índice, numeración y formato |
| markdownlint | Reglas de estilo y estructura |
| Markdown Preview Mermaid Support | Diagramas Mermaid en la previsualización |
| Markdown Preview Enhanced | Exportación, matemáticas y diagramas |
| Paste Image | Pegar capturas como archivos |
| Code Spell Checker | Corrección ortográfica |
| GitLens | Contexto de Git en el editor |

**Configuración de ejemplo** (`settings.json`):

```json
{
  "editor.wordWrap": "on",
  "editor.formatOnSave": true,
  "markdown.preview.breaks": false,
  "markdown.preview.typographer": true,
  "markdown.validate.enabled": true
}
```

> `markdown.preview.breaks` cambia el tratamiento de los saltos de línea y **no** reproduce exactamente GitHub. Para validar la compatibilidad real, usa el renderizador de destino o un linting específico.

**Ventajas:** ecosistema enorme, Git integrado, terminal, linting, previsualización, soporte de muchos lenguajes y *workspaces*.

**Limitaciones:** la previsualización no es idéntica a GitHub, GitLab o al sitio final; requiere extensiones para Mermaid, matemáticas o exportación avanzada; el consumo de recursos es alto.

- Documentación oficial: <https://code.visualstudio.com/docs/languages/markdown>

## 30.4 Obsidian

**Qué es:** aplicación de notas y base de conocimiento local que trabaja sobre una carpeta (*vault*) de archivos Markdown. Su propuesta central son los enlaces bidireccionales, el grafo de notas y los plugins.

**Características Markdown:**

- Archivos `.md` en disco, sin base de datos propietaria para el contenido.
- **Wikilinks** `[[Otra nota]]` y enlaces con alias `[[nota|texto]]`.
- **Embeds** `![[imagen.png]]` o `![[nota]]`.
- **Callouts** con sintaxis propia:

```markdown
> [!note]
> Esto es una nota.

> [!warning]
> Esto es una advertencia.
```

- Etiquetas `#etiqueta`, propiedades en Front Matter y bloques de código.
- Soporte de Mermaid, matemáticas y plugins de la comunidad.

**Ventajas:** excelente para notas personales, investigación y documentación interconectada; búsqueda rápida; funcionamiento local; comunidad grande.

**Limitaciones:** los wikilinks, callouts y embeds **no son Markdown estándar**; GitHub no los interpreta igual; el ecosistema de plugins puede afectar al rendimiento y a la seguridad; la sincronización oficial es de pago.

- Sitio oficial: <https://obsidian.md/>
- Ayuda: <https://help.obsidian.md/>

## 30.5 Typora

**Qué es:** editor WYSIWYG que muestra el resultado mientras se escribe, sin una ventana de previsualización separada. Es popular para escritura de artículos, apuntes y documentos que se exportan a PDF.

**Características:** tablas, listas de tareas, notas al pie, matemáticas, diagramas Mermaid, índices, imágenes y exportación a PDF, HTML, DOCX, EPUB y LaTeX (según versión y configuración).

**Ventajas:** experiencia de escritura muy limpia; buen renderizado; exportación integrada; curva de aprendizaje baja.

**Limitaciones:** software **de pago y cerrado**; menos orientado a repositorios grandes; la personalización y la automatización son limitadas; no es la mejor opción si se necesita linting o CI.

- Sitio oficial: <https://typora.io/>

## 30.6 MarkText

**Qué es:** editor Markdown de código abierto, multiplataforma y con enfoque WYSIWYG. Permite alternar entre modo fuente y modo visual, y ofrece modos de enfoque y máquina de escribir.

**Ventajas:** gratuito, ligero, interfaz sencilla, soporte de tablas, matemáticas, diagramas y exportación a HTML/PDF.

**Limitaciones:** el desarrollo es menos activo que el de otras alternativas; el ecosistema de plugins es reducido; algunas funciones avanzadas dependen de la versión.

- Sitio oficial: <https://www.marktext.cc/>
- Repositorio: <https://github.com/marktext/marktext>

## 30.7 Zettlr

**Qué es:** editor orientado a la escritura académica y a la gestión de conocimiento. Combina Markdown con citas bibliográficas, integración con Zotero, exportación mediante Pandoc y organización por espacios de trabajo.

**Características:** Front Matter YAML, enlaces internos, etiquetas, estadísticas, modo enfoque, exportación a PDF/DOCX/LaTeX y soporte de sintaxis matemática.

**Ventajas:** muy adecuado para tesis, artículos e informes con bibliografía; software libre; flujo de trabajo académico completo.

**Limitaciones:** más complejo que un editor básico; la configuración de citas y plantillas requiere tiempo; no está pensado para documentación de API.

- Sitio oficial: <https://www.zettlr.com/>

## 30.8 Vim y Neovim

**Qué son:** editores modales de terminal, altamente configurables y eficientes para usuarios con experiencia. Neovim es un fork moderno de Vim con soporte de Lua, LSP y plugins asíncronos.

**Plugins habituales:**

| Plugin | Función |
|---|---|
| `preservim/vim-markdown` | Resaltado, plegado y navegación |
| `iamcco/markdown-preview.nvim` | Previsualización en navegador |
| `nvim-treesitter` | Resaltado y análisis sintáctico |
| `nvim-telescope/telescope.nvim` | Búsqueda de archivos y texto |
| `mason.nvim` + LSP | Autocompletado y diagnóstico |

**Ventajas:** velocidad, control total, funcionamiento en servidores remotos, integración con Git y herramientas de terminal.

**Limitaciones:** curva de aprendizaje alta; la previsualización y el soporte de Mermaid requieren plugins; no es adecuado para usuarios que prefieren WYSIWYG.

- Neovim: <https://neovim.io/>
- `vim-markdown`: <https://github.com/preservim/vim-markdown>

## 30.9 Emacs

**Qué es:** editor extensible, con una de las comunidades más antiguas del software libre. Para Markdown se usa `markdown-mode`, que ofrece resaltado, navegación por títulos, comandos de formato y previsualización.

**Ventajas:** personalización prácticamente ilimitada; Org Mode para notas y publicación; integración con Git, LaTeX y Pandoc; funciona en terminal.

**Limitaciones:** configuración y curva de aprendizaje muy altas; la experiencia Markdown depende de paquetes externos; el ecosistema es menos accesible para principiantes.

- `markdown-mode`: <https://jblevins.org/projects/markdown-mode/>

## 30.10 Otros editores relevantes

- **Zed:** editor moderno y rápido, con previsualización de Markdown, colaboración en tiempo real y soporte de LSP. Ideal si se busca rendimiento y trabajo en equipo. <https://zed.dev/>
- **JetBrains IDEs (IntelliJ IDEA, PyCharm, WebStorm…):** previsualización integrada, refactorización, Git y soporte de Markdown. Útil cuando la documentación vive junto al código. <https://www.jetbrains.com/help/idea/markdown.html>
- **Ghostwriter:** editor minimalista y libre, con modo enfoque, corrector y previsualización. <https://ghostwriter.kde.org/>
- **iA Writer:** editor de pago centrado en tipografía y concentración, con sintaxis Markdown y exportación. <https://ia.net/writer>
- **Logseq:** outliner local con Markdown, enlaces, diarios y plugins; orientado a gestión personal del conocimiento. <https://logseq.com/>
- **Joplin:** aplicación de notas con Markdown, sincronización, cifrado de extremo a extremo y clientes multiplataforma. <https://joplinapp.org/>

## 30.11 Qué editor elegir según el caso

| Necesidad | Opciones recomendadas |
|---|---|
| Documentación en un repositorio Git | VS Code, Neovim, JetBrains, Zed |
| Notas personales y base de conocimiento | Obsidian, Logseq, Joplin |
| Escritura académica con bibliografía | Zettlr, Emacs + Org Mode, VS Code + Pandoc |
| Edición WYSIWYG sencilla | Typora, MarkText |
| Escritura sin distracciones | Ghostwriter, iA Writer, Typora |
| Trabajo en terminal o servidor remoto | Vim, Neovim, Emacs |
| Colaboración en tiempo real | Zed, VS Code Live Share |

## 30.12 Recomendaciones prácticas

1. Guarda siempre en **UTF-8** y, si el proyecto es multiplataforma, usa **LF** como salto de línea.
2. Mantén los archivos en una carpeta versionada con Git; evita depender de una base de datos propietaria.
3. Activa el **linting** y la **previsualización** antes de publicar.
4. Si la portabilidad importa, limita el uso de sintaxis específica del editor (wikilinks, callouts propietarios, plugins).
5. Revisa cómo se ve el documento en el **renderizador final** (GitHub, GitLab, MkDocs, Docusaurus), no solo en el editor.
6. Haz copias de seguridad y prueba la exportación antes de depender de ella.

---

[← 29. MDX: creación de páginas web con Markdown y componentes](29-mdx-creacion-de-paginas-web-con-markdown-y-componentes.md) · [Índice general](README.md) · [31. Conversión de Markdown →](31-conversion-de-markdown.md)
