# 47. Accesibilidad

> [← Índice general](README.md) · Capítulo 47 de 63

Markdown se convierte en HTML; por tanto, la accesibilidad depende tanto de cómo se escribe el documento como del **renderizador**, la **plantilla** y el **CSS** del sitio. Un Markdown bien estructurado facilita la navegación con lector de pantalla, teclado y otros productos de apoyo.

Las referencia principal es **WCAG 2.2**, del W3C. Sus cuatro principios son **Perceptible**, **Operable**, **Comprensible** y **Robusto** (POUR).

## 47.1 Principios WCAG aplicados a Markdown

| Principio | Qué significa | Ejemplo en Markdown |
|---|---|---|
| **Perceptible** | La información debe poder percibirse | Texto alternativo en imágenes, tablas con encabezados |
| **Operable** | La interfaz debe poder usarse con teclado | Enlaces accesibles, navegación lógica, sin trampas de foco |
| **Comprensible** | El contenido y el funcionamiento deben entenderse | Lenguaje claro, estructura predecible, enlaces descriptivos |
| **Robusto** | Debe funcionar con tecnologías de apoyo | HTML semántico, jerarquía correcta, ARIA solo cuando haga falta |

- WCAG 2.2: <https://www.w3.org/TR/WCAG22/>
- Resumen rápido: <https://www.w3.org/WAI/WCAG22/quickref/>

## 47.2 Estructura correcta de títulos

Los encabezados son la columna vertebral de la navegación con lector de pantalla. Reglas prácticas:

1. **Un solo `#` (H1)** por documento, normalmente el título.
2. **No saltes niveles**: de `##` a `###`, no de `##` a `####`.
3. **Usa encabezados para estructurar**, no para agrandar texto.
4. **Sé descriptivo**: "Instalación en Linux" es mejor que "Paso 2".
5. **No dupliques el mismo encabezado** sin necesidad; si lo haces, los anclas pueden colisionar.
6. **Mantén una jerarquía coherente** en todos los documentos del sitio.

```markdown
# Guía de instalación

## Requisitos

## Instalación en Linux

### Debian y Ubuntu

### Fedora

## Verificación
```

Mal:

```markdown
# Guía

### Instalación

##### Comprobación
```

## 47.3 Texto alternativo

El texto alternativo (`alt`) describe la **función o el contenido** de una imagen, no su apariencia. Los lectores de pantalla lo anuncian; si falta, pueden leer el nombre del archivo.

| Tipo de imagen | Texto alternativo recomendado |
|---|---|
| Informativa | Describe lo que aporta: "Diagrama de flujo: carrito → pago → confirmación" |
| Decorativa | `alt=""` (vacío) o, mejor, eliminarla del contenido y usar CSS |
| Funcional (enlace/botón) | Describe la acción: "Descargar informe en PDF" |
| Logotipo | "Logotipo de Acme" |
| Captura de pantalla | Describe la parte relevante: "Botón Guardar en la esquina superior derecha" |
| Gráfico complejo | Resume la tendencia y enlaza a una tabla o descripción larga |
| Fórmula o diagrama | Proporciona una descripción textual y, si es posible, el código fuente |

```markdown
![Diagrama de arquitectura: el cliente envía una petición a la API, que consulta la base de datos y devuelve JSON](docs/arquitectura.png)
```

Evita:

```markdown
![imagen](foto1.png)
![captura](captura.png)
```

Recomendaciones:

- No empieces con "Imagen de…": el lector ya anuncia que es una imagen.
- No repitas el pie de foto en el `alt`.
- Si la imagen contiene texto esencial, reproduce ese texto en el cuerpo o en una descripción.
- Para diagramas Mermaid, ofrece una alternativa textual (lista de pasos, tabla o párrafo).
- Para imágenes decorativas, `![](separador.png)` es válido, pero un separador visual suele ser mejor con CSS.

- Decisión de texto alternativo (W3C): <https://www.w3.org/WAI/tutorials/images/decision-tree/>
- Texto alternativo (WebAIM): <https://webaim.org/techniques/alttext/>

## 47.4 Enlaces descriptivos

El texto de un enlace debe tener sentido **fuera de contexto**, porque los lectores de pantalla permiten navegar de enlace en enlace.

| Evita | Usa |
|---|---|
| "Haz clic aquí" | "Consulta la guía de instalación" |
| "Más información" | "Más información sobre la API de pagos" |
| "Este enlace" | "Descarga el archivo de configuración de ejemplo" |
| URL desnuda | Un texto descriptivo que apunte a la URL |
| "Leer más" repetido | "Leer la política de privacidad" |

```markdown
Consulta la [guía de instalación en Linux](docs/instalacion.md) antes de continuar.
```

Si el enlace abre en una pestaña nueva, indícalo en el texto o con un icono acompañado de texto. No dependas solo del color para distinguir enlaces.

## 47.5 Tablas accesibles

- Incluye siempre una **fila de encabezado**.
- Usa tablas para **datos**, no para maquetar.
- Mantén las tablas simples; si tienen celdas combinadas o muchos niveles, divide o complementa con texto.
- Añade una introducción o un título antes de la tabla que explique su contenido.
- No uses imágenes de tablas.
- En HTML, usa `<caption>`, `<th scope="col">` y `<th scope="row">` cuando sea necesario.

```markdown
La tabla siguiente resume los planes disponibles.

| Plan | Precio | Límite |
|---|---|---|
| Libre | 0 € | 1 proyecto |
| Pro | 9 € | 20 proyectos |
| Empresa | 49 € | Ilimitado |
```

## 47.6 Imágenes y multimedia

- **Imágenes:** `alt` obligatorio; evita imágenes de texto; optimiza el tamaño; usa formatos adecuados (SVG para diagramas, WebP/PNG para capturas).
- **Vídeo:** ofrece subtítulos, transcripción y, si es necesario, audiodescripción. En Markdown puro no hay sintaxis de vídeo; usa HTML o un componente del sitio:

```html
<video controls preload="metadata" poster="video/poster.jpg">
  <source src="video/demo.mp4" type="video/mp4">
  <track kind="captions" src="video/demo.vtt" srclang="es" label="Español">
  Tu navegador no admite vídeo HTML5.
</video>
```

- **Audio:** incluye transcripción y controla el volumen; no uses reproducción automática.
- **Animaciones:** evita parpadeos y movimiento excesivo; respeta `prefers-reduced-motion` en el CSS del sitio.

## 47.7 Contraste y color

Markdown no controla colores, pero el HTML embebido, los componentes y el CSS sí.

| Elemento | Contraste mínimo WCAG 2.2 |
|---|---|
| Texto normal | 4.5:1 |
| Texto grande (≥ 24 px o ≥ 18.66 px en negrita) | 3:1 |
| Componentes de interfaz y gráficos esenciales | 3:1 |
| Indicadores de foco | Visibles y con contraste suficiente |

- No transmitas información **solo por color**: añade texto, iconos o patrones.
- Revisa el modo oscuro y el modo claro.
- Asegura que los enlaces se distingan del texto (subrayado o contraste suficiente).
- Comprueba el contraste del resaltado de sintaxis.

- Criterio 1.4.3: <https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html>

## 47.8 Lenguaje claro

- Frases cortas y párrafos breves.
- Voz activa y verbos concretos.
- Define siglas y términos técnicos la primera vez.
- Usa una terminología consistente.
- Evita ambigüedades, dobles negaciones y lenguaje innecesariamente formal.
- Incluye ejemplos y resúmenes.
- Estructura con listas y tablas cuando ayuden.
- No supongas conocimiento previo que no se ha explicado.

## 47.9 Navegación y lectores de pantalla

- El orden de lectura del HTML debe coincidir con el orden visual.
- Proporciona un **índice** en documentos largos.
- Usa **anclas** y enlaces internos con texto descriptivo.
- En la plantilla HTML del sitio, añade un enlace "Saltar al contenido principal".
- Define el idioma del documento (`<html lang="es">`) y, si hay fragmentos en otro idioma, `lang` en el elemento correspondiente.
- Usa landmarks (`header`, `nav`, `main`, `footer`) en la plantilla.
- Evita tablas de maquetación y `div` con `onClick` sin alternativa de teclado.
- No uses emojis como único indicador de estado; acompáñalos de texto.
- Para iconos decorativos, `aria-hidden="true"`; para iconos con significado, un nombre accesible.

## 47.10 Código y diagramas

- Especifica el lenguaje en los bloques de código; mejora el resaltado y la semántica.
- Evita líneas extremadamente largas; el desplazamiento horizontal debe ser posible.
- No uses el color como única forma de explicar el código.
- Para diagramas Mermaid, incluye una descripción textual y, si es posible, una tabla equivalente.
- Si el diagrama es una imagen, usa `alt` descriptivo y un pie de figura.
- Los botones de "copiar código" deben ser accesibles por teclado y anunciar su estado.

## 47.11 Formularios y HTML embebido

Aunque Markdown no tiene formularios, la documentación puede incluir HTML o componentes. En ese caso:

- Asocia cada campo con un `<label>`.
- Usa `<fieldset>` y `<legend>` para grupos.
- Marca los campos obligatorios con texto, no solo con color.
- Proporciona mensajes de error claros y asociados al campo.
- No uses `placeholder` como sustituto de la etiqueta.
- Asegura que los botones tengan texto o nombre accesible.

## 47.12 Cómo probar la accesibilidad

| Prueba | Herramienta |
|---|---|
| Navegación solo con teclado | Tab, Shift+Tab, Enter, Espacio |
| Lector de pantalla | NVDA (Windows), JAWS (Windows), VoiceOver (macOS/iOS), TalkBack (Android) |
| Zoom y reflujo | 200 % de zoom, ancho de 320 px |
| Contraste | WebAIM Contrast Checker, axe DevTools |
| Auditoría automática | axe, Lighthouse, WAVE |
| Revisión manual | Estructura, alt, enlaces, tablas, formularios |

Ninguna herramienta automática detecta todos los problemas. La revisión manual y las pruebas con personas usuarias son insustituibles.

- Tutoriales WAI: <https://www.w3.org/WAI/tutorials/>
- Evaluación: <https://www.w3.org/WAI/test-evaluate/>
- Consejos rápidos: <https://www.w3.org/WAI/tips/>

## 47.13 Checklist de accesibilidad

- [ ] Un solo H1 y jerarquía sin saltos.
- [ ] Imágenes con `alt` adecuado; decorativas con `alt=""`.
- [ ] Enlaces descriptivos y con sentido fuera de contexto.
- [ ] Tablas con encabezados y sin uso para maquetación.
- [ ] Contraste suficiente si hay HTML/CSS.
- [ ] Lenguaje claro y siglas definidas.
- [ ] Índice o navegación en documentos largos.
- [ ] Diagramas con descripción textual.
- [ ] Vídeos con subtítulos y transcripción.
- [ ] Formularios con etiquetas y errores claros.
- [ ] Prueba con teclado y lector de pantalla.

---

[← 46. Linting y validación](46-linting-y-validacion.md) · [Índice general](README.md) · [48. Seguridad →](48-seguridad.md)
