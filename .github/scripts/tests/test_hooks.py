"""Pruebas de los hooks de Git (.githooks/): repositorios temporales reales y comandos de git de verdad.

Todos los datos son sintéticos y se escriben partidos ("a" "b") para que este fichero no los contenga enteros.

Ejecutar desde la raíz del repositorio:
    python3 -m unittest discover -s .github/scripts/tests -v
"""
import sys

sys.dont_write_bytecode = True  # las pruebas no dejan __pycache__ dentro del repositorio
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ_REPO = Path(__file__).resolve().parents[3]
CORREO = "usuario@" "correo-ficticio.es"
DNI = "12345678" "Z"
ENV = {**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"}


def git(cwd, *args, entrada=None, ok=True):
    r = subprocess.run(["git", "-c", "user.name=Prueba", "-c", "user.email=prueba@users.noreply.github.com",
                        "-c", "commit.gpgsign=false", "-C", str(cwd), *args],
                       input=entrada, capture_output=True, text=True, env=ENV)
    if ok and r.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} falló: {r.stderr}")
    return r


class Base(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.raiz = Path(self.t.name) / "repo"
        self.raiz.mkdir()
        git(self.raiz, "init", "-q", "-b", "main")
        for carpeta in (".githooks", ".github/scripts"):
            shutil.copytree(RAIZ_REPO / carpeta, self.raiz / carpeta, ignore=shutil.ignore_patterns("tests", "__pycache__"))
        (self.raiz / "README.md").write_text("# base\n", encoding="utf-8")
        git(self.raiz, "add", "-A")
        git(self.raiz, "commit", "-q", "--no-verify", "-m", "chore: base")
        git(self.raiz, "config", "core.hooksPath", ".githooks")
        git(self.raiz, "checkout", "-q", "-b", "docs/1-prueba")

    def escribir(self, nombre, contenido):
        ruta = self.raiz / nombre
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_bytes(contenido if isinstance(contenido, bytes) else contenido.encode("utf-8"))

    def commit(self, mensaje="docs: prueba"):
        return git(self.raiz, "commit", "-q", "-m", mensaje, ok=False)

    def n_commits(self):
        return int(git(self.raiz, "rev-list", "--count", "HEAD").stdout)


class TestPreCommit(Base):
    def test_commit_limpio_pasa(self):
        self.escribir("analitica/ventas.csv", "producto,precio\nlapiz,2\n")
        git(self.raiz, "add", "-A")
        r = self.commit()
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        self.assertEqual(self.n_commits(), 2)

    def test_no_se_puede_commitear_en_main(self):
        git(self.raiz, "checkout", "-q", "main")
        self.escribir("a.md", "# A\n")
        git(self.raiz, "add", "-A")
        r = self.commit()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("git checkout -b", r.stderr)
        self.assertEqual(self.n_commits(), 1)

    def test_datos_personales_bloquean_sin_mostrar_el_valor(self):
        self.escribir("analitica/clientes.csv", f"nombre,email\nAna,{CORREO}\n")
        self.escribir("notas.md", f"# N\nDNI {DNI}\n")
        git(self.raiz, "add", "-A")
        r = self.commit()
        self.assertNotEqual(r.returncode, 0)
        salida = r.stdout + r.stderr
        for valor in (CORREO, DNI):
            self.assertNotIn(valor, salida)
        self.assertIn("correo electrónico", salida)
        self.assertEqual(self.n_commits(), 1)

    def test_se_revisa_lo_que_esta_en_el_indice_no_el_disco(self):
        self.escribir("a.txt", f"contacto {CORREO}\n")
        git(self.raiz, "add", "a.txt")
        self.escribir("a.txt", "limpio\n")  # en disco ya está corregido, pero en el índice no
        self.assertNotEqual(self.commit().returncode, 0)
        git(self.raiz, "add", "a.txt")
        self.assertEqual(self.commit().returncode, 0)

    def test_lo_que_solo_esta_en_el_disco_no_bloquea(self):
        self.escribir("a.txt", "limpio\n")
        git(self.raiz, "add", "a.txt")
        self.escribir("a.txt", f"contacto {CORREO}\n")  # sin añadir al índice
        self.assertEqual(self.commit().returncode, 0)

    def test_lista_de_excepciones_se_respeta(self):
        self.escribir(".github/privacidad-permitidos.txt", "correo | analitica/sinteticos/* | * | inventados\n")
        self.escribir("analitica/sinteticos/a.csv", f"id,contacto\n1,{CORREO}\n")
        git(self.raiz, "add", "-A")
        self.assertEqual(self.commit().returncode, 0)

    def test_formatos_no_admitidos_bloquean_y_binarios_avisan(self):
        self.escribir("analitica/datos.zip", b"PK")
        git(self.raiz, "add", "-A")
        self.assertNotEqual(self.commit().returncode, 0)
        git(self.raiz, "rm", "-q", "--cached", "analitica/datos.zip")
        (self.raiz / "analitica/datos.zip").unlink()
        self.escribir("analitica/informe.pdf", b"%PDF-1.4")
        git(self.raiz, "add", "-A")
        r = self.commit()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("revisará a mano", r.stdout + r.stderr)

    def test_marcas_de_conflicto_bloquean_pero_no_dentro_de_codigo_markdown(self):
        self.escribir("a.py", "x = 1\n<<<<<<< HEAD\ny = 2\n=======\ny = 3\n>>>>>>> main\n")
        git(self.raiz, "add", "-A")
        r = self.commit()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("marca de conflicto", r.stderr)
        git(self.raiz, "rm", "-q", "-f", "--cached", "a.py")
        self.escribir("b.md", "# B\n\n```text\n<<<<<<< HEAD\n=======\n>>>>>>> main\n```\n")
        git(self.raiz, "add", "b.md")
        self.assertEqual(self.commit().returncode, 0)

    def test_enlace_roto_en_markdown_bloquea(self):
        self.escribir("a.md", "# A\n[x](no-existe.md)\n")
        git(self.raiz, "add", "-A")
        self.assertNotEqual(self.commit().returncode, 0)

    def test_commit_sin_cambios_de_ficheros_no_falla(self):
        r = git(self.raiz, "commit", "-q", "--allow-empty", "-m", "chore: vacio", ok=False)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_nombres_con_espacios(self):
        self.escribir("analitica/mi fichero.csv", f"id,contacto\n1,{CORREO}\n")
        git(self.raiz, "add", "-A")
        self.assertNotEqual(self.commit().returncode, 0)


class TestCommitMsg(Base):
    def probar(self, mensaje):
        self.escribir("analitica/x.csv", "a,b\n1,2\n")
        git(self.raiz, "add", "-A")
        return git(self.raiz, "commit", "-q", "-m", mensaje, ok=False)

    def test_mensajes_validos(self):
        for m in ("docs: añadir ejemplo", "feat(analitica): leer csv", "fix!: rompe algo", "chore: ajustes"):
            r = self.probar(m)
            self.assertEqual(r.returncode, 0, (m, r.stderr))
            git(self.raiz, "reset", "-q", "--soft", "HEAD~1")

    def test_mensajes_invalidos_explican_el_formato(self):
        for m in ("cambios", "Docs: mayúscula", "docs:sin espacio", "docs: " + "x" * 120):
            r = self.probar(m)
            self.assertNotEqual(r.returncode, 0, m)
            self.assertIn("Conventional Commits", r.stderr)
            self.assertIn("docs: añadir ejemplo", r.stderr)

    def test_fusion_fixup_y_revert_se_permiten(self):
        for m in ('Merge branch "main" into x', "fixup! docs: algo", 'Revert "docs: algo"'):
            self.assertEqual(self.probar(m).returncode, 0, m)
            git(self.raiz, "reset", "-q", "--soft", "HEAD~1")


class TestPrePush(Base):
    def setUp(self):
        super().setUp()
        self.remoto = Path(self.t.name) / "remoto.git"
        git(self.t.name, "init", "-q", "--bare", "-b", "main", str(self.remoto))
        git(self.raiz, "remote", "add", "origin", str(self.remoto))
        git(self.raiz, "push", "-q", "--no-verify", "origin", "main")
        git(self.raiz, "fetch", "-q", "origin")

    def subir(self, rama="docs/1-prueba", destino=None):
        return git(self.raiz, "push", "-q", "origin", f"{rama}:{destino or rama}", ok=False)

    def test_rama_limpia_se_sube(self):
        self.escribir("analitica/x.csv", "a,b\n1,2\n")
        git(self.raiz, "add", "-A")
        self.assertEqual(self.commit().returncode, 0)
        r = self.subir()
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_no_se_sube_a_main(self):
        self.escribir("a.md", "# A\n")
        git(self.raiz, "add", "-A")
        self.assertEqual(self.commit().returncode, 0)
        r = self.subir("docs/1-prueba", "main")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("protegida", r.stderr)

    def test_lo_que_se_colo_con_no_verify_se_detecta_al_subir_y_sin_valor(self):
        self.escribir("analitica/clientes.csv", f"nombre,email\nAna,{CORREO}\n")
        git(self.raiz, "add", "-A")
        git(self.raiz, "commit", "-q", "--no-verify", "-m", "docs: colado")
        r = self.subir()
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn(CORREO, r.stdout + r.stderr)
        heads = git(self.remoto, "branch", "--list", "docs/1-prueba").stdout
        self.assertEqual(heads.strip(), "")  # no se subió nada

    def test_segundo_push_solo_revisa_lo_nuevo(self):
        self.escribir("a.md", "# A\n")
        git(self.raiz, "add", "-A")
        self.assertEqual(self.commit().returncode, 0)
        self.assertEqual(self.subir().returncode, 0)
        self.escribir("b.md", "# B\n")
        git(self.raiz, "add", "-A")
        self.assertEqual(self.commit().returncode, 0)
        self.assertEqual(self.subir().returncode, 0)

    def test_borrar_una_rama_remota_no_se_revisa(self):
        self.escribir("a.md", "# A\n")
        git(self.raiz, "add", "-A")
        self.commit()
        self.subir()
        r = git(self.raiz, "push", "-q", "origin", "--delete", "docs/1-prueba", ok=False)
        self.assertEqual(r.returncode, 0, r.stderr)


class TestInstalarYEnvoltorios(Base):
    def test_instalar_configura_hooks_path(self):
        git(self.raiz, "config", "--unset", "core.hooksPath")
        r = subprocess.run([sys.executable, ".githooks/hooks.py", "instalar"], cwd=self.raiz, capture_output=True, text=True, env=ENV)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(git(self.raiz, "config", "core.hooksPath").stdout.strip(), ".githooks")

    def test_los_hooks_tienen_permiso_de_ejecucion(self):
        for h in ("pre-commit", "commit-msg", "pre-push"):
            self.assertTrue(os.access(RAIZ_REPO / ".githooks" / h, os.X_OK), h)

    def test_sin_python_el_envoltorio_avisa_y_deja_pasar(self):
        vacio = Path(self.t.name) / "vacio"
        vacio.mkdir()
        r = subprocess.run(["/bin/sh", ".githooks/pre-commit"], cwd=self.raiz, capture_output=True, text=True,
                           env={"PATH": str(vacio)})
        self.assertEqual(r.returncode, 0)
        self.assertIn("Python 3.11", r.stderr)

    def test_el_envoltorio_pasa_los_argumentos_y_la_entrada(self):
        msg = Path(self.t.name) / "msg"
        msg.write_text("cambios\n", encoding="utf-8")
        r = subprocess.run(["/bin/sh", ".githooks/commit-msg", str(msg)], cwd=self.raiz, capture_output=True, text=True, env=ENV)
        self.assertNotEqual(r.returncode, 0)
        r = subprocess.run(["/bin/sh", ".githooks/pre-push", "origin", "x"], cwd=self.raiz, input="", capture_output=True, text=True, env=ENV)
        self.assertEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
