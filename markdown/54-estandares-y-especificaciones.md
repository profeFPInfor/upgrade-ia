# 54. Estándares y especificaciones

> [← Índice general](README.md) · Capítulo 54 de 63

Markdown no nació como un estándar formal. Hoy conviven el **Markdown original**, **CommonMark** y **GFM**, además de estándares independientes que se usan junto a él (HTML, YAML, Mermaid, SemVer, WCAG). Esta sección distingue qué es una especificación, qué es una convención y qué es una extensión de plataforma.

## 54.1 Marco general

| Nombre | Organización / origen | Qué define | Estado | Enlace |
|---|---|---|---|---|
| **Markdown original** | John Gruber | Sintaxis y comportamiento del `Markdown.pl` original | Descripción informal, no especificación formal | <https://daringfireball.net/projects/markdown/> |
| **CommonMark** | CommonMark Project | Especificación formal del núcleo de Markdown y suite de pruebas | Especificación comunitaria, ampliamente adoptada | <https://commonmark.org/> |
| **CommonMark Spec** | CommonMark Project | Reglas detalladas y ejemplos de conformidad | Versión vigente en el sitio | <https://spec.commonmark.org/> |
| **GFM** | GitHub | Superconjunto de CommonMark con extensiones | Especificación formal de GitHub | <https://github.github.com/gfm/> |
| **HTML** | WHATWG | Estructura y semántica de documentos web | Living Standard | <https://html.spec.whatwg.org/> |
| **Mermaid** | Mermaid Project | Sintaxis de diagramas y renderizado | Proyecto independiente | <https://mermaid.js.org/> |
| **Semantic Versioning** | semver.org | Esquema de versiones `MAJOR.MINOR.PATCH` | Especificación 2.0.0 | <https://semver.org/> |
| **Keep a Changelog** | keepachangelog.com | Formato de changelogs legibles | Especificación 1.1.0 | <https://keepachangelog.com/> |
| **WCAG 2.2** | W3C | Pautas de accesibilidad web | Recomendación del W3C | <https://www.w3.org/TR/WCAG22/> |
| **RFC 7763** | IETF | Tipo de medio `text/markdown` | RFC informativo | <https://www.rfc-editor.org/rfc/rfc7763> |
| **YAML 1.2** | YAML.org | Formato de serialización usado en Front Matter | Especificación | <https://yaml.org/spec/> |
| **Conventional Commits** | conventionalcommits.org | Convención para mensajes de commit | Especificación 1.0.0 | <https://www.conventionalcommits.org/> |

## 54.2 Markdown original

John Gruber publicó Markdown en **2004** como una sintaxis ligera y un script en Perl (`Markdown.pl`). La documentación original describe la sintaxis y el comportamiento esperado, pero **no es una especificación formal**: no define con precisión todos los casos límite.

- Sitio: <https://daringfireball.net/projects/markdown/>
- Sintaxis: <https://daringfireball.net/projects/markdown/syntax>

Es la referencia histórica. Cuando se dice "Markdown estándar" de forma coloquial, a menudo se quiere decir "Markdown original" o "CommonMark", pero conviene precisar.

## 54.3 CommonMark

**CommonMark** nació para resolver las ambigüedades del Markdown original. Define:

- Una gramática precisa.
- Una suite de ejemplos con salida HTML esperada.
- Implementaciones de referencia (`cmark` en C, `commonmark.js` en JavaScript).
- Un conjunto de extensiones posibles, que no forman parte del núcleo.

- Sitio: <https://commonmark.org/>
- Especificación: <https://spec.commonmark.org/>
- Tutorial: <https://commonmark.org/help/tutorial/>
- Dingus (probador): <https://spec.commonmark.org/dingus/>

CommonMark **no incluye** tablas, listas de tareas, tachado, notas al pie ni Mermaid. Esas funciones se añaden con extensiones o dialectos.

## 54.4 GitHub Flavored Markdown (GFM)

**GFM** es un **superconjunto estricto de CommonMark**. La especificación de GitHub define extensiones como:

- Tablas.
- Listas de tareas.
- Tachado.
- Autolinks extendidos.
- Filtro de etiquetas HTML peligrosas (*tagfilter*).

Además, github.com ofrece funciones que **no** están en la especificación GFM: alertas, Mermaid, matemáticas, notas al pie, menciones, referencias a issues, emojis, etc. Es importante no confundir "GFM" con "todo lo que hace GitHub".

- Especificación: <https://github.github.com/gfm/>
- Documentación de GitHub: <https://docs.github.com/en/get-started/writing-on-github>

## 54.5 Mermaid

**Mermaid** es una biblioteca independiente de JavaScript para generar diagramas a partir de texto. **No forma parte de Markdown, CommonMark ni GFM**. Plataformas como GitHub, GitLab, Obsidian, Docusaurus o MkDocs la integran, pero la sintaxis y el renderizado dependen de la versión y del plugin.

- Sitio: <https://mermaid.js.org/>
- Referencia de sintaxis: <https://mermaid.js.org/intro/syntax-reference.html>
- Repositorio: <https://github.com/mermaid-js/mermaid>
- Editor: <https://mermaid.live/>

## 54.6 HTML

HTML es el estándar de estructura de las páginas web. Markdown se convierte a HTML, pero **no es HTML**: no describe estilos, scripts ni el documento completo. HTML tiene su propia especificación (WHATWG) y su propia documentación (MDN).

- Especificación: <https://html.spec.whatwg.org/>
- MDN: <https://developer.mozilla.org/en-US/docs/Web/HTML>

## 54.7 Semantic Versioning

**SemVer** define el esquema `MAJOR.MINOR.PATCH` y las reglas para incrementar cada número. Es habitual en bibliotecas y se usa junto a los changelogs.

- Especificación: <https://semver.org/>
- Versión en español: <https://semver.org/lang/es/>

## 54.8 Keep a Changelog

**Keep a Changelog** propone una estructura para los archivos `CHANGELOG.md`: secciones `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed` y `Security`, con versiones y fechas.

- Sitio: <https://keepachangelog.com/>
- Versión en español: <https://keepachangelog.com/es-ES/1.1.0/>

## 54.9 WCAG

Las **Web Content Accessibility Guidelines (WCAG)** del W3C definen criterios de accesibilidad. La versión 2.2 es una recomendación estable; WCAG 3 está en desarrollo. Markdown puede contribuir a la accesibilidad con estructura, texto alternativo, enlaces descriptivos y tablas bien formadas.

- WCAG 2.2: <https://www.w3.org/TR/WCAG22/>
- Resumen: <https://www.w3.org/WAI/WCAG22/quickref/>
- WAI: <https://www.w3.org/WAI/>

## 54.10 RFC 7763 y el tipo de medio `text/markdown`

El RFC 7763 registra `text/markdown` como tipo de medio. No define la sintaxis, pero es útil para servidores, APIs y herramientas que necesitan identificar Markdown.

- RFC: <https://www.rfc-editor.org/rfc/rfc7763>

## 54.11 YAML y Front Matter

El **Front Matter** es una convención: un bloque YAML al inicio del archivo, delimitado por `---`. No forma parte de Markdown. Los generadores de sitios lo usan para metadatos (título, fecha, borrador, etiquetas, etc.).

```yaml
---
title: "Guía de instalación"
description: "Cómo instalar el proyecto"
date: 2026-10-28
tags: [instalación, linux]
draft: false
---
```

- YAML 1.2: <https://yaml.org/spec/>

## 54.12 Qué NO es un estándar

| Característica | Naturaleza | Dónde funciona |
|---|---|---|
| Alertas `> [!NOTE]` | Extensión de GitHub | GitHub y algunas plataformas |
| Mermaid | Proyecto independiente | GitHub, GitLab, Obsidian, SSG con plugin |
| Front Matter | Convención de SSG | Jekyll, Hugo, Astro, Docusaurus, etc. |
| Wikilinks `[[...]]` | Extensión de Obsidian y otros | Obsidian, Logseq, algunos SSG |
| Callouts `> [!note]` | Extensión de Obsidian | Obsidian |
| Admoniciones | Extensión de Docusaurus/MkDocs | Esas herramientas |
| Matemáticas `$...$` | Extensión | GitHub, GitLab, MathJax/KaTeX |
| Notas al pie | Extensión | GitHub, GitLab, algunos parsers |
| MDX | Formato independiente | Frameworks React compatibles |
| Tablas | GFM (no CommonMark) | GitHub, GitLab, muchos parsers con extensión |

## 54.13 Cómo citar correctamente una característica

Cuando dokumentes una función, indica su origen:

- "En **CommonMark**, los encabezados ATX…"
- "En **GFM**, las tablas…"
- "En **GitHub**, las alertas…"
- "Con **Mermaid** (proyecto independiente)…"
- "En **MDX**, los componentes…"
- "En **Obsidian**, los wikilinks…"

Esta precisión evita afirmaciones falsas del tipo "Markdown permite Mermaid" o "GFM es el estándar".

---

[← 53. Ejemplo de documento Markdown profesional](53-ejemplo-de-documento-markdown-profesional.md) · [Índice general](README.md) · [55. Recursos y documentación oficial →](55-recursos-y-documentacion-oficial.md)
