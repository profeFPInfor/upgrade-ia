# 63. Publicación y distribución: SEO, metadatos y feeds

> [← Índice general](README.md) · Capítulo 63 de 63

Convertir Markdown en HTML es solo la mitad del trabajo. Una vez publicado, el contenido compite por atención con millones de páginas: necesita títulos comprensibles, URLs estables, metadatos correctos, un sitemap y, si el proyecto lo justifica, un feed. Nada de esto garantiza posiciones en un buscador; todo ello evita que el contenido sea difícil de encontrar, de compartir o de citar.

Este capítulo trata la publicación como una cadena de decisiones editoriales y técnicas, no como una lista de trucos.

## 63.1 Del Markdown al sitio publicado

Un generador de sitios estáticos convierte cada archivo en una página y usa el Front Matter para completar la plantilla:

```yaml
---
title: "Instalación en Linux"
description: "Requisitos, pasos y verificación para instalar la herramienta en Linux."
slug: "instalacion-linux"
canonical: "https://ejemplo.com/guia/instalacion-linux/"
image: "/assets/instalacion-linux.png"
date: 2026-10-28
updated: 2026-10-28
noindex: false
---
```

| Campo | Uso | Obligatorio |
|---|---|---|
| `title` | Título visible y etiqueta `<title>` | Sí |
| `description` | Resumen para buscadores y redes | Recomendado |
| `slug` | Parte final de la URL | Según el generador |
| `canonical` | URL preferida si hay duplicados | Solo si hay duplicados |
| `image` | Imagen social | Recomendado |
| `date` / `updated` | Fechas de publicación y modificación | Recomendado |
| `noindex` | Excluir una página de los buscadores | Solo en casos concretos |

La plantilla debe imprimir esos valores una sola vez y con escapes correctos. Un título con comillas mal escapadas rompe el HTML; una descripción ausente deja que el buscador invente el fragmento.

## 63.2 Títulos, descripciones y estructura

Un título útil dice **qué** ofrece la página y **para quién**:

| Mal | Mejor |
|---|---|
| Introducción | Instalar la CLI en Linux paso a paso |
| API | Referencia de la API de pagos |
| Documentación | Guía de migración de la versión 1 a la 2 |

Recomendaciones, no reglas:

- Un solo `<h1>` por página y jerarquía sin saltos.
- Títulos únicos: dos páginas con el mismo título compiten entre sí.
- Como orientación, un `<title>` de 50-60 caracteres se muestra completo en muchos resultados; los buscadores pueden reescribirlo.
- Una descripción de 150-160 caracteres suele ser suficiente; también puede reescribirse.
- Enlaces internos con texto descriptivo, no «clic aquí».
- Encabezados que se entiendan fuera de contexto: ayudan a las personas y a los sistemas de recuperación.

El capítulo [17](17-enlaces-internos.md) detalla los enlaces internos y el [47](47-accesibilidad.md) la estructura accesible.

## 63.3 URL, canonical y redirecciones

La URL es una interfaz pública. Cambiarla rompe enlaces, marcadores y citas.

- **Elige una forma y mantenla:** con o sin barra final, minúsculas, guiones.
- **Evita fechas y números de versión en la ruta** salvo que la versión sea parte del contrato (`/v1/`, `/v2/`).
- **No incluyas parámetros innecesarios:** `?utm_source=` no debe definir la página canónica.
- **Usa una URL canónica absoluta** cuando existan duplicados (por ejemplo, con y sin `www`, o con parámetros de campaña).
- **Redirige con 301** los cambios permanentes; evita cadenas de redirecciones.

```html
<link rel="canonical" href="https://ejemplo.com/guia/instalacion-linux/">
```

La etiqueta canónica es una **señal**, no una orden: los buscadores pueden ignorarla si detectan contradicciones. Debe apuntar a la versión que quieres indexar y ser coherente con el sitemap y los enlaces internos.

En un sitio estático, las redirecciones dependen del host. GitHub Pages no ofrece reglas de servidor arbitrarias; si usas Jekyll, el plugin `jekyll-redirect-from` genera páginas de redirección y está en la lista de plugins admitidos. Si el generador no lo permite, una página de aviso con enlace permanente es la alternativa, aunque no equivale a un 301.

Para contenido multilingüe, `hreflang` indica las variantes (véase [45.8](45-internacionalizacion-y-escritura-multilingue.md)). Debe ser recíproco: cada versión enlaza a todas las demás y a sí misma.

## 63.4 Open Graph y tarjetas sociales

Cuando alguien comparte una URL, la red social genera una tarjeta con título, descripción e imagen. Open Graph define esas propiedades:

```html
<meta property="og:type" content="article">
<meta property="og:title" content="Instalación en Linux">
<meta property="og:description" content="Requisitos, pasos y verificación.">
<meta property="og:url" content="https://ejemplo.com/guia/instalacion-linux/">
<meta property="og:image" content="https://ejemplo.com/assets/instalacion-linux.png">
<meta property="og:site_name" content="Guía de ejemplo">
<meta name="twitter:card" content="summary_large_image">
```

Buenas prácticas:

- **URLs absolutas** en `og:url` y `og:image`; una ruta relativa puede fallar.
- **Una imagen por página**, representativa y legible en miniatura. El formato 1200 × 630 es habitual, pero cada red puede recortar de forma distinta.
- **Texto alternativo** en la imagen social cuando la plataforma lo permita.
- **Descripciones específicas**, no el mismo texto para todo el sitio.
- **Comprueba la vista previa** con las herramientas de cada plataforma antes de publicar.

Open Graph es un protocolo abierto ([ogp.me](https://ogp.me/)); las redes pueden añadir o ignorar propiedades. No existe una garantía de que la tarjeta se muestre exactamente como la diseñas.

## 63.5 Datos estructurados

Los datos estructurados describen la página en un vocabulario que los buscadores pueden interpretar. El formato más habitual es JSON-LD dentro de un `<script type="application/ld+json">`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "Instalación en Linux",
  "description": "Requisitos, pasos y verificación para instalar la herramienta.",
  "datePublished": "2026-10-28",
  "dateModified": "2026-10-28",
  "author": {
    "@type": "Organization",
    "name": "Equipo de documentación"
  },
  "url": "https://ejemplo.com/guia/instalacion-linux/"
}
</script>
```

- Usa tipos de [schema.org](https://schema.org/) que describan el contenido real: `TechArticle`, `HowTo`, `FAQPage`, `BreadcrumbList`.
- Los datos deben coincidir con lo visible. Marcar un `FAQPage` sin preguntas visibles es una mala práctica.
- Valida con la prueba de resultados enriquecidos de Google y con el validador de schema.org.
- Los resultados enriquecidos cambian con el tiempo: una página puede ser válida y no recibir el tratamiento especial que esperabas.

Los datos estructurados no sustituyen al contenido ni mejoran por sí solos la calidad. Ayudan a que un buscador entienda la página cuando ya la ha rastreado.

## 63.6 Sitemap y robots.txt

Un sitemap enumera las URLs que quieres que se rastreen:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://ejemplo.com/guia/</loc>
    <lastmod>2026-10-28</lastmod>
  </url>
  <url>
    <loc>https://ejemplo.com/guia/instalacion-linux/</loc>
    <lastmod>2026-10-28</lastmod>
  </url>
</urlset>
```

- `lastmod` debe reflejar un cambio real, no la fecha de generación del sitio.
- Incluye solo páginas canónicas e indexables.
- Si hay muchas URLs, usa un índice de sitemaps.
- Envía el sitemap a Google Search Console y a Bing Webmaster Tools.
- Declara su ubicación en `robots.txt`:

```text
User-agent: *
Allow: /

Sitemap: https://ejemplo.com/sitemap.xml
```

`robots.txt` controla el rastreo, no la indexación. Una página bloqueada puede seguir apareciendo si otros sitios la enlazan; para excluirla de los resultados, usa `noindex` además de las reglas de rastreo.

## 63.7 RSS y Atom

Un feed permite que lectores y agregadores sigan las novedades sin visitar el sitio. RSS 2.0 y Atom son formatos distintos; elige uno y sé consistente.

RSS 2.0:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Guía de ejemplo</title>
    <link>https://ejemplo.com/guia/</link>
    <description>Artículos y actualizaciones</description>
    <language>es</language>
    <item>
      <title>Instalación en Linux</title>
      <link>https://ejemplo.com/guia/instalacion-linux/</link>
      <guid isPermaLink="true">https://ejemplo.com/guia/instalacion-linux/</guid>
      <pubDate>Wed, 28 Oct 2026 10:00:00 +0000</pubDate>
      <description>Requisitos, pasos y verificación.</description>
    </item>
  </channel>
</rss>
```

Atom:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Guía de ejemplo</title>
  <id>https://ejemplo.com/guia/</id>
  <updated>2026-10-28T10:00:00Z</updated>
  <link href="https://ejemplo.com/guia/feed.xml" rel="self"/>
  <entry>
    <title>Instalación en Linux</title>
    <id>https://ejemplo.com/guia/instalacion-linux/</id>
    <link href="https://ejemplo.com/guia/instalacion-linux/"/>
    <updated>2026-10-28T10:00:00Z</updated>
    <summary>Requisitos, pasos y verificación.</summary>
  </entry>
</feed>
```

Detalles que suelen fallar:

- **Fechas:** RSS usa RFC 822; Atom usa RFC 3339.
- **IDs estables:** el `guid` o el `id` no debe cambiar si cambia la URL.
- **Contenido completo o resumen:** decide y documenta; un resumen sin enlace es inútil.
- **Descubrimiento:** añade `<link rel="alternate" type="application/rss+xml" href="/feed.xml">` en el `<head>`.
- **Validación:** comprueba el feed con el validador del W3C.

## 63.8 Comprobación y medición

Antes de anunciar una publicación:

1. **Códigos de estado.** Las URLs principales responden 200; las retiradas, 301 o 410.
2. **Canonical y sitemap.** Coinciden y no apuntan a páginas `noindex`.
3. **Metadatos.** Título, descripción e imagen se ven bien en una vista previa social.
4. **Datos estructurados.** Sin errores en el validador.
5. **Feed.** Válido y con fechas correctas.
6. **Rendimiento.** Imágenes optimizadas y sin JavaScript innecesario.
7. **Accesibilidad.** Enlaces, encabezados y contraste (capítulo [47](47-accesibilidad.md)).
8. **Enlaces internos.** Sin 404 ni anclas rotas.

Para medir, usa datos de búsqueda (impresiones, consultas, páginas), registros de 404 y analítica del sitio. Ten en cuenta que:

- Una posición media mejor no implica más tráfico si bajan las impresiones.
- Las métricas de interacción no son comparables entre páginas de distinta longitud.
- Los datos de Search Console tienen retraso y umbrales de privacidad.
- La analítica puede fallar si hay bloqueadores o consentimiento rechazado.

La medición sirve para priorizar, no para declarar victoria. Un cambio de título puede mejorar una página y empeorar otra; conviene registrar qué se cambió y cuándo.

## 63.9 Lista de comprobación

- [ ] Cada página tiene un título único y una descripción específica.
- [ ] Hay un solo `<h1>` y la jerarquía no salta niveles.
- [ ] Las URLs son estables, en minúsculas y sin parámetros innecesarios.
- [ ] Las páginas duplicadas declaran una canónica absoluta.
- [ ] Las URLs retiradas redirigen o muestran una página de aviso.
- [ ] `hreflang` es recíproco si hay varias lenguas.
- [ ] Las etiquetas Open Graph usan URLs absolutas y una imagen adecuada.
- [ ] Los datos estructurados coinciden con el contenido visible y validan.
- [ ] El sitemap incluye solo páginas indexables y declara `lastmod` real.
- [ ] `robots.txt` no bloquea recursos necesarios ni contradice el sitemap.
- [ ] El feed es válido, tiene fechas correctas y se descubre desde el `<head>`.
- [ ] Los códigos de estado, enlaces y anclas se comprobaron tras publicar.

---

[← 62. Gobierno, frescura y métricas de la documentación](62-gobierno-frescura-y-metricas.md) · [Índice general](README.md)
