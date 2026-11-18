"""Pruebas del detector de datos personales.

Todos los datos son SINTÉTICOS (inventados). Los valores se escriben como literales adyacentes
partidos ("1234" "5678Z") para que este fichero no contenga ningún dato que el propio detector
reconozca: así el CI no salta con sus propias pruebas.

Ejecutar desde la raíz del repositorio:
    python3 -m unittest discover -s .github/scripts/tests -v
"""
import sys

sys.dont_write_bytecode = True  # las pruebas no dejan __pycache__ dentro del repositorio
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

RAIZ_SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ_SCRIPTS))

import detectar_datos_personales as d  # noqa: E402

# ---- datos sintéticos (nunca reales) ----------------------------------------------------------
DNI_OK = "12345678" "Z"
DNI_MAL = "12345678" "A"
NIE_OK = "X" "1234567" "L"
IBAN_OK = "ES91 2100 0418 " "4502 0005 1332"
IBAN_MAL = "ES92 2100 0418 " "4502 0005 1332"
TARJETA_OK = "4111 1111 " "1111 1111"
TARJETA_MAL = "4111 1111 " "1111 1112"
NSS_OK = "28 12345678 " "40"
NSS_MAL = "28 12345678 " "41"
MOVIL = "612 345 " "678"
FIJO = "+34 91 234 " "5678"
CORREO = "usuario@" "correo-ficticio.es"
CORREO2 = "otra.persona@" "dominio-inventado.com"
FECHA = "14/03/" "2001"
CLAVE_PRIVADA = "-----BEGIN RSA " "PRIVATE KEY-----"
CONTRASENA = "pass" "word = \"Zx9Qw7Lm2Rt5\""
CONTRASENA_ENV = "DB_PASS" "WORD=Zx9Qw7Lm2Rt5"
TODOS_LOS_VALORES = [DNI_OK, NIE_OK, IBAN_OK, TARJETA_OK, NSS_OK, MOVIL, FIJO, CORREO, CORREO2, FECHA,
                     "Zx9Qw7Lm2Rt5", "12345678", "612" "345678"]


def tipos(nombre: str, contenido: bytes | str, ctx=None) -> list:
    """Escribe un fichero temporal, lo analiza y devuelve la lista de tipos detectados."""
    with tempfile.TemporaryDirectory() as t:
        ruta = Path(t) / nombre
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_bytes(contenido if isinstance(contenido, bytes) else contenido.encode("utf-8"))
        rec = d.analizar_fichero(t, nombre, ctx or d.Contexto())
        return sorted(h.tipo for h in rec.items)


def detalle(nombre: str, contenido, ctx=None):
    with tempfile.TemporaryDirectory() as t:
        ruta = Path(t) / nombre
        ruta.write_bytes(contenido if isinstance(contenido, bytes) else contenido.encode("utf-8"))
        return d.analizar_fichero(t, nombre, ctx or d.Contexto())


def zip_bytes(partes: dict) -> bytes:
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w", zipfile.ZIP_DEFLATED) as z:
        for nombre, contenido in partes.items():
            z.writestr(nombre, contenido)
    return b.getvalue()


class TestDocumentosDeIdentidad(unittest.TestCase):
    def test_dni_con_letra_valida_se_detecta(self):
        self.assertEqual(tipos("a.txt", f"DNI: {DNI_OK}\n"), ["dni"])

    def test_dni_con_letra_incorrecta_no_se_detecta(self):
        self.assertEqual(tipos("a.txt", f"código {DNI_MAL}\n"), [])

    def test_nie_valido_se_detecta(self):
        self.assertEqual(tipos("a.txt", f"NIE {NIE_OK}\n"), ["dni"])

    def test_dni_dentro_de_otra_cadena_no_se_detecta(self):
        self.assertEqual(tipos("a.txt", "hash a" + DNI_OK + "b\n"), [])


class TestCorreos(unittest.TestCase):
    def test_correo_normal_se_detecta(self):
        self.assertEqual(tipos("a.md", f"escribe a {CORREO}.\n"), ["correo"])

    def test_se_ignoran_noreply_y_dominios_de_ejemplo(self):
        for ok in ("12345" "+alumno@users.noreply.github.com", "a@example.com", "a@x.example.org",
                   "a@example.net", "git@github.com:org/repo.git"):
            self.assertEqual(tipos("a.md", ok + "\n"), [], ok)

    def test_dominio_permitido_en_el_contexto(self):
        ctx = d.Contexto(frozenset({"dominio-inventado.com"}))
        self.assertEqual(tipos("a.md", CORREO2 + "\n", ctx), [])
        self.assertEqual(tipos("a.md", CORREO + "\n", ctx), ["correo"])

    def test_decorador_y_arroba_sin_dominio_no_son_correos(self):
        self.assertEqual(tipos("a.py", "@pytest.mark.parametrize\nx = a @ b\n"), [])


class TestTelefonos(unittest.TestCase):
    def test_movil_y_fijo_con_prefijo(self):
        self.assertEqual(tipos("a.txt", MOVIL + "\n"), ["telefono"])
        self.assertEqual(tipos("a.txt", FIJO + "\n"), ["telefono"])

    def test_formatos_con_guiones_y_puntos(self):
        self.assertEqual(tipos("a.txt", "612" "-34-56-78" "\n"), ["telefono"])  # 9 dígitos con guiones
        self.assertEqual(tipos("a.txt", "612" ".345" ".678" "\n"), ["telefono"])
        self.assertEqual(tipos("a.txt", "61" "-34-56-78" "\n"), [])  # solo 8 dígitos

    def test_numeros_de_servicio_y_decimales_no_son_telefonos(self):
        self.assertEqual(tipos("a.txt", "900 123 " "456\n"), [])
        self.assertEqual(tipos("a.txt", "valor 0." "612" "345678\n"), [])

    def test_numero_largo_no_es_telefono(self):
        self.assertEqual(tipos("a.txt", "id 1" "612" "345678" "9\n"), [])


class TestDatosBancarios(unittest.TestCase):
    def test_iban_valido_con_y_sin_espacios(self):
        self.assertEqual(tipos("a.txt", IBAN_OK + "\n"), ["iban"])
        self.assertEqual(tipos("a.txt", IBAN_OK.replace(" ", "") + "\n"), ["iban"])

    def test_iban_con_checksum_incorrecto_no_se_detecta(self):
        self.assertEqual(tipos("a.txt", IBAN_MAL + "\n"), [])

    def test_iban_seguido_de_texto_se_detecta(self):
        self.assertEqual(tipos("a.txt", f"cuenta {IBAN_OK} de nada\n"), ["iban"])

    def test_tarjeta_luhn_valida(self):
        self.assertEqual(tipos("a.txt", TARJETA_OK + "\n"), ["tarjeta"])

    def test_tarjeta_luhn_invalida_o_repetida_no(self):
        self.assertEqual(tipos("a.txt", TARJETA_MAL + "\n"), [])
        self.assertEqual(tipos("a.txt", "4444 4444 " "4444 4444\n"), [])


class TestSeguridadSocialYNacimiento(unittest.TestCase):
    def test_nss_con_control_valido(self):
        self.assertEqual(tipos("a.txt", NSS_OK + "\n"), ["nss"])

    def test_nss_con_control_incorrecto_no(self):
        self.assertEqual(tipos("a.txt", NSS_MAL + "\n"), [])

    def test_fecha_solo_junto_a_una_palabra_de_nacimiento(self):
        self.assertEqual(tipos("a.txt", f"fecha de nacimiento: {FECHA}\n"), ["nacimiento"])
        self.assertEqual(tipos("a.txt", f"reunión el {FECHA}\n"), [])

    def test_fecha_en_columna_de_nacimiento(self):
        self.assertEqual(tipos("a.csv", f"id,fecha_nacimiento\n1,{FECHA}\n"), ["cabecera", "nacimiento"])

    def test_fecha_futura_no(self):
        self.assertEqual(tipos("a.txt", "nacimiento: 14/03/" "2999\n"), [])


class TestTablas(unittest.TestCase):
    def test_cabeceras_sospechosas_en_csv(self):
        h = detalle("a.csv", "nombre,apellidos,email,telefono,direccion,fecha_nacimiento,iban,dni\n")
        self.assertEqual(len([x for x in h.items if x.tipo == "cabecera"]), 7)  # nombre y apellidos cuentan una vez

    def test_cabeceras_en_ingles(self):
        h = detalle("a.csv", "first_name,last_name,phone,address,date_of_birth\n")
        self.assertGreaterEqual(len(h.items), 4)

    def test_cabeceras_inocentes_no_saltan(self):
        self.assertEqual(tipos("a.csv", "producto,precio,unidades\nlapiz,1.5,10\n"), [])

    def test_separador_punto_y_coma_y_tabulador(self):
        self.assertEqual(tipos("a.csv", f"id;contacto\n1;{CORREO}\n"), ["correo"])
        self.assertEqual(tipos("a.tsv", f"id\tcontacto\n1\t{CORREO}\n"), ["correo"])

    def test_la_linea_de_un_hallazgo_en_csv(self):
        h = detalle("a.csv", f"id,contacto\n1,x\n2,{CORREO}\n")
        self.assertEqual([(x.tipo, x.linea) for x in h.items], [("correo", 3)])

    def test_cabecera_en_texto_normal_no_salta(self):
        self.assertEqual(tipos("a.md", "nombre,email\n"), [])


def hoja_xlsx(filas: list, compartidas: list) -> dict:
    def celda(ref, v):
        if isinstance(v, int):
            return f'<c r="{ref}"><v>{v}</v></c>'
        return f'<c r="{ref}" t="s"><v>{compartidas.index(v)}</v></c>'
    cuerpo = ""
    for n, fila in enumerate(filas, 1):
        celdas = "".join(celda(f"{chr(65 + i)}{n}", v) for i, v in enumerate(fila))
        cuerpo += f'<row r="{n}">{celdas}</row>'
    return {
        "[Content_Types].xml": "<Types/>",
        "xl/workbook.xml": "<workbook/>",
        "xl/sharedStrings.xml": "<sst>" + "".join(f"<si><t>{s}</t></si>" for s in compartidas) + "</sst>",
        "xl/worksheets/sheet1.xml": f"<worksheet><sheetData>{cuerpo}</sheetData></worksheet>",
    }


class TestHojasDeCalculo(unittest.TestCase):
    def test_xlsx_detecta_cabecera_correo_y_numero(self):
        comp = ["Email", "Movil", "id", CORREO]
        partes = hoja_xlsx([["Email", "Movil"], [CORREO, int("612" "345678")]], comp)
        h = detalle("datos.xlsx", zip_bytes(partes))
        self.assertEqual(sorted((x.tipo, x.linea, x.lugar) for x in h.items),
                         [("cabecera", 1, "hoja 1"), ("cabecera", 1, "hoja 1"), ("correo", 2, "hoja 1"),
                          ("telefono", 2, "hoja 1")])

    def test_xlsx_inofensivo(self):
        partes = hoja_xlsx([["producto", "precio"], ["lapiz", 2]], ["producto", "precio", "lapiz"])
        self.assertEqual(tipos("datos.xlsx", zip_bytes(partes)), [])

    def test_xlsm_con_macros(self):
        partes = hoja_xlsx([["producto"], ["lapiz"]], ["producto", "lapiz"])
        partes["xl/vbaProject.bin"] = "binario"
        self.assertEqual(tipos("datos.xlsm", zip_bytes(partes)), ["macros"])

    def test_xlsx_comentarios_y_autor(self):
        partes = hoja_xlsx([["producto"], ["lapiz"]], ["producto", "lapiz"])
        partes["xl/comments1.xml"] = f"<comments><t>{CORREO}</t></comments>"
        partes["docProps/core.xml"] = "<cp><dc:creator>Alguien Inventado</dc:creator></cp>"
        h = detalle("datos.xlsx", zip_bytes(partes))
        self.assertEqual([x.tipo for x in h.items], ["correo"])
        self.assertEqual(len(h.avisos), 1)

    def test_ods(self):
        contenido = (
            "<office:document-content><table:table table:name=\"h\">"
            "<table:table-row><table:table-cell><text:p>Correo</text:p></table:table-cell></table:table-row>"
            f"<table:table-row><table:table-cell><text:p>{CORREO}</text:p></table:table-cell></table:table-row>"
            "</table:table></office:document-content>")
        h = detalle("datos.ods", zip_bytes({"content.xml": contenido}))
        self.assertEqual(sorted(x.tipo for x in h.items), ["cabecera", "correo"])

    def test_ods_con_macros(self):
        self.assertEqual(tipos("datos.ods", zip_bytes({"content.xml": "<a/>", "Basic/x.xml": "1"})), ["macros"])

    def test_zip_corrupto_solo_avisa(self):
        h = detalle("datos.xlsx", b"esto no es un zip")
        self.assertEqual(h.items, [])
        self.assertEqual(len(h.avisos), 1)

    def test_zip_con_miembro_enorme_se_rechaza(self):
        b = io.BytesIO()
        with zipfile.ZipFile(b, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("xl/sharedStrings.xml", b"\0" * (d.MAX_MIEMBRO + 1))
        self.assertEqual(tipos("datos.xlsx", b.getvalue()), ["tamano"])


def cuaderno(celdas: list) -> str:
    return json.dumps({"cells": celdas, "metadata": {}, "nbformat": 4, "nbformat_minor": 5}, indent=1)


class TestCuadernos(unittest.TestCase):
    def test_salida_con_correo_y_linea_de_la_celda(self):
        texto = cuaderno([
            {"cell_type": "code", "source": ["x = 1\n"], "outputs": []},
            {"cell_type": "code", "source": ["print(df)\n"],
             "outputs": [{"output_type": "stream", "name": "stdout", "text": [f"contacto: {CORREO}\n"]}]},
        ])
        h = detalle("a.ipynb", texto)
        self.assertEqual([(x.tipo, x.lugar) for x in h.items], [("correo", "celda 2 (salida)")])
        esperada = [n for n, l in enumerate(texto.splitlines(), 1) if '"cell_type"' in l][1]
        self.assertEqual(h.items[0].linea, esperada)

    def test_salida_en_data_text_plain_y_html(self):
        texto = cuaderno([{"cell_type": "code", "source": [], "outputs": [
            {"output_type": "execute_result", "data": {"text/plain": [CORREO], "text/html": [f"<td>{MOVIL}</td>"]}}]}])
        self.assertEqual(tipos("a.ipynb", texto), ["correo", "telefono"])

    def test_codigo_con_contrasena(self):
        texto = cuaderno([{"cell_type": "code", "source": [CONTRASENA + "\n"], "outputs": []}])
        self.assertEqual(tipos("a.ipynb", texto), ["secreto"])

    def test_imagen_en_salida_solo_avisa(self):
        texto = cuaderno([{"cell_type": "code", "source": [], "outputs": [
            {"output_type": "display_data", "data": {"image/png": "iVBORw0KGgo="}}]}])
        h = detalle("a.ipynb", texto)
        self.assertEqual(h.items, [])
        self.assertEqual(len(h.avisos), 1)

    def test_json_invalido_se_analiza_como_texto(self):
        h = detalle("a.ipynb", f"no es json {CORREO}")
        self.assertEqual([x.tipo for x in h.items], ["correo"])
        self.assertEqual(len(h.avisos), 1)


class TestSecretos(unittest.TestCase):
    def test_asignacion_literal(self):
        self.assertEqual(tipos("a.py", CONTRASENA + "\n"), ["secreto"])
        self.assertEqual(tipos("a.json", '{"api_' 'key": "Zx9Qw7Lm2Rt5"}\n'), ["secreto"])

    def test_variables_de_entorno_y_placeholders_no(self):
        for ok in ('pass' 'word = os.environ["DB_PASS"]', 'tok' 'en = "tu_clave_aqui"', 'api_' 'key = "xxxxxxxxxxxx"',
                   'sec' 'ret = "<pon-aqui-tu-secreto>"', 'pass' 'word = password_input'):
            self.assertEqual(tipos("a.py", ok + "\n"), [], ok)

    def test_valor_corto_no(self):
        self.assertEqual(tipos("a.py", 'pass' 'word = "abc"\n'), [])

    def test_formato_env_y_yaml_sin_comillas(self):
        self.assertEqual(tipos("config.txt", CONTRASENA_ENV + "\n"), ["secreto"])
        self.assertEqual(tipos("config.yml", "pass" "word: Zx9Qw7Lm2Rt5\n"), ["secreto"])

    def test_clave_privada(self):
        self.assertEqual(tipos("a.txt", CLAVE_PRIVADA + "\n"), ["clave-privada"])

    def test_ficheros_de_claves_por_nombre(self):
        for nombre in (".env", ".env.local", "servidor.pem", "firma.key", "id_" "rsa", "almacen.p12"):
            self.assertEqual(tipos(nombre, "x"), ["fichero-secreto"], nombre)
        for ok in (".env.example", ".env.sample", "clave.md"):
            self.assertEqual(tipos(ok, "texto"), [], ok)


class TestTamanoBinariosYEnlaces(unittest.TestCase):
    def test_fichero_de_mas_de_5_mb_falla(self):
        self.assertEqual(tipos("grande.csv", b"a,b\n" + b"x" * d.MAX_BYTES), ["tamano"])

    def test_binarios_no_soportados_solo_avisan(self):
        for nombre, datos in (("foto.png", b"\x89PNG\0\0"), ("informe.pdf", b"%PDF-1.4"), ("datos.parquet", b"PAR1"),
                              ("raro.bin", b"\0\1\2")):
            h = detalle(nombre, datos)
            self.assertEqual(h.items, [], nombre)
            self.assertEqual(len(h.avisos), 1, nombre)

    def test_enlace_simbolico_no_se_sigue(self):
        with tempfile.TemporaryDirectory() as t:
            os.symlink("/etc/hostname", os.path.join(t, "enlace.csv"))
            rec = d.analizar_fichero(t, "enlace.csv", d.Contexto())
            self.assertEqual(rec.items, [])
            self.assertEqual(len(rec.avisos), 1)

    def test_tope_de_hallazgos_por_fichero(self):
        filas = "\n".join(f"{n}x{CORREO.replace('usuario', 'u' + str(n))}" for n in range(d.MAX_POR_FICHERO + 20))
        rec = detalle("muchos.txt", filas)
        self.assertEqual(len(rec.items), d.MAX_POR_FICHERO)
        self.assertTrue(rec.truncado)


class TestEntradasPatologicas(unittest.TestCase):
    """Regresiones: estas entradas colgaban el detector (coste cuadrático). El CI procesa texto que controla el alumno."""

    LIMITE = 5.0

    def medir(self, nombre, contenido):
        import time
        t0 = time.time()
        rec = detalle(nombre, contenido)
        self.assertLess(time.time() - t0, self.LIMITE, nombre)
        return rec

    def test_lineas_con_separadores_repetidos_no_cuelgan(self):
        for texto in ("1-" * 150_000, "a@" + "-" * 150_000 + "a.com", "a@" + "b." * 60_000 + "com", "a." * 100_000):
            self.medir("a.txt", texto)

    def test_xml_con_etiquetas_sin_cerrar_falla_cerrado_y_rapido(self):
        casos = {
            "a.xlsx": {"xl/worksheets/sheet1.xml": "<worksheet><sheetData>" + '<row r="1">' * 40_000 + "</sheetData></worksheet>"},
            "b.xlsx": {"xl/sharedStrings.xml": "<sst>" + "<si>" * 40_000 + "</sst>"},
            "c.ods": {"content.xml": "<a><table:table>" + "<table:table-row>" * 40_000 + "</table:table></a>"},
        }
        for nombre, partes in casos.items():
            self.assertEqual([h.tipo for h in self.medir(nombre, zip_bytes(partes)).items], ["error-analisis"], nombre)

    def test_doctype_se_rechaza_sin_expandir_entidades(self):
        bomba = ('<?xml version="1.0"?><!DOCTYPE l [<!ENTITY a "aaaaaaaaaa"><!ENTITY b "&a;&a;&a;&a;&a;&a;&a;&a;&a;&a;">]>'
                 '<sst><si><t>&b;</t></si></sst>')
        rec = self.medir("a.xlsx", zip_bytes({"xl/sharedStrings.xml": bomba}))
        self.assertEqual([h.tipo for h in rec.items], ["error-analisis"])

    def test_hoja_grande_y_valida_es_lineal(self):
        filas = "".join(f'<row r="{i}"><c r="A{i}"><v>{i}</v></c></row>' for i in range(1, 60_001))
        rec = self.medir("a.xlsx", zip_bytes({"xl/worksheets/sheet1.xml": f"<worksheet><sheetData>{filas}</sheetData></worksheet>"}))
        self.assertEqual(rec.items, [])


class TestExcepciones(unittest.TestCase):
    def escribir(self, texto: str) -> str:
        f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
        f.write(texto)
        f.close()
        self.addCleanup(os.unlink, f.name)
        return f.name

    def hallazgo(self, tipo, valor, fichero="analitica/a.csv"):
        return d.Hallazgo(fichero, 1, tipo, huella=d.huella(tipo, valor))

    def test_comodin_por_fichero(self):
        p = d.cargar_permitidos(self.escribir(f"correo | analitica/sinteticos/* | * | datos inventados\n"))
        self.assertTrue(d.esta_permitido(self.hallazgo("correo", CORREO, "analitica/sinteticos/x.csv"), p))
        self.assertFalse(d.esta_permitido(self.hallazgo("correo", CORREO, "analitica/otro/x.csv"), p))

    def test_huella_solo_permite_ese_valor(self):
        h = d.huella("correo", CORREO)
        p = d.cargar_permitidos(self.escribir(f"correo | * | {h} | contacto institucional\n"))
        self.assertTrue(d.esta_permitido(self.hallazgo("correo", CORREO), p))
        self.assertTrue(d.esta_permitido(self.hallazgo("correo", CORREO.upper()), p))  # normaliza mayúsculas
        self.assertFalse(d.esta_permitido(self.hallazgo("correo", CORREO2), p))

    def test_cabecera_literal_y_dominio(self):
        p = d.cargar_permitidos(self.escribir(
            "cabecera | analitica/productos.csv | nombre y apellidos | son nombres de producto\n"
            "dominio | * | dominio-inventado.com | dominio ficticio\n"))
        cab = d.Hallazgo("analitica/productos.csv", 1, "cabecera", huella=d.literal_categoria("nombre y apellidos"))
        self.assertTrue(d.esta_permitido(cab, p))
        self.assertEqual(d.dominios_permitidos(p), frozenset({"dominio-inventado.com"}))

    def test_nunca_se_permiten_claves_privadas_ni_tamano_ni_rutas(self):
        for tipo in ("clave-privada", "tamano", "ruta-protegida"):
            self.assertFalse(d.esta_permitido(d.Hallazgo("x", 1, tipo), [d.Permitido(tipo, "*", "*", "m", 1)]))
        with self.assertRaises(d.ErrorConfig):
            d.cargar_permitidos(self.escribir("clave-privada | * | * | no debería poder\n"))

    def test_lineas_mal_formadas_fallan_cerrado(self):
        for mala in ("correo | * | * |\n", "correo | * | huella-falsa | m\n", "secreto | * | sha256:" + "0" * 64 + " | m\n",
                     "inventado | * | * | m\n", "solo tres | campos | aqui\n"):
            with self.assertRaises(d.ErrorConfig, msg=mala):
                d.cargar_permitidos(self.escribir(mala))

    def test_comentarios_y_lineas_vacias(self):
        self.assertEqual(d.cargar_permitidos(self.escribir("# nada\n\n   \n")), [])


class TestGuardiaDeRutas(unittest.TestCase):
    CAMBIOS = [".github/workflows/pr-privacidad.yml", ".github/scripts/detectar_datos_personales.py",
               ".github/privacidad-permitidos.txt", ".github/CODEOWNERS", ".githooks/pre-commit", "analitica/x.csv",
               "README.md"]

    def test_un_alumno_no_puede_tocar_rutas_protegidas(self):
        h = d.guardia_rutas(self.CAMBIOS, "alumno-inventado", "profeFPInfor")
        self.assertEqual([x.fichero for x in h], self.CAMBIOS[:5])
        self.assertTrue(all(x.tipo == "ruta-protegida" for x in h))

    def test_el_code_owner_si_sin_distinguir_mayusculas(self):
        self.assertEqual(d.guardia_rutas(self.CAMBIOS, "PROFEfpinfor", "profeFPInfor"), [])

    def test_autor_vacio_falla_cerrado(self):
        self.assertEqual(len(d.guardia_rutas(self.CAMBIOS, "", "profeFPInfor")), 5)

    def test_rutas_normales_no(self):
        self.assertEqual(d.guardia_rutas(["analitica/x.csv", ".github/ISSUE_TEMPLATE/a.md"], "alumno", "profeFPInfor"), [])


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=Prueba", "-c", "user.email=prueba@users.noreply.github.com",
                    "-c", "commit.gpgsign=false", "-C", str(cwd), *args], check=True, capture_output=True)


class TestPuntoAPunto(unittest.TestCase):
    """Simula un PR: repositorio con rama base y rama del alumno, y ejecuta main() como lo hace el CI."""

    def montar(self, ficheros: dict, base_extra: dict | None = None):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        raiz = Path(t.name)
        git(raiz, "init", "-q", "-b", "main")
        for nombre, c in (base_extra or {"README.md": "base\n"}).items():
            (raiz / nombre).parent.mkdir(parents=True, exist_ok=True)
            (raiz / nombre).write_text(c, encoding="utf-8")
        git(raiz, "add", "-A")
        git(raiz, "commit", "-q", "-m", "base")
        git(raiz, "checkout", "-q", "-b", "alumno")
        for nombre, c in ficheros.items():
            (raiz / nombre).parent.mkdir(parents=True, exist_ok=True)
            (raiz / nombre).write_bytes(c if isinstance(c, bytes) else c.encode("utf-8"))
        git(raiz, "add", "-A")
        git(raiz, "commit", "-q", "-m", "pr")
        return raiz

    def ejecutar(self, raiz, *extra):
        resumen = Path(raiz) / "resumen.md"
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            codigo = d.main(["--base", "main", "--raiz", str(raiz), "--formato", "github",
                             "--resumen", str(resumen), *extra])
        return codigo, out.getvalue(), err.getvalue(), resumen.read_text(encoding="utf-8") if resumen.exists() else ""

    def test_pr_limpio_sale_0(self):
        raiz = self.montar({"analitica/ventas.csv": "producto,precio\nlapiz,2\n"})
        codigo, out, err, resumen = self.ejecutar(raiz)
        self.assertEqual(codigo, 0, out + err)
        self.assertIn("sin hallazgos", resumen)

    def test_pr_con_datos_sale_1_y_nunca_imprime_el_valor(self):
        raiz = self.montar({
            "analitica/clientes con espacios.csv": f"nombre,email,telefono\nAna,{CORREO},{MOVIL}\n",
            "analitica/notas.md": f"DNI {DNI_OK}, IBAN {IBAN_OK}, tarjeta {TARJETA_OK}, nacimiento {FECHA}\n{CONTRASENA}\n",
            "analitica/datos.xlsx": zip_bytes(hoja_xlsx([["Email"], [CORREO2]], ["Email", CORREO2])),
        })
        codigo, out, err, resumen = self.ejecutar(raiz)
        self.assertEqual(codigo, 1)
        self.assertIn("clientes con espacios.csv", out)  # el nombre con espacios se maneja bien
        for texto in (out, err, resumen):
            for valor in TODOS_LOS_VALORES:
                self.assertNotIn(valor, texto, f"se ha impreso un valor sensible: {valor[:3]}…")
        self.assertRegex(out, r"::error file=analitica/clientes con espacios\.csv,line=\d+,title=Privacidad::")
        self.assertIn("valor no mostrado", out)

    def test_solo_se_analizan_los_ficheros_del_pr(self):
        raiz = self.montar({"nuevo.md": "limpio\n"}, base_extra={"viejo.md": f"{CORREO}\n"})
        codigo, out, err, _ = self.ejecutar(raiz)
        self.assertEqual(codigo, 0, out + err)  # el correo ya estaba en la base, no es del PR

    def test_ficheros_borrados_no_se_analizan(self):
        raiz = self.montar({"nuevo.md": "limpio\n"}, base_extra={"viejo.md": "x\n"})
        git(raiz, "rm", "-q", "viejo.md")
        git(raiz, "commit", "-q", "-m", "borra")
        self.assertEqual(self.ejecutar(raiz)[0], 0)

    def test_nombres_con_caracteres_raros_se_escapan_en_la_anotacion(self):
        raiz = self.montar({"a, b: c%d\ne.txt": f"{CORREO}\n"})
        codigo, out, _, resumen = self.ejecutar(raiz)
        self.assertEqual(codigo, 1)
        linea = [l for l in out.splitlines() if l.startswith("::error")]
        self.assertEqual(len(linea), 1)  # el salto de línea del nombre no rompió la anotación
        self.assertIn("file=a%2C b%3A c%25d%0Ae.txt", linea[0])
        self.assertNotIn("\n::", resumen)

    def test_guardia_de_rutas_en_el_pr(self):
        raiz = self.montar({".github/workflows/pr-privacidad.yml": "name: x\n"})
        self.assertEqual(self.ejecutar(raiz, "--autor", "un-alumno")[0], 1)
        self.assertEqual(self.ejecutar(raiz, "--autor", "profeFPInfor")[0], 0)

    def test_excepciones_del_pr_se_aplican(self):
        raiz = self.montar({"analitica/sinteticos/a.csv": f"id,contacto\n1,{CORREO}\n",
                            ".github/privacidad-permitidos.txt": "correo | analitica/sinteticos/* | * | datos inventados\n"})
        self.assertEqual(self.ejecutar(raiz, "--autor", "profeFPInfor")[0], 0)
        self.assertEqual(self.ejecutar(raiz, "--autor", "un-alumno")[0], 1)  # toca la lista sin ser el code owner

    def test_lista_de_excepciones_rota_falla_cerrado(self):
        raiz = self.montar({".github/privacidad-permitidos.txt": "esto no es una excepcion valida\n"})
        self.assertEqual(self.ejecutar(raiz)[0], 2)

    def test_base_inexistente_o_invalida_da_error(self):
        raiz = self.montar({"a.md": "x\n"})
        for base in ("no-existe", "-evil", "a b", "x..y;rm"):
            err = io.StringIO()
            with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(d.main([f"--base={base}", "--raiz", str(raiz)]), 2, base)


class TestAyudantes(unittest.TestCase):
    def test_huella_por_entrada_estandar(self):
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            sys.stdin = io.StringIO(CORREO.upper() + "\n")
            try:
                self.assertEqual(d.main(["--huella", "correo"]), 0)
            finally:
                sys.stdin = sys.__stdin__
        h = salida.getvalue().strip()
        self.assertRegex(h, r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(h, d.huella("correo", CORREO))

    def test_sanear_y_escapes(self):
        self.assertEqual(d.sanear("a|b`c<d>\n"), "a?b?c?d??")
        self.assertEqual(d.escapar_propiedad("a:b,c%\r\n"), "a%3Ab%2Cc%25%0D%0A")
        self.assertEqual(d.escapar_dato("a:b,c"), "a:b,c")
        self.assertEqual(d.a_utf8("a\udcffb"), "a?b")

    def test_los_hallazgos_no_exponen_el_valor_ni_en_repr(self):
        c = d.Coincidencia(0, 1, "correo", CORREO)
        self.assertNotIn(CORREO, repr(c))
        h = d.Hallazgo("f", 1, "correo", huella=d.huella("correo", CORREO))
        self.assertNotIn("sha256", repr(h))


class TestElRepositorioSePasaSuPropiaComprobacion(unittest.TestCase):
    """El PR que añade el CI no debe saltar con sus propios ficheros (pruebas incluidas)."""

    def test_ficheros_del_ci_sin_hallazgos(self):
        raiz = RAIZ_SCRIPTS.parents[1]
        candidatos = [".github/scripts/detectar_datos_personales.py", ".github/scripts/tests/test_detectar.py",
                      ".github/workflows/pr-privacidad.yml", ".github/privacidad-permitidos.txt"]
        existentes = [c for c in candidatos if (raiz / c).exists()]
        self.assertGreaterEqual(len(existentes), 2)
        permitidos = d.cargar_permitidos(str(raiz / ".github/privacidad-permitidos.txt"))
        ctx = d.Contexto(d.dominios_permitidos(permitidos))
        for c in existentes:
            rec = d.analizar_fichero(str(raiz), c, ctx)
            self.assertEqual([(h.linea, h.tipo) for h in rec.items if not d.esta_permitido(h, permitidos)], [], c)


if __name__ == "__main__":
    unittest.main()
