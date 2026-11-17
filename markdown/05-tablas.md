# 5. Tablas

> [← Índice general](README.md) · Capítulo 5 de 63

Las tablas **no forman parte** de Markdown original ni de CommonMark base; son una **extensión GFM** (también presente en Markdown Extra, MultiMarkdown, Pandoc y otras implementaciones). Esa origen explica sus límites: sirven para datos tabulares simples, no para maquetar una página ni para reproducir una hoja de cálculo.

Este capítulo cubre la sintaxis, las restricciones reales y las decisiones que evitan tablas ilegibles al exportar o al leer con un lector de pantalla.

## 5.1 Qué es una tabla GFM

Una tabla consta de tres partes:

1. Una **fila de cabecera** con los nombres de columna.
2. Una **fila de separación** obligatoria, formada por guiones y, opcionalmente, dos puntos para alinear.
3. Una o más **filas de datos**.

```markdown
| Nombre | Edad | Ciudad  |
|--------|:----:|--------:|
| Ana    | 30   | Madrid  |
| Luis   | 25   | Sevilla |
```

| Nombre | Edad | Ciudad |
|--------|:----:|-------:|
| Ana    | 30   | Madrid |
| Luis   | 25   | Sevilla |

Las barras verticales de los extremos son opcionales, pero se recomiendan: hacen visible el límite de la tabla y evitan ambigüedades al editar. La fila de separación debe tener el mismo número de celdas que la cabecera; si no coincide, la tabla no se reconoce.

## 5.2 Alineación

| Sintaxis | Alineación | Uso habitual |
|---|---|---|
| `:---` | Izquierda | Texto, nombres, rutas |
| `:---:` | Centro | Estados, iconos, columnas cortas |
| `---:` | Derecha | Números, importes, versiones |
| `---` | Por defecto | Cuando la alineación no aporta |

La alineación se aplica al contenido de la columna, no a la cabecera. En una tabla de precios, alinear a la derecha facilita comparar cifras; en una de texto, alinear a la izquierda es más legible.

No abuses del centrado: una columna centrada de párrafos largos es difícil de seguir. El centro funciona mejor con valores cortos y homogéneos.

## 5.3 Contenido dentro de las celdas

Dentro de una celda se permite **contenido inline**: énfasis, código, enlaces, imágenes y texto normal. No se permiten bloques: listas, párrafos múltiples, citas o bloques de código.

```markdown
| Comando | Descripción |
|---|---|
| `a \| b` | Escapa la barra con `\|` |
| **negrita** | Se permite formato inline |
| [enlace](https://example.com) | Enlaces e imágenes inline |
```

Reglas prácticas:

- **Escapa la barra** (`\|`) si forma parte del contenido; de lo contrario, se interpreta como separador de columna.
- **No uses saltos de línea reales** dentro de una fila: cada fila debe ocupar una sola línea del archivo.
- **`<br>`** puede introducir un salto visual en muchos renderizadores, pero no crea un párrafo ni una lista. Su compatibilidad varía; úsalo con moderación.
- **El código inline** ayuda a distinguir nombres de campos, comandos y valores.
- **Las imágenes** dentro de celdas suelen quedar diminutas; si necesitas una figura, sácala de la tabla.

Si el contenido necesita varios párrafos, listas o celdas combinadas, la tabla de Markdown no es la herramienta adecuada (véase 5.7).

## 5.4 Tablas anchas y tablas largas

Una tabla con muchas columnas se vuelve ilegible en móvil. Antes de añadir una columna, pregúntate si ese dato se puede mover al texto, a una nota o a una segunda tabla.

| Problema | Alternativa |
|---|---|
| Muchas columnas | Dividir en dos tablas por tema |
| Celdas con párrafos | Lista de definiciones o subsecciones |
| Texto que se repite | Eliminar la columna y explicarlo una vez |
| Demasiadas filas | Agrupar por categoría o paginar en el sitio |
| Datos jerárquicos | Lista anidada o tabla con columna de nivel |

En el sitio generado, envuelve las tablas anchas en un contenedor con desplazamiento horizontal y `tabindex="0"` para que se puedan recorrer con el teclado. En PDF y DOCX, comprueba que la tabla no se corta en un salto de página y que la cabecera se repite.

## 5.5 Accesibilidad de tablas

Una tabla accesible no es solo una tabla que se ve bien. Los lectores de pantalla la recorren anunciando la posición de cada celda y, si está bien construida, la cabecera correspondiente.

Recomendaciones:

- **Usa tablas solo para datos.** Nunca para maquetar columnas o colocar una imagen al lado de un texto.
- **Una cabecera clara en la primera fila.** GFM genera `<th>` para esa fila; sin ella, el lector no sabe qué representa cada columna.
- **Evita celdas vacías sin explicación.** Un guion o «no aplica» es más informativo que un hueco.
- **No dependas del color** para transmitir estado; añade texto o un símbolo.
- **Evita tablas anidadas.** Confunden la navegación y el render.
- **Añade una leyenda** antes de la tabla si el título no basta: «Tabla 3. Códigos de error de la API».
- **En HTML**, usa `<caption>`, `<th scope="col">` y `<th scope="row">` cuando la tabla lo necesite. Markdown no permite expresar `scope`; si la accesibilidad es un requisito estricto, genera la tabla en HTML o posprocesa el HTML.
- **Comprueba el zoom al 200 %** y el modo de alto contraste.

El capítulo [47](47-accesibilidad.md) desarrolla los criterios WCAG; el [46](46-linting-y-validacion.md) explica cómo automatizar parte de la revisión.

## 5.6 Tablas en la exportación

| Destino | Qué comprobar |
|---|---|
| HTML | Desplazamiento horizontal, cabeceras `<th>`, contraste |
| PDF (LaTeX) | Ancho de columna, cortes de página, `longtable` si es larga |
| PDF (HTML/CSS) | `page-break-inside: avoid` en tablas cortas, repetición de cabecera |
| DOCX | Estilo de tabla, cabecera repetida, tamaño de fuente |
| EPUB | Ancho variable del lector, tablas que no se cortan |
| Presentaciones | Una tabla por diapositiva, sin más de cinco columnas |

Pandoc permite definir el ancho relativo de las columnas en las tablas de tipo *pipe* y ofrece tablas de rejilla (*grid tables*) con bloques dentro de las celdas. Las tablas de rejilla no son portables a GFM: si el documento debe publicarse en GitHub, mantén la sintaxis pipe.

## 5.7 Cuándo usar HTML

La tabla de Markdown no admite `colspan`, `rowspan`, cabeceras múltiples ni bloques dentro de celdas. Si necesitas alguna de esas funciones, tienes tres opciones:

1. **Simplificar la tabla** para que quepa en la sintaxis estándar. Suele ser la mejor decisión editorial.
2. **Usar HTML** `<table>` con `<thead>`, `<tbody>`, `<th scope>` y `<caption>`. Es portable en HTML, pero no en todos los visores Markdown y complica el mantenimiento.
3. **Generar la tabla** desde datos (CSV, JSON, consulta) con un script. Evita el error manual y permite actualizarla.

```html
<table>
  <caption>Cobertura por plataforma</caption>
  <thead>
    <tr><th scope="col">Plataforma</th><th scope="col">Tablas</th></tr>
  </thead>
  <tbody>
    <tr><th scope="row">GitHub</th><td>Sí</td></tr>
    <tr><th scope="row">CommonMark</th><td>No</td></tr>
  </tbody>
</table>
```

HTML dentro de Markdown está limitado por el sanitizador de cada plataforma (capítulo [13](13-html-dentro-de-markdown.md)). GitHub elimina atributos y etiquetas peligrosas; no cuentes con JavaScript ni con estilos inline.

## 5.8 Errores frecuentes

| Error | Resultado | Solución |
|---|---|---|
| Falta la fila de separación | Se muestra como texto | Añadir `|---|---|` |
| Guiones insuficientes | Algunos parsers no la reconocen | Usar al menos tres por celda |
| Barras sin escapar | Columnas desplazadas | Escribir `\|` |
| Filas con distinto número de celdas | Celdas vacías o datos perdidos | Revisar cada fila |
| Bloques dentro de celdas | Render inconsistente | Sacar el bloque de la tabla |
| Tabla para maquetar | Mala experiencia con lector de pantalla | Usar CSS o secciones |
| Cabecera vacía | Sin contexto para los datos | Nombrar cada columna |

## 5.9 Lista de comprobación

- [ ] La tabla tiene cabecera y fila de separación con el mismo número de celdas.
- [ ] La alineación se eligió por tipo de dato, no por estética.
- [ ] Las barras del contenido están escapadas.
- [ ] Cada fila ocupa una sola línea y tiene el número correcto de celdas.
- [ ] La tabla se lee bien en móvil y con zoom al 200 %.
- [ ] No se usa una tabla para maquetar.
- [ ] Las cabeceras describen el contenido y no dependen del color.
- [ ] Las tablas largas tienen cabecera repetida al exportar.
- [ ] Si hay celdas combinadas, se justifica el uso de HTML.
- [ ] La tabla se comprobó en el render final, no solo en el editor.

---

[← 4. Sintaxis básica](04-sintaxis-basica.md) · [Índice general](README.md) · [6. Listas de tareas →](06-listas-de-tareas.md)
