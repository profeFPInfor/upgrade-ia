# 8. Práctica guiada sin riesgo

← [Anterior: Carpeta de trabajo](03-primer-dia.md) · [Índice](README.md) · [Siguiente: Cómo trabajamos en este repositorio](09-como-trabajamos.md) →

Aquí practicas el ciclo de Git **en tu ordenador, sin tocar el repositorio del proyecto**. Nada de lo que hagas se sube a ningún sitio, así que puedes equivocarte y repetir. Es el mejor entrenamiento antes de tu primera Issue real.

> **Haz esta práctica antes de coger tu primera Issue.** Necesitas haber completado el [paso 2](02-preparar-el-equipo.md).

Tiempo aproximado: 30 minutos. Consejo: hazla en la terminal integrada de VS Code.

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

   Debe mostrar algo como `1 file changed, 3 insertions(+)`.
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
2. En VS Code, cambia la línea 3 de `notas.md` para que diga `Línea de Ana` y guarda.
3. Mira qué ha cambiado, con el cambio sin preparar y luego preparado:

   ```bash
   git diff
   git add notas.md
   git diff --staged
   ```

   `git diff` muestra lo que has cambiado y aún no has preparado; `git diff --staged` muestra lo que ya está preparado para el commit. Revisar `--staged` antes de cada commit es un buen hábito.
4. Haz el commit:

   ```bash
   git commit -m "docs: cambiar la línea tres"
   ```

**Autocomprobación:** `git log --oneline` muestra dos commits y `git status` indica `On branch ana`.

## Ejercicio 3: provocar y resolver un conflicto

Un **conflicto** ocurre cuando dos ramas cambian las mismas líneas. Es normal, y mejor aprender a resolverlo aquí.

1. Vuelve a `main`:

   ```bash
   git checkout main
   ```

2. En VS Code, cambia **la misma línea 3** de `notas.md` a `Línea de Beto` y guarda. Haz commit:

   ```bash
   git add notas.md
   git commit -m "docs: cambiar la línea tres desde main"
   ```

3. Vuelve a tu rama e intenta traer lo de `main`:

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

4. Abre `notas.md`. Verás las marcas del conflicto:

   ```text
   # Mis notas

   Línea uno
   <<<<<<< HEAD
   Línea de Ana
   =======
   Línea de Beto
   >>>>>>> main
   Línea dos
   ```

   - Entre `<<<<<<< HEAD` y `=======` está **tu** versión.
   - Entre `=======` y `>>>>>>> main` está la que viene de `main`.

5. **Resuélvelo:** decide qué se queda. Deja el fichero así, con las dos líneas y **sin ninguna de las tres marcas**:

   ```text
   # Mis notas

   Línea uno
   Línea de Ana
   Línea de Beto
   Línea dos
   ```

6. Termina la unión:

   ```bash
   git add notas.md
   git commit --no-edit
   ```

   `--no-edit` acepta el mensaje que Git ya ha preparado para la unión (*Merge branch 'main' into ana*), así no se abre ningún editor.

7. Mira el historial:

   ```bash
   git log --oneline --graph
   ```

   Verás cómo las dos ramas se unen en un commit de fusión.

**Y si te pierdes a medias:** mientras el conflicto no esté terminado, puedes volver al estado anterior con `git merge --abort`. Prueba a provocar el conflicto otra vez y abortarlo.

**Autocomprobación:** `git status` dice `nothing to commit` y `notas.md` no contiene ninguna marca `<<<<<<<`, `=======` ni `>>>>>>>`.

## Ejercicio 4: deshacer errores sin miedo

**a) Prepaste un fichero que no querías.** Crea un fichero `borrador.md` cualquiera y haz:

```bash
git add borrador.md
git restore --staged borrador.md
git status
```

El fichero vuelve a *Untracked*, sin perder su contenido.

**b) Te equivocaste en el mensaje del último commit.** Mientras no lo hayas subido a ningún sitio:

```bash
git commit --amend -m "docs: mensaje corregido"
```

**c) Hiciste un commit en `main` por error.** Es el error más típico. En tu práctica:

1. Vuelve a `main` y haz un cambio y un commit "equivocado".
2. Rescátalo como describe la [página de errores](06-errores-frecuentes.md#hice-commits-estando-en-main-por-error).

**Autocomprobación:** sabes explicar con tus palabras qué hace cada uno de los tres arreglos.

## Qué has aprendido

- [ ] Crear commits y ramas.
- [ ] Ver diferencias con `git diff` y `git diff --staged`.
- [ ] Resolver un conflicto, y abortarlo si te pierdes.
- [ ] Deshacer los tres errores más típicos.

Cuando lo hayas hecho todo, estás listo para tu primera Issue real: [cómo trabajamos en este repositorio](09-como-trabajamos.md). Puedes borrar la carpeta `practica-git` cuando quieras: no forma parte del proyecto.

## Fuentes

- [Pro Git: guardando cambios en el repositorio](https://git-scm.com/book/es/v2/Fundamentos-de-Git-Guardando-cambios-en-el-Repositorio)
- [git merge (`--abort`, `--no-edit`)](https://git-scm.com/docs/git-merge)
