# 11. Más allá del tutorial

← [Anterior: Chuleta](07-chuleta.md) · [Índice](README.md)

Esta página es para cuando ya dominas el ciclo básico y quieres entender **por qué** se hace así y qué hay más allá. No es necesaria para aportar al proyecto.

## Conceptos que se confunden

### `pull` y `fetch`

- `git fetch` **trae** las novedades de GitHub a tu ordenador pero **no las mezcla** con tu trabajo: solo las descarga para que puedas mirarlas.
- `git pull` hace `fetch` y, además, **mezcla** lo traído con tu rama actual.

En este tutorial usamos `pull` porque es lo más sencillo. Quien quiere mirar antes de mezclar, usa `fetch`.

### La fusión local y la fusión del pull request

- Cuando haces `git merge main` en tu ordenador, estás trayendo lo nuevo de `main` **a tu rama** (para ponerla al día o resolver un conflicto).
- Cuando el profesor **fusiona el pull request** en GitHub, está llevando **tu rama a `main`**. Son direcciones opuestas.

### `checkout`, `switch` y `restore`

`git checkout` hace varias cosas distintas (cambiar de rama, crear una rama, restaurar ficheros). Por eso Git incorporó dos comandos más específicos:

- `git switch` para cambiar de rama (y `git switch -c nombre` para crearla).
- `git restore` para restaurar ficheros (`git restore --staged` quita un fichero de lo preparado).

El tutorial usa `checkout` porque funciona en todas las versiones y es el más extendido. Verás los otros en documentación moderna.

### `--global` y el ámbito de la configuración

`git config --global` guarda tu nombre y correo para **todos tus proyectos** en ese equipo. Sin `--global`, la configuración vale solo para el repositorio donde estás. Sirve, por ejemplo, para usar un correo distinto en un proyecto concreto.

## Por qué se hace así

### ¿Por qué una rama por Issue?

Porque aísla el trabajo: se revisa solo lo tuyo, se puede rehacer sin afectar a nadie y `main` siempre queda en estado bueno. Además, una rama por Issue deja el historial ordenado: cada rama cuenta una historia.

### ¿Por qué se actualiza `main` antes de ramificar?

Para que tu rama parta de la versión más reciente. Si partes de una antigua, al final tendrás que unir más cambios ajenos y habrá más conflictos.

### ¿Por qué `merge` y no `rebase`?

Ambos comandos integran cambios de una rama en otra:

- `merge` **une** las dos historias con un commit de unión. No reescribe nada: es seguro.
- `rebase` **recoloca** tus commits sobre la punta de la otra rama, dejando un historial lineal, pero **reescribe** esos commits.

Aquí usamos `merge` porque es más difícil estropear algo y porque nunca se debe reescribir historia ya compartida. `rebase` es habitual en equipos con más experiencia, usado con cuidado. Lo importante es saber que existe.

### ¿Por qué no se reescribe el historial compartido?

Los commits ya subidos son la **referencia común**: otros los tienen en su ordenador y construyen sobre ellos. Si los reescribes (con `push --force`, `reset` o `rebase`), la historia de cada uno deja de coincidir con la tuya y se rompe el trabajo ajeno. Además, aquí el historial es la prueba de tu aportación. Reescribir solo es razonable en tu **rama privada, antes de subirla** (por ejemplo, `git commit --amend`).

## Cuando algo ya está subido o se pierde

Estas herramientas sirven cuando el error ya no se arregla con un simple `--amend` o `git restore`. Cada comando se ha probado con Git 2.53 en un repositorio de prueba.

### `revert` frente a `reset`

Para deshacer un commit **que ya está subido y otros pueden haber descargado**, no se reescribe la historia: se añade un commit nuevo que lo contrarresta.

| | `git revert` | `git reset --hard` |
|---|---|---|
| Qué hace | Crea un commit nuevo que **deshace** el cambio de otro | **Mueve** la rama atrás y descarta commits |
| Historia | La conserva (queda el commit original y su reverso) | La reescribe |
| Seguro para commits ya subidos | **Sí** | **No** (exigiría `push --force`) |

```bash
git revert --no-edit HEAD
```

Responde algo como `[main c7fba53] Revert "docs: añadir línea mala"`. El commit malo sigue en el historial, y el contenido vuelve a ser el anterior. `--no-edit` acepta el mensaje que Git prepara.

### `reflog`: la red de seguridad

Git recuerda dónde ha estado tu `HEAD` (la punta de lo que tienes abierto). Si crees que has perdido un commit tras un `reset --hard`, mira el registro:

```bash
git reflog -4
```

Verás líneas como `90fc04c HEAD@{1}: commit: docs: trabajo valioso`. Para volver a ese punto:

```bash
git reset --hard "HEAD@{1}"
```

Responde `HEAD is now at 90fc04c docs: trabajo valioso`. Las comillas no son necesarias en Git Bash, pero **sí se recomiendan en PowerShell**, donde las llaves `{ }` tienen un significado propio. En ambos casos funcionan, así que úsalas siempre.

El `reflog` es **local** (solo de tu ordenador) y **caduca**: por defecto Git conserva sus entradas **90 días**, y **30 días** las de commits que ya no forman parte de ninguna rama (por ejemplo, los anteriores a un `--amend`). Úsalo pronto. ([Valores por defecto: `gc.reflogExpire` y `gc.reflogExpireUnreachable`](https://git-scm.com/docs/git-gc).)

### `stash`: guardar cambios a medias

Si tienes cambios sin terminar y necesitas cambiar de rama o hacer `pull`, puedes apartarlos:

```bash
git stash          # guarda tus cambios y deja la carpeta limpia
git stash list     # ver lo guardado
git stash pop      # recuperarlo y quitarlo de la lista
```

Por defecto `stash` guarda solo los ficheros que Git ya conocía; los ficheros nuevos sin rastrear requieren `git stash -u`.

### `--force-with-lease`: reescribir tu rama con red

Si reescribes un commit ya subido de **tu propia rama** (por ejemplo, con `git commit --amend`), un `git push` normal se rechaza con `(non-fast-forward)` (*sin avance directo*: tu rama ya no es una continuación directa de la de GitHub, porque has reescrito commits que ya estaban allí). La opción de siempre, `--force`, pisa lo que haya en GitHub. Una más segura es:

```bash
git push --force-with-lease
```

Solo sobrescribe si la rama de GitHub está **tal como tú la conoces**. Si otra persona ha subido algo mientras tanto, Git lo rechaza con `(stale info)` y no pierdes su trabajo.

**Un matiz importante:** `--force-with-lease` compara con tu copia local de la rama de GitHub (`origin/…`). Si **después de que otra persona subiera algo haces un `git fetch`** (o lo hace sin que lo notes un programa en segundo plano, como el auto-fetch de VS Code), esa copia se actualiza, la comprobación pasa y **tu push sobrescribe los commits de la otra persona sin que los hayas visto**. Lo he comprobado: en ese caso el comando responde `(forced update)` y el commit ajeno desaparece de la rama.

La opción `--force-if-includes` añade la comprobación que falta: solo permite el push si has **integrado** en tu rama lo que había en GitHub.

```bash
git push --force-with-lease --force-if-includes
```

Con ella, en el mismo caso Git rechaza el push. ([Documentación de `git push`: `--force-with-lease` y `--force-if-includes`](https://git-scm.com/docs/git-push).) Reglas:

- Solo en **tu rama propia**, nunca en `main`.
- Si ya tienes un pull request abierto, **avisa en el PR**: reescribir la rama puede descolocar los comentarios de la revisión.
- Ante la duda, no lo uses: haz un commit nuevo, que es siempre seguro.

### `git pull` con ramas divergentes

Si tu rama y la de GitHub han avanzado cada una por su lado, `git pull` se detiene con:

```text
hint: You have divergent branches and need to specify how to reconcile them.
fatal: Need to specify how to reconcile divergent branches.
```

Git te pide que elijas cómo integrarlas. La opción que usamos en este tutorial es **fusionar**:

```bash
git pull --no-rebase
```

Si hay conflicto, se resuelve como en la [práctica guiada](08-practica-guiada.md). Para no tener que repetirlo, puedes fijarlo para ese repositorio con `git config pull.rebase false`.

Documentación: [git revert](https://git-scm.com/docs/git-revert), [git reflog](https://git-scm.com/docs/git-reflog), [git stash](https://git-scm.com/docs/git-stash), [git push](https://git-scm.com/docs/git-push) y [git pull](https://git-scm.com/docs/git-pull).

## Fork o rama

- **Rama (lo que hacemos aquí):** trabajas en una rama del propio repositorio porque eres **colaborador** y tienes permiso de escritura.
- **Fork:** una copia del repositorio en tu propia cuenta. Se usa cuando **no** tienes permiso de escritura (por ejemplo, para contribuir a un proyecto ajeno). Haces los cambios en tu copia y propones el PR desde ella.

La documentación de GitHub indica que, para abrir un pull request, necesitas acceso de escritura a la rama de origen ([Creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)); sin él, el fork es el camino.

## Cómo se fusiona un pull request

GitHub ofrece varias formas de fusionar, y el profesor elige una:

| Forma | Qué hace con tus commits |
|---|---|
| **Merge commit** | Mantiene **todos** tus commits y añade un commit de unión. |
| **Squash** | Junta todos tus commits en **uno solo** en `main`. |
| **Rebase** | Coloca tus commits uno a uno sobre `main`, sin commit de unión. |

En este repositorio solo está activado el *squash* (comprobado en los ajustes el 2026-11-18). Importa para el historial: con *squash*, `main` muestra un único commit de tu trabajo (aunque tus commits siguen visibles dentro del pull request). Por eso Git no siempre reconoce tu rama como fusionada y `git branch -d` puede avisar o negarse a borrarla ([ver la revisión](05-la-revision.md#cuando-se-fusiona)).

## Buenas prácticas profesionales

- **Revisa tu propio trabajo antes de pedir revisión:** `git diff --staged` antes de cada commit, y la pestaña *Files changed* de tu PR antes de avisar.
- **PR pequeños y centrados**, con un propósito. Cuanto más pequeño, más rápido y mejor se revisa.
- **Borrador (*draft*)** si quieres enseñar algo sin terminar.
- **Autenticación en dos pasos (2FA)** en tu cuenta ([guía](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication)).
- **Correo privado (`noreply`)** en los repositorios públicos.
- **Commits atómicos:** cada commit hace una cosa y se puede entender solo.

## `.gitignore` y secretos

Un fichero llamado `.gitignore` en la raíz de un repositorio lista los ficheros y carpetas que Git **no debe rastrear ni subir** (por ejemplo, ficheros `.env` con claves). Si un secreto ya se subió, **añadirlo al `.gitignore` no lo borra del historial**. La respuesta correcta es siempre:

1. Avisar al responsable del repositorio.
2. **Revocar y cambiar** la clave en el servicio que la emitió.
3. Dejar que el responsable decida cómo limpiar el historial.

Para empezar bien: no guardes claves en ficheros del proyecto; usa variables de entorno o ficheros ignorados.

## Para seguir aprendiendo

- [Pro Git (en español)](https://git-scm.com/book/es/v2): el libro de referencia, gratuito.
- [Documentación de Git](https://git-scm.com/docs): todos los comandos, con sus opciones.
- [Documentación de GitHub](https://docs.github.com): Issues, pull requests, ramas protegidas y más.
- [Documentación de VS Code: control de código fuente](https://code.visualstudio.com/docs/sourcecontrol/overview).
- [Conventional Commits](https://www.conventionalcommits.org/es/): el formato de los mensajes.
