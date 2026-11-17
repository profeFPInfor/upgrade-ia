# 46. Linting y validación

> [← Índice general](README.md) · Capítulo 46 de 63

El **linting** analiza el texto y señala problemas de estilo, estructura o sintaxis. La **validación** comprueba que el documento cumple una especificación o un esquema (por ejemplo, Front Matter YAML o MDX compilable). Ambas prácticas son especialmente útiles en documentación colaborativa y en integración continua.

## 46.1 Qué se puede validar

| Aspecto | Herramienta típica | Ejemplo de problema |
|---|---|---|
| Estructura de títulos | markdownlint | Saltar de `#` a `###` |
| Listas | markdownlint | Anidación incorrecta |
| Longitud de línea | markdownlint, Prettier | Líneas de 300 caracteres |
| Bloques de código | markdownlint | Lenguaje no especificado |
| Enlaces | lychee, markdown-link-check | URL rota o ancla inexistente |
| Imágenes | markdownlint | Falta de texto alternativo |
| Tablas | markdownlint, Prettier | Columnas desalineadas |
| Front Matter | JSON Schema, Zod | Campo obligatorio ausente |
| Ortografía | cspell, LanguageTool | Falta o error tipográfico |
| Estilo de prosa | Vale | Términos inconsistentes |
| MDX/JSX | ESLint, compilador MDX | Etiqueta sin cerrar |
| Mermaid | mermaid-cli | Sintaxis inválida |

## 46.2 markdownlint

**markdownlint** es la herramienta de referencia para validar estilo en Markdown. Está escrita en JavaScript y se distribuye como paquete npm. Aplica reglas con identificadores (`MD001`, `MD013`, etc.) y permite configurar excepciones.

- Repositorio: <https://github.com/DavidAnson/markdownlint>
- Reglas: <https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md>

### 46.2.1 Reglas habituales

| Regla | Qué comprueba |
|---|---|
| `MD001` | Los encabezados incrementan de nivel de uno en uno |
| `MD003` | Estilo de encabezado consistente (ATX o Setext) |
| `MD004` | Estilo de lista consistente (`-`, `*`, `+`) |
| `MD007` | Indentación de listas anidadas |
| `MD009` | Espacios al final de línea |
| `MD012` | Líneas en blanco múltiples |
| `MD013` | Longitud máxima de línea |
| `MD022` | Líneas en blanco alrededor de encabezados |
| `MD024` | Encabezados duplicados |
| `MD031` | Líneas en blanco alrededor de bloques de código |
| `MD032` | Líneas en blanco alrededor de listas |
| `MD033` | HTML en línea |
| `MD034` | URLs sin formato de enlace |
| `MD040` | Lenguaje en bloques de código |
| `MD041` | Primer línea debe ser un encabezado de nivel 1 |
| `MD046` | Estilo de bloque de código consistente |
| `MD047` | El archivo termina con una sola línea en blanco |

### 46.2.2 Configuración

Archivo `.markdownlint.json`:

```json
{
  "default": true,
  "MD013": {
    "line_length": 120,
    "code_blocks": false,
    "tables": false
  },
  "MD033": {
    "allowed_elements": ["details", "summary", "kbd", "br"]
  },
  "MD041": false,
  "MD024": {
    "siblings_only": true
  }
}
```

Archivo `.markdownlintignore` (solo para `markdownlint-cli`):

```text
node_modules/
dist/
CHANGELOG.md
```

> `markdownlint-cli2` **no** lee `.markdownlintignore`; usa la propiedad `ignores` de su configuración o patrones negados como `"#node_modules"`.

### 46.2.3 Uso

```bash
# Instalar
npm install --save-dev markdownlint-cli2

# Validar todos los Markdown
npx markdownlint-cli2 "**/*.md" "#node_modules"

# Corregir automáticamente lo que sea seguro
npx markdownlint-cli2 --fix "**/*.md"
```

Con `markdownlint-cli` (otro cliente):

```bash
npm install --save-dev markdownlint-cli
npx markdownlint "**/*.md" --ignore node_modules
npx markdownlint "**/*.md" --fix
```

### 46.2.4 Desactivar reglas puntualmente

```markdown
<!-- markdownlint-disable MD013 -->
Esta línea puede ser muy larga sin que el linter la señale.
<!-- markdownlint-enable MD013 -->
```

```markdown
<!-- markdownlint-disable-next-line MD033 -->
<div class="ejemplo">HTML permitido solo aquí</div>
```

> Las excepciones deben ser justificadas y revisadas. Un exceso de `disable` vacía de sentido al linter.

## 46.3 markdownlint-cli2

`markdownlint-cli2` es el cliente recomendado actualmente. Acepta una configuración JSONC con comentarios, patrones glob y reglas por archivo.

`.markdownlint-cli2.jsonc`:

```jsonc
{
  "config": {
    "default": true,
    "MD013": { "line_length": 120, "tables": false },
    "MD033": { "allowed_elements": ["details", "summary", "kbd"] }
  },
  "globs": ["**/*.md", "**/*.mdx"],
  "ignores": ["node_modules/**", "dist/**", "CHANGELOG.md"]
}
```

```bash
npx markdownlint-cli2
npx markdownlint-cli2 --fix
npx markdownlint-cli2 --config .markdownlint-cli2.jsonc
```

- Repositorio: <https://github.com/DavidAnson/markdownlint-cli2>

## 46.4 remark-lint

**remark** es un procesador de Markdown basado en el ecosistema **unified**. `remark-lint` aplica reglas sobre el árbol AST, lo que permite validaciones más semánticas y compatibilidad con MDX.

```bash
npm install --save-dev remark-cli remark-preset-lint-recommended
```

`.remarkrc.mjs`:

```javascript
import remarkPresetLintRecommended from "remark-preset-lint-recommended";

export default {
  plugins: [remarkPresetLintRecommended]
};
```

```bash
npx remark . --frail --quiet
```

- `remark-lint`: <https://github.com/remarkjs/remark-lint>

Ventajas: reglas sobre AST, integración con `remark-gfm`, `remark-mdx` y otros plugins. Limitaciones: configuración más técnica; no todas las reglas tienen corrección automática.

## 46.5 Prettier

**Prettier** es un formateador de código que también formatea Markdown. No busca errores semánticos: normaliza espacios, listas, tablas, comillas y saltos de línea.

`.prettierrc.json`:

```json
{
  "proseWrap": "always",
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false
}
```

`.prettierignore`:

```text
node_modules/
dist/
*.min.md
```

```bash
npx prettier --check "**/*.md"
npx prettier --write "**/*.md"
```

> Prettier y markdownlint pueden discrepar (por ejemplo, en el ajuste de líneas o en el formato de tablas). Define un orden: primero Prettier, después markdownlint, y documenta las excepciones.

## 46.6 Vale, cspell y correctores de prosa

| Herramienta | Función | Enlace |
|---|---|---|
| **Vale** | Reglas de estilo de prosa, terminología y consistencia | <https://vale.sh/> |
| **cspell** | Corrector ortográfico para código y documentación | <https://cspell.org/> |
| **LanguageTool** | Corrección gramatical y de estilo | <https://languagetool.org/> |
| **textlint** | Linting de texto con reglas en JavaScript | <https://textlint.github.io/> |

Ejemplo de `.vale.ini`:

```ini
StylesPath = .vale/styles
MinAlertLevel = suggestion

[*.md]
BasedOnStyles = Vale, Microsoft
```

```bash
vale sync
vale README.md
```

## 46.7 Validación de enlaces

Los enlaces rotos son uno de los defectos más frecuentes en documentación. Automatizarlos evita revisiones manuales.

| Herramienta | Uso | Enlace |
|---|---|---|
| **lychee** | Comprobación rápida de enlaces en Markdown, HTML y sitios | <https://github.com/lycheeverse/lychee> |
| **markdown-link-check** | Comprobación de enlaces en archivos Markdown | <https://github.com/tcort/markdown-link-check> |
| **htmltest** | Comprobación de enlaces en sitios HTML generados | <https://github.com/wjdp/htmltest> |

```bash
lychee --verbose --no-progress "**/*.md"
npx markdown-link-check README.md
```

Para CI, conviene distinguir entre enlaces internos (siempre obligatorios) y externos (pueden fallar por red o por bloqueo del servidor). Algunos proyectos usan `--offline` para validar solo enlaces relativos y anclas.

## 46.8 Validación de Front Matter

El Front Matter YAML puede validarse con un esquema. Ejemplo conceptual con Zod (JavaScript):

```javascript
import { z } from "zod";

const FrontMatter = z.object({
  title: z.string().min(1),
  description: z.string().min(1),
  date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  tags: z.array(z.string()).default([]),
  draft: z.boolean().default(false)
});

const result = FrontMatter.safeParse(data);
if (!result.success) {
  console.error(result.error.format());
}
```

En Astro, las *content collections* permiten definir esquemas con Zod de forma nativa. En Docusaurus y Nextra, el Front Matter se valida según la configuración del plugin o del tema.

## 46.9 Validación de MDX y Mermaid

- **MDX:** el propio compilador detecta etiquetas sin cerrar, imports inválidos y expresiones mal formadas. Añade `eslint-plugin-mdx` o `eslint-mdx` para reglas adicionales.
- **Mermaid:** `mermaid-cli` puede parsear un diagrama y fallar si la sintaxis es incorrecta:

```bash
mmdc -i diagrama.mmd -o diagrama.svg
```

Si el comando termina con código 0 y genera el SVG, la sintaxis es válida para esa versión de Mermaid.

- `eslint-plugin-mdx`: <https://github.com/mdx-js/eslint-mdx>

## 46.10 Integración en CI/CD

Ejemplo de GitHub Actions:

```yaml
name: Documentación

on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configurar Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - name: Instalar dependencias
        run: npm ci

      - name: Formatear
        run: npx prettier --check "**/*.md"

      - name: Lint de Markdown
        run: npx markdownlint-cli2 "**/*.md" "#node_modules"

      - name: Comprobar enlaces
        uses: lycheeverse/lychee-action@v2
        with:
          args: --verbose --no-progress "**/*.md"
```

Notas:

- Fija las acciones por versión o, mejor, por SHA para reducir riesgos de cadena de suministro.
- Ejecuta el lint en pull requests y en la rama principal.
- Si el proyecto es grande, cachea dependencias y limita el alcance a los archivos modificados.
- No bloquees el desarrollo por enlaces externos inestables; separa la comprobación de enlaces internos de la de externos.

## 46.11 Pre-commit

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace

  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.41.0
    hooks:
      - id: markdownlint
        args: ["--fix"]
```

```bash
pre-commit install
pre-commit run --all-files
```

## 46.12 Estrategia de adopción

1. Empieza con un conjunto pequeño de reglas y añade más de forma incremental.
2. Corrige primero los errores automáticos y revisa manualmente los que cambian contenido.
3. Documenta las excepciones en el propio repositorio.
4. Añade el linting a CI antes de exigirlo en las revisiones.
5. Mantén las versiones de las herramientas fijadas y actualízalas de forma controlada.
6. Separa las reglas de **estilo** de las de **corrección**: no todas deben bloquear una publicación.
7. Revisa los falsos positivos y ajusta la configuración en lugar de desactivar reglas completas.

## 46.13 Checklist de linting y validación

- [ ] Los encabezados siguen una jerarquía correcta.
- [ ] Los bloques de código indican lenguaje.
- [ ] Las tablas tienen encabezado y columnas coherentes.
- [ ] Las imágenes tienen texto alternativo.
- [ ] Los enlaces internos y externos funcionan.
- [ ] El Front Matter cumple el esquema.
- [ ] La ortografía y la terminología son consistentes.
- [ ] El documento compila (MDX, Mermaid, plantillas).
- [ ] El linting se ejecuta en CI.
- [ ] Las excepciones están justificadas.

---

[← 31. Conversión de Markdown](31-conversion-de-markdown.md) · [Índice general](README.md) · [47. Accesibilidad →](47-accesibilidad.md)
