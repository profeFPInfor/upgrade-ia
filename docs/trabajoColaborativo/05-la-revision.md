# 5. La revisión

← [Anterior: Una aportación completa](04-una-aportacion-completa.md) · [Siguiente: Errores frecuentes](06-errores-frecuentes.md) →

Cuando abres un pull request, el profesor lo revisa. **Que te pida cambios es lo normal**, no es una nota negativa: es así como se trabaja en cualquier equipo.

La rama `main` exige que un pull request tenga una aprobación del responsable del código (el profesor) antes de poder fusionarse. Por eso nada entra sin revisión ([documentación](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)).

## Qué puede pasar

| Resultado | Qué significa | Qué haces |
|---|---|---|
| **Comentarios** | Preguntas o sugerencias en líneas concretas | Respóndelas o aplícalas |
| **Changes requested** | Hay que cambiar algo antes de fusionar | Haz los cambios y súbelos |
| **Approved** | El profesor lo aprueba | Espera a que lo fusione |
| **Merged** | Tu rama se ha unido a `main` | Limpia y empieza la siguiente |

## Responder a una petición de cambios

1. Lee los comentarios en la pestaña *Conversation* o *Files changed*.
2. En tu ordenador, estando en tu rama, haz los cambios.
3. Prepara, haz commit y sube **a la misma rama**:

   ```bash
   git add proceso/01-analisis/mi-aportacion.md
   git commit -m "docs: aplicar los comentarios de la revisión"
   git push
   ```

   `git push` responde con una lista de lo que sube y la línea `docs/12-analisis-sota -> docs/12-analisis-sota`.
4. **No abras un PR nuevo:** el que ya existe se actualiza solo con tus commits nuevos.
5. Contesta en GitHub a cada comentario (por ejemplo, "hecho") para que el profesor sepa que lo has visto.

## Si `main` ha avanzado mientras tanto

Mientras tu PR esperaba, otros PR pueden haberse fusionado. Si GitHub avisa de que tu rama tiene **conflictos** con `main`, o simplemente quieres ponerla al día, trae lo nuevo a tu rama y resuelve lo que haga falta. El paso a paso, con ejemplo, está en [Mi rama está desactualizada o hay conflictos](06-errores-frecuentes.md#mi-rama-está-desactualizada-o-hay-conflictos). Si lo practicaste en la [práctica guiada](08-practica-guiada.md#ejercicio-3-provocar-y-resolver-un-conflicto), ya sabes hacerlo.

## Cuando se fusiona

Cuando el profesor fusiona tu PR, tu aportación ya está en `main`. Limpia tu ordenador:

```bash
git checkout main
git pull
git branch -d docs/12-analisis-sota
```

`-d` (minúscula) borra la rama **solo si está totalmente fusionada**; es la opción segura. Si Git se niega con un mensaje como `error: the branch '…' is not fully merged`, es porque el PR se fusionó de una forma que Git no reconoce como "fusionada" (por ejemplo, si el profesor aplasta tus commits en uno solo). En ese caso, y **solo cuando tu PR ya esté fusionado**, usa `-D` (mayúscula), que borra la rama sin comprobar nada.

Documentación: [git branch](https://git-scm.com/docs/git-branch).

Y ya puedes empezar con la siguiente Issue desde el paso 1.

## Cómo recibir bien una revisión

- Los comentarios son sobre el **trabajo**, no sobre ti.
- Si no entiendes un comentario, **pregunta**.
- Si no estás de acuerdo, explícalo con razones: la conversación es parte del aprendizaje.

## Comprobación

- [ ] Sabes qué hacer si te piden cambios.
- [ ] Sabes que los cambios se suben a la misma rama y que el PR se actualiza solo.
- [ ] Sabes qué hacer si `main` avanza mientras esperas.
- [ ] Sabes cómo limpiar tu ordenador cuando se fusiona, y cuándo usar `-d` y cuándo `-D`.

Siguiente: [errores frecuentes](06-errores-frecuentes.md).
