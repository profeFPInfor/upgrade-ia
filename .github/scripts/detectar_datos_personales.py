#!/usr/bin/env python3
"""Detecta datos personales y secretos en los ficheros que cambia un pull request.

Solo usa la biblioteca estándar (Python 3.11 o superior). Se ejecuta en el CI `pr-privacidad`
y también en local.

REGLA DE ORO: el valor detectado NO se imprime nunca (ni en pantalla, ni en las anotaciones,
ni en el resumen). Los registros de Actions de un repositorio público son públicos. Solo se
muestran fichero, línea y tipo de dato. Tampoco se muestra ningún hash del valor: un hash de un
teléfono o de un DNI se puede recuperar probando todas las combinaciones.

Uso en el CI:
  detectar_datos_personales.py --base origin/main --autor <login del autor del PR>

Uso en local, sobre ficheros concretos:
  detectar_datos_personales.py --ficheros analitica/datos.csv notebook.ipynb

Calcular la huella de un valor para la lista de excepciones (el valor entra por la entrada
estándar, nunca por argumentos, para que no quede en el historial de la terminal):
  echo -n 'valor' | detectar_datos_personales.py --huella correo

Código de salida: 0 sin hallazgos, 1 con hallazgos, 2 error de configuración o de uso.
"""
from __future__ import annotations

import argparse
import csv
import fnmatch
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import unicodedata
import xml.parsers.expat as expat
import zipfile
from dataclasses import dataclass, field
from datetime import date

if sys.version_info < (3, 11):  # pragma: no cover
    print("Se necesita Python 3.11 o superior.", file=sys.stderr)
    sys.exit(2)

# ----------------------------------------------------------------------------------------------
# Límites
# ----------------------------------------------------------------------------------------------
MAX_BYTES = 5 * 1024 * 1024            # tamaño máximo de un fichero analizable
MAX_DESCOMPRIMIDO = 100 * 1024 * 1024  # suma máxima de un zip (xlsx, ods) ya descomprimido
MAX_MIEMBRO = 20 * 1024 * 1024         # tamaño máximo de una parte de un zip
MAX_MIEMBROS_ZIP = 2000
VENTANA = 20000                        # caracteres de una línea que se analizan de una vez
SOLAPE = 200
MAX_POR_FICHERO = 100                  # hallazgos que se listan por fichero
MAX_FILAS_RESUMEN = 200

# slug -> etiqueta que se muestra (texto fijo: nunca contiene el valor detectado)
TIPOS = {
    "correo": "correo electrónico",
    "dni": "DNI/NIE",
    "telefono": "teléfono",
    "iban": "IBAN",
    "tarjeta": "tarjeta de pago",
    "nss": "nº de la Seguridad Social",
    "nacimiento": "fecha de nacimiento",
    "cabecera": "cabecera de datos personales",
    "secreto": "posible secreto (clave, token o contraseña)",
    "clave-privada": "clave privada",
    "fichero-secreto": "fichero de claves o de entorno",
    "macros": "macros en el documento",
    "tamano": "fichero demasiado grande (reduce su tamaño)",
    "ruta-protegida": "ruta protegida modificada por quien no es el code owner",
    "error-analisis": "no se pudo analizar el fichero (pide revisión al profesor)",
}
# Tipos que pueden aparecer en la lista de excepciones, y cómo se identifica el valor.
CON_HUELLA = {"correo", "dni", "telefono", "iban", "tarjeta", "nss", "nacimiento"}
SOLO_COMODIN = {"secreto", "fichero-secreto", "macros"}
LITERAL = {"cabecera", "dominio"}
TIPOS_PERMITIBLES = CON_HUELLA | SOLO_COMODIN | LITERAL

RUTAS_PROTEGIDAS = (
    ".github/workflows/*",
    ".github/scripts/*",
    ".githooks/*",
    ".github/privacidad-permitidos.txt",
    ".github/CODEOWNERS",
)


class ErrorConfig(Exception):
    """Error de configuración o de uso (código de salida 2)."""


# ----------------------------------------------------------------------------------------------
# Normalización y huellas
# ----------------------------------------------------------------------------------------------
def quitar_acentos(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


def norm_cabecera(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", quitar_acentos(s).lower()).strip("_")


def norm_valor(tipo: str, v: str) -> str:
    if tipo == "correo":
        return v.strip().lower()
    if tipo == "dni":
        return re.sub(r"[\s-]", "", v).upper()
    if tipo == "iban":
        return re.sub(r"[\s-]", "", v).upper()
    if tipo in ("telefono", "tarjeta", "nss"):
        d = re.sub(r"\D", "", v)
        return d[-9:] if tipo == "telefono" else d
    if tipo == "nacimiento":
        return re.sub(r"\s", "", v)
    return v.strip()


def huella(tipo: str, valor: str) -> str:
    return "sha256:" + hashlib.sha256(f"{tipo}:{norm_valor(tipo, valor)}".encode("utf-8")).hexdigest()


# ----------------------------------------------------------------------------------------------
# Modelo
# ----------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Hallazgo:
    fichero: str
    linea: int
    tipo: str
    lugar: str = ""          # "hoja 2", "celda 5"... (nunca un valor)
    huella: str = field(default="", repr=False, compare=False)


@dataclass(frozen=True)
class Aviso:
    fichero: str
    mensaje: str


@dataclass
class Contexto:
    dominios_permitidos: frozenset = frozenset()


@dataclass(frozen=True)
class Coincidencia:
    inicio: int
    fin: int
    tipo: str
    valor: str = field(repr=False)


class Recolector:
    """Acumula los hallazgos de un fichero sin duplicados y con un tope."""

    def __init__(self, fichero: str):
        self.fichero = fichero
        self.items: list[Hallazgo] = []
        self.avisos: list[Aviso] = []
        self._vistos: set = set()
        self.truncado = False

    def add(self, linea: int, tipo: str, valor: str | None = None, lugar: str = "", literal: str | None = None):
        h = literal if literal is not None else (huella(tipo, valor) if (valor is not None and tipo in CON_HUELLA) else "")
        clave = (linea, tipo, h, lugar)
        if clave in self._vistos:
            return
        if len(self.items) >= MAX_POR_FICHERO:
            self.truncado = True
            return
        self._vistos.add(clave)
        self.items.append(Hallazgo(self.fichero, linea, tipo, lugar, h))

    def aviso(self, mensaje: str):
        self.avisos.append(Aviso(self.fichero, mensaje))


# ----------------------------------------------------------------------------------------------
# Detectores de línea
# ----------------------------------------------------------------------------------------------
LETRAS_DNI = "TRWAGMYFPDXBNJZSQVHLCKE"
RE_DNI = re.compile(r"(?<![A-Za-z0-9])(\d{8})[ -]?([A-Za-z])(?![A-Za-z0-9])")
RE_NIE = re.compile(r"(?<![A-Za-z0-9])([XYZxyz])[ -]?(\d{7})[ -]?([A-Za-z])(?![A-Za-z0-9])")


def dni_valido(numero: int, letra: str) -> bool:
    return LETRAS_DNI[numero % 23] == letra.upper()


RE_TEL = re.compile(r"(?<![\w+])(?<!\d[.,])(?:(?:\+|00)34[ .\-]?)?((?:\d[ .\-]?){8}\d)(?![\w])")
RE_TEL_VALIDO = re.compile(r"6\d{8}|7[1-4]\d{7}|8[1-8]\d{7}|9[1-8]\d{7}")

RE_CORREO = re.compile(
    r"(?<![\w.%+\-])([A-Za-z0-9][A-Za-z0-9._%+\-]*)@((?:[A-Za-z0-9](?:[A-Za-z0-9\-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,})(?![\w\-]|@)"
)
DOMINIOS_EJEMPLO = ("example.com", "example.org", "example.net")

RE_IBAN = re.compile(r"(?<![A-Za-z0-9])([A-Za-z]{2}\d{2}(?:[ -]?[A-Za-z0-9]{4}){2,7}(?:[ -]?[A-Za-z0-9]{1,4})?)(?![A-Za-z0-9])")
LONG_IBAN = {"ES": 24, "FR": 27, "DE": 22, "IT": 27, "PT": 25, "GB": 22, "NL": 18, "BE": 16, "AD": 24,
             "IE": 22, "LU": 20, "CH": 21, "AT": 20}

RE_TARJETA = re.compile(r"(?<!\w)(?:\d[ -]?){12,18}\d(?!\w)")
RE_NSS = re.compile(r"(?<!\w)(\d{2})[ /-]?(\d{8})[ /-]?(\d{2})(?!\w)")

RE_FECHA = re.compile(r"(?<!\d)(?:(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})|(\d{4})[/\-.](\d{1,2})[/\-.](\d{1,2}))(?!\d)")
RE_CLAVE_NACIMIENTO = re.compile(r"nacimiento|nacid[oa]|\bf\.? ?nac|\bnac\.|birth|\bborn\b|\bdob\b")

PRIORIDAD = {"iban": 0, "tarjeta": 1, "nss": 2, "dni": 3, "correo": 4, "telefono": 5, "nacimiento": 6}


def iban_valido(s: str) -> bool:
    s = re.sub(r"[\s-]", "", s).upper()
    if not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]{11,30}", s):
        return False
    esperado = LONG_IBAN.get(s[:2])
    if esperado is not None and len(s) != esperado:
        return False
    reordenado = s[4:] + s[:4]
    numero = "".join(str(int(c, 36)) for c in reordenado)
    return int(numero) % 97 == 1


def iban_en(candidato: str) -> str | None:
    """Prueba el candidato entero y luego recortado por la derecha en límites de grupo."""
    cortes = [len(candidato)] + [i for i in range(len(candidato) - 1, 14, -1) if candidato[i] in " -"]
    for fin in cortes:
        trozo = candidato[:fin]
        if len(re.sub(r"[\s-]", "", trozo)) >= 15 and iban_valido(trozo):
            return trozo
    return None


def luhn(digitos: str) -> bool:
    total = 0
    for i, c in enumerate(reversed(digitos)):
        n = int(c)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def prefijo_tarjeta_valido(d: str) -> bool:
    n = len(d)
    p2, p4 = int(d[:2]), int(d[:4])
    return (
        (d[0] == "4" and n in (13, 16, 19))
        or (51 <= p2 <= 55 and n == 16)
        or (2221 <= p4 <= 2720 and n == 16)
        or (d[:2] in ("34", "37") and n == 15)
        or (d[:4] == "6011" and n in (16, 19))
        or (d[:2] == "65" and n == 16)
        or (d[:2] in ("36", "38") and n == 14)
        or (d[:2] == "35" and n in (16, 19))
    )


def nss_valido(provincia: str, numero: str, control: str) -> bool:
    n = int(numero)
    base = int(provincia) * 10_000_000 + n if n < 10_000_000 else int(provincia + numero)
    return base % 97 == int(control)


def fecha_plausible(m: re.Match) -> bool:
    try:
        if m.group(1):
            d, mes, a = int(m.group(1)), int(m.group(2)), int(m.group(3))
        else:
            a, mes, d = int(m.group(4)), int(m.group(5)), int(m.group(6))
        f = date(a, mes, d)
    except ValueError:
        return False
    return 1900 <= a and f <= date.today()


def correo_ignorado(local: str, dominio: str, ctx: Contexto) -> bool:
    d = dominio.lower()
    if d == "users.noreply.github.com" or d.endswith(".users.noreply.github.com"):
        return True
    if d in DOMINIOS_EJEMPLO or any(d.endswith("." + x) for x in DOMINIOS_EJEMPLO):
        return True
    if local.lower() == "git" and d == "github.com":
        return True
    return d in ctx.dominios_permitidos or any(d.endswith("." + x) for x in ctx.dominios_permitidos)


def buscar(linea: str, ctx: Contexto, forzar: str | None = None) -> list[Coincidencia]:
    """Devuelve las coincidencias de datos personales de una línea o de una celda.

    `forzar` ("nacimiento" o "nss") lo da la cabecera de la columna en las tablas.
    """
    candidatas: list[Coincidencia] = []

    for m in RE_IBAN.finditer(linea):
        buena = iban_en(m.group(1))
        if buena:
            candidatas.append(Coincidencia(m.start(1), m.start(1) + len(buena), "iban", buena))

    for m in RE_TARJETA.finditer(linea):
        d = re.sub(r"\D", "", m.group(0))
        if 13 <= len(d) <= 19 and len(set(d)) > 1 and luhn(d) and prefijo_tarjeta_valido(d):
            candidatas.append(Coincidencia(m.start(), m.end(), "tarjeta", d))

    for m in RE_NSS.finditer(linea):
        if nss_valido(*m.groups()):
            candidatas.append(Coincidencia(m.start(), m.end(), "nss", "".join(m.groups())))
    if forzar == "nss":
        for m in re.finditer(r"(?<!\d)\d{10,12}(?!\d)", linea):
            candidatas.append(Coincidencia(m.start(), m.end(), "nss", m.group(0)))

    for m in RE_DNI.finditer(linea):
        if dni_valido(int(m.group(1)), m.group(2)):
            candidatas.append(Coincidencia(m.start(), m.end(), "dni", m.group(1) + m.group(2)))
    for m in RE_NIE.finditer(linea):
        numero = int(str("XYZ".index(m.group(1).upper())) + m.group(2))  # X=0, Y=1, Z=2
        if dni_valido(numero, m.group(3)):
            candidatas.append(Coincidencia(m.start(), m.end(), "dni", m.group(1) + m.group(2) + m.group(3)))

    for m in RE_CORREO.finditer(linea):
        if not correo_ignorado(m.group(1), m.group(2), ctx):
            candidatas.append(Coincidencia(m.start(), m.end(), "correo", m.group(0)))

    for m in RE_TEL.finditer(linea):
        d = re.sub(r"\D", "", m.group(1))
        if len(d) == 9 and RE_TEL_VALIDO.fullmatch(d):
            candidatas.append(Coincidencia(m.start(), m.end(), "telefono", d))

    if forzar == "nacimiento" or RE_CLAVE_NACIMIENTO.search(quitar_acentos(linea).lower()):
        for m in RE_FECHA.finditer(linea):
            if fecha_plausible(m):
                candidatas.append(Coincidencia(m.start(), m.end(), "nacimiento", m.group(0)))

    # Si dos detectores marcan el mismo trozo, gana el más específico.
    candidatas.sort(key=lambda c: (PRIORIDAD[c.tipo], c.inicio))
    elegidas: list[Coincidencia] = []
    for c in candidatas:
        if not any(c.inicio < e.fin and e.inicio < c.fin for e in elegidas):
            elegidas.append(c)
    return elegidas


# ----------------------------------------------------------------------------------------------
# Secretos
# ----------------------------------------------------------------------------------------------
RE_CLAVE_PRIVADA = re.compile(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----")
# Los nombres de variable se acotan a 40 caracteres a cada lado. Con `*` (sin límite) la expresión se reintentaba desde
# cada posición de una línea como `1-1-1-1-...` y el coste era cuadrático: un fichero así colgaba el CI.
_NOMBRE_SECRETO = r"[A-Za-z0-9_.\-]{0,40}(?:api[_\-]?key|apikey|access[_\-]?key|secret|token|passwd|password|pwd|contrase[ñn]a)[A-Za-z0-9_.\-]{0,40}"
RE_SECRETO_ENTRECOMILLADO = re.compile(
    # El valor entre comillas no lleva espacios: así `"secreto": "texto descriptivo largo"` no salta. Límite conocido:
    # una contraseña con espacios (una frase) no se detecta con este patrón.
    r"(?i)(?<![A-Za-z0-9_])" + _NOMBRE_SECRETO + r"[\"']?\s*[:=]\s*(?P<q>[\"'])(?P<v>[^\"'\s]{8,})(?P=q)"
)
RE_SECRETO_SIN_COMILLAS = re.compile(
    r"(?im)^\s*(?:export\s+)?" + _NOMBRE_SECRETO + r"\s*[:=]\s*(?P<v>[^\s\"'#$<{(\[]{8,})\s*(?:#.*)?$"
)
MARCAS_PLACEHOLDER = ("xxxx", "****", "changeme", "cambiame", "cambiar", "tu_", "tu-", "tuclave", "your", "example",
                      "ejemplo", "placeholder", "<", "${", "{{", "os.environ", "getenv", "none", "null", "todo",
                      "aqui", "here", "...", "dummy", "secret_key_here", "contraseña", "password")


def es_placeholder(valor: str) -> bool:
    v = valor.strip().lower()
    if len(set(v)) <= 2:
        return True
    if v.startswith(("$", "%", "@")):
        return True
    return any(marca in v for marca in MARCAS_PLACEHOLDER)


def hay_secreto(linea: str) -> bool:
    for m in RE_SECRETO_ENTRECOMILLADO.finditer(linea):
        if not es_placeholder(m.group("v")):
            return True
    for m in RE_SECRETO_SIN_COMILLAS.finditer(linea):
        v = m.group("v")
        # Sin comillas (ficheros de entorno, YAML) se exige que parezca un valor y no el nombre de una
        # variable: letras y al menos un dígito. Así `password = password_input` no salta.
        if re.search(r"\d", v) and re.search(r"[A-Za-z]", v) and not es_placeholder(v):
            return True
    return False


# ----------------------------------------------------------------------------------------------
# Cabeceras de tablas
# ----------------------------------------------------------------------------------------------
_CABECERAS = {
    "nombre": "nombre y apellidos",
    "nombres": "nombre y apellidos",
    "nombre_completo": "nombre y apellidos",
    "nombre_y_apellidos": "nombre y apellidos",
    "apellidos": "nombre y apellidos",
    "apellido": "nombre y apellidos",
    "apellido1": "nombre y apellidos",
    "apellido2": "nombre y apellidos",
    "primer_apellido": "nombre y apellidos",
    "segundo_apellido": "nombre y apellidos",
    "name": "nombre y apellidos",
    "first_name": "nombre y apellidos",
    "last_name": "nombre y apellidos",
    "full_name": "nombre y apellidos",
    "firstname": "nombre y apellidos",
    "lastname": "nombre y apellidos",
    "fullname": "nombre y apellidos",
    "surname": "nombre y apellidos",
    "given_name": "nombre y apellidos",
    "family_name": "nombre y apellidos",
    "dni": "documento de identidad",
    "nie": "documento de identidad",
    "nif": "documento de identidad",
    "documento": "documento de identidad",
    "documento_identidad": "documento de identidad",
    "passport": "documento de identidad",
    "pasaporte": "documento de identidad",
    "national_id": "documento de identidad",
    "id_number": "documento de identidad",
    "email": "correo electrónico",
    "e_mail": "correo electrónico",
    "mail": "correo electrónico",
    "correo": "correo electrónico",
    "correo_electronico": "correo electrónico",
    "email_address": "correo electrónico",
    "telefono": "teléfono",
    "tfno": "teléfono",
    "tel": "teléfono",
    "movil": "teléfono",
    "celular": "teléfono",
    "phone": "teléfono",
    "phone_number": "teléfono",
    "mobile": "teléfono",
    "telephone": "teléfono",
    "direccion": "dirección",
    "domicilio": "dirección",
    "calle": "dirección",
    "address": "dirección",
    "home_address": "dirección",
    "street": "dirección",
    "street_address": "dirección",
    "fecha_nacimiento": "fecha de nacimiento",
    "fecha_de_nacimiento": "fecha de nacimiento",
    "nacimiento": "fecha de nacimiento",
    "f_nacimiento": "fecha de nacimiento",
    "birth_date": "fecha de nacimiento",
    "birthdate": "fecha de nacimiento",
    "date_of_birth": "fecha de nacimiento",
    "dob": "fecha de nacimiento",
    "birthday": "fecha de nacimiento",
    "iban": "datos bancarios",
    "cuenta_bancaria": "datos bancarios",
    "bank_account": "datos bancarios",
    "numero_tarjeta": "datos bancarios",
    "card_number": "datos bancarios",
    "credit_card": "datos bancarios",
    "nss": "Seguridad Social",
    "seguridad_social": "Seguridad Social",
    "numero_seguridad_social": "Seguridad Social",
    "social_security": "Seguridad Social",
    "ssn": "Seguridad Social",
}
_FORZAR_POR_CATEGORIA = {"fecha de nacimiento": "nacimiento", "Seguridad Social": "nss"}


def categoria_cabecera(texto: str) -> str | None:
    return _CABECERAS.get(norm_cabecera(texto))


def literal_categoria(categoria: str) -> str:
    return norm_cabecera(categoria)


# slug de la categoría -> texto con tildes, para mostrarlo
CATEGORIA_VISIBLE = {literal_categoria(c): c for c in set(_CABECERAS.values())}


# ----------------------------------------------------------------------------------------------
# Escaneo de texto, tablas y contenedores
# ----------------------------------------------------------------------------------------------
def ventanas(linea: str):
    if len(linea) <= VENTANA:
        yield linea
        return
    paso = VENTANA - SOLAPE
    for i in range(0, len(linea), paso):
        yield linea[i:i + VENTANA]


def escanear_linea(linea: str, rec: Recolector, ctx: Contexto, numero: int, lugar: str = "", forzar: str | None = None):
    for trozo in ventanas(linea):
        for c in buscar(trozo, ctx, forzar):
            rec.add(numero, c.tipo, c.valor, lugar)
        if RE_CLAVE_PRIVADA.search(trozo):
            rec.add(numero, "clave-privada", lugar=lugar)
        if hay_secreto(trozo):
            rec.add(numero, "secreto", lugar=lugar)


def escanear_texto(texto: str, rec: Recolector, ctx: Contexto, lugar: str = "", linea_fija: int | None = None):
    for n, linea in enumerate(texto.splitlines(), 1):
        escanear_linea(linea, rec, ctx, linea_fija or n, lugar)


def registrar_cabeceras(celdas: list[str], rec: Recolector, linea: int, lugar: str = "") -> list[str | None]:
    """Marca las cabeceras sospechosas y devuelve el modo de comprobación de cada columna."""
    modos: list[str | None] = []
    vistas: set = set()
    for celda in celdas:
        cat = categoria_cabecera(celda)
        modos.append(_FORZAR_POR_CATEGORIA.get(cat) if cat else None)
        if cat and cat not in vistas:
            vistas.add(cat)
            rec.add(linea, "cabecera", lugar=lugar, literal=literal_categoria(cat))
    return modos


def decodificar(datos: bytes) -> str:
    try:
        return datos.decode("utf-8-sig")
    except UnicodeDecodeError:
        return datos.decode("latin-1")


def escanear_tabular(texto: str, rec: Recolector, ctx: Contexto, delimitador_por_defecto: str = ","):
    try:
        try:
            dialecto = csv.Sniffer().sniff(texto[:8192], delimiters=",;\t|")
        except csv.Error:
            class dialecto(csv.excel):  # no se modifica csv.excel, que es global
                delimiter = delimitador_por_defecto
        lector = csv.reader(io.StringIO(texto, newline=""), dialecto)
        modos: list[str | None] = []
        primera = True
        for fila in lector:
            if not any(c.strip() for c in fila):
                continue
            if primera:
                modos = registrar_cabeceras(fila, rec, lector.line_num)
                primera = False
                continue
            for i, celda in enumerate(fila):
                if celda:
                    escanear_linea(celda, rec, ctx, lector.line_num, forzar=modos[i] if i < len(modos) else None)
    except csv.Error:
        escanear_texto(texto, rec, ctx)


RE_AUTOR = re.compile(r"<(?:dc:creator|cp:lastModifiedBy|meta:initial-creator)>\s*[^<\s][^<]*</")


class XmlNoPermitido(Exception):
    """El XML trae una declaración DOCTYPE. Un documento de Office nunca la lleva, y es la puerta de los ataques
    de entidades (billion laughs): se rechaza sin interpretarla."""


def _sin_prefijo(nombre: str) -> str:
    return nombre.rsplit(":", 1)[-1]


def recorrer_xml(datos: bytes, inicio, fin, texto):
    """Recorre un XML con el analizador expat de la biblioteca estándar (coste lineal).

    Se usa expat en lugar de expresiones regulares porque un XML con miles de etiquetas sin cerrar hacía cuadrático
    el coste de `.*?` y colgaba el CI con menos de 1 MB.
    """
    p = expat.ParserCreate()

    def doctype(*_args):
        raise XmlNoPermitido()

    p.StartDoctypeDeclHandler = doctype
    p.StartElementHandler = inicio
    p.EndElementHandler = fin
    p.CharacterDataHandler = texto
    p.buffer_text = True
    p.Parse(datos, True)


def abrir_zip(ruta: str, rec: Recolector) -> zipfile.ZipFile | None:
    try:
        zf = zipfile.ZipFile(ruta)
    except zipfile.BadZipFile:
        rec.aviso("no es un zip válido: revísalo a mano")
        return None
    infos = zf.infolist()
    if len(infos) > MAX_MIEMBROS_ZIP or sum(i.file_size for i in infos) > MAX_DESCOMPRIMIDO or any(
            i.file_size > MAX_MIEMBRO for i in infos):
        rec.add(1, "tamano")
        zf.close()
        return None
    return zf


def leer_parte(zf: zipfile.ZipFile, nombre: str) -> str:
    return decodificar(zf.read(nombre))


def textos_de_t(datos: bytes) -> str:
    """Todo el texto de los elementos <t> (cadenas de Excel, comentarios...)."""
    trozos: list[str] = []
    en_t = 0

    def ini(nombre, _attrs):
        nonlocal en_t
        if _sin_prefijo(nombre) == "t":
            en_t += 1

    def fin(nombre):
        nonlocal en_t
        if _sin_prefijo(nombre) == "t":
            en_t = max(0, en_t - 1)
            trozos.append(" ")

    def txt(c):
        if en_t:
            trozos.append(c)

    recorrer_xml(datos, ini, fin, txt)
    return "".join(trozos)


def leer_compartidas(datos: bytes) -> list[str]:
    """Tabla de cadenas compartidas de un xlsx (la posición de cada <si> es su índice)."""
    cadenas: list[str] = []
    actual: list[str] | None = None
    en_t = 0

    def ini(nombre, _attrs):
        nonlocal actual, en_t
        n = _sin_prefijo(nombre)
        if n == "si":
            actual = []
        elif n == "t":
            en_t += 1

    def fin(nombre):
        nonlocal actual, en_t
        n = _sin_prefijo(nombre)
        if n == "si":
            cadenas.append("".join(actual or []))
            actual = None
        elif n == "t":
            en_t = max(0, en_t - 1)

    def txt(c):
        if actual is not None and en_t:
            actual.append(c)

    recorrer_xml(datos, ini, fin, txt)
    return cadenas


def recorrer_hoja_xlsx(datos: bytes, compartidas: list[str], al_terminar_fila):
    """Llama a al_terminar_fila(numero_de_fila, [texto de cada celda]) por cada fila de la hoja."""
    siguiente = 0
    num = 0
    celdas: list[str] | None = None
    tipo = "n"
    partes: list[str] = []
    en_celda = en_v = False
    en_t = 0

    def ini(nombre, attrs):
        nonlocal siguiente, num, celdas, tipo, partes, en_celda, en_v, en_t
        n = _sin_prefijo(nombre)
        if n == "row":
            siguiente += 1
            try:
                num = int(attrs.get("r", siguiente))
            except ValueError:
                num = siguiente
            celdas = []
        elif n == "c" and celdas is not None:
            tipo, partes, en_celda, en_v, en_t = attrs.get("t", "n"), [], True, False, 0
        elif n == "v" and en_celda:
            en_v = True
        elif n == "t" and en_celda:
            en_t += 1

    def fin(nombre):
        nonlocal celdas, en_celda, en_v, en_t
        n = _sin_prefijo(nombre)
        if n == "v":
            en_v = False
        elif n == "t":
            en_t = max(0, en_t - 1)
        elif n == "c" and en_celda and celdas is not None:
            texto = "".join(partes)
            if tipo == "s":  # el valor es el índice de la cadena compartida
                try:
                    texto = compartidas[int(texto.strip())]
                except (ValueError, IndexError):
                    texto = ""
            celdas.append(texto)
            en_celda = False
        elif n == "row" and celdas is not None:
            al_terminar_fila(num, celdas)
            celdas = None

    def txt(c):
        if en_celda and (en_v or en_t):
            partes.append(c)

    recorrer_xml(datos, ini, fin, txt)


def recorrer_hoja_ods(datos: bytes, al_comenzar_hoja, al_terminar_fila):
    """Equivalente para content.xml de un ods. Las repeticiones de filas o columnas no se expanden."""
    num = 0
    celdas: list[str] | None = None
    valor = ""
    partes: list[str] | None = None
    en_p = 0

    def ini(nombre, attrs):
        nonlocal num, celdas, valor, partes, en_p
        if nombre == "table:table":
            num = 0
            al_comenzar_hoja()
        elif nombre == "table:table-row":
            num += 1
            celdas = []
        elif nombre in ("table:table-cell", "table:covered-table-cell") and celdas is not None:
            valor, partes = attrs.get("office:value", ""), []
        elif nombre == "text:p" and partes is not None:
            en_p += 1

    def fin(nombre):
        nonlocal celdas, partes, en_p
        if nombre == "text:p":
            en_p = max(0, en_p - 1)
        elif nombre in ("table:table-cell", "table:covered-table-cell") and celdas is not None and partes is not None:
            celdas.append((valor + " " + "".join(partes)).strip())
            partes = None
        elif nombre == "table:table-row" and celdas is not None:
            al_terminar_fila(num, celdas)
            celdas = None

    def txt(c):
        if partes is not None and en_p:
            partes.append(c)

    recorrer_xml(datos, ini, fin, txt)


class _Hoja:
    """Estado de una hoja mientras se recorre: la primera fila con contenido son las cabeceras."""

    def __init__(self, rec: Recolector, ctx: Contexto, lugar: str):
        self.rec, self.ctx, self.lugar = rec, ctx, lugar
        self.modos: list[str | None] = []
        self.primera = True

    def fila(self, num: int, celdas: list[str]):
        if not any(c.strip() for c in celdas):
            return
        if self.primera:
            self.modos = registrar_cabeceras(celdas, self.rec, num, self.lugar)
            self.primera = False
            return
        for i, celda in enumerate(celdas):
            if celda:
                escanear_linea(celda, self.rec, self.ctx, num, self.lugar, self.modos[i] if i < len(self.modos) else None)


def escanear_xlsx(ruta: str, rec: Recolector, ctx: Contexto):
    zf = abrir_zip(ruta, rec)
    if zf is None:
        return
    with zf:
        nombres = zf.namelist()
        if any(n.lower().endswith("vbaproject.bin") for n in nombres):
            rec.add(1, "macros")
        compartidas = leer_compartidas(zf.read("xl/sharedStrings.xml")) if "xl/sharedStrings.xml" in nombres else []
        hojas = sorted((n for n in nombres if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n)),
                       key=lambda n: int(re.search(r"(\d+)", n.rsplit("/", 1)[1]).group(1)))
        for indice, nombre in enumerate(hojas, 1):
            recorrer_hoja_xlsx(zf.read(nombre), compartidas, _Hoja(rec, ctx, f"hoja {indice}").fila)
        for nombre in nombres:
            if re.fullmatch(r"xl/comments\d*\.xml", nombre):
                escanear_texto(textos_de_t(zf.read(nombre)), rec, ctx, "comentarios", linea_fija=1)
        if "docProps/core.xml" in nombres and RE_AUTOR.search(leer_parte(zf, "docProps/core.xml")):
            rec.aviso("los metadatos del documento incluyen un nombre de autor: revísalos")


def escanear_ods(ruta: str, rec: Recolector, ctx: Contexto):
    zf = abrir_zip(ruta, rec)
    if zf is None:
        return
    with zf:
        nombres = zf.namelist()
        if any(n.startswith(("Basic/", "Scripts/")) for n in nombres):
            rec.add(1, "macros")
        if "content.xml" in nombres:
            estado = {"hoja": 0, "actual": None}

            def comienza():
                estado["hoja"] += 1
                estado["actual"] = _Hoja(rec, ctx, f"hoja {estado['hoja']}")

            def fila(num, celdas):
                if estado["actual"] is not None:
                    estado["actual"].fila(num, celdas)

            recorrer_hoja_ods(zf.read("content.xml"), comienza, fila)
        if "meta.xml" in nombres and RE_AUTOR.search(leer_parte(zf, "meta.xml")):
            rec.aviso("los metadatos del documento incluyen un nombre de autor: revísalos")


RE_ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def _como_texto(valor) -> str:
    if isinstance(valor, str):
        return valor
    if isinstance(valor, list):
        return "".join(str(x) for x in valor)
    return ""


def escanear_notebook(texto: str, rec: Recolector, ctx: Contexto):
    try:
        cuaderno = json.loads(texto)
        celdas = cuaderno["cells"]
        if not isinstance(celdas, list):
            raise ValueError
    except (ValueError, KeyError, TypeError):
        rec.aviso("el cuaderno no es un JSON de notebook válido: se ha analizado como texto")
        escanear_texto(texto, rec, ctx)
        return
    lineas_celda = [n for n, l in enumerate(texto.splitlines(), 1) if '"cell_type"' in l]
    imagen = False
    for i, celda in enumerate(celdas):
        if not isinstance(celda, dict):
            continue
        linea = lineas_celda[i] if i < len(lineas_celda) else 1
        lugar = f"celda {i + 1}"
        escanear_texto(_como_texto(celda.get("source")), rec, ctx, lugar + " (código)", linea_fija=linea)
        for salida in celda.get("outputs") or []:
            if not isinstance(salida, dict):
                continue
            trozos = [_como_texto(salida.get("text")), _como_texto(salida.get("evalue")),
                      _como_texto(salida.get("traceback"))]
            for mime, valor in (salida.get("data") or {}).items():
                if mime.startswith("image/") and mime != "image/svg+xml":
                    imagen = True
                    continue
                trozos.append(_como_texto(valor) if isinstance(valor, (str, list)) else json.dumps(valor))
            escanear_texto(RE_ANSI.sub("", "\n".join(trozos)), rec, ctx, lugar + " (salida)", linea_fija=linea)
    if imagen:
        rec.aviso("hay imágenes en las salidas del cuaderno: no se pueden analizar, revísalas a mano")


# ----------------------------------------------------------------------------------------------
# Análisis de un fichero
# ----------------------------------------------------------------------------------------------
EXT_TABULAR = {".csv": ",", ".tsv": "\t", ".tab": "\t"}
EXT_XLSX = {".xlsx", ".xlsm"}
EXT_BINARIAS = {".xls", ".xlsb", ".doc", ".docx", ".ppt", ".pptx", ".pdf", ".odt", ".odp", ".png", ".jpg", ".jpeg",
                ".gif", ".webp", ".bmp", ".zip", ".7z", ".gz", ".tar", ".parquet", ".feather", ".pkl", ".pickle",
                ".sqlite", ".sqlite3", ".db", ".h5", ".hdf5", ".npy", ".npz", ".sav", ".dta", ".rds", ".rdata"}
EXT_CLAVES = {".pem", ".key", ".p12", ".pfx", ".jks", ".keystore", ".ppk"}
NOMBRES_CLAVES = {"id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"}


def es_fichero_secreto(nombre: str) -> bool:
    n = nombre.lower()
    if n == ".env" or (n.startswith(".env.") and not n.endswith((".example", ".sample", ".template", ".dist"))):
        return True
    return n in NOMBRES_CLAVES or os.path.splitext(n)[1] in EXT_CLAVES


def analizar_fichero(raiz: str, ruta: str, ctx: Contexto) -> Recolector:
    rec = Recolector(ruta)
    completa = os.path.join(raiz, ruta)
    nombre = os.path.basename(ruta)
    try:
        if es_fichero_secreto(nombre):
            rec.add(1, "fichero-secreto")
            return rec
        if os.path.islink(completa):
            rec.aviso("es un enlace simbólico: no se sigue, revísalo a mano")
            return rec
        if not os.path.isfile(completa):
            return rec
        if os.path.getsize(completa) > MAX_BYTES:
            rec.add(1, "tamano")
            return rec
        ext = os.path.splitext(nombre)[1].lower()
        if ext in EXT_XLSX:
            escanear_xlsx(completa, rec, ctx)
        elif ext == ".ods":
            escanear_ods(completa, rec, ctx)
        elif ext in EXT_BINARIAS:
            rec.aviso("formato binario que no se puede analizar: revísalo a mano")
        else:
            with open(completa, "rb") as f:
                datos = f.read()
            if b"\x00" in datos[:8192]:
                rec.aviso("fichero binario que no se puede analizar: revísalo a mano")
                return rec
            texto = decodificar(datos)
            if ext in EXT_TABULAR:
                escanear_tabular(texto, rec, ctx, EXT_TABULAR[ext])
            elif ext == ".ipynb":
                escanear_notebook(texto, rec, ctx)
            else:
                escanear_texto(texto, rec, ctx)
    except Exception:  # falla cerrado: un fichero que no se puede analizar no se da por bueno
        rec.add(1, "error-analisis")
    return rec


# ----------------------------------------------------------------------------------------------
# Lista de excepciones
# ----------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Permitido:
    tipo: str
    patron: str
    valor: str
    motivo: str
    linea: int


def cargar_permitidos(ruta: str) -> list[Permitido]:
    if not os.path.isfile(ruta):
        return []
    permitidos = []
    with open(ruta, encoding="utf-8") as f:
        for n, bruta in enumerate(f, 1):
            texto = bruta.strip()
            if not texto or texto.startswith("#"):
                continue
            partes = [p.strip() for p in texto.split("|", 3)]
            if len(partes) != 4 or not all(partes):
                raise ErrorConfig(f"{ruta}:{n}: cada excepción necesita 4 campos: tipo | fichero | valor | motivo")
            tipo, patron, valor, motivo = partes
            if tipo not in TIPOS_PERMITIBLES:
                raise ErrorConfig(f"{ruta}:{n}: tipo no permitido (usa uno de: {', '.join(sorted(TIPOS_PERMITIBLES))})")
            if tipo in CON_HUELLA and not (valor == "*" or re.fullmatch(r"sha256:[0-9a-f]{64}", valor)):
                raise ErrorConfig(f"{ruta}:{n}: para '{tipo}' el valor es '*' o 'sha256:<64 hex>'")
            if tipo in SOLO_COMODIN and valor != "*":
                raise ErrorConfig(f"{ruta}:{n}: para '{tipo}' solo se admite '*' (no se guardan huellas de secretos)")
            permitidos.append(Permitido(tipo, patron, norm_cabecera(valor) if tipo == "cabecera" else valor,
                                        motivo, n))
    return permitidos


def dominios_permitidos(permitidos: list[Permitido]) -> frozenset:
    return frozenset(p.valor.lower() for p in permitidos if p.tipo == "dominio")


def esta_permitido(h: Hallazgo, permitidos: list[Permitido]) -> bool:
    if h.tipo in ("clave-privada", "tamano", "ruta-protegida", "error-analisis"):
        return False
    for p in permitidos:
        if p.tipo != h.tipo or not fnmatch.fnmatchcase(h.fichero, p.patron):
            continue
        if p.valor == "*" or p.valor == h.huella:
            return True
    return False


# ----------------------------------------------------------------------------------------------
# Git y guardia de rutas
# ----------------------------------------------------------------------------------------------
def raiz_git() -> str:
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except OSError:
        pass
    return os.getcwd()


def ficheros_cambiados(raiz: str, base: str, filtro: str | None) -> list[str]:
    if not re.fullmatch(r"[A-Za-z0-9._/][A-Za-z0-9._/\-]*", base):
        raise ErrorConfig("la referencia base no tiene un formato válido")
    cmd = ["git", "-C", raiz, "diff", "--name-only", "-z", "--no-renames"]
    if filtro:
        cmd.append(f"--diff-filter={filtro}")
    cmd += [f"{base}...HEAD", "--"]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise ErrorConfig("no se pudo calcular la lista de ficheros cambiados (¿falta fetch-depth: 0?)")
    return [p.decode("utf-8", "surrogateescape") for p in r.stdout.split(b"\0") if p]


def guardia_rutas(cambios: list[str], autor: str | None, code_owner: str) -> list[Hallazgo]:
    """Un PR que toca el workflow, los scripts o las excepciones solo es válido si lo abre el code owner."""
    if autor and autor.strip().lower() == code_owner.strip().lower():
        return []
    return [Hallazgo(ruta, 1, "ruta-protegida") for ruta in cambios
            if any(fnmatch.fnmatchcase(ruta, p) for p in RUTAS_PROTEGIDAS)]


# ----------------------------------------------------------------------------------------------
# Salida: anotaciones, resumen y texto (nunca incluyen el valor detectado)
# ----------------------------------------------------------------------------------------------
def escapar_dato(s: str) -> str:
    return s.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def escapar_propiedad(s: str) -> str:
    return escapar_dato(s).replace(":", "%3A").replace(",", "%2C")


def a_utf8(s: str) -> str:
    return s.encode("utf-8", "replace").decode("utf-8")


def sanear(s: str, maximo: int = 200) -> str:
    """Para mostrar rutas de un PR (las controla quien abre el PR) dentro de Markdown o de texto."""
    seguro = "".join(c if (c.isalnum() or c in " ._-/()[]+,#@&=~") else "?" for c in a_utf8(s))
    return seguro[:maximo]


def etiqueta(tipo: str, h: Hallazgo | None = None) -> str:
    """Texto fijo del tipo. Para las cabeceras añade la categoría (sale de nuestro diccionario, no de la celda)."""
    base = TIPOS.get(tipo, tipo)
    if h is not None and tipo == "cabecera" and h.huella:
        base += f": {CATEGORIA_VISIBLE.get(h.huella, 'otra')}"
    return base


def emitir_anotaciones(hallazgos: list[Hallazgo], avisos: list[Aviso]):
    for h in hallazgos:
        print(f"::error file={escapar_propiedad(a_utf8(h.fichero))},line={h.linea},"
              f"title={escapar_propiedad('Privacidad')}::{escapar_dato(etiqueta(h.tipo, h))} (valor no mostrado)")
    for a in avisos:
        print(f"::warning file={escapar_propiedad(a_utf8(a.fichero))},"
              f"title={escapar_propiedad('Privacidad')}::{escapar_dato(a.mensaje)}")


def emitir_texto(hallazgos: list[Hallazgo], avisos: list[Aviso]):
    for h in hallazgos:
        donde = f" ({h.lugar})" if h.lugar else ""
        print(f"{sanear(h.fichero)}:{h.linea}: {etiqueta(h.tipo, h)}{donde}")
    for a in avisos:
        print(f"{sanear(a.fichero)}: aviso: {a.mensaje}")


def resumen_markdown(hallazgos: list[Hallazgo], avisos: list[Aviso], n_ficheros: int, truncados: list[str]) -> str:
    out = ["## Comprobación de privacidad", ""]
    if hallazgos:
        out += [f"**Resultado: {len(hallazgos)} posible(s) dato(s) personal(es) o secreto(s).** El pull request queda bloqueado.", "",
                "| Fichero | Línea | Qué se ha detectado | Dónde |", "|---|---|---|---|"]
        for h in hallazgos[:MAX_FILAS_RESUMEN]:
            out.append(f"| `{sanear(h.fichero)}` | {h.linea} | {etiqueta(h.tipo, h)} | {h.lugar or '-'} |")
        if len(hallazgos) > MAX_FILAS_RESUMEN:
            out.append(f"| … | | {len(hallazgos) - MAX_FILAS_RESUMEN} hallazgos más no listados | |")
        out += ["", "> El valor detectado **no se muestra** a propósito: este registro es público.", "",
                "### Qué hacer", "",
                "1. Quita el dato del fichero (o sustitúyelo por datos inventados) y vuelve a subirlo.",
                "2. **Si el dato ya estaba en un commit anterior de tu rama, borrarlo en un commit nuevo no basta:** "
                "sigue en el historial y el repositorio es público. Avisa al profesor antes de seguir.",
                "3. Si es un falso positivo (por ejemplo, datos de ejemplo inventados), pide una excepción al profesor. "
                "No edites la lista de excepciones tú mismo.", ""]
    else:
        out += [f"**Resultado: sin hallazgos** en {n_ficheros} fichero(s) analizado(s).", ""]
    if avisos:
        out += ["### Avisos (no bloquean)", ""]
        for a in avisos[:MAX_FILAS_RESUMEN]:
            out.append(f"- `{sanear(a.fichero)}`: {a.mensaje}")
        out.append("")
    if truncados:
        out += ["### Listados parciales", "",
                "En estos ficheros hay más de {} hallazgos y solo se listan los primeros:".format(MAX_POR_FICHERO)]
        out += [f"- `{sanear(t)}`" for t in truncados[:20]] + [""]
    out += ["### Límites de esta comprobación", "",
            "- Detecta **patrones** (correos, DNI/NIE, teléfonos, IBAN, tarjetas, Seguridad Social, fechas de nacimiento "
            "junto a su cabecera, secretos y cabeceras de columnas). **No detecta nombres propios ni datos identificativos "
            "en texto libre.**",
            "- Una detección bloquea el PR; **un PR limpio no garantiza que no haya datos personales.** No sustituye la "
            "revisión del profesor.",
            "- Los formatos binarios no soportados (por ejemplo `.xls`, `.pdf`, `.parquet`, `.pkl`, `.db`) y las imágenes "
            "solo generan un aviso."]
    return "\n".join(out) + "\n"


# ----------------------------------------------------------------------------------------------
# Programa principal
# ----------------------------------------------------------------------------------------------
def construir_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Detecta datos personales y secretos (no imprime nunca el valor).")
    ap.add_argument("--base", help="referencia base del PR, p. ej. origin/main")
    ap.add_argument("--ficheros", nargs="+", help="analiza estos ficheros en lugar de calcular el diff")
    ap.add_argument("--raiz", help="raíz del repositorio (por defecto, la de git)")
    ap.add_argument("--permitidos", help="lista de excepciones (por defecto .github/privacidad-permitidos.txt)")
    ap.add_argument("--autor", help="login del autor del PR; activa la guardia de rutas protegidas")
    ap.add_argument("--code-owner", default="profeFPInfor")
    ap.add_argument("--resumen", help="ruta del resumen Markdown (por defecto $GITHUB_STEP_SUMMARY)")
    ap.add_argument("--formato", choices=("auto", "github", "texto"), default="auto")
    ap.add_argument("--huella", metavar="TIPO", help="imprime la huella del valor que entra por la entrada estándar")
    return ap


def main(argv: list[str] | None = None) -> int:
    args = construir_parser().parse_args(argv)
    try:
        if args.huella:
            if args.huella not in CON_HUELLA:
                raise ErrorConfig(f"tipo sin huella (usa uno de: {', '.join(sorted(CON_HUELLA))})")
            print(huella(args.huella, sys.stdin.read().rstrip("\n")))
            return 0
        raiz = os.path.abspath(args.raiz or raiz_git())
        permitidos = cargar_permitidos(args.permitidos or os.path.join(raiz, ".github", "privacidad-permitidos.txt"))
        ctx = Contexto(dominios_permitidos(permitidos))
        if args.ficheros:
            a_analizar = todos = list(args.ficheros)
        elif args.base:
            a_analizar = ficheros_cambiados(raiz, args.base, "AM")
            todos = ficheros_cambiados(raiz, args.base, None)
        else:
            raise ErrorConfig("indica --base o --ficheros")
    except ErrorConfig as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    hallazgos: list[Hallazgo] = []
    avisos: list[Aviso] = []
    truncados: list[str] = []
    if args.autor is not None:
        hallazgos += guardia_rutas(todos, args.autor, args.code_owner)
    for ruta in a_analizar:
        rec = analizar_fichero(raiz, ruta, ctx)
        hallazgos += [h for h in rec.items if not esta_permitido(h, permitidos)]
        avisos += rec.avisos
        if rec.truncado:
            truncados.append(ruta)

    formato = args.formato
    if formato == "auto":
        formato = "github" if os.environ.get("GITHUB_ACTIONS") == "true" else "texto"
    (emitir_anotaciones if formato == "github" else emitir_texto)(hallazgos, avisos)
    destino = args.resumen or os.environ.get("GITHUB_STEP_SUMMARY")
    if destino:
        with open(destino, "a", encoding="utf-8") as f:
            f.write(resumen_markdown(hallazgos, avisos, len(a_analizar), truncados))
    if hallazgos:
        print(f"Privacidad: {len(hallazgos)} hallazgo(s). El valor detectado no se muestra.", file=sys.stderr)
        return 1
    print(f"Privacidad: sin hallazgos en {len(a_analizar)} fichero(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
