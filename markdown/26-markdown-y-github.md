# 26. Markdown y GitHub

> [← Índice general](README.md) · Capítulo 26 de 63

GitHub es probablemente el lugar donde más Markdown se escribe y se lee. README, issues, pull requests, discusiones, releases y wikis usan el mismo dialecto, **GFM**, con extensiones que no forman parte de CommonMark. Conocer qué acepta GitHub —y qué no— evita depender de funciones que solo existen en la interfaz web.

Este capítulo recorre los lugares donde aparece Markdown, las plantillas que ordenan la colaboración y los límites que conviene anticipar.

## 26.1 Dónde aparece Markdown

| Lugar | Uso | Plantilla o ruta |
|---|---|---|
| README | Portada del repositorio | `README.md` en raíz, `docs/` o `.github/` |
| Perfil | README del usuario u organización | Repositorio `usuario/usuario` |
| Issues | Descripción, comentarios, casillas | `.github/ISSUE_TEMPLATE/` |
| Pull Requests | Descripción, revisión, sugerencias | `.github/pull_request_template.md` |
| Discussions | Hilos y respuestas | Categorías del repositorio |
| Releases | Notas de versión | Interfaz o `gh release create` |
| Wiki | Páginas Markdown | Repositorio Git aparte |
| Comentarios | Commits, PRs, issues | — |
| Documentación | Archivos `.md` y GitHub Pages | `docs/`, Actions |
| Mermaid | Diagramas en bloques `mermaid` | Véase [15](15-mermaid-en-github.md) |
| Badges | Imágenes enlazadas | Véase [27](27-badges.md) |

El render de GitHub.com no es idéntico al de GitHub Pages. Pages usa Jekyll y kramdown por defecto; GitHub.com usa su propio render de GFM. Un documento puede verse bien en el repositorio y distinto en el sitio publicado.

## 26.2 GFM y funciones de GitHub

GFM añade a CommonMark tablas, listas de tareas, tachado, autovinculación de URLs y notas al pie, entre otras extensiones. Además, GitHub ofrece funciones que **no forman parte de GFM**:

- Menciones (`@usuario`), referencias a issues (`#123`) y a commits (SHA).
- Alertas (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`).
- Diagramas Mermaid, matemáticas y mapas GeoJSON o STL.
- Casillas interactivas en issues y PRs.
- Sugerencias de cambio en revisiones.
- Enlaces permanentes a líneas de código.

Si el documento va a publicarse fuera de GitHub, no supongas que estas funciones existirán. El capítulo [10](10-github-flavored-markdown-gfm.md) separa la especificación GFM de las funciones de la plataforma; el [51](51-compatibilidad.md) compara el render entre plataformas.

## 26.3 README y perfil

El README es la primera página que ve quien llega al repositorio. Un buen README responde en menos de un minuto:

1. **Qué es** el proyecto.
2. **Para qué sirve** y qué problema resuelve.
3. **Cómo se instala** o se prueba.
4. **Dónde está la documentación** completa.
5. **Cómo contribuir** y con qué licencia.

````markdown
# Nombre del proyecto

Una frase que explique qué hace y para quién.

## Instalación

```bash
npm install nombre-del-proyecto
```

## Uso

```js
import { crear } from "nombre-del-proyecto";
```

## Documentación

- [Guía de inicio](docs/inicio.md)
- [Referencia de la API](docs/api.md)

## Licencia

MIT.
````

El README del perfil se muestra en `github.com/usuario` si existe un repositorio con el mismo nombre que el usuario y un `README.md` en la raíz. Es útil para presentar el trabajo, pero no sustituye la documentación del proyecto.

## 26.4 Issues y plantillas

Las plantillas de issue reducen preguntas incompletas. GitHub admite dos formatos:

- **Plantillas Markdown** (`.md`) con Front Matter para el nombre, la descripción y las etiquetas.
- **Formularios de issue** (`.yml`) con campos obligatorios, desplegables y validación.

```yaml
# .github/ISSUE_TEMPLATE/bug.yml (fragmento)
name: Error
description: Notificar un comportamiento incorrecto
title: "[Bug]: "
labels: ["bug"]
body:
  - type: textarea
    id: pasos
    attributes:
      label: Pasos para reproducir
      description: Indica los comandos y el resultado esperado.
    validations:
      required: true
```

Además:

- `config.yml` permite desactivar el formulario en blanco y añadir enlaces de contacto.
- Las etiquetas y los hitos organizan el trabajo, pero no sustituyen una descripción clara.
- Las casillas `- [ ]` son interactivas en issues y PRs; en un archivo `.md` son solo texto.
- `gh issue create` permite abrir un issue desde la terminal.

Una plantilla demasiado larga desanima a quien la rellena. Pide lo mínimo para reproducir el problema y deja el resto para la conversación.

## 26.5 Pull requests y sugerencias

La descripción de un PR debe explicar **qué cambia**, **por qué** y **cómo se probó**. Una plantilla ayuda:

```markdown
## Qué cambia

- Añade la guía de instalación en Linux.

## Por qué

- Faltaba el requisito de permisos.

## Cómo se probó

- [ ] Enlaces verificados con lychee.
- [ ] Render revisado en local.
```

En una revisión, GitHub permite proponer un cambio concreto con un bloque `suggestion`:

````markdown
```suggestion
El comando requiere privilegios de administrador.
```
````

La persona que revisa puede aceptar la sugerencia con un clic. Es útil para correcciones pequeñas; para cambios de estructura, es mejor explicar el problema y dejar que el autor reescriba.

Otras funciones:

- **Revisión por archivos** y comentarios en líneas concretas.
- **Borradores de PR** para trabajo en curso.
- **PR enlazados a issues** con palabras clave como `closes #12`.
- **Checks** de CI que deben pasar antes de fusionar.

## 26.6 Discussions, Releases y wiki

**Discussions** sirve para conversaciones abiertas: preguntas, ideas, anuncios y encuestas. No es un sustituto de los issues: un error reproducible debe tener seguimiento y cierre.

**Releases** usa Markdown para las notas de versión. GitHub puede generarlas automáticamente a partir de los PR fusionados, pero conviene editarlas: un listado de commits no explica el impacto para quien usa el producto.

```bash
gh release create v2.4.0 --notes-file CHANGELOG.md
```

**Wiki** es un repositorio Git independiente (`repo.wiki.git`). Se puede clonar y editar como cualquier otro, pero no pasa por la revisión de un PR del repositorio principal. Si la documentación necesita revisión, es mejor mantenerla en `docs/`.

## 26.7 Actions y Pages

GitHub Actions ejecuta flujos definidos en `.github/workflows/*.yml`. Para documentación, los usos más habituales son:

- Validar Markdown con markdownlint.
- Comprobar enlaces con lychee o markdown-link-check.
- Revisar Front Matter y fechas.
- Generar el sitio y publicarlo en Pages.

```yaml
name: docs
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  validar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npx markdownlint-cli2 "**/*.md"
```

Buenas prácticas:

- Declara `permissions` con el mínimo necesario.
- Fija las acciones por versión o, mejor, por SHA.
- No imprimas secretos en los logs.
- Separa la validación de la publicación.
- Ejecuta el flujo en PR y en la rama principal.

GitHub Pages publica un sitio estático. Puede construirse con Jekyll o con un flujo de Actions que suba un artefacto. Si usas Jekyll, el resultado depende de la versión y de los plugins admitidos; si usas otro generador, constrúyelo en CI y publica el directorio de salida.

## 26.8 Colaboración y propiedad

- **`CODEOWNERS`** solicita revisión según la ruta; el último patrón que coincide tiene prioridad.
- **Protección de rama** puede exigir revisión, checks y conversaciones resueltas.
- **Plantillas** de issue y PR reducen idas y vueltas.
- **Etiquetas** y **hitos** hacen visible el estado, pero no lo documentan.
- **Equipos** con permiso de escritura son más fáciles de mantener que listas de personas.

El capítulo [62](62-gobierno-frescura-y-metricas.md) desarrolla la propiedad y el ciclo de vida; el [25](25-markdown-y-git.md), la revisión y los conflictos.

## 26.9 Límites, seguridad y enlaces

- **HTML sanitizado.** GitHub elimina scripts y atributos peligrosos; no confíes en HTML embebido para funciones interactivas.
- **Enlaces relativos.** En un README, `docs/api.md` se resuelve dentro del repositorio; en un sitio generado, la ruta puede cambiar.
- **Anclas.** Los encabezados generan anclas, pero el algoritmo puede diferir del de tu generador. Usa un ID explícito si el enlace es crítico.
- **Imágenes.** Las imágenes externas pueden fallar o rastrear a quien las ve; para documentación estable, guárdalas en el repositorio.
- **Secretos.** No pegues tokens, claves ni datos personales en issues, PRs o logs. Si ocurre, revócalos y limpia el historial.
- **Contenido generado.** Un README gigante generado desde otro archivo se desactualiza; genera en CI o enlaza la fuente.

## 26.10 Lista de comprobación

- [ ] El README explica qué es el proyecto, cómo se instala y dónde está la documentación.
- [ ] Las plantillas de issue y PR existen y piden la información mínima.
- [ ] Las casillas y alertas se usan solo donde GitHub las renderiza.
- [ ] Las sugerencias de cambio se reservan para correcciones pequeñas.
- [ ] Las notas de release explican el impacto, no solo enumeran commits.
- [ ] La wiki no se usa para contenido que necesita revisión.
- [ ] Los flujos de Actions declaran permisos mínimos y fijan versiones.
- [ ] `CODEOWNERS` cubre las rutas críticas.
- [ ] No hay secretos ni datos personales en el historial visible.
- [ ] Los enlaces relativos y las anclas funcionan en el render de GitHub y en el sitio publicado.

---

[← 25. Markdown y Git](25-markdown-y-git.md) · [Índice general](README.md) · [27. Badges →](27-badges.md)
