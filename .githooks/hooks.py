#!/usr/bin/env python3
"""Hooks de Git del repositorio: pre-commit, commit-msg y pre-push. Solo biblioteca estándar (Python 3.11+).

Instalar (una vez por clon del repositorio):
    python3 .githooks/hooks.py instalar
que equivale a:
    git config core.hooksPath .githooks

Qué hacen:
  pre-commit  impide commitear en main; revisa el contenido que vas a commitear (datos personales y secretos,
              formatos que no se pueden revisar, marcas de conflicto, enlaces rotos en Markdown)
  commit-msg  el mensaje debe seguir Conventional Commits
  pre-push    impide subir a main y revisa los commits que se suben, por si algo se coló con --no-verify

Estos hooks AYUDAN pero NO son la barrera: `git commit --no-verify` y `git push --no-verify` los saltan. La
barrera es el CI del pull request (pr-privacidad y pr-calidad). Aquí el valor detectado no se muestra nunca.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile

# Los hooks importan los scripts de .github/scripts: sin esto Python crearía __pycache__/*.pyc dentro del repositorio
# y un `git add .` los metería en el commit.
sys.dont_write_bytecode = True

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, ".github", "scripts"))

PROTEGIDAS = ("main", "master")
CEROS = "0" * 40
CEROS_SHA256 = "0" * 64


def git(*args: str, entrada: bytes | None = None, comprobar: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], input=entrada, capture_output=True, check=comprobar)


def texto(b: bytes) -> str:
    return b.decode("utf-8", "surrogateescape").strip()


def rama_actual() -> str:
    r = git("symbolic-ref", "--short", "-q", "HEAD")
    return texto(r.stdout) if r.returncode == 0 else ""


def lista(*args: str) -> list[str]:
    r = git(*args)
    return [p.decode("utf-8", "surrogateescape") for p in r.stdout.split(b"\0") if p] if r.returncode == 0 else []


def exportar(rev: str | None, rutas: list[str], destino: str) -> None:
    """Escribe en `destino` el contenido de `rutas` tal como está en el índice (rev=None) o en la revisión `rev`.

    Se lee del repositorio (no del disco) para revisar exactamente lo que se va a commitear o a subir.
    """
    prefijo = (rev or "") + ":"
    simples = [r for r in rutas if "\n" not in r]
    especiales = [r for r in rutas if "\n" in r]
    if simples:
        entrada = "".join(f"{prefijo}{r}\n" for r in simples).encode("utf-8", "surrogateescape")
        p = subprocess.run(["git", "cat-file", "--batch"], input=entrada, capture_output=True)
        datos, pos = p.stdout, 0
        for r in simples:
            fin = datos.index(b"\n", pos)
            cabecera = datos[pos:fin].split()
            pos = fin + 1
            if len(cabecera) == 3 and cabecera[1] == b"blob":
                n = int(cabecera[2])
                contenido, pos = datos[pos:pos + n], pos + n + 1
                _escribir(destino, r, contenido)
    for r in especiales:  # nombres con salto de línea: no caben en el protocolo de --batch
        p = git("cat-file", "blob", f"{prefijo}{r}")
        if p.returncode == 0:
            _escribir(destino, r, p.stdout)


def _escribir(destino: str, ruta: str, contenido: bytes) -> None:
    objetivo = os.path.normpath(os.path.join(destino, ruta))
    if not objetivo.startswith(os.path.normpath(destino) + os.sep):
        return  # una ruta con ".." no puede salir de la carpeta temporal
    os.makedirs(os.path.dirname(objetivo), exist_ok=True)
    with open(objetivo, "wb") as f:
        f.write(contenido)


def revisar(rev: str | None, cambios: list[str], nuevos: set, avisar_calidad: bool) -> int:
    """Revisa privacidad (sobre el contenido exportado) y, opcionalmente, calidad. Devuelve el número de errores."""
    try:
        import detectar_datos_personales as dp
        import comprobar_calidad as cq
    except ImportError:
        print("AVISO: faltan los scripts de .github/scripts; se omite la comprobación local.", file=sys.stderr)
        return 0
    try:
        permitidos = dp.cargar_permitidos(os.path.join(RAIZ, ".github", "privacidad-permitidos.txt"))
    except dp.ErrorConfig as e:
        print(f"ERROR en la lista de excepciones: {e}", file=sys.stderr)
        return 1
    ctx = dp.Contexto(dp.dominios_permitidos(permitidos))
    hallazgos, avisos = [], []
    with tempfile.TemporaryDirectory() as tmp:
        exportar(rev, cambios, tmp)
        for ruta in cambios:
            rec = dp.analizar_fichero(tmp, ruta, ctx)
            hallazgos += [h for h in rec.items if not dp.esta_permitido(h, permitidos)]
            avisos += rec.avisos
    problemas = []
    for ruta in cambios:
        problemas += cq.comprobar_estructura(RAIZ, ruta, ruta in nuevos) if avisar_calidad else []
    if avisar_calidad:
        repo_md = cq.RepoMd(RAIZ)
        for ruta in cambios:
            if ruta.lower().endswith(".md") and os.path.isfile(os.path.join(RAIZ, ruta)):
                problemas += cq.comprobar_markdown(RAIZ, ruta, repo_md)
    errores = len(hallazgos) + sum(1 for p in problemas if p.error)
    dp.emitir_texto(hallazgos, avisos)
    cq.emitir([p for p in problemas], "Calidad", "texto")
    if hallazgos:
        print("\nSe han detectado posibles datos personales o secretos (el valor no se muestra). Quítalos o "
              "sustitúyelos por datos inventados antes de seguir. Si es un falso positivo, pide una excepción al "
              "profesor. Si el dato ya estaba en un commit anterior, avisa al profesor.", file=sys.stderr)
    return errores


def pre_commit() -> int:
    rama = rama_actual()
    if rama in PROTEGIDAS:
        print(f"No se puede commitear en '{rama}': está protegida y todo entra por pull request.\n"
              "Crea tu rama con:  git checkout -b docs/<n>-<tema>   (por ejemplo docs/12-analisis-sota)\n"
              "Si ya habías editado ficheros, no pierdes nada: se van contigo a la rama nueva.", file=sys.stderr)
        return 1
    staged = lista("diff", "--cached", "--name-only", "-z", "--diff-filter=AM", "--no-renames")
    if not staged:
        return 0
    nuevos = set(lista("diff", "--cached", "--name-only", "-z", "--diff-filter=A", "--no-renames"))
    conflictos = marcas_de_conflicto(staged)
    errores = revisar(None, staged, nuevos, True) + conflictos
    if errores:
        print(f"\nNo se ha creado el commit: {errores} problema(s) que hay que corregir.", file=sys.stderr)
        return 1
    return 0


def marcas_de_conflicto(rutas: list[str]) -> int:
    """Marcas sin resolver en ficheros que no son Markdown (en Markdown las revisa comprobar_calidad)."""
    try:
        import comprobar_calidad as cq
    except ImportError:
        return 0
    n = 0
    with tempfile.TemporaryDirectory() as tmp:
        sin_md = [r for r in rutas if not r.lower().endswith(".md")]
        exportar(None, sin_md, tmp)
        for r in sin_md:
            ruta = os.path.join(tmp, r)
            if not os.path.isfile(ruta):
                continue
            with open(ruta, "rb") as f:
                datos = f.read(5 * 1024 * 1024)
            if b"\0" in datos[:8192]:
                continue
            for i, linea in enumerate(datos.decode("utf-8", "replace").split("\n"), 1):
                if cq.RE_CONFLICTO.match(linea):
                    print(f"{cq.base.sanear(r)}:{i}: error: marca de conflicto sin resolver", file=sys.stderr)
                    n += 1
                    break
    return n


def commit_msg(ruta_mensaje: str) -> int:
    import comprobar_calidad as cq
    with open(ruta_mensaje, encoding="utf-8", errors="replace") as f:
        lineas = [l.rstrip("\n") for l in f if not l.startswith("#")]
    primera = next((l.strip() for l in lineas if l.strip()), "")
    if not primera or primera.startswith(("Merge ", "Revert \"", "fixup! ", "squash! ", "amend! ")):
        return 0
    if cq.RE_TITULO_CC.match(primera) and len(primera) <= cq.MAX_TITULO:
        return 0
    print("El mensaje del commit debe seguir Conventional Commits: un tipo, dos puntos y una frase corta.\n"
          f"  Tipos: {', '.join(cq.TIPOS_CC)}\n"
          "  Ejemplos:  docs: añadir ejemplo de matriz comparativa\n"
          "             fix: corregir un enlace roto del glosario\n"
          f"  (máximo {cq.MAX_TITULO} caracteres en la primera línea)", file=sys.stderr)
    return 1


def pre_push(entrada: str) -> int:
    errores = 0
    for linea in entrada.splitlines():
        partes = linea.split()
        if len(partes) != 4:
            continue
        _local_ref, local_sha, remote_ref, remote_sha = partes
        if set(local_sha) <= {"0"}:
            continue  # borrado de una rama remota
        rama = remote_ref.removeprefix("refs/heads/")
        if remote_ref.startswith("refs/heads/") and rama in PROTEGIDAS:
            print(f"No se sube directamente a '{rama}': está protegida. Sube tu rama y abre un pull request.",
                  file=sys.stderr)
            errores += 1
            continue
        if set(remote_sha) <= {"0"}:
            base = "origin/main" if git("rev-parse", "--verify", "-q", "origin/main").returncode == 0 else ""
        else:
            base = remote_sha if git("cat-file", "-e", remote_sha).returncode == 0 else (
                "origin/main" if git("rev-parse", "--verify", "-q", "origin/main").returncode == 0 else "")
        if not base:
            print("AVISO: no hay una rama base con la que comparar; se omite la revisión de lo que se sube.",
                  file=sys.stderr)
            continue
        rango = f"{base}...{local_sha}" if base.startswith("origin/") else f"{base}..{local_sha}"
        cambios = lista("diff", "--name-only", "-z", "--diff-filter=AM", "--no-renames", rango)
        nuevos = set(lista("diff", "--name-only", "-z", "--diff-filter=A", "--no-renames", rango))
        errores += revisar(local_sha, cambios, nuevos, False)
    if errores:
        print(f"\nNo se ha subido nada: {errores} problema(s) en lo que ibas a subir.", file=sys.stderr)
        return 1
    return 0


def instalar() -> int:
    if sys.version_info < (3, 11):
        print("Se necesita Python 3.11 o superior.", file=sys.stderr)
        return 1
    r = git("config", "core.hooksPath", ".githooks")
    if r.returncode != 0:
        print("No se pudo configurar Git. ¿Estás dentro del repositorio?", file=sys.stderr)
        return 1
    sin_permiso = [h for h in ("pre-commit", "commit-msg", "pre-push")
                   if os.name != "nt" and not os.access(os.path.join(RAIZ, ".githooks", h), os.X_OK)]
    print("Hooks instalados: Git usará .githooks/ en este clon (git config core.hooksPath .githooks).")
    if sin_permiso:
        print(f"AVISO: estos hooks no tienen permiso de ejecución y Git los ignoraría: {', '.join(sin_permiso)}.\n"
              "       Arréglalo con:  chmod +x .githooks/pre-commit .githooks/commit-msg .githooks/pre-push")
        return 1
    print("Para desinstalarlos:  git config --unset core.hooksPath")
    return 0


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    cmd, resto = argv[0], argv[1:]
    if cmd == "instalar":
        return instalar()
    os.chdir(RAIZ)
    if cmd == "pre-commit":
        return pre_commit()
    if cmd == "commit-msg" and resto:
        return commit_msg(resto[0])
    if cmd == "pre-push":
        return pre_push(sys.stdin.read())
    print(f"Orden desconocida: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
