# 28. Generadores de sitios estáticos

> [← Índice general](README.md) · Capítulo 28 de 63

Un **generador de sitios estáticos (SSG)** convierte archivos Markdown con Front Matter en un sitio HTML que se sirve sin base de datos ni servidor de aplicación. El contenido se escribe una vez, se versiona en Git y se publica como un conjunto de archivos.

La promesa es atractiva: menos infraestructura, más velocidad y control del contenido. La contrapartida es que la búsqueda, los comentarios, la autenticación o los formularios necesitan servicios externos o no existen.

## 28.1 El pipeline

```text
Markdown + Front Matter
        ↓
  parser del dialecto
        ↓
  plantillas y layouts
        ↓
  HTML + CSS + JS + assets
        ↓
  despliegue en un host estático
```

Cada etapa añade decisiones:

- **Parser:** qué extensiones acepta (tablas, notas, matemáticas, Mermaid).
- **Plantillas:** qué lenguaje y qué grado de personalización.
- **Rutas:** cómo se generan las URLs y si cambian al mover archivos.
- **Assets:** cómo se procesan CSS, imágenes y JavaScript.
- **Build:** cuánto tarda y si se puede ejecutar en CI.

## 28.2 Tabla comparativa

| Herramienta | Lenguaje / base | Orientación | Markdown | MDX |
|---|---|---|---|---|
| Jekyll | Ruby | Blogs, GitHub Pages | Kramdown por defecto; GFM disponible | No nativo |
| MkDocs (+ Material) | Python | Documentación técnica | Python-Markdown | No |
| Docusaurus | React | Documentación y blogs | Sí (MDX) | Sí |
| Hugo | Go | Sitios rápidos, blogs y docs | Goldmark (CommonMark + extensiones) | No nativo |
| Astro | JS/TS | Sitios de contenido | Sí | Sí, con integración oficial |
| VitePress | Vue | Documentación | Markdown-it (+ Vue en Markdown) | No (usa Vue) |
| GitBook | SaaS | Documentación gestionada | Sincroniza con Markdown | Propietario |
| Quartz | Node/TS | Publicar notas de Obsidian | Markdown + sintaxis Obsidian | No |
| Gatsby | React | Sitios React (menos activo) | Sí (remark) | Sí |
| Next.js + Nextra | React | Documentación y blogs | Sí | Sí |
| Eleventy | JS | Sitios flexibles | Markdown-it | No nativo |

La tabla envejece: antes de adoptar una herramienta, comprueba la actividad del repositorio, la frecuencia de versiones y si la comunidad responde.

## 28.3 Cómo elegir

| Criterio | Pregunta |
|---|---|
| Lenguaje del equipo | ¿Quién va a mantener las plantillas y los plugins? |
| Dialecto | ¿Acepta las extensiones que necesitas? |
| Velocidad de build | ¿Cuántas páginas y cuánto tarda en CI? |
| Búsqueda | ¿Incluye índice local o exige un servicio? |
| Internacionalización | ¿Soporta varios idiomas y `hreflang`? |
| Versionado | ¿Permite publicar varias versiones del producto? |
| Despliegue | ¿Funciona en GitHub Pages o requiere otro host? |
| Comunidad | ¿Hay ejemplos, plugins y soporte? |

Para documentación técnica, MkDocs, Docusaurus, VitePress y Hugo son opciones habituales. Para un blog, Jekyll o Hugo. Para un sitio con componentes interactivos, Astro o Docusaurus. Para publicar notas de Obsidian, Quartz.

No elijas por popularidad: elige por el **mantenimiento** que puedes sostener. Un generador que nadie del equipo entiende se convierte en una caja negra.

## 28.4 Estructura típica

Aunque cada herramienta usa nombres distintos, el patrón se repite:

```text
proyecto/
├── content/ o docs/       Archivos Markdown
├── layouts/ o _layouts/   Plantillas
├── assets/ o static/      Imágenes, CSS, JS
├── _data/ o data/         Datos estructurados (navegación, versiones)
├── config.*               Configuración del sitio
└── public/ o _site/       Salida generada (no se versiona)
```

Reglas:

- **El contenido no vive en las plantillas.** Si un texto aparece en dos sitios, está en el lugar equivocado.
- **La navegación se genera desde datos**, no se escribe a mano en cada página.
- **La salida no se versiona** si se puede regenerar en CI.
- **Los assets se organizan por tipo**, no por página.

## 28.5 URLs y navegación

La URL es una interfaz pública. Decide desde el principio:

- **Con o sin barra final.**
- **Minúsculas y guiones.**
- **Fecha en la ruta** (blogs) o **estructura por secciones** (documentación).
- **Versión en la ruta** (`/v1/`, `/v2/`) si hay varias versiones.
- **Idioma en la ruta** (`/es/`, `/en/`) si hay traducciones.

Cambiar el esquema de URLs después de publicar rompe enlaces, marcadores y citas. Si el generador permite `permalink` o `slug`, fíjalo por página y documenta la regla.

La navegación debe incluir:

- Índice general y barra lateral.
- Migas de pan.
- Enlace anterior/siguiente.
- Búsqueda si el corpus es grande.
- Enlace a la página de inicio desde el logotipo.

## 28.6 Búsqueda

| Opción | Ventaja | Inconveniente |
|---|---|---|
| Índice local (Lunr, Pagefind, FlexSearch) | Sin servicio externo; privacidad | Índice que descargar; menos relevancia |
| Servicio externo (Algolia, Typesense) | Búsqueda potente y analítica | Coste, dependencia y envío de datos |
| Búsqueda del navegador | Cero configuración | Solo encuentra texto visible en la página |

Para documentación, un índice local suele ser suficiente. Si se usa un servicio externo, revisa qué datos se envían y cómo se configura la privacidad.

## 28.7 Versionado de la documentación

Un producto con versiones necesita una política:

1. **Versión activa** en la ruta principal.
2. **Versiones anteriores** en rutas separadas, solo si siguen soportadas.
3. **Aviso** en las versiones antiguas con enlace a la actual.
4. **Archivo** para lo que ya no se mantiene.
5. **Redirecciones** cuando una versión desaparece.

Duplicar todo el corpus por versión multiplica el mantenimiento. Si una página es idéntica en dos versiones, enlaza a la común o genera la variante desde una fuente única.

## 28.8 Despliegue

- **GitHub Pages:** Jekyll de forma nativa; otros generadores publican la salida mediante Actions.
- **Netlify, Vercel, Cloudflare Pages:** build automático desde el repositorio y previsualizaciones por pull request.
- **Servidor propio:** los archivos estáticos se sirven con Nginx, Caddy o similar.
- **Almacenamiento de objetos + CDN:** útil para sitios grandes o con requisitos de cache.

Comprueba siempre:

- La ruta base (`baseurl`) coincide con la del host.
- Las redirecciones funcionan en el host, no solo en local.
- Los encabezados de caché no sirven contenido antiguo.
- El sitio se genera con la misma versión de la herramienta que en local.

## 28.9 Límites

Un sitio estático no tiene, por defecto:

- Comentarios.
- Formularios con servidor.
- Autenticación.
- Contenido personalizado por usuario.
- Búsqueda global sin índice.
- Analítica sin un servicio externo.

Se pueden añadir con servicios, funciones serverless o JavaScript, pero cada añadido recupera la complejidad que el sitio estático pretendía evitar. Decide qué necesitas de verdad.

## 28.10 Lista de comprobación

- [ ] El generador y su versión están fijados.
- [ ] El dialecto de Markdown y las extensiones están documentados.
- [ ] La estructura de carpetas separa contenido, plantillas y assets.
- [ ] La salida generada no se versiona.
- [ ] Las URLs son estables y coherentes.
- [ ] La navegación se genera desde datos.
- [ ] La búsqueda funciona con el corpus real.
- [ ] La ruta base de producción está probada.
- [ ] Las redirecciones funcionan en el host.
- [ ] El build se ejecuta en CI y falla si el sitio no se genera.

---

[← 27. Badges](27-badges.md) · [Índice general](README.md) · [29. MDX: creación de páginas web con Markdown y componentes →](29-mdx-creacion-de-paginas-web-con-markdown-y-componentes.md)
