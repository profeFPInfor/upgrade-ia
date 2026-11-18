#!/usr/bin/env python3
"""Comprobaciones de calidad de un pull request. Solo biblioteca estándar (Python 3.11 o superior).

Subcomandos:
  markdown    enlaces y anclas relativos, bloques de código, títulos, diagramas Mermaid, marcas de conflicto
  estructura  ficheros que no se pueden revisar (ejecutables, comprimidos, pickle, bases de datos), nombres, carpetas
  titulo      el título del PR sigue Conventional Commits, y el PR enlaza su Issue
  enlaces     comprueba por red los enlaces externos de todos los .md (para el workflow programado)

Cada subcomando devuelve 0 sin errores (los avisos no cuentan), 1 con errores y 2 si hay un error de uso.
El texto que viene del PR (rutas, título, cuerpo, rama) controla a quien abre el PR: se sanea antes de mostrarlo y
nunca se interpola en una orden.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass

sys.dont_write_bytecode = True  # no dejar __pycache__ dentro del repositorio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import detectar_datos_personales as base  # noqa: E402

MAX_IMAGEN = 1024 * 1024
MAX_MERMAID_README_RAIZ = 2
MAX_LINEA_TITULO = 2000

TIPOS_CC = ("feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert")
RE_TITULO_CC = re.compile(r"^(" + "|".join(TIPOS_CC) + r")(\([a-z0-9._/\-]+\))?!?: \S.*$")
RE_CIERRA_ISSUE = re.compile(r"(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\b:?\s+#\d+")
RE_RAMA = re.compile(r"^(docs|feat|fix|chore|refactor|test|ci)/[a-z0-9][a-z0-9._\-]*$")
MAX_TITULO = 100

EXT_BLOQUEADAS = {
    ".exe": "ejecutable", ".dll": "ejecutable", ".so": "ejecutable", ".dylib": "ejecutable", ".msi": "instalador",
    ".dmg": "instalador", ".apk": "aplicación", ".jar": "programa compilado", ".class": "programa compilado",
    ".pyc": "programa compilado", ".pyo": "programa compilado", ".whl": "paquete", ".iso": "imagen de disco",
    ".zip": "comprimido", ".rar": "comprimido", ".7z": "comprimido", ".tar": "comprimido", ".gz": "comprimido",
    ".tgz": "comprimido", ".bz2": "comprimido", ".xz": "comprimido",
    ".pkl": "pickle (puede ejecutar código al abrirse)", ".pickle": "pickle (puede ejecutar código al abrirse)",
    ".sqlite": "base de datos", ".sqlite3": "base de datos", ".db": "base de datos", ".mdb": "base de datos",
    ".accdb": "base de datos",
}
EXT_AVISO = {".xls", ".xlsb", ".doc", ".docx", ".ppt", ".pptx", ".pdf", ".parquet", ".feather", ".h5", ".hdf5",
             ".npy", ".npz", ".sav", ".dta", ".rds", ".rdata"}
EXT_IMAGEN = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
RAICES_PERMITIDAS = {".github", ".githooks", "assets", "docs", "herramientas-ia", "markdown", "proceso", "analitica"}
NOMBRES_EXENTOS = {"README.md", "LICENSE.md", "CONTRIBUTING.md", "CODEOWNERS"}
RE_NOMBRE_BUENO = re.compile(r"^[a-z0-9][a-z0-9._\-]*$")
MERMAID_CONOCIDOS = ("flowchart", "graph", "sequencediagram", "classdiagram", "statediagram", "erdiagram", "gantt", "pie",
                     "journey", "gitgraph", "mindmap", "timeline", "quadrantchart", "requirementdiagram", "c4context",
                     "xychart", "block", "sankey", "architecture", "packet", "kanban")


@dataclass(frozen=True)
class Problema:
    fichero: str
    linea: int
    mensaje: str
    error: bool = True


# ----------------------------------------------------------------------------------------------
# Markdown
# ----------------------------------------------------------------------------------------------
RE_FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")
RE_TITULO = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
# El texto del enlace y el destino están acotados: con `[^\]]*` sin límite, una línea de miles de "[" sin cerrar
# hacía cuadrático el coste (200.000 corchetes tardaban 73 s).
RE_ENLACE = re.compile(r"(!?)\[([^\]]{0,300})\]\(\s*<?((?:[^()\s>]|\([^()\s]{0,300}\)){1,600})>?(?:\s+\"[^\"]{0,300}\")?\s*\)")
RE_CONFLICTO = re.compile(r"^(<{7}( |$)|={7}$|>{7}( |$))")


def slug_gh(titulo: str) -> str:
    t = re.sub(r"[`*_]", "", titulo.strip().lower())
    t = re.sub(r"[^\w\- ]", "", t)
    return t.replace(" ", "-")


def analizar_md(texto: str) -> dict:
    """Devuelve líneas con su estado de código, títulos (con anclas únicas) y bloques mermaid."""
    lineas = texto.split("\n")
    en_codigo = [False] * len(lineas)
    bloques_mermaid: list[tuple[int, list[str]]] = []
    abierto: tuple[str, int, str] | None = None  # (carácter, longitud, lenguaje)
    actual: list[str] = []
    inicio_mermaid = 0
    for i, linea in enumerate(lineas):
        m = RE_FENCE.match(linea)
        if abierto is None:
            if m:
                abierto = (m.group(1)[0], len(m.group(1)), m.group(2).strip().split(" ")[0].lower())
                en_codigo[i] = True
                actual, inicio_mermaid = [], i + 1
        else:
            en_codigo[i] = True
            if m and m.group(1)[0] == abierto[0] and len(m.group(1)) >= abierto[1] and not m.group(2).strip():
                if abierto[2] == "mermaid":
                    bloques_mermaid.append((inicio_mermaid, actual))
                abierto = None
            else:
                actual.append(linea)
    titulos: list[tuple[int, int, str]] = []
    vistos: dict[str, int] = {}
    for i, linea in enumerate(lineas):
        if en_codigo[i]:
            continue
        m = RE_TITULO.match(linea[:MAX_LINEA_TITULO])
        if m:
            s = slug_gh(m.group(2))
            n = vistos.get(s, 0)
            vistos[s] = n + 1
            titulos.append((i + 1, len(m.group(1)), s if n == 0 else f"{s}-{n}"))
    return {"lineas": lineas, "codigo": en_codigo, "abierto": abierto is not None, "titulos": titulos,
            "mermaid": bloques_mermaid}


class RepoMd:
    """Lee y cachea los .md del repositorio para resolver enlaces y anclas."""

    def __init__(self, raiz: str):
        self.raiz = raiz
        self._cache: dict[str, dict | None] = {}

    def md(self, ruta_abs: str) -> dict | None:
        if ruta_abs not in self._cache:
            try:
                with open(ruta_abs, "rb") as f:
                    self._cache[ruta_abs] = analizar_md(base.decodificar(f.read(base.MAX_BYTES)))
            except OSError:
                self._cache[ruta_abs] = None
        return self._cache[ruta_abs]


def _sin_metadatos_mermaid(cuerpo: list[str]) -> list[str]:
    """Líneas útiles de un diagrama, sin el bloque de metadatos YAML (--- ... ---) ni los comentarios (%%)."""
    lineas = [l.strip() for l in cuerpo if l.strip()]
    if lineas and lineas[0] == "---":
        try:
            lineas = lineas[lineas.index("---", 1) + 1:]
        except ValueError:
            lineas = []
    return [l for l in lineas if not l.startswith("%%")]


def comprobar_markdown(raiz: str, ruta: str, repo: RepoMd | None = None) -> list[Problema]:
    repo = repo or RepoMd(raiz)
    completa = os.path.join(raiz, ruta)
    a = repo.md(completa)
    if a is None:
        return []
    out: list[Problema] = []
    if a["abierto"]:
        out.append(Problema(ruta, 1, "hay un bloque de código sin cerrar"))
    nivel = 0
    n_h1 = 0
    for linea, n, _ in a["titulos"]:
        if n == 1:
            n_h1 += 1
        if nivel and n > nivel + 1:
            out.append(Problema(ruta, linea, f"salto de título de H{nivel} a H{n}: no te saltes niveles"))
        nivel = n
    if n_h1 > 1:
        out.append(Problema(ruta, 1, "hay más de un título de nivel 1 (#)", error=False))
    for i, (linea, cod) in enumerate(zip(a["lineas"], a["codigo"]), 1):
        if cod:
            continue
        if "\t" in linea:
            out.append(Problema(ruta, i, "tabulador: usa espacios", error=False))
        if RE_CONFLICTO.match(linea):
            out.append(Problema(ruta, i, "marca de conflicto sin resolver (<<<<<<<, ======= o >>>>>>>)"))
        limpia = re.sub(r"`[^`]{0,300}`", "", linea[:base.VENTANA])
        for m in RE_ENLACE.finditer(limpia):
            es_imagen, texto, destino = m.group(1) == "!", m.group(2), m.group(3)
            if es_imagen and not texto.strip():
                out.append(Problema(ruta, i, "imagen sin texto alternativo (accesibilidad)", error=False))
            if destino.startswith(("http://", "https://", "mailto:", "data:", "tel:")):
                continue
            ruta_dest, _, ancla = destino.partition("#")
            objetivo = os.path.normpath(os.path.join(os.path.dirname(completa), ruta_dest)) if ruta_dest else completa
            if ruta_dest and not os.path.exists(objetivo):
                out.append(Problema(ruta, i, f"enlace relativo roto: {base.sanear(destino, 80)}"))
                continue
            if ancla and objetivo.endswith(".md") and os.path.isfile(objetivo):
                destino_md = repo.md(objetivo)
                if destino_md is not None and ancla.lower() not in {s for _, _, s in destino_md["titulos"]}:
                    out.append(Problema(ruta, i, f"ancla inexistente: {base.sanear(destino, 80)}"))
    es_readme_raiz = ruta == "README.md"
    if es_readme_raiz and len(a["mermaid"]) > MAX_MERMAID_README_RAIZ:
        out.append(Problema(ruta, 1, f"el README raíz admite como máximo {MAX_MERMAID_README_RAIZ} diagramas Mermaid "
                                     f"(hay {len(a['mermaid'])})"))
    for inicio, cuerpo in a["mermaid"]:
        utiles = _sin_metadatos_mermaid(cuerpo)
        if not utiles:
            out.append(Problema(ruta, inicio, "diagrama Mermaid vacío"))
        elif not utiles[0].lower().startswith(MERMAID_CONOCIDOS):
            out.append(Problema(ruta, inicio, "el diagrama Mermaid no empieza por un tipo conocido (flowchart, "
                                              "sequenceDiagram...): comprueba que se ve bien", error=False))
    return out


# ----------------------------------------------------------------------------------------------
# Estructura
# ----------------------------------------------------------------------------------------------
def comprobar_estructura(raiz: str, ruta: str, nuevo: bool) -> list[Problema]:
    out: list[Problema] = []
    nombre = os.path.basename(ruta)
    ext = os.path.splitext(nombre)[1].lower()
    completa = os.path.join(raiz, ruta)
    if os.path.islink(completa):
        out.append(Problema(ruta, 1, "es un enlace simbólico: no se admiten", error=False))
        return out
    if ext in EXT_BLOQUEADAS:
        out.append(Problema(ruta, 1, f"formato no admitido ({EXT_BLOQUEADAS[ext]}): no se puede revisar. "
                                     "Sube los datos o el código sin comprimir"))
    elif ext in EXT_AVISO:
        out.append(Problema(ruta, 1, "formato binario: no se puede revisar automáticamente; el profesor lo "
                                     "revisará a mano", error=False))
    if ext in EXT_IMAGEN and os.path.isfile(completa) and os.path.getsize(completa) > MAX_IMAGEN:
        out.append(Problema(ruta, 1, "imagen de más de 1 MB: optimízala (reduce su tamaño)", error=False))
    if nuevo:
        partes = ruta.split("/")
        if len(partes) > 1 and partes[0] not in RAICES_PERMITIDAS:
            out.append(Problema(ruta, 1, "carpeta nueva en la raíz del repositorio: confirma con el profesor dónde va",
                                error=False))
        if partes[0] not in (".github", ".githooks") and nombre not in NOMBRES_EXENTOS and not RE_NOMBRE_BUENO.match(nombre):
            out.append(Problema(ruta, 1, "nombre de fichero fuera de convención: minúsculas, números, guiones y sin "
                                         "espacios ni datos personales", error=False))
    return out


# ----------------------------------------------------------------------------------------------
# Título, cuerpo y rama del PR
# ----------------------------------------------------------------------------------------------
def comprobar_titulo(titulo: str, cuerpo: str = "", rama: str = "") -> list[Problema]:
    out: list[Problema] = []
    t = (titulo or "").strip()
    if not RE_TITULO_CC.match(t):
        out.append(Problema("(título del PR)", 1,
                            "el título debe seguir Conventional Commits: tipo, dos puntos y una frase (por ejemplo "
                            "`docs: añadir la guía de pruebas`). Tipos: " + ", ".join(TIPOS_CC)))
    elif len(t) > MAX_TITULO:
        out.append(Problema("(título del PR)", 1, f"el título es demasiado largo ({len(t)} caracteres; máximo {MAX_TITULO})"))
    tipo = t.split(":", 1)[0].split("(")[0].rstrip("!") if ":" in t else ""
    if tipo in ("docs", "feat", "fix") and not RE_CIERRA_ISSUE.search(cuerpo or ""):
        out.append(Problema("(descripción del PR)", 1,
                            "la descripción no enlaza su Issue: añade `Closes #N` (con el número de tu Issue)",
                            error=False))
    if rama and not RE_RAMA.match(rama):
        out.append(Problema("(rama del PR)", 1,
                            "el nombre de la rama no sigue la convención `docs/<n>-<tema>` (o feat/, fix/, chore/...)",
                            error=False))
    return out


# ----------------------------------------------------------------------------------------------
# Enlaces externos
# ----------------------------------------------------------------------------------------------
def urls_externas(raiz: str, rutas: list[str]) -> dict[str, list[tuple[str, int]]]:
    repo = RepoMd(raiz)
    salida: dict[str, list[tuple[str, int]]] = {}
    for ruta in rutas:
        a = repo.md(os.path.join(raiz, ruta))
        if a is None:
            continue
        for i, (linea, cod) in enumerate(zip(a["lineas"], a["codigo"]), 1):
            if cod:
                continue
            for m in RE_ENLACE.finditer(re.sub(r"`[^`]{0,300}`", "", linea[:base.VENTANA])):
                d = m.group(3).rstrip(".,;")
                if d.startswith(("http://", "https://")):
                    salida.setdefault(d, []).append((ruta, i))
    return salida


def estado_url(url: str) -> int:
    cabeceras = {"User-Agent": "Mozilla/5.0 (comprobador de enlaces del repositorio)"}
    for metodo in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=metodo, headers=cabeceras)
            with urllib.request.urlopen(req, timeout=15) as r:
                return r.status
        except urllib.error.HTTPError as e:
            if metodo == "HEAD" and e.code in (403, 405, 501):
                continue
            return e.code
        except Exception:
            if metodo == "HEAD":
                continue
            return 0
    return 0


def comprobar_enlaces(raiz: str, rutas: list[str], estado=estado_url) -> list[Problema]:
    urls = urls_externas(raiz, rutas)
    if not urls:
        return []
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        codigos = dict(zip(urls, ex.map(estado, urls)))
    out: list[Problema] = []
    for url, usos in urls.items():
        c = codigos[url]
        if 200 <= c < 400:
            continue
        ruta, linea = usos[0]
        if c in (401, 403, 429, 999):
            out.append(Problema(ruta, linea, f"un enlace responde {c} (acceso restringido o límite de peticiones): "
                                             "compruébalo a mano", error=False))
        else:
            out.append(Problema(ruta, linea, f"enlace externo roto ({c or 'sin respuesta'}): {base.sanear(url, 100)}"))
    return out


# ----------------------------------------------------------------------------------------------
# Salida
# ----------------------------------------------------------------------------------------------
def emitir(problemas: list[Problema], titulo: str, formato: str):
    for p in problemas:
        nivel = "error" if p.error else "warning"
        if formato == "github":
            print(f"::{nivel} file={base.escapar_propiedad(base.a_utf8(p.fichero))},line={p.linea},"
                  f"title={base.escapar_propiedad(titulo)}::{base.escapar_dato(p.mensaje)}")
        else:
            print(f"{base.sanear(p.fichero)}:{p.linea}: {'error' if p.error else 'aviso'}: {p.mensaje}")


def resumen(problemas: list[Problema], titulo: str, n: int) -> str:
    errores = [p for p in problemas if p.error]
    avisos = [p for p in problemas if not p.error]
    out = [f"## {titulo}", ""]
    out.append(f"**Resultado: {len(errores)} error(es) y {len(avisos)} aviso(s)** en {n} elemento(s) comprobado(s)."
               if problemas else f"**Resultado: todo en orden** ({n} elemento(s) comprobado(s)).")
    out.append("")
    if problemas:
        out += ["| Fichero | Línea | | Qué pasa |", "|---|---|---|---|"]
        for p in problemas[:base.MAX_FILAS_RESUMEN]:
            out.append(f"| `{base.sanear(p.fichero)}` | {p.linea} | {'error' if p.error else 'aviso'} | "
                       f"{base.sanear(p.mensaje, 300).replace('|', '/')} |")
        out.append("")
    return "\n".join(out) + "\n"


def terminar(problemas: list[Problema], titulo: str, n: int, args) -> int:
    formato = args.formato
    if formato == "auto":
        formato = "github" if os.environ.get("GITHUB_ACTIONS") == "true" else "texto"
    emitir(problemas, titulo, formato)
    destino = args.resumen or os.environ.get("GITHUB_STEP_SUMMARY")
    if destino:
        with open(destino, "a", encoding="utf-8") as f:
            f.write(resumen(problemas, titulo, n))
    errores = sum(1 for p in problemas if p.error)
    print(f"{titulo}: {errores} error(es), {len(problemas) - errores} aviso(s).", file=sys.stderr if errores else sys.stdout)
    return 1 if errores else 0


# ----------------------------------------------------------------------------------------------
# Programa principal
# ----------------------------------------------------------------------------------------------
def construir_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz")
    ap.add_argument("--resumen")
    ap.add_argument("--formato", choices=("auto", "github", "texto"), default="auto")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for nombre in ("markdown", "estructura"):
        p = sub.add_parser(nombre)
        p.add_argument("--base")
        p.add_argument("--ficheros", nargs="+")
    sub.add_parser("titulo")
    sub.add_parser("enlaces")
    return ap


def main(argv: list[str] | None = None) -> int:
    args = construir_parser().parse_args(argv)
    raiz = os.path.abspath(args.raiz or base.raiz_git())
    try:
        if args.cmd == "titulo":
            p = comprobar_titulo(os.environ.get("PR_TITULO", ""), os.environ.get("PR_CUERPO", ""),
                                 os.environ.get("PR_RAMA", ""))
            return terminar(p, "Título del PR", 1, args)
        if args.cmd == "enlaces":
            rutas = [r for r in _todos_md(raiz)]
            return terminar(comprobar_enlaces(raiz, rutas), "Enlaces externos", len(rutas), args)
        if args.ficheros:
            cambios = nuevos = list(args.ficheros)
        elif args.base:
            cambios = base.ficheros_cambiados(raiz, args.base, "AM")
            nuevos = set(base.ficheros_cambiados(raiz, args.base, "A"))
        else:
            raise base.ErrorConfig("indica --base o --ficheros")
    except base.ErrorConfig as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    problemas: list[Problema] = []
    if args.cmd == "markdown":
        repo = RepoMd(raiz)
        mds = [c for c in cambios if c.lower().endswith(".md") and os.path.isfile(os.path.join(raiz, c))]
        for c in mds:
            problemas += comprobar_markdown(raiz, c, repo)
        return terminar(problemas, "Markdown", len(mds), args)
    for c in cambios:
        problemas += comprobar_estructura(raiz, c, c in nuevos)
    return terminar(problemas, "Estructura", len(cambios), args)


def _todos_md(raiz: str) -> list[str]:
    salida = []
    for carpeta, dirs, ficheros in os.walk(raiz):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for f in ficheros:
            if f.lower().endswith(".md"):
                salida.append(os.path.relpath(os.path.join(carpeta, f), raiz).replace(os.sep, "/"))
    return sorted(salida)


if __name__ == "__main__":
    sys.exit(main())
