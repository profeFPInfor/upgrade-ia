# 6. Errores frecuentes

← [Anterior: La revisión](05-la-revision.md) · [Siguiente: Chuleta de comandos](07-chuleta.md) →

Todo el mundo se equivoca con Git al principio. Casi todo tiene arreglo. Antes de tocar nada, ejecuta **`git status`** y lee lo que dice. Muchos de estos arreglos los puedes practicar sin riesgo en la [práctica guiada](08-practica-guiada.md).

> Regla de oro: **si no estás seguro, no borres nada y pregunta.** Pega el texto del error en un mensaje al profesor.

## No puedo clonar o subir: error de permisos o de autenticación

Textos típicos: `Permission denied`, `403`, `Authentication failed`, `repository not found`.

Causas más probables:

1. **No has aceptado la invitación** al repositorio (paso [2.2](02-preparar-el-equipo.md#22-aceptar-la-invitación-al-repositorio)).
2. **No has hecho el acceso** (paso [2.5](02-preparar-el-equipo.md#25-acceso-desde-tu-ordenador)). Recuerda que la contraseña de la cuenta no vale.
3. Has iniciado sesión con **otra cuenta** de GitHub. Comprueba con `gh auth status`.

## Me rechaza el push a `main`

Texto típico: `remote: error: GH006: Protected branch update failed`.

`main` está protegida a propósito. Crea una rama y sube esa (ver [pasos 3 y 7](04-una-aportacion-completa.md#3-crear-tu-rama)).

## Git dice `nothing to commit`

Significa que no hay nada preparado ni modificado. Causas típicas: no guardaste el fichero en VS Code, editaste otra carpeta, o ya hiciste el commit. Ejecuta `git status` y mira la carpeta que tienes abierta.

## Git dice `Author identity unknown`

Texto típico, al hacer `git commit`:

```text
Author identity unknown

*** Please tell me who you are.
```

Git no sabe quién eres, porque no has configurado tu nombre y tu correo. Se arregla una sola vez, con tus datos y tu correo `noreply` (paso [2.4](02-preparar-el-equipo.md#24-decirle-a-git-quién-eres)):

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo-noreply"
```

Después repite el `git commit`.

## `git pull` se queja de mis cambios locales

Si tienes cambios sin guardar en un fichero que también cambió en GitHub, Git se niega a sobrescribirlos y te lo dice (un mensaje que habla de *local changes would be overwritten*). **No pasa nada.** Mira primero en qué rama estás con `git status`:

- **En tu rama de trabajo:** haz commit de tus cambios (`git add` y `git commit`) y vuelve a hacer `git pull`.
- **En `main`:** **no hagas commit en `main`**. No deberías estar editando ahí; pregunta al profesor antes de tocar nada, para no perder tus cambios.

Si no quieres conservar esos cambios, pregunta antes de descartarlos.

## Hice commits estando en `main` por error

Si **aún no has hecho `git push`**, se arregla así. Comprueba antes con `git status` que no tienes cambios sin guardar.

```bash
git checkout -b docs/mi-rama     # tus commits se quedan en esta rama nueva
git checkout main
git reset --hard origin/main     # main vuelve a ser igual que GitHub
git checkout docs/mi-rama
```

> **Cuidado con `git reset --hard`:** deshace **sin avisar** todos los cambios que no estén guardados en un commit, y no se pueden recuperar. Úsalo solo si estás seguro de que lo que quieres conservar ya está en un commit (los de la rama nueva lo están). Si dudas, pregunta antes.

Puedes ensayarlo en la [práctica guiada](08-practica-guiada.md#ejercicio-4-deshacer-errores-sin-miedo).

## Se abre un editor raro al hacer commit

Si haces `git commit` sin `-m`, Git abre un editor (muchas veces *vim*) para escribir el mensaje. Si te quedas atrapado:

1. Pulsa `Esc`.
2. Escribe `:q!` y pulsa `Enter`. Sales sin hacer el commit.
3. Repite el commit con `git commit -m "docs: tu mensaje"`.

> **Excepción importante:** si estás terminando la unión de un conflicto, el editor ya trae un mensaje preparado. **No uses `:q!`**, porque cancelarías la unión. En ese caso haz el commit con `git commit --no-edit` (ver más abajo) y no se abrirá ningún editor.

## Añadí un fichero que no quería

Si has hecho `git add` de algo que no querías y **aún no has hecho commit**:

```bash
git restore --staged nombre-del-fichero
```

El fichero vuelve a *sin preparar* y sus cambios se conservan.

## Me equivoqué en el mensaje del último commit

Si **aún no has hecho push**:

```bash
git commit --amend -m "docs: mensaje corregido"
```

Si ya has subido el commit, deja el mensaje como está y sigue; no se reescribe la historia compartida.

## Mi rama está desactualizada o hay conflictos

Mientras trabajabas, `main` ha avanzado. Para traer lo nuevo a tu rama:

```bash
git checkout main
git pull
git checkout docs/12-analisis-sota
git merge main
```

Si no se tocan las mismas líneas, Git lo une solo. Si sí, hay un **conflicto**, y Git responde algo como:

```text
Auto-merging proceso/01-analisis/mi-aportacion.md
CONFLICT (content): Merge conflict in proceso/01-analisis/mi-aportacion.md
Automatic merge failed; fix conflicts and then commit the result.
```

Abre el fichero marcado. Verás las dos versiones separadas por marcas. Por ejemplo, un fichero así **antes** de resolverlo:

```text
# Mi aportación

Línea uno
<<<<<<< HEAD
Texto que escribí yo
=======
Texto que llegó de main
>>>>>>> main
Línea final
```

Entre `<<<<<<< HEAD` y `=======` está **tu** versión; entre `=======` y `>>>>>>> main`, la que viene de `main`. Decide qué texto se queda (el tuyo, el otro o una mezcla) y **borra las tres líneas de marcas**. Por ejemplo, **después** de resolverlo:

```text
# Mi aportación

Línea uno
Texto que escribí yo, ajustado con lo que llegó de main
Línea final
```

Guarda el fichero y termina la unión:

```bash
git add proceso/01-analisis/mi-aportacion.md
git commit --no-edit
git push
```

`--no-edit` acepta el mensaje que Git ya ha preparado para la unión (*Merge branch 'main' into …*), así no se abre ningún editor.

**Si te pierdes a medias,** antes de terminar la unión puedes volver al estado anterior con `git merge --abort`. No pierdes tu trabajo ya guardado en commits. Si lo ejecutas cuando no hay ninguna unión en curso, Git responde `fatal: There is no merge to abort (MERGE_HEAD missing).`: no hay nada que abortar.

Si no sabes qué versión conservar, **pregunta**: no elijas al azar.

Documentación: [git merge](https://git-scm.com/docs/git-merge). Practícalo en la [práctica guiada](08-practica-guiada.md#ejercicio-3-provocar-y-resolver-un-conflicto).

## Mi PR muestra que borro muchos ficheros que no toqué

Es una señal de que tu rama **no parte del `main` actual** (por ejemplo, la creaste en otro repositorio o con otro historial). Se arregla creando una rama nueva desde `main` y llevándote solo tu fichero:

1. Copia tu fichero a una carpeta **fuera** del repositorio.
2. Actualiza `main` y crea la rama nueva:

   ```bash
   git checkout main
   git pull
   git checkout -b docs/12-analisis-sota-v2
   ```

3. Copia tu fichero de vuelta a la carpeta correcta, y haz `git add`, `git commit` y `git push -u origin docs/12-analisis-sota-v2`.
4. Abre un PR nuevo y cierra el anterior, avisando al profesor.

## Subí una clave o un dato personal sin querer

1. **Avisa al profesor inmediatamente.**
2. **Revoca la clave** en el servicio que la emitió (OpenRouter, GitHub…) y crea otra. Borrar el fichero en un commit nuevo **no basta**: la clave sigue en el historial y el repositorio es público.
3. **No intentes limpiar el historial tú solo.** Reescribir el historial de un repositorio compartido es delicado; lo decide y lo hace el profesor.
4. Para que no vuelva a pasar, guarda los secretos en **variables de entorno** o en ficheros que Git ignora (lista de ficheros que Git no sube, el `.gitignore`; ver [Más allá](11-mas-alla.md#gitignore-y-secretos)).

## Comprobación

- [ ] Sabes qué hacer si te rechazan el push a `main`.
- [ ] Sabes salir del editor de commit, y cuándo no usar `:q!`.
- [ ] Sabes resolver un conflicto y abortarlo si te pierdes.
- [ ] Sabes que, ante una clave subida por error, lo primero es avisar y revocarla.

Siguiente: [chuleta de comandos](07-chuleta.md).
