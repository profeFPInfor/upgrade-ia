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

Importa para el historial: con *squash*, `main` muestra un único commit de tu trabajo (aunque tus commits siguen visibles dentro del pull request). Por eso `git branch -d` puede negarse a borrar tu rama tras fusionarse ([ver la revisión](05-la-revision.md#cuando-se-fusiona)).

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
