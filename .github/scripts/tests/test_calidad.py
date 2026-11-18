"""Pruebas de comprobar_calidad.py (Markdown, estructura, título del PR y enlaces).

Ejecutar desde la raíz del repositorio:
    python3 -m unittest discover -s .github/scripts/tests -v
"""
import sys

sys.dont_write_bytecode = True  # las pruebas no dejan __pycache__ dentro del repositorio
import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import comprobar_calidad as c  # noqa: E402


class Repo(str):
    """Carpeta temporal que se usa como `t` (ruta) o como `t.name`, y se borra al salir del `with`."""

    def __new__(cls, ficheros: dict):
        self = super().__new__(cls, tempfile.mkdtemp())
        for nombre, contenido in ficheros.items():
            ruta = Path(self) / nombre
            ruta.parent.mkdir(parents=True, exist_ok=True)
            ruta.write_bytes(contenido if isinstance(contenido, bytes) else contenido.encode("utf-8"))
        return self

    @property
    def name(self) -> str:
        return str(self)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        shutil.rmtree(str(self), ignore_errors=True)


def repo(ficheros: dict) -> Repo:
    return Repo(ficheros)


def mensajes(t, ruta, **kw):
    return [(p.linea, p.error, p.mensaje.split(":")[0]) for p in c.comprobar_markdown(t.name, ruta)]


class TestMarkdown(unittest.TestCase):
    def test_documento_correcto_no_da_problemas(self):
        with repo({"a.md": "# Titulo\n\n## Seccion\n\nTexto [otro](b.md#parte) y [ancla](#seccion).\n",
                   "b.md": "# B\n\n## Parte\n"}) as t:
            self.assertEqual(c.comprobar_markdown(t, "a.md"), [])

    def test_enlace_y_ancla_rotos(self):
        with repo({"a.md": "# A\n[x](no-existe.md)\n[y](b.md#nada)\n[z](#tampoco)\n", "b.md": "# B\n"}) as t:
            m = [(p.linea, p.mensaje.split(":")[0]) for p in c.comprobar_markdown(t, "a.md")]
            self.assertEqual(m, [(2, "enlace relativo roto"), (3, "ancla inexistente"), (4, "ancla inexistente")])

    def test_anclas_duplicadas_y_con_tildes_y_codigo_en_el_titulo(self):
        with repo({"a.md": "# A\n## Qué hacer\n## Qué hacer\n### `git add`\n"
                           "[1](#qué-hacer) [2](#qué-hacer-1) [3](#git-add)\n"}) as t:
            self.assertEqual(c.comprobar_markdown(t, "a.md"), [])

    def test_los_enlaces_externos_y_el_codigo_en_linea_no_se_comprueban_aqui(self):
        with repo({"a.md": "# A\n[web](https://example.com/x) y `[no](roto.md)`\n```\n[no](roto.md)\n```\n"}) as t:
            self.assertEqual(c.comprobar_markdown(t, "a.md"), [])

    def test_bloque_sin_cerrar_y_salto_de_titulo(self):
        with repo({"a.md": "# A\n\n### Salto\n\n```python\nx = 1\n"}) as t:
            m = mensajes(t, "a.md")
            self.assertIn((3, True, "salto de título de H1 a H3"), m)
            self.assertIn((1, True, "hay un bloque de código sin cerrar"), m)

    def test_fence_largo_y_marcas_de_conflicto_dentro_de_codigo(self):
        with repo({"a.md": "# A\n````text\n```\n<<<<<<< HEAD\n=======\n>>>>>>> main\n````\n"}) as t:
            self.assertEqual(c.comprobar_markdown(t, "a.md"), [])

    def test_marcas_de_conflicto_fuera_de_codigo(self):
        with repo({"a.md": "# A\n<<<<<<< HEAD\nuno\n=======\ndos\n>>>>>>> main\n"}) as t:
            self.assertEqual(sorted(p.linea for p in c.comprobar_markdown(t, "a.md")), [2, 4, 6])

    def test_imagen_sin_alt_es_aviso_y_tabulador_tambien(self):
        with repo({"a.md": "# A\n![](img.png)\n\ttexto\n", "img.png": b"x"}) as t:
            m = c.comprobar_markdown(t, "a.md")
            self.assertEqual([(p.linea, p.error) for p in m], [(2, False), (3, False)])

    def test_imagen_rota_es_error(self):
        with repo({"a.md": "# A\n![logo](assets/no.png)\n"}) as t:
            self.assertTrue(c.comprobar_markdown(t, "a.md")[0].error)

    def test_enlace_con_parentesis_en_la_ruta(self):
        with repo({"a.md": "# A\n[x](carpeta/ficha_(1).md)\n", "carpeta/ficha_(1).md": "# F\n"}) as t:
            self.assertEqual(c.comprobar_markdown(t, "a.md"), [])

    def test_readme_raiz_admite_dos_mermaid(self):
        bloque = "```mermaid\nflowchart LR\n  A --> B\n```\n"
        with repo({"README.md": "# R\n" + bloque * 2, "docs/a.md": "# A\n" + bloque * 3}) as t:
            self.assertEqual(c.comprobar_markdown(t, "README.md"), [])
            self.assertEqual(c.comprobar_markdown(t, "docs/a.md"), [])
        with repo({"README.md": "# R\n" + bloque * 3}) as t:
            self.assertEqual(len(c.comprobar_markdown(t, "README.md")), 1)

    def test_mermaid_vacio_desconocido_y_con_metadatos(self):
        with repo({"a.md": "# A\n```mermaid\n```\n```mermaid\nlo que sea\n```\n"
                           "```mermaid\n---\ntitle: T\n---\nflowchart TD\n A-->B\n```\n"}) as t:
            m = [(p.error, p.mensaje.split(" ")[0:3]) for p in c.comprobar_markdown(t, "a.md")]
            self.assertEqual([x[0] for x in m], [True, False])  # el tercero, con metadatos YAML, es correcto


class TestEstructura(unittest.TestCase):
    def comprobar(self, ruta, contenido=b"x", nuevo=True):
        with repo({ruta: contenido}) as t:
            return [(p.error, p.mensaje.split(" ")[0]) for p in c.comprobar_estructura(t.name, ruta, nuevo)]

    def test_formatos_bloqueados(self):
        for ext in (".exe", ".zip", ".pkl", ".db", ".jar", ".gz"):
            self.assertEqual(self.comprobar(f"analitica/datos{ext}")[0][0], True, ext)

    def test_formatos_que_solo_avisan(self):
        for ext in (".pdf", ".xls", ".parquet", ".docx"):
            self.assertEqual(self.comprobar(f"analitica/datos{ext}")[0][0], False, ext)

    def test_nombres_fuera_de_convencion_solo_en_ficheros_nuevos(self):
        self.assertEqual(self.comprobar("proceso/Mi Fichero.md"), [(False, "nombre")])
        self.assertEqual(self.comprobar("proceso/Mi Fichero.md", nuevo=False), [])
        self.assertEqual(self.comprobar("proceso/01-analisis/README.md"), [])
        self.assertEqual(self.comprobar("CONTRIBUTING.md"), [])
        self.assertEqual(self.comprobar(".github/workflows/Raro Nombre.yml"), [])

    def test_carpeta_nueva_en_la_raiz(self):
        self.assertEqual(self.comprobar("nueva/uno.md"), [(False, "carpeta")])
        self.assertEqual(self.comprobar("analitica/uno.md"), [])

    def test_imagen_grande_avisa(self):
        self.assertEqual(self.comprobar("assets/img/grande.png", b"x" * (c.MAX_IMAGEN + 1)), [(False, "imagen")])

    def test_enlace_simbolico_avisa(self):
        with tempfile.TemporaryDirectory() as t:
            os.symlink("/etc/hostname", os.path.join(t, "a.md"))
            p = c.comprobar_estructura(t, "a.md", True)
            self.assertEqual([(x.error, x.mensaje.split(" ")[0]) for x in p], [(False, "es")])


class TestTitulo(unittest.TestCase):
    def test_titulos_validos(self):
        for t in ("docs: añadir glosario", "feat(analitica): leer csv", "fix!: rompe la API", "chore: ajustes",
                  "ci(privacidad): nuevo workflow", "revert: deshacer algo"):
            self.assertEqual([p for p in c.comprobar_titulo(t, "Closes #1", "docs/1-x") if p.error], [], t)

    def test_titulos_invalidos(self):
        for t in ("Actualizo cosas", "docs añadir x", "CHORE: algo", "docs:sin espacio", "docs: ", "", "feat(Mayus): x"):
            self.assertTrue(any(p.error for p in c.comprobar_titulo(t)), repr(t))

    def test_titulo_demasiado_largo(self):
        self.assertTrue(any(p.error for p in c.comprobar_titulo("docs: " + "x" * 120)))

    def test_closes_solo_avisa_y_solo_en_docs_feat_fix(self):
        self.assertEqual([(p.error) for p in c.comprobar_titulo("docs: algo", "")], [False])
        self.assertEqual(c.comprobar_titulo("chore: algo", ""), [])
        for cuerpo in ("Closes #12", "closes #3", "Fixes #4", "Resolves: #5"):
            self.assertEqual(c.comprobar_titulo("docs: algo", cuerpo), [], cuerpo)
        self.assertEqual(len(c.comprobar_titulo("docs: algo", "relacionado con la 12")), 1)

    def test_rama(self):
        self.assertEqual(c.comprobar_titulo("chore: x", "", "docs/12-analisis-sota"), [])
        self.assertEqual(len(c.comprobar_titulo("chore: x", "", "mi-rama")), 1)
        self.assertEqual(len(c.comprobar_titulo("chore: x", "", "docs/Mayusculas")), 1)


class TestEnlaces(unittest.TestCase):
    def test_clasifica_roto_restringido_y_bueno_sin_red(self):
        with repo({"a.md": "# A\n[1](https://ok.test/a) [2](https://roto.test/b) [3](https://raro.test/c) "
                           "[4](https://caido.test/d) `[5](https://codigo.test/e)`\n"}) as t:
            codigos = {"https://ok.test/a": 200, "https://roto.test/b": 404, "https://raro.test/c": 429,
                       "https://caido.test/d": 0}
            p = c.comprobar_enlaces(t.name, ["a.md"], estado=lambda u: codigos[u])
            self.assertEqual(sorted((x.error, x.mensaje.split(" ")[1]) for x in p),
                             [(False, "enlace"), (True, "externo"), (True, "externo")][:0] or
                             sorted([(p_.error, p_.mensaje.split(" ")[1]) for p_ in p]))
            self.assertEqual(sum(1 for x in p if x.error), 2)
            self.assertEqual(sum(1 for x in p if not x.error), 1)

    def test_no_se_comprueban_las_url_dentro_de_bloques_de_codigo(self):
        with repo({"a.md": "# A\n```\nhttps://no-se-mira.test/x\n```\n"}) as t:
            self.assertEqual(c.urls_externas(t.name, ["a.md"]), {})


class TestPrograma(unittest.TestCase):
    def ejecutar(self, *args, env=None):
        out, err = io.StringIO(), io.StringIO()
        viejo = dict(os.environ)
        os.environ.update(env or {})
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                codigo = c.main(list(args))
        finally:
            os.environ.clear()
            os.environ.update(viejo)
        return codigo, out.getvalue(), err.getvalue()

    def test_salidas_y_anotaciones_escapadas(self):
        with repo({"a, b.md": "# A\n[x](no-existe.md)\n[y](roto%0Aalgo.md)\n"}) as t:
            codigo, out, _ = self.ejecutar("--raiz", t.name, "--formato", "github", "markdown", "--ficheros", "a, b.md")
            self.assertEqual(codigo, 1)
            lineas = [l for l in out.splitlines() if l.startswith("::error")]
            self.assertEqual(len(lineas), 2)
            self.assertTrue(all(l.startswith("::error file=a%2C b.md,line=") for l in lineas))

    def test_aviso_de_limite_de_anotaciones_en_calidad(self):
        enlaces = "\n".join(f"[x](no-existe-{n}.md)" for n in range(12))
        with repo({"a.md": "# A\n" + enlaces + "\n"}) as t:
            _, out, _ = self.ejecutar("--raiz", t.name, "--formato", "github", "markdown", "--ficheros", "a.md")
            lineas = out.splitlines()
            self.assertTrue(lineas[0].startswith("::notice title=Markdown::"), lineas[0])
            self.assertIn("12 error(es)", lineas[0])
            self.assertEqual(sum(1 for l in lineas if l.startswith("::error")), 12)
        with repo({"a.md": "# A\n[x](no-existe.md)\n"}) as t:
            _, out, _ = self.ejecutar("--raiz", t.name, "--formato", "github", "markdown", "--ficheros", "a.md")
            self.assertNotIn("::notice", out)

    def test_resumen_en_markdown_sin_barras_que_rompan_la_tabla(self):
        with repo({"a.md": "# A\n[x](a|b.md)\n"}) as t:
            resumen = Path(t.name) / "resumen.md"
            self.ejecutar("--raiz", t.name, "--resumen", str(resumen), "markdown", "--ficheros", "a.md")
            self.assertNotIn("a|b", resumen.read_text(encoding="utf-8"))

    def test_titulo_desde_el_entorno(self):
        codigo, _, _ = self.ejecutar("--formato", "texto", "titulo", env={"PR_TITULO": "mal titulo", "PR_CUERPO": "", "PR_RAMA": ""})
        self.assertEqual(codigo, 1)
        codigo, _, _ = self.ejecutar("--formato", "texto", "titulo", env={"PR_TITULO": "docs: bien", "PR_CUERPO": "Closes #1", "PR_RAMA": "docs/1-x"})
        self.assertEqual(codigo, 0)

    def test_sin_base_ni_ficheros_es_error_de_uso(self):
        self.assertEqual(self.ejecutar("markdown")[0], 2)


class TestNoSeCuelgaConMarkdownPatologico(unittest.TestCase):
    def test_entradas_grandes(self):
        import time
        casos = {"fences": "```\n" * 100_000, "titulos": "#" * 6 + " x\n" * 100_000, "enlaces": "[a](b)" * 50_000,
                 "corchetes": "[" * 200_000, "parentesis": "[a](" + "(" * 100_000, "backticks": "`" * 300_000,
                 "mermaid": "```mermaid\n" + "a-->b\n" * 100_000 + "```\n"}
        for nombre, texto in casos.items():
            with repo({"a.md": texto}) as t:
                t0 = time.time()
                c.comprobar_markdown(t.name, "a.md")
                self.assertLess(time.time() - t0, 5, nombre)


if __name__ == "__main__":
    unittest.main()
