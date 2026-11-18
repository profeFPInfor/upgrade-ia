# 7. Chuleta de comandos

← [Anterior: Errores frecuentes](06-errores-frecuentes.md) · [Índice](README.md) · [Siguiente: Más allá](11-mas-alla.md) →

Para consultar, no para aprender. Si una palabra no te suena, mira el [glosario](../glosario.md).

## Una sola vez

| Qué | Comando |
|---|---|
| Comprobar Git | `git --version` |
| Poner tu nombre | `git config --global user.name "Tu Nombre"` |
| Poner tu correo | `git config --global user.email "correo"` |
| Descargar el repositorio | `git clone https://github.com/profeFPInfor/upgrade-ia.git` |
| Acceso con GitHub CLI | `gh auth login` y `gh auth setup-git` |

## Cada aportación

| Qué | Comando |
|---|---|
| Ver dónde estás y qué cambió | `git status` |
| Ir a `main` | `git checkout main` |
| Traer lo nuevo de GitHub | `git pull` |
| Crear una rama y entrar | `git checkout -b docs/12-tema` |
| Preparar un fichero | `git add ruta/fichero.md` |
| Ver lo que está preparado | `git diff --staged` |
| Guardar con mensaje | `git commit -m "docs: mensaje"` |
| Subir una rama nueva | `git push -u origin docs/12-tema` |
| Subir de nuevo la misma rama | `git push` |

## Para mirar

| Qué | Comando |
|---|---|
| Ver los últimos commits | `git log --oneline -5` |
| Ver las ramas locales | `git branch` |
| Ver lo que has cambiado y no has preparado | `git diff` |
| Ver los remotos | `git remote -v` |

## Para deshacer (con cuidado)

| Qué | Comando |
|---|---|
| Quitar un fichero de "preparado" | `git restore --staged fichero` |
| Corregir el último mensaje (antes de subirlo) | `git commit --amend -m "mensaje"` |
| Terminar la unión de un conflicto ya resuelto | `git add fichero` y `git commit --no-edit` |
| Cancelar una unión con conflictos | `git merge --abort` |
| Borrar una rama ya fusionada (opción segura) | `git branch -d nombre-de-la-rama` |

> **Solo si Git se niega con `-d`** (*not fully merged*) **y tu PR ya está fusionado:** `git branch -D nombre-de-la-rama`. `-D` borra sin comprobar nada; no lo uses por costumbre. Si solo ves un *warning* y después `Deleted branch`, la rama ya está borrada ([detalle](05-la-revision.md#cuando-se-fusiona)).

## VS Code

| Qué | Cómo |
|---|---|
| Abrir la terminal integrada | Menú *Terminal → New Terminal* |
| Control de código fuente | `Ctrl+Shift+G` |
| Abrir una carpeta | *File → Open Folder…* |

## Los tipos de commit

`docs:` documentación · `fix:` corrección · `feat:` funcionalidad nueva · `chore:` mantenimiento

## El ciclo en una línea

Issue → `git checkout main` → `git pull` → `git checkout -b rama` → editar → `git add` → `git diff --staged` → `git commit` → `git push -u origin rama` → pull request → revisión → fusión.

## Fuentes

[Pro Git](https://git-scm.com/book/es/v2) · [Documentación de Git](https://git-scm.com/docs) · [Documentación de GitHub](https://docs.github.com)
