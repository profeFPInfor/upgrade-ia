# 41. Matemáticas y notación científica

> [← Índice general](README.md) · Capítulo 41 de 63

Markdown original no incluye matemáticas. Las fórmulas se escriben con sintaxis **LaTeX** y se renderizan con un motor externo (MathJax, KaTeX o MathML) o se convierten directamente en LaTeX al exportar a PDF. Este capítulo explica la sintaxis, la compatibilidad y los errores más habituales.

## 41.1 Qué es estándar y qué no

| Contexto | Soporte |
|---|---|
| Markdown original | No |
| CommonMark | No |
| GFM (GitHub) | Matemáticas con `$...$` y `$$...$$` |
| Pandoc Markdown | `$...$`, `$$...$$`, `\(...\)`, `\[...\]` |
| Jekyll/kramdown | Según `math_engine` |
| MkDocs, Docusaurus, Hugo | Mediante extensiones o plugins |

No todos los visores renderizan matemáticas: si el documento debe leerse en un cliente que no las admite, la fórmula aparecerá como texto. Para documentación crítica, incluye una explicación textual o una imagen de respaldo.

## 41.2 Sintaxis básica

```markdown
La energía es $E = mc^2$.

$$
\int_{0}^{1} x^2 \, dx = \frac{1}{3}
$$
```

- `$...$`: matemáticas en línea.
- `$$...$$`: bloque centrado.
- `\(...\)` y `\[...\]`: alternativas que algunos parsers prefieren para evitar conflictos con el dinero (`$5`).

Para escribir un dólar literal: `\$`.

## 41.3 Expresiones habituales

| Expresión | Sintaxis | Resultado |
|---|---|---|
| Fracción | `\frac{a}{b}` | a/b |
| Raíz | `\sqrt{x}`, `\sqrt[3]{x}` | √x |
| Suma | `\sum_{i=1}^{n} i` | Σ |
| Integral | `\int_{a}^{b} f(x)\,dx` | ∫ |
| Límite | `\lim_{x \to 0} \frac{\sin x}{x}` | límite |
| Derivada | `\frac{dy}{dx}`, `f'(x)` | derivada |
| Parcial | `\frac{\partial f}{\partial x}` | parcial |
| Producto | `\prod_{i=1}^{n} i` | producto |
| Vector | `\vec{v}`, `\mathbf{v}` | vector |
| Conjunto | `\{1, 2, 3\}`, `\mathbb{R}` | conjuntos |

## 41.4 Alineación, matrices y casos

```markdown
$$
\begin{aligned}
  f(x) &= x^2 + 2x + 1 \\
       &= (x + 1)^2
\end{aligned}
$$
```

```markdown
$$
A = \begin{pmatrix}
  a & b \\
  c & d
\end{pmatrix}
$$
```

```markdown
$$
f(x) = \begin{cases}
  x^2 & \text{si } x \ge 0 \\
  -x  & \text{si } x < 0
\end{cases}
$$
```

- `\\` separa filas.
- `&` alinea columnas.
- `\text{...}` escribe texto normal dentro de una fórmula.
- `\operatorname{...}` define operadores.

## 41.5 Numeración y referencias

En LaTeX o PDF, una ecuación puede numerarse con un entorno:

```latex
\begin{equation}
  E = mc^2
  \label{eq:energia}
\end{equation}

La ecuación~\ref{eq:energia} muestra la equivalencia.
```

En MathJax o KaTeX no hay referencias cruzadas reales; se puede forzar una etiqueta visual:

```markdown
$$
E = mc^2 \tag{1}
$$
```

Para referencias cruzadas automáticas en documentos largos, usa LaTeX o un filtro como `pandoc-crossref`.

## 41.6 Motores de renderizado

| Motor | Ventajas | Limitaciones |
|---|---|---|
| **MathJax** | Muy completo: LaTeX, MathML, AsciiMath; extensiones | Más pesado y lento |
| **KaTeX** | Rápido, salida HTML + MathML | Subconjunto de LaTeX |
| **MathML** | Nativo, sin JavaScript | Soporte y calidad variables |
| **WebTeX** | Imágenes generadas en servidor | Dependencia de red; no accesible |

Con Pandoc:

```bash
pandoc apuntes.md -s --mathjax -o apuntes.html
pandoc apuntes.md -s --katex  -o apuntes.html
pandoc apuntes.md -s --mathml -o apuntes.html
```

- MathJax: <https://www.mathjax.org/>
- KaTeX: <https://katex.org/>
- Funciones admitidas por KaTeX: <https://katex.org/docs/supported.html>

## 41.7 Configuración por plataforma

- **Jekyll/kramdown**: `math_engine: mathjax` en `_config.yml`.
- **Hugo**: extensión `passthrough` de Goldmark para proteger las fórmulas.
- **MkDocs**: `pymdownx.arithmatex` con MathJax o KaTeX.
- **Docusaurus**: `remark-math` + `rehype-katex`.
- **GitHub**: matemáticas en Markdown con `$...$` y `$$...$$`; el renderizado es del lado del servidor.

La configuración debe **proteger** las fórmulas antes de que el parser de Markdown interprete `_` o `*` como énfasis.

## 41.8 Química y unidades

Con la extensión `mhchem`:

```markdown
$$
\ce{2H2 + O2 -> 2H2O}
$$
```

- `mhchem`: <https://mhchem.github.io/MathJax-mhchem/>

Unidades y cifras:

```markdown
La distancia es $10\ \mathrm{km}$ y la masa $2{,}5\ \mathrm{kg}$.
```

- En LaTeX, `{,}` evita el espacio que produce la coma decimal.
- En español se usa coma decimal; en contextos internacionales, punto.
- No mezcles unidades del Sistema Internacional con símbolos inventados.

## 41.9 Errores frecuentes

| Problema | Causa | Solución |
|---|---|---|
| `_` aparece como cursiva | El parser interpreta énfasis dentro de la fórmula | Protege las fórmulas o usa `\(...\)` |
| `\\` no separa líneas | Barra escapada por Markdown | Usa un bloque `$$` o duplica la barra |
| La tabla se rompe | `|` dentro de una fórmula | Escapa `\|` o evita tablas |
| `$5 y $10` se vuelve fórmula | Dólares sin escapar | Escribe `\$5` y `\$10` |
| Fórmula cortada | Contenedor con ancho fijo | `overflow-x: auto` |
| Símbolos desconocidos | Función no admitida por KaTeX | Consulta la lista o usa MathJax |
| Fuente distinta | El motor usa su propia fuente matemática | Configura la fuente del motor |

## 41.10 Accesibilidad

- MathML permite que los lectores de pantalla accedan a la estructura.
- KaTeX genera HTML y MathML; MathJax puede generar MathML.
- Para fórmulas muy complejas, añade una descripción textual cercana.
- No uses una imagen de fórmula como única representación.
- Comprueba el contraste de las fórmulas en modo oscuro.
- Evita depender solo del color para distinguir términos.

## 41.11 Lista de comprobación

- [ ] El motor matemático está configurado y protegido del parser.
- [ ] Las fórmulas se ven en el destino real (web, PDF, EPUB).
- [ ] Los delimitadores son coherentes en todo el documento.
- [ ] No hay dólares sin escapar.
- [ ] Las fórmulas largas no desbordan.
- [ ] Hay alternativa textual para las fórmulas esenciales.
- [ ] La notación y las unidades son coherentes.

---

[← 40. Exportación a imágenes y otros destinos](40-exportacion-a-imagenes-y-otros-destinos.md) · [Índice general](README.md) · [42. Notas al pie, definiciones y referencias →](42-notas-al-pie-definiciones-y-referencias.md)
