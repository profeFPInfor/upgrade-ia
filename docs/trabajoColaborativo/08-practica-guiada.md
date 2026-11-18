# 8. Práctica guiada sin riesgo

← [Anterior: Carpeta de trabajo](03-primer-dia.md) · [Índice](README.md) · [Siguiente: Cómo trabajamos en este repositorio](09-como-trabajamos.md) →

Aquí practicas el ciclo de Git **en tu ordenador, sin tocar el repositorio del proyecto**. Nada de lo que hagas se sube a ningún sitio, así que puedes equivocarte y repetir. Es el mejor entrenamiento antes de tu primera Issue real.

> **Haz esta práctica antes de coger tu primera Issue.** Necesitas haber completado el [paso 2](02-preparar-el-equipo.md).

Tiempo aproximado: 30 a 45 minutos. Consejo: hazla en la terminal integrada de VS Code.

> **Antes de empezar, comprueba tres cosas:**
>
> 1. **Tu identidad en Git está configurada** (paso [2.4](02-preparar-el-equipo.md#24-decirle-a-git-quién-eres)). Si no, el primer `git commit` fallará con `Author identity unknown` ([qué hacer](06-errores-frecuentes.md#git-dice-author-identity-unknown)).
> 2. **Tu Git es la versión 2.28 o posterior** (`git --version`), porque usamos `git init -b main`. Si es más antigua, usa `git init` y después `git branch -M main`.
> 3. **Los mensajes de Git pueden salir en español o en inglés** según tu equipo. Aquí se muestran en inglés; lo importante es que el sentido sea el mismo.

## Preparar el terreno

1. Crea una carpeta nueva **fuera** de tu carpeta de trabajo del proyecto, por ejemplo `practica-git` dentro de `Documentos`.
2. Ábrela en VS Code: *File → Open Folder…*.
3. Abre la terminal: *Terminal → New Terminal*.
4. Convierte la carpeta en un repositorio:

   ```bash
   git init -b main
   ```

   Debe responder algo como `Initialized empty Git repository`.

## Ejercicio 1: tu primer commit

1. En VS Code, crea un fichero `notas.md` con este contenido y guárdalo:

   ```text
   # Mis notas

   Línea uno
   Línea dos
   Línea tres
   Línea cuatro
   ```

2. Mira el estado:

   ```bash
   git status
   ```

   Verás `notas.md` en *Untracked files* (archivos sin rastrear).
3. Prepáralo y haz commit:

   ```bash
   git add notas.md
   git commit -m "docs: crear notas"
   ```

   Debe mostrar algo como `1 file changed, 6 insertions(+)` (las seis líneas del fichero, la vacía incluida).
4. Comprueba el historial:

   ```bash
   git log --oneline
   ```

**Autocomprobación:** `git status` ahora dice `nothing to commit, working tree clean` y `git log` muestra un commit.

## Ejercicio 2: una rama

1. Crea una rama y entra en ella:

   ```bash
   git checkout -b ana
   ```

   (Pon tu nombre si quieres.) Responde `Switched to a new branch 'ana'`.
2. En VS Code, cambia la línea que dice `Línea dos` para que diga `Línea de Ana` y guarda.
3. Mira qué ha cambiado, con el cambio sin preparar y luego preparado:

   ```bash
   git diff
   git add notas.md
   git diff --staged
   ```

   `git diff` muestra, con `-` y `+`, la línea quitada (`-Línea dos`) y la añadida (`+Línea de Ana`). Muestra lo que has cambiado y aún no has preparado; `git diff --staged` muestra lo que ya está preparado para el commit. Revisar `--staged` antes de cada commit es un buen hábito.
4. Haz el commit:

   ```bash
   git commit -m "docs: cambiar la línea dos"
   ```

   Debe responder `1 file changed, 1 insertion(+), 1 deletion(-)`.

**Autocomprobación:** `git log --oneline` muestra dos commits y `git status` indica `On branch ana`.

## Ejercicio 3: provocar y resolver un conflicto

Un **conflicto** ocurre cuando dos ramas cambian las mismas líneas. Es normal, y mejor aprender a resolverlo aquí.

1. Vuelve a `main`:

   ```bash
   git checkout main
   ```

   Debe responder `Switched to branch 'main'`.

2. En VS Code, cambia **la misma línea**, la que dice `Línea dos`, para que diga `Línea de Beto`, y guarda. (Ahora el fichero de `main` y el de tu rama `ana` tienen una versión distinta de esa línea.) Haz commit:

   ```bash
   git add notas.md
   git commit -m "docs: cambiar la línea dos desde main"
   ```

3. Vuelve a tu rama (debe responder `Switched to branch 'ana'`) e intenta **fusionar** (*merge*): traer a tu rama lo que hay en `main`:

   ```bash
   git checkout ana
   git merge main
   ```

   Git responde algo como:

   ```text
   Auto-merging notas.md
   CONFLICT (content): Merge conflict in notas.md
   Automatic merge failed; fix conflicts and then commit the result.
   ```

4. **Antes de resolverlo, practica el aborto.** Mientras el conflicto no esté terminado, puedes volver al estado anterior:

   ```bash
   git merge --abort
   git status
   ```

   `git status` dice `nothing to commit, working tree clean`: tu rama vuelve a estar como antes del `merge`. Provoca el conflicto otra vez:

   ```bash
   git merge main
   ```

   Si ya hubieras terminado la unión, `git merge main` respondería `Already up to date` y no habría conflicto que provocar; por eso el aborto se practica **ahora**.

5. Abre `notas.md`. Verás las marcas del conflicto:

   ```text
   # Mis notas

   Línea uno
   <<<<<<< HEAD
   Línea de Ana
   =======
   Línea de Beto
   >>>>>>> main
   Línea tres
   Línea cuatro
   ```

   - `HEAD` es la rama en la que estás ahora (aquí, `ana`). Entre `<<<<<<< HEAD` y `=======` está **tu** versión.
   - Entre `=======` y `>>>>>>> main` está la que viene de `main`.

6. **Resuélvelo:** decide qué se queda. Deja el fichero así, con las dos líneas y **sin ninguna de las tres marcas**:

   ```text
   # Mis notas

   Línea uno
   Línea de Ana
   Línea de Beto
   Línea tres
   Línea cuatro
   ```

7. Termina la unión:

   ```bash
   git add notas.md
   git commit --no-edit
   ```

   `--no-edit` acepta el mensaje que Git ya ha preparado para la unión (*Merge branch 'main' into ana*), así no se abre ningún editor.

8. Mira el historial:

   ```bash
   git log --oneline --graph
   ```

   Verás cómo las dos ramas se unen en un commit de fusión.

**Y si te pierdes a medias,** `git merge --abort` te devuelve al estado anterior. Si lo ejecutas cuando **no** hay una unión en curso, Git responde `fatal: There is no merge to abort (MERGE_HEAD missing).`: significa que no hay nada que abortar.

**Autocomprobación:** `git status` dice `nothing to commit` y `notas.md` no contiene ninguna marca `<<<<<<<`, `=======` ni `>>>>>>>`.

## Ejercicio 4: deshacer errores sin miedo

**a) Prepaste un fichero que no querías.** Crea un fichero `borrador.md` cualquiera y haz:

```bash
git add borrador.md
git restore --staged borrador.md
git status
```

El fichero vuelve a *Untracked*, sin perder su contenido.

**b) Te equivocaste en el mensaje del último commit.** Mientras no lo hayas subido a ningún sitio. Para practicarlo, estando en la rama `ana`:

1. Añade una línea `Línea cinco` al final de `notas.md` y guarda.
2. Haz un commit con un mensaje deliberadamente malo (estando en la rama `ana`: comprueba con `git status`):

   ```bash
   git add notas.md
   git commit -m "cambios"
   ```

3. Corrige el mensaje:

   ```bash
   git commit --amend -m "docs: añadir la línea cinco"
   git log --oneline -2
   ```

   El commit de arriba pasa a tener el mensaje nuevo y sigue siendo uno solo.

**c) Hiciste un commit en `main` por error.** Es el error más típico. En tu práctica:

1. Vuelve a `main`:

   ```bash
   git checkout main
   ```

2. Añade una línea cualquiera al final de `notas.md`, guarda y haz el commit "equivocado":

   ```bash
   git add notas.md
   git commit -m "docs: commit por error"
   git log --oneline
   ```

   El commit equivocado aparece el primero de la lista.
3. **Guárdalo en una rama nueva y quita el commit de `main`:**

   ```bash
   git branch rescate
   git reset --hard HEAD~1
   ```

   `git branch rescate` crea la rama `rescate` apuntando a ese commit (no cambia de rama). `git reset --hard HEAD~1` hace que `main` vuelva **un commit atrás**.
4. Comprueba que `main` ya no tiene el commit y `rescate` sí:

   ```bash
   git log --oneline
   git log --oneline rescate
   ```

> En tu repositorio de práctica no hay GitHub, por eso el arreglo usa `HEAD~1` ("un commit atrás"). En el proyecto real, donde existe `origin`, el arreglo equivalente está en [errores frecuentes](06-errores-frecuentes.md#hice-commits-estando-en-main-por-error). Y recuerda: `git reset --hard` **descarta cambios sin guardar**; aquí es seguro porque tu commit ya está a salvo en `rescate`.

**Autocomprobación:** `git log --oneline` en `main` **no** muestra `docs: commit por error`, y `git log --oneline rescate` **sí** lo muestra. Además, `git log --oneline -2` en `ana` muestra el commit con el mensaje corregido `docs: añadir la línea cinco`.

## Qué has aprendido

- [ ] Crear commits y ramas.
- [ ] Ver diferencias con `git diff` y `git diff --staged`.
- [ ] Resolver un conflicto, y abortarlo si te pierdes.
- [ ] Deshacer los tres errores más típicos.

Cuando lo hayas hecho todo, estás listo para tu primera Issue real: [cómo trabajamos en este repositorio](09-como-trabajamos.md). Puedes borrar la carpeta `practica-git` cuando quieras: no forma parte del proyecto.

## Cómo se ha verificado

Esta práctica se ha ejecutado de principio a fin, siguiendo exactamente estos pasos, con **Git 2.53** en un repositorio de prueba (2026-11-18). Las salidas que se muestran son las reales. Si la tuya difiere en detalles (números de commit, mensajes en español), es normal; si difiere en lo importante, pregunta.

## Fuentes

- [Pro Git: guardando cambios en el repositorio](https://git-scm.com/book/es/v2/Fundamentos-de-Git-Guardando-cambios-en-el-Repositorio)
- [git merge (`--abort`, `--no-edit`)](https://git-scm.com/docs/git-merge)
