# 17. Enlaces internos

> [← Índice general](README.md) · Capítulo 17 de 63

Un enlace interno conecta una página con otra sección del mismo corpus. Parece una operación trivial, pero depende de tres cosas que Markdown no controla: el **algoritmo de anclas** del renderizador, la **ruta pública** que genera el sitio y la **estabilidad** de los títulos. Un enlace que funciona en el editor puede fallar en producción.

## 17.1 Cómo se generan las anclas

Markdown no define identificadores para los títulos. El renderizador crea un *slug* a partir del texto y lo usa como `id` del encabezado. El algoritmo varía:

| Paso | GitHub (GFM) | Algunos generadores estáticos |
|---|---|---|
| Minúsculas | Sí | Sí |
| Espacios | Guion `-` | Guion `-` |
| Puntuación | Se elimina | Se elimina o se sustituye |
| Acentos | Se conservan | Pueden transliterarse (`instalación` → `instalacion`) |
| Repeticiones | Sufijo `-1`, `-2` | Sufijo `-1` o similar |
| Enlaces explícitos | No admite `{#id}` | Kramdown, Docusaurus y otros sí |

En GitHub:

| Título | Enlace |
|---|---|
| `## Instalación` | `[ir](#instalación)` |
| `## 4.1 Títulos` | `[ir](04-sintaxis-basica.md#41-títulos)` |
| `## ¿Qué es Markdown?` | `[ir](#qué-es-markdown)` |
| `## Uso (avanzado)` | `[ir](#uso-avanzado)` |

No escribas el ancla «a mano» mirando el título: cópiala del HTML generado o del índice del sitio. Es la única forma de saber qué `id` produjo realmente el motor.

## 17.2 Enlaces a encabezados del mismo documento

```markdown
## Índice

- [Instalación](#instalación)
- [Uso](#uso)
- [Solución de problemas](#solución-de-problemas)
```

Buenas prácticas:

- **Texto descriptivo.** «Configuración de la red» es mejor que «ver aquí».
- **No dupliques el título** en el texto del enlace si el contexto ya lo deja claro, pero evita los enlaces vacíos.
- **Actualiza el índice** cuando cambies un título; el ancla anterior deja de existir.
- **Evita títulos que solo se diferencian en puntuación**, porque pueden generar el mismo slug y recibir sufijos numéricos.

## 17.3 Anclas explícitas

Cuando el identificador debe ser estable aunque el título cambie, declara el ancla:

```markdown
<a id="configuracion-red"></a>
## Configuración de la red

[Volver a la configuración](#configuracion-red)
```

Ventajas: el enlace no depende del texto visible. Inconvenientes: el HTML embebido puede ser filtrado y la sintaxis no es universal.

En kramdown (Jekyll) y en varios generadores modernos se puede escribir:

```markdown
## Configuración de la red {#configuracion-red}
```

Esta forma **no funciona en GitHub**: el texto `{#configuracion-red}` se muestra tal cual. Si el documento se publica en varios destinos, usa el ancla HTML o mantén el título estable.

## 17.4 Enlaces entre documentos

```markdown
[Guía de instalación](./instalacion.md)
[Sección de configuración](./configuracion.md#variables-de-entorno)
[Subir de nivel](../README.md)
```

Reglas:

- **Rutas relativas al archivo** que contiene el enlace. En `docs/guias/uso.md`, `../api.md` sube a `docs/`.
- **Sin rutas absolutas del sistema** (`C:\...`, `/home/...`): no funcionan en otro equipo ni en el sitio.
- **Sin espacios ni mayúsculas** en los nombres de archivo; si existen, se codifican y complican el mantenimiento.
- **Con o sin `./`**: ambos funcionan, pero sé consistente.
- **Enlaces a carpetas**: apunta a un archivo concreto (`README.md` o `index.md`), no a un directorio, salvo que el servidor resuelva el índice automáticamente.

En el sitio generado, los enlaces `.md` deben convertirse a `.html`. Si el generador no lo hace, el enlace descarga el archivo fuente o devuelve 404. El capítulo [28](28-generadores-de-sitios-estaticos.md) explica cómo lo resuelve cada herramienta.

## 17.5 Rutas en el sitio publicado

| Situación | Enlace recomendado |
|---|---|
| Misma carpeta | `otra-pagina.html` |
| Subcarpeta | `guias/instalacion.html` |
| Carpeta superior | `../index.html` |
| Raíz del sitio con `baseurl` | Ruta relativa o helper del generador |
| GitHub Pages de proyecto | Evitar `/guia/...` absoluto si el sitio vive en `/repo/` |

Un error frecuente: probar el sitio con `jekyll serve` en `http://localhost:4000/` y publicarlo en `https://usuario.github.io/repo/`. Los enlaces absolutos que funcionaban en local apuntan a la raíz del dominio y fallan en producción.

Si el generador ofrece un helper (`relative_url` en Jekyll, `withBaseUrl` en Docusaurus), úsalo. Si no, mantén rutas relativas y comprueba el sitio con la misma ruta base que tendrá en producción.

## 17.6 Índices y navegación

Un índice puede ser manual o generado:

- **Manual:** controlas el orden y el texto, pero se desactualiza.
- **Generado:** se actualiza con los encabezados, pero incluye títulos que no quieres (por ejemplo, los de un bloque de código si el script no los excluye).
- **Mixto:** una lista curada de páginas principales y un índice automático de secciones.

En este corpus, el `README.md` mantiene un índice con enlaces a cada capítulo y sus secciones, y el sitio genera la barra lateral desde `_data/toc.yml`. Ambos deben usar las mismas anclas que el render.

Un índice que promete una sección inexistente es peor que no tener índice: el lector pierde la confianza en la navegación.

## 17.7 Validar enlaces y anclas

| Comprobación | Herramienta habitual |
|---|---|
| Enlaces rotos entre archivos | lychee, markdown-link-check |
| Anclas inexistentes | Verificador propio contra el HTML generado |
| Enlaces externos | lychee con comprobación de red |
| Redirecciones | `curl -I` y revisión del código de estado |
| Enlaces en el sitio | Rastreo local con el servidor de previsualización |

El capítulo [46](46-linting-y-validacion.md) muestra cómo integrar estas comprobaciones en CI. Una validación útil distingue entre enlace roto (404), ancla inexistente (200 con fragmento inválido) y redirección (301/302). Las dos primeras rompen la navegación; la tercera puede ser aceptable si el destino es el correcto.

## 17.8 Enlaces rotos y redirecciones

Cuando un documento se mueve o se retira:

1. **Actualiza los enlaces internos** en todo el repositorio.
2. **Añade una redirección** si la URL pública cambia.
3. **Conserva el ancla** o redirige a la sección equivalente.
4. **Comprueba enlaces externos** que apunten a la página antigua.
5. **Documenta el cambio** en el historial o en el changelog.

En un sitio estático sin reglas de servidor, una página de aviso con enlace al sustituto es mejor que un 404, aunque no equivale a una redirección permanente. El capítulo [63](63-publicacion-y-distribucion.md) trata las limitaciones de cada host.

## 17.9 Lista de comprobación

- [ ] Los enlaces internos usan rutas relativas y nombres sin espacios.
- [ ] Las anclas se copiaron del HTML generado, no se supusieron.
- [ ] Los títulos estables no dependen de puntuación ambigua.
- [ ] Las anclas críticas son explícitas si el renderizador lo permite.
- [ ] Los enlaces `.md` se convierten a `.html` en el sitio.
- [ ] La ruta base de producción coincide con la de las pruebas.
- [ ] El índice y la barra lateral usan las mismas anclas.
- [ ] La validación distingue 404, ancla inválida y redirección.
- [ ] Los documentos movidos tienen redirección o aviso.
- [ ] Se comprobó el enlace en el render final, no solo en el editor.

---

[← 16. UML y Markdown](16-uml-y-markdown.md) · [Índice general](README.md) · [18. Imágenes y recursos multimedia →](18-imagenes-y-recursos-multimedia.md)
