# 13. HTML dentro de Markdown

> [← Índice general](README.md) · Capítulo 13 de 63

## 13.1 HTML en bloque e inline

Markdown permite incrustar HTML (comportamiento heredado del original).

```markdown
Texto con <kbd>Ctrl</kbd> + <kbd>C</kbd> y H<sub>2</sub>O.

<details>
<summary>Ver más</summary>

Contenido que **sí** puede usar Markdown (nota la línea en blanco).

</details>

<div align="center">
  <img src="logo.png" alt="Logo del proyecto" width="200">
</div>
```

Reglas prácticas (CommonMark):
- Un **bloque HTML** comienza con una etiqueta de bloque al inicio de línea y termina con una línea en blanco (según el tipo).
- Dentro de un bloque HTML, el Markdown **no se procesa** por defecto; para dentro de `<details>` se deja una línea en blanco tras `<summary>`.
- Las etiquetas **inline** (`<span>`, `<kbd>`, `<sub>`) funcionan dentro de párrafos.

## 13.2 Limitaciones

- **Sanitizado**: GitHub, GitLab, etc., eliminan `<script>`, `<style>`, `<iframe>`, atributos `style`/`on*`, y restringen atributos.
- **Conversión**: al exportar a PDF/DOCX/EPUB, el HTML puede ignorarse o comportarse de forma distinta.
- **Portabilidad**: lo que funciona en un sitio puede romperse en otro.

| Entorno | Comportamiento con HTML |
|---|---|
| CommonMark | Pasa el HTML sin modificarlo (el parser no lo sanea) |
| GFM / GitHub | Aplica *tagfilter* y sanitización: elimina `<script>`, estilos, `<iframe>`, `onclick`… |
| GitLab, Bitbucket | Sanitizan con listas propias de etiquetas y atributos permitidos |
| Conversión a PDF/DOCX | Puede ignorarse o mostrarse como texto |
| `style` y CSS en línea | Normalmente eliminados en plataformas de colaboración |
| Etiquetas desconocidas | Pueden mostrarse como texto o descartarse |

## 13.3 Seguridad

Si el Markdown procede de **usuarios no confiables**, el HTML embebido es un vector de **XSS**. Debe sanitizarse la salida (DOMPurify, `rehype-sanitize`, `bleach`…) o deshabilitarse el HTML en el parser. Véase la [sección 48](48-seguridad.md).

## 13.4 Cuándo usarlo y cuándo evitarlo

| Úsalo para | Evítalo para |
|---|---|
| Alinear/redimensionar imágenes | Cosas con equivalente Markdown (negrita, listas, enlaces) |
| Contenido plegable (`<details>`) | Maquetación compleja de páginas |
| Teclas (`<kbd>`), subíndices | Contenido de usuarios no confiables sin sanitizar |
| Tablas con celdas combinadas | Documentos que se exportan a múltiples formatos |

## 13.5 Ejemplos útiles

**Texto con teclas, subíndices y superíndices:**

```markdown
Pulsa <kbd>Ctrl</kbd> + <kbd>C</kbd> para copiar. H<sub>2</sub>O y E = mc<sup>2</sup>.
```

**Imagen centrada y con tamaño:**

```markdown
<p align="center">
  <img src="docs/images/arquitectura.png" alt="Diagrama de arquitectura del sistema" width="600">
</p>
```

**Comentario oculto:**

```markdown
<!-- Este comentario no se muestra en el resultado -->
```

> En **MDX** los comentarios HTML `<!-- -->` **no son válidos**; se usan comentarios JSX `{/* ... */}` (ver [sección 29](29-mdx-creacion-de-paginas-web-con-markdown-y-componentes.md)).

---

[← 12. Variantes y dialectos de Markdown](12-variantes-y-dialectos-de-markdown.md) · [Índice general](README.md) · [14. Mermaid →](14-mermaid.md)
