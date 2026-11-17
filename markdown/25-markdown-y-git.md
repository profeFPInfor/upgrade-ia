# 25. Markdown y Git

> [← Índice general](README.md) · Capítulo 25 de 63

Markdown y Git encajan porque ambos trabajan con **texto plano**. Un cambio en un párrafo produce una diferencia legible, no un binario opaco. Esa legibilidad es la base de la revisión: permite ver qué cambió, quién lo cambió y por qué.

Pero Git no está diseñado específicamente para prosa. Los saltos de línea, los conflictos de fusión y los archivos grandes requieren decisiones explícitas. Este capítulo recoge las que más afectan a un corpus Markdown.

## 25.1 Por qué encajan

| Uso | Descripción |
|---|---|
| README | Puerta de entrada del repositorio |
| Commits | El mensaje es texto plano; la plataforma puede renderizar Markdown en la descripción de un PR, no en el mensaje del cliente `git` |
| Pull Requests | Descripción, comentarios y sugerencias en GFM |
| Issues | Cuerpos en GFM; plantillas en `.github/ISSUE_TEMPLATE/` |
| Wiki | Repositorio Git aparte (`repo.wiki.git`) con páginas Markdown |
| Documentación versionada | *Docs as code*: misma rama, misma revisión y mismo CI que el código |
| Historial | `git log -p -- docs/uso.md` muestra la evolución |
| Ramas | La documentación de una función viaja en la rama de esa función |
| Revisión | Los cambios se revisan en un PR como cualquier código |

El beneficio no es solo técnico: obliga a que la documentación tenga un proceso. Un cambio de comportamiento y su documentación pueden revisarse juntos, y el historial conserva por qué se tomó una decisión.

## 25.2 Qué versionar y qué no

Versiona:

- Archivos `.md`, imágenes fuente y diagramas editables.
- Plantillas, configuraciones y scripts de generación.
- El archivo `README.md`, la licencia y la guía de contribución.

No versiones:

- Salidas generadas (`_site/`, `dist/`, PDF construidos en CI).
- Cachés, credenciales, archivos de entorno y datos personales.
- Binarios enormes que no necesitan historial.

La regla práctica: **si se puede regenerar, no se versiona**. Si un PDF tarda segundos en generarse, no hace falta guardarlo; si es el entregable que se publica, puede tener sentido adjuntarlo a una release.

## 25.3 Una frase por línea

Escribir **una frase por línea** (*semantic line breaks*) hace que las diferencias de Git sean más precisas. En lugar de un párrafo completo en una línea, cada frase ocupa la suya:

```markdown
Markdown es un lenguaje de marcado ligero.
Permite escribir texto con estructura y convertirlo a HTML.
El texto fuente sigue siendo legible sin renderizar.
```

Si cambias la segunda frase, el diff muestra una línea modificada, no un párrafo entero. En prosa revisada por varias personas, esto reduce el ruido y facilita la revisión.

No es una obligación de Markdown: el render une las líneas en un párrafo. Es una convención de escritura que mejora el trabajo con Git. Algunos editores y formateadores pueden reflowar el texto; si el equipo adopta la convención, conviene desactivar el reflow automático o aplicarlo solo al guardar de forma consciente.

## 25.4 Finales de línea y `.gitattributes`

Windows y Unix usan finales de línea distintos. Git puede normalizarlos, pero la configuración global de cada persona no basta: el repositorio debe declarar la regla.

```gitattributes
# Normalizar Markdown a LF en el repositorio
*.md text eol=lf

# Usar el driver de diff de Markdown
*.md diff=markdown

# Tratar binarios como binarios
*.png binary
*.jpg binary
*.pdf binary
```

- `text` indica que el archivo es texto.
- `eol=lf` fuerza LF en el árbol de trabajo al hacer checkout.
- `binary` evita conversiones y diffs de texto.
- `diff=markdown` usa el driver integrado de Git para resaltar mejor los cambios.

En Windows, `core.autocrlf` puede entrar en conflicto con `.gitattributes`. Cuando ambos existen, las reglas del repositorio tienen prioridad, pero conviene documentar la configuración y comprobar el resultado con `git diff --check`.

## 25.5 Conflictos de fusión

Un conflicto ocurre cuando dos ramas cambian la misma región. En Markdown son frecuentes porque dos personas editan el mismo párrafo o la misma lista.

```text
<<<<<<< HEAD
El comando se ejecuta con privilegios de administrador.
=======
El comando requiere privilegios de administrador.
>>>>>>> rama
```

Pasos para resolverlo:

1. **Entiende el contexto:** `git log --merge -p -- archivo.md`.
2. **Elige o combina:** no te limites a borrar marcas; reescribe la frase final.
3. **Comprueba el render:** un conflicto mal resuelto puede dejar una tabla rota.
4. **Marca como resuelto:** `git add archivo.md`.
5. **Ejecuta las pruebas y el linting** antes de continuar.

Ayudas útiles:

- `git checkout --conflict=diff3 -- archivo.md` muestra también la versión base.
- `git rerere` reutiliza resoluciones anteriores de conflictos similares.
- `git merge --abort` cancela la fusión y vuelve al estado anterior.

El atributo `merge=union` combina automáticamente las líneas de ambas ramas, pero suele duplicar frases y no es adecuado para prosa. Úsalo solo en archivos donde la unión sea segura, como listas de entradas independientes.

## 25.6 Revisar diferencias

| Comando | Para qué |
|---|---|
| `git diff` | Cambios no preparados |
| `git diff --staged` | Cambios preparados |
| `git diff --word-diff` | Diferencias por palabra |
| `git diff --color-words` | Igual, con color en el terminal |
| `git diff --stat` | Resumen por archivo |
| `git log -p --follow -- docs/uso.md` | Historial con cambios, siguiendo renombrados |
| `git blame -w -C -C -C -- docs/uso.md` | Autoría por línea, ignorando espacios y detectando movimientos |

`git blame` no es una herramienta para culpar: sirve para encontrar el contexto de una línea. Combínalo con `git log` para leer el commit completo, no solo el fragmento.

Antes de abrir un PR, revisa el diff tú mismo. Un cambio de una palabra puede alterar el significado de una instrucción; el diff es el último punto donde se detecta sin publicar.

## 25.7 Renombrados y enlaces

Git detecta renombrados por similitud, pero no actualiza los enlaces de Markdown. Si mueves un archivo:

1. Usa `git mv viejo.md nuevo.md` para conservar el historial.
2. Busca referencias al nombre antiguo en todo el repositorio.
3. Actualiza los enlaces relativos y las anclas.
4. Añade una redirección si la URL pública cambia.
5. Comprueba el sitio generado, no solo el editor.

```bash
git mv docs/instalacion.md docs/inicio/instalacion.md
rg "instalacion\.md" -n
```

`git log --follow -- docs/inicio/instalacion.md` sigue el historial a través del renombrado, aunque no es infalible si el archivo cambió mucho. El capítulo [63](63-publicacion-y-distribucion.md) trata las redirecciones desde el punto de vista del sitio publicado.

## 25.8 Archivos grandes con Git LFS

Las imágenes, los vídeos y los PDF pueden inflar el repositorio. Git LFS (Large File Storage) guarda un puntero en Git y el archivo en un almacenamiento aparte:

```bash
git lfs install
git lfs track "*.mp4"
git lfs track "*.psd"
git add .gitattributes
```

- `git lfs track` escribe las reglas en `.gitattributes`; versiona ese archivo.
- Los clones necesitan `git lfs install` y acceso al servidor LFS.
- GitHub, GitLab y otros hosts tienen cuotas y límites; compruébalos antes de subir.
- LFS no sustituye una política de assets: si un vídeo no necesita historial, publícalo fuera del repositorio.

Para imágenes pequeñas de documentación, un PNG optimizado suele ser suficiente; LFS añade complejidad y dependencia del host.

## 25.9 Commits, firma y revisión

Un mensaje de commit útil explica **qué** y **por qué**, no solo «cambios»:

```text
docs(instalacion): aclarar requisitos de Linux

Separa los requisitos de sistema de los pasos de instalación.
Añade verificación con `ejemplo --version`.
```

- **Conventional Commits** es una convención opcional; si se adopta, documenta los tipos y el alcance.
- **Firma de commits:** `git commit -S` firma con GPG o SSH; `git config commit.gpgsign true` lo hace por defecto. La plataforma muestra el estado de verificación.
- **Sign-off:** `git commit -s` añade la línea `Signed-off-by`, usada por proyectos con DCO.
- **Revisión:** una persona distinta del autor aprueba los cambios sustantivos; los arreglos triviales pueden tener un flujo más ligero.

El capítulo [26](26-markdown-y-github.md) describe las plantillas y la revisión en GitHub; el [62](62-gobierno-frescura-y-metricas.md), la propiedad y la revisión programada.

## 25.10 Lista de comprobación

- [ ] El repositorio tiene `.gitattributes` con finales de línea y binarios.
- [ ] Los archivos generados no se versionan.
- [ ] El equipo conoce la convención de una frase por línea (si se adopta).
- [ ] Los conflictos se resuelven reescribiendo, no borrando marcas a ciegas.
- [ ] Los renombrados actualizan enlaces y redirecciones.
- [ ] Las imágenes y vídeos grandes tienen una política (LFS o externa).
- [ ] Los mensajes de commit explican el cambio.
- [ ] Los commits importantes están firmados o tienen sign-off, si el proyecto lo exige.
- [ ] El diff se revisa antes de abrir el PR.
- [ ] El linting y la validación de enlaces se ejecutan en CI.

---

[← 24. Front Matter](24-front-matter.md) · [Índice general](README.md) · [26. Markdown y GitHub →](26-markdown-y-github.md)
