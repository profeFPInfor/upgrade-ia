# 45. Internacionalización y escritura multilingüe

> [← Índice general](README.md) · Capítulo 45 de 63

Markdown es texto Unicode, lo que permite escribir en cualquier idioma. Sin embargo, la **internacionalización** (i18n) afecta a los identificadores, las URL, la tipografía, la dirección de lectura y la forma de organizar las traducciones. Este capítulo reúne las prácticas que evitan documentos rotos al cambiar de idioma.

## 45.1 Unicode, UTF-8 y normalización

- Guarda siempre en **UTF-8 sin BOM**.
- Evita depender de la configuración regional del sistema.
- Comprueba que el editor no convierte comillas, guiones o espacios en caracteres invisibles.

Unicode permite representar una letra acentuada de dos formas:

| Forma | Ejemplo | Descripción |
|---|---|---|
| **NFC** | `é` (U+00E9) | Carácter precompuesto |
| **NFD** | `e` + `◌́` | Letra base + acento combinado |

Dos nombres de archivo o dos anclas que parecen iguales pueden ser distintos si usan formas diferentes. Normaliza a **NFC** antes de comparar o publicar.

- Normalización Unicode: <https://unicode.org/reports/tr15/>

## 45.2 Identificadores y anclas

Los generadores de IDs no se ponen de acuerdo:

- Unos conservan los acentos (`#introducción`).
- Otros los eliminan o los transliteran (`#introduccion`).
- Otros codifican la URL (`%C3%B3`).

Consecuencias:

- Un enlace interno puede funcionar en GitHub y fallar en otro renderizador.
- Cambiar la forma de un acento puede romper un ancla.
- Los IDs duplicados reciben sufijos distintos según la herramienta.

Recomendaciones:

1. Usa **IDs explícitos** cuando el destino lo permita: `## Introducción {#introduccion}`.
2. Si publicas en varios sistemas, usa IDs ASCII estables.
3. Verifica las anclas después de cada conversión.
4. No renombres encabezados sin actualizar los enlaces.

## 45.3 Tipografía en español

| Elemento | Uso | Ejemplo |
|---|---|---|
| Comillas angulares | Citas en español | «texto citado» |
| Comillas inglesas | Citas dentro de una cita | “texto” |
| Raya | Diálogo o inciso | —dijo— |
| Guion | Palabras compuestas | teórico-práctico |
| Puntos suspensivos | Una sola vez | … |
| Signos de apertura | Interrogación y exclamación | ¿Qué?, ¡Hola! |
| Espacio duro | Unidades y cifras | 10 km, 5 % |

- No uses el guion corto como raya.
- Escribe los porcentajes con espacio duro en español: `5 %`.
- Usa coma decimal (`2,5`) y punto o espacio fino para miles (`1 000`), según la norma de estilo.
- Evita mayúsculas sostenidas en títulos largos.

## 45.4 Dirección de lectura (RTL)

Para árabe, hebreo, persa o urdu:

```html
<article lang="ar" dir="rtl">
  ...
</article>
```

- `dir="rtl"` cambia la dirección base; no cambies el orden lógico del texto.
- Los bloques de código y las fórmulas suelen mantenerse en LTR: `dir="ltr"`.
- Los signos de puntuación pueden quedar en el lado incorrecto; usa caracteres de aislamiento bidi si hace falta.
- Las tablas deben alinear el texto según la dirección, no según la columna.
- Prueba con textos mixtos (árabe + números + inglés).

En CSS, usa propiedades lógicas (`margin-inline-start`, `padding-inline-end`, `text-align: start`) en lugar de `left`/`right`.

## 45.5 Chino, japonés y coreano (CJK)

- No hay espacios entre palabras; el navegador necesita reglas de salto de línea (`line-break`, `word-break`).
- Usa fuentes con cobertura CJK; si no, aparecen cajas.
- La puntuación de ancho completo (`。`, `、`, `：`) no debe separarse de la frase.
- Evita justificar sin control: puede crear espacios enormes.
- Declara el idioma (`lang="ja"`, `lang="zh"`, `lang="ko"`) para que el navegador elija fuentes y reglas.

## 45.6 Comillas tipográficas y sustituciones

Muchos procesadores convierten automáticamente:

- `"` → `“ ”`
- `'` → `‘ ’`
- `--` → `–` o `—`
- `...` → `…`

Estas sustituciones pueden ser deseables en prosa y **peligrosas en código**. En Pandoc:

```bash
# Desactivar las sustituciones inteligentes
pandoc documento.md -f markdown-smart -o documento.html
```

En markdown-it, `typographer: true` activa sustituciones; en código, desactívalas o usa bloques con lenguaje.

## 45.7 Fechas, números y ordenación

- **Fechas**: ISO 8601 (`2026-10-28`) para metadatos y ordenación; formato local para la lectura.
- **Números**: coma decimal en español, punto en inglés; no mezcles en el mismo documento.
- **Ordenación**: usa reglas locales (`Intl.Collator` en JavaScript) en lugar de comparar cadenas byte a byte.
- **Monedas**: indica el código (`EUR`, `USD`) y el símbolo según el contexto.
- **Unidades**: espacio duro entre número y unidad; no traduzcas los símbolos del SI.

## 45.8 Organizar traducciones

| Estrategia | Ejemplo | Ventaja | Riesgo |
|---|---|---|---|
| **Sufijo de idioma** | `README.es.md`, `README.en.md` | Sencillo y visible | Duplicación |
| **Carpeta por idioma** | `es/`, `en/`, `pt/` | Aísla el contenido | Rutas duplicadas |
| **Archivos PO/gettext** | `es.po`, `en.po` | Herramientas maduras | Requiere extraer cadenas |
| **Plataforma de traducción** | Weblate, Crowdin | Flujo colaborativo | Dependencia externa |

Buenas prácticas:

1. Define el idioma **fuente** y congela el contenido antes de traducir.
2. Mantén un **glosario** de términos técnicos.
3. No traduzcas nombres de archivos, comandos ni claves de código.
4. Revisa la longitud: el alemán y el finés suelen ser más largos que el español.
5. Añade un selector de idioma accesible.
6. Declara `hreflang` en HTML y enlaces recíprocos.

- Weblate: <https://weblate.org/>
- Crowdin: <https://crowdin.com/>
- gettext: <https://www.gnu.org/software/gettext/>

## 45.9 URL y nombres de archivo

- Usa ASCII en rutas publicadas (`guia-markdown.html`), aunque el título tenga acentos.
- Si usas acentos, normaliza a NFC y comprueba el servidor.
- Evita espacios; si los usas, codifícalos (`%20`).
- Mantén las URL antiguas con redirecciones al renombrar.
- No cambies mayúsculas y minúsculas en sistemas sensibles a ellas.

## 45.10 Búsqueda y filtros

Para que la búsqueda funcione con acentos:

- Normaliza el texto (NFC) y, si el motor lo permite, elimina diacríticos al indexar.
- Configura analizadores lingüísticos (`spanish`, `portuguese`…).
- Prueba búsquedas con y sin tildes, y con mayúsculas.
- En SQLite FTS5, el tokenizador `unicode61` admite `remove_diacritics`.
- En Elasticsearch/OpenSearch, usa analizadores por idioma.

## 45.11 Accesibilidad multilingüe

- Declara `lang` en el documento y en los fragmentos en otro idioma.
- Usa `dir` para la dirección de lectura.
- Evita texto en imágenes: no se puede traducir ni leer.
- Los lectores de pantalla dependen del idioma para pronunciar correctamente.
- Prueba con fuentes de respaldo y tamaños grandes.
- Añade subtítulos traducidos en los vídeos.

## 45.12 Pruebas

1. **Pseudo-localización**: sustituye vocales por caracteres acentuados y alarga los textos para detectar recortes.
2. **Cadenas largas**: prueba títulos y botones con el doble de longitud.
3. **RTL**: revisa iconos, tablas y fórmulas.
4. **Fuentes**: comprueba que no faltan glifos.
5. **Enlaces**: valida anclas con y sin acentos.
6. **Lectores de pantalla**: escucha la pronunciación en cada idioma.

## 45.13 Lista de comprobación

- [ ] Todo el contenido está en UTF-8 sin BOM.
- [ ] Los nombres y anclas están normalizados.
- [ ] El idioma está declarado en el documento.
- [ ] La tipografía y las comillas son coherentes.
- [ ] Las fechas y números siguen una convención.
- [ ] Las traducciones tienen glosario y revisión.
- [ ] La dirección RTL se ha probado con texto mixto.
- [ ] La búsqueda funciona con y sin acentos.

---

[← 44. Bases de conocimiento personal](44-bases-de-conocimiento-personal.md) · [Índice general](README.md) · [46. Linting y validación →](46-linting-y-validacion.md)
