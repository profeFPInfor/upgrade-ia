# Glosario

Las palabras que usamos en este proyecto, explicadas de forma sencilla. Están agrupadas por tema y, dentro de cada tema, por orden alfabético.

> ¿Falta una palabra? Propónla en una Issue o añádela en tu pull request, con el mismo formato.

**Índice:** [Git y GitHub](#git-y-github) · [Qué hacer si te pasa](#qué-hacer-si-te-pasa) · [Proceso de desarrollo](#proceso-de-desarrollo-multiplataforma) · [IA y herramientas](#ia-y-herramientas) · [Documentación](#documentación)

## Antes de empezar

No necesitas saber nada previo. Si es tu primera vez con Git y GitHub, empieza por el [tutorial de trabajo colaborativo](trabajoColaborativo/README.md): este glosario te acompaña mientras lo sigues.

- **Busca la palabra** en el tema que corresponda. Si una definición usa otra palabra que no conoces, búscala también.
- En la tabla de **Git y GitHub**, la tercera columna te dice **qué comando usar o qué página del tutorial lo explica**.
- Los comandos se escriben en una **terminal** (mira la entrada *Terminal*).
- Para profundizar: [Pro Git, el libro oficial y gratuito, en español](https://git-scm.com/book/es/v2).

## Git y GitHub

| Término | Qué significa | Cómo se usa o dónde se explica |
|---|---|---|
| **Aprobar (approve)** | Dar el visto bueno a un *pull request* (una petición para unir una rama con `main`). Aquí solo lo hace el profesor. | [La revisión](trabajoColaborativo/05-la-revision.md) |
| **Asignado (assignee)** | Persona que se ha encargado de una Issue o de un pull request. | [Issues y etiquetas](trabajoColaborativo/10-issues-y-etiquetas.md) |
| **Cambiar de rama (checkout, switch)** | Moverte de una rama a otra en tu ordenador. | `git checkout rama` o `git switch rama`. Para crear una nueva y entrar: `git checkout -b rama` o `git switch -c rama` |
| **Clonar (clone)** | Descargar a tu ordenador una copia completa de un repositorio, con su historia. | `git clone <dirección>`. [Carpeta de trabajo](trabajoColaborativo/03-primer-dia.md) |
| **Code owner** | Persona responsable de revisar los cambios de ciertos ficheros. En este repo, el profesor. | [La revisión](trabajoColaborativo/05-la-revision.md) |
| **Commit** | Una "foto" (copia guardada) de tus cambios, con un mensaje que explica qué hiciste. | `git commit -m "docs: mensaje"` |
| **Commit hash** | Código corto y único que identifica un commit (por ejemplo, `a53416f`). | `git log --oneline` los muestra |
| **Conflicto** | Situación en la que dos personas cambiaron las mismas líneas y Git no sabe cuál conservar. Se resuelve a mano. | [Qué hacer si te pasa](#qué-hacer-si-te-pasa). Practícalo en la [práctica guiada](trabajoColaborativo/08-practica-guiada.md) |
| **Conventional Commits** | Forma de escribir mensajes de commit: un tipo, dos puntos y una frase (`docs: añadir glosario`). | [Tipos de commit](trabajoColaborativo/04-una-aportacion-completa.md#6-preparar-y-hacer-commit) |
| **Diff (diferencias)** | Lo que cambia entre dos versiones: líneas quitadas (`-`) y líneas añadidas (`+`). | `git diff` (sin preparar) y `git diff --staged` (preparado) |
| **Directorio de trabajo** | La carpeta de tu ordenador donde ves y editas los ficheros del proyecto. | `git status` muestra su estado |
| **Etiqueta (label)** | Marca con nombre y color que clasifica una Issue o un pull request (por ejemplo `docs`). | [Issues y etiquetas](trabajoColaborativo/10-issues-y-etiquetas.md) |
| **Fork** | Copia de un repositorio ajeno en tu propia cuenta de GitHub. Aquí no hace falta, porque eres colaborador y trabajas con ramas del propio repositorio. | [Fork o rama](trabajoColaborativo/11-mas-alla.md#fork-o-rama) |
| **Fusionar (merge)** | Unir los cambios de una rama con otra. | `git merge main` trae lo de `main` a tu rama |
| **Git** | Programa que guarda la historia de los cambios de un proyecto. Funciona en tu ordenador. | `git --version` comprueba que está instalado |
| **GitHub** | Web que aloja repositorios de Git y ayuda a colaborar (Issues, pull requests). | [github.com](https://github.com) |
| **`.gitignore`** | Fichero que lista lo que Git no debe rastrear ni subir (por ejemplo, ficheros con claves). | [`.gitignore` y secretos](trabajoColaborativo/11-mas-alla.md#gitignore-y-secretos) |
| **HEAD** | La rama (o commit) en la que estás ahora mismo. En un conflicto al hacer `git merge`, `HEAD` es **tu** versión, la de tu rama. | Aparece en las marcas de un conflicto y en `git reflog` |
| **HTTPS y SSH** | Dos formas de conectar tu ordenador con GitHub. Este tutorial usa HTTPS. | [Acceso desde tu ordenador](trabajoColaborativo/02-preparar-el-equipo.md#25-acceso-desde-tu-ordenador) |
| **Issue** | Tarea o propuesta de trabajo, con su conversación. En este repo las propone el profesor. | [Issues y etiquetas](trabajoColaborativo/10-issues-y-etiquetas.md) |
| **`main`** | Rama principal del repositorio: la versión buena. Está protegida y no se edita directamente. | `git checkout main` |
| **Non-fast-forward** | Mensaje de Git al subir cuando la rama de GitHub tiene commits que tu rama no tiene (o has reescrito commits ya subidos). Git rechaza el `push` para no perder trabajo. | [Qué hacer si te pasa](#qué-hacer-si-te-pasa) |
| **Origin** | Nombre con el que Git recuerda el repositorio de GitHub del que clonaste. | `git remote -v` |
| **Pull** | Traer a tu ordenador lo nuevo que hay en GitHub y mezclarlo con tu rama. | `git pull` |
| **Pull request (PR)** | Petición para unir tu rama con `main`. Es donde se revisa tu trabajo. | [Cómo trabajamos](trabajoColaborativo/09-como-trabajamos.md#6-abre-el-pull-request) |
| **Push** | Enviar tus commits a GitHub. | `git push -u origin rama` la primera vez; después, `git push` |
| **Rama (branch)** | Línea de trabajo paralela. Trabajas en ella sin tocar `main`. | `git branch` lista las ramas |
| **Rama protegida** | Rama con reglas que impiden subir cambios directamente: todo entra por pull request. | Si te rechaza el push a `main`: [errores frecuentes](trabajoColaborativo/06-errores-frecuentes.md#me-rechaza-el-push-a-main) |
| **Rebase** | Otra forma de integrar cambios: recoloca tus commits sobre la punta de otra rama y los reescribe. Aquí usamos `merge`. | [¿Por qué `merge` y no `rebase`?](trabajoColaborativo/11-mas-alla.md#por-qué-merge-y-no-rebase) |
| **Reflog** | Registro local de los sitios donde ha estado tu `HEAD`. Sirve para recuperar commits que parecen perdidos. | `git reflog`. [Más allá](trabajoColaborativo/11-mas-alla.md#reflog-la-red-de-seguridad) |
| **Remoto** | La copia del repositorio que está en GitHub (en contraste con la local, en tu ordenador). | `git remote -v` |
| **Repositorio** | La carpeta de un proyecto con toda su historia de cambios. | `git clone` lo descarga |
| **Revert** | Crear un commit nuevo que deshace otro ya publicado, sin reescribir la historia. | `git revert --no-edit <hash>`. [Más allá](trabajoColaborativo/11-mas-alla.md#revert-frente-a-reset) |
| **Revisión (review)** | Lectura de un pull request por otra persona, que comenta, pide cambios o aprueba. | [La revisión](trabajoColaborativo/05-la-revision.md) |
| **Squash** | Forma de fusionar un pull request que junta todos tus commits en uno solo en `main`. En este repositorio es la única activada (comprobado el 2026-11-18). | [Cómo se fusiona un PR](trabajoColaborativo/11-mas-alla.md#cómo-se-fusiona-un-pull-request) |
| **Staging (preparado)** | Zona intermedia donde dejas los cambios que irán en el próximo commit. | `git add fichero`; para quitarlo, `git restore --staged fichero` |
| **Stash** | Apartar temporalmente cambios sin terminar para dejar la carpeta limpia y recuperarlos después. | `git stash` y `git stash pop` |
| **Terminal** | Ventana donde escribes comandos. En VS Code, la terminal integrada. | Menú *Terminal → New Terminal* |
| **Token (de acceso)** | Clave que identifica tu cuenta ante GitHub cuando subes cambios. **No se comparte ni se sube nunca.** No es lo mismo que el token de un modelo de IA (ver más abajo). | [Acceso desde tu ordenador](trabajoColaborativo/02-preparar-el-equipo.md#25-acceso-desde-tu-ordenador) |
| **Upstream (rama de seguimiento)** | La rama de GitHub con la que está enlazada tu rama local. | Se enlaza con `git push -u origin rama` |

## Qué hacer si te pasa

Las tres situaciones que más desconciertan a quien empieza, con el aspecto que tienen.

### Conflicto

Git lo avisa al hacer `git merge main` o `git pull`:

```text
CONFLICT (content): Merge conflict in notas.md
Automatic merge failed; fix conflicts and then commit the result.
```

Al abrir el fichero verás las dos versiones separadas por marcas:

```text
<<<<<<< HEAD
Línea de Ana
=======
Línea de Beto
>>>>>>> main
```

Entre `<<<<<<< HEAD` y `=======` está **tu** versión; entre `=======` y `>>>>>>> main`, la otra. **Qué hacer:** decide qué texto se queda, borra las tres líneas de marcas, guarda, y termina con `git add fichero` y `git commit --no-edit`. Si te pierdes, `git merge --abort` vuelve al estado anterior. Paso a paso: [errores frecuentes](trabajoColaborativo/06-errores-frecuentes.md#mi-rama-está-desactualizada-o-hay-conflictos).

### Non-fast-forward (push rechazado)

Al hacer `git push`:

```text
 ! [rejected]        docs/20-x -> docs/20-x (non-fast-forward)
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.
```

Significa que en GitHub hay commits que tu rama no tiene. **Qué hacer:** `git pull` (trae lo que falta; si hay conflicto, resuélvelo como arriba) y después vuelve a hacer `git push`. No uses `--force` para "arreglarlo": pisarías el trabajo de otra persona.

### Un commit que parece perdido

Tras un `git reset --hard`, el commit ya no aparece en `git log`, pero sigue registrado. **Qué hacer:** `git reflog` lista dónde ha estado tu `HEAD`:

```text
90fc04c HEAD@{1}: commit: docs: trabajo valioso
```

Con el código de esa línea puedes volver: `git reset --hard "HEAD@{1}"`. Detalle en [Más allá](trabajoColaborativo/11-mas-alla.md#reflog-la-red-de-seguridad).

## Proceso de desarrollo multiplataforma

| Término | Qué significa |
|---|---|
| **ADR** | *Architecture Decision Record.* Documento corto que registra una decisión de arquitectura y por qué se tomó. |
| **Alcance** | Qué entra y qué no entra en el proyecto. |
| **API** | Forma en que dos programas se comunican: define qué se puede pedir y qué se recibe. |
| **Aplicación multiplataforma** | Aplicación que funciona en varios sistemas (por ejemplo Android, iOS, Windows, web) a partir de un código común o compartido. |
| **Arquitectura** | La organización general del código y sus partes. Por ejemplo, por capas: **presentación** (lo que ve el usuario), **dominio** (las reglas de la aplicación) y **datos** (dónde se guarda la información). |
| **Benchmark (análisis comparativo)** | Comparar alternativas con los mismos criterios para elegir con fundamento. |
| **CI/CD** | Integración y entrega continuas: automatizar las pruebas y la publicación cada vez que cambia el código. |
| **Criterio de aceptación** | Condición concreta que debe cumplirse para dar por terminada una tarea. |
| **Despliegue** | Poner la aplicación a disposición de los usuarios. |
| **Enfoque nativo** | Una aplicación escrita específicamente para una plataforma, con sus herramientas propias. |
| **Framework** | Conjunto de herramientas y reglas que facilita construir un tipo de aplicación. |
| **Go / no-go** | Decisión de seguir adelante con un proyecto o no, razonada con criterios (coste, plazo, riesgos, licencias). |
| **Historia de usuario** | Descripción breve de una necesidad desde el punto de vista de quien usa la aplicación. |
| **Licencia** | Condiciones con las que se permite usar, copiar y modificar un software o un contenido. Este repo usa MIT. |
| **MVC / MVVM** | Patrones (formas de organizar el código) que separan la interfaz, los datos y la lógica de una aplicación. MVC es *Modelo-Vista-Controlador* y MVVM, *Modelo-Vista-VistaModelo*. |
| **Prueba (test)** | Comprobación de que una parte de la aplicación hace lo que debe. Pueden ser unitarias, de integración o de interfaz. |
| **PWA** | *Progressive Web App.* Web que se puede instalar y usar como una aplicación. |
| **Requisito** | Lo que la aplicación debe hacer (funcional) o cómo debe comportarse (no funcional: rendimiento, seguridad…). |
| **Riesgo** | Algo que puede salir mal, con su probabilidad y su impacto. |
| **SOTA (estado del arte)** | *State of the art.* Lo que ya existe y se sabe hoy sobre un problema: soluciones, tecnologías y sus límites. |
| **Supuesto** | Algo que damos por cierto sin haberlo comprobado. Conviene anotarlo, porque puede fallar. |
| **UML** | Lenguaje de diagramas para describir el diseño de un sistema. |
| **Viabilidad** | Si el proyecto se puede hacer en lo técnico, lo económico y lo legal. |

## IA y herramientas

| Término | Qué significa |
|---|---|
| **Agente** | Programa de IA que, además de responder, puede actuar: leer ficheros, ejecutar comandos y encadenar pasos hasta cumplir una tarea. |
| **Alucinación** | Cuando un modelo de IA inventa algo (un dato, una cita, un comando) y lo presenta como cierto. Por eso **todo se verifica**. |
| **Antigravity** | Entorno de desarrollo (IDE) con asistencia de IA, que se estudia en el tema de IDEs. *(Se ampliará en su tema.)* |
| **Contexto** | La información que el modelo tiene delante al responder: tu mensaje, los ficheros y la conversación. Es limitado. |
| **Cuota gratuita** | Límite de uso que un servicio permite sin pagar. Se agota y varía con el tiempo, así que hay que comprobarla. |
| **Harness** | Todo lo que rodea al modelo para que trabaje como agente: herramientas, reglas, memoria y el bucle que lo ejecuta. *(Se ampliará en su tema.)* |
| **IDE** | Entorno de desarrollo: el programa donde escribes, ejecutas y depuras código. |
| **LLM** | *Large Language Model.* Modelo de IA entrenado con mucho texto, capaz de escribir, resumir y generar código. |
| **MCP** | *Model Context Protocol.* Protocolo abierto para conectar a un modelo de IA con herramientas y fuentes de datos externas. |
| **OpenCode** | Agente de programación de código abierto, con interfaz de terminal, escritorio y web. Es la herramienta del taller. Ver [herramientas-ia/opencode](../herramientas-ia/opencode/). |
| **OpenRouter** | Servicio que da acceso a muchos modelos de IA con una sola cuenta, algunos gratuitos. *(Se ampliará en su tema.)* |
| **Plugin** | Extensión que añade funciones a una herramienta. |
| **Prompt** | El texto que le das a un modelo de IA para pedirle algo. Cuanto más claro y con más contexto, mejor respuesta. |
| **Proveedor** | Empresa o servicio que ofrece los modelos de IA (y su acceso). |
| **Reflection** | Técnica en la que el modelo revisa y critica su propia respuesta para mejorarla. *(Se ampliará en su tema.)* |
| **Skill** | Paquete de instrucciones reutilizables que un agente carga cuando las necesita para una tarea concreta. *(Se ampliará en su tema.)* |
| **Token (de un modelo)** | Trozo de texto (una palabra o parte de ella) que el modelo procesa. Los límites y los costes se miden en tokens. No es lo mismo que el token de acceso de GitHub. |

## Documentación

| Término | Qué significa |
|---|---|
| **Changelog** | Registro ordenado de los cambios de un proyecto entre versiones. |
| **Enlace relativo** | Enlace a otro fichero del repo por su ruta (`../glosario.md`), que sigue funcionando aunque el repo se mueva. |
| **Fuente primaria** | Origen original de una información: la documentación oficial, la norma o el autor, no un resumen de un tercero. |
| **Markdown** | Lenguaje sencillo para escribir texto con formato (títulos, listas, enlaces) en ficheros `.md`. Ver el [curso de Markdown](../markdown/). |
| **Mermaid** | Forma de dibujar diagramas escribiendo texto, que GitHub muestra como imagen. |
| **README** | Fichero de presentación de un repositorio o de una carpeta: qué es y cómo orientarse. |
