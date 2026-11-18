"""
reflection_loop.py — Ejemplo didáctico del patrón Reflection (generar → verificar → criticar → corregir).

Tarea de ejemplo: que un LLM escriba la función letra_dni(numero) que calcula la letra
del DNI español. Los tests unitarios hacen de "verdad externa": la crítica se apoya en
fallos reales, no solo en la opinión del modelo.

Modos de uso:
    python reflection_loop.py --demo            # sin API: LLM simulado, para entender el flujo
    python reflection_loop.py                   # con OpenRouter (necesita OPENROUTER_API_KEY)

Variables de entorno (modo real):
    OPENROUTER_API_KEY   clave de https://openrouter.ai
    MODELO               opcional; por defecto "openrouter/free" (router de modelos gratuitos)

Aviso: el código generado por un LLM se ejecuta en un proceso aparte con tiempo límite,
pero no es un sandbox real. Úsalo solo en tu máquina de pruebas o en un contenedor.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import urllib.request
from datetime import datetime
from pathlib import Path

MAX_ITERACIONES = 3          # condición de parada: nunca bucles infinitos
MEMORIA = Path("reflexiones.md")  # memoria tipo Reflexion: lecciones entre intentos

TAREA = """Escribe en Python la función letra_dni(numero) que devuelve la letra del DNI español.
- La letra es "TRWAGMYFPDXBNJZSQVHLCKE"[numero % 23].
- Si numero no es un int, o es negativo, o tiene más de 8 cifras, lanza ValueError.
Devuelve SOLO el código dentro de un bloque ```python```."""

TESTS = textwrap.dedent("""
    import os, sys, unittest
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from solucion import letra_dni

    class TestLetraDNI(unittest.TestCase):
        def test_casos_conocidos(self):
            self.assertEqual(letra_dni(12345678), "Z")
            self.assertEqual(letra_dni(0), "T")
            self.assertEqual(letra_dni(99999999), "R")

        def test_negativo(self):
            with self.assertRaises(ValueError):
                letra_dni(-1)

        def test_demasiadas_cifras(self):
            with self.assertRaises(ValueError):
                letra_dni(123456789)

        def test_tipo_incorrecto(self):
            with self.assertRaises(ValueError):
                letra_dni("12345678")

    if __name__ == "__main__":
        unittest.main(verbosity=0)
""")


# ---------------------------------------------------------------- LLM real (OpenRouter)
def llamar_llm(sistema: str, usuario: str) -> str:
    clave = os.environ["OPENROUTER_API_KEY"]
    cuerpo = {
        "model": os.environ.get("MODELO", "openrouter/free"),
        "messages": [
            {"role": "system", "content": sistema},
            {"role": "user", "content": usuario},
        ],
        "temperature": 0.2,
    }
    peticion = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(cuerpo).encode(),
        headers={"Authorization": f"Bearer {clave}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(peticion, timeout=120) as r:
        return json.load(r)["choices"][0]["message"]["content"]


# ---------------------------------------------------------------- LLM simulado (--demo)
class LLMSimulado:
    """Devuelve respuestas fijas para enseñar el flujo sin gastar tokens."""

    def __init__(self):
        self.intentos_generador = 0

    def __call__(self, sistema: str, usuario: str) -> str:
        if "crítico" in sistema:
            return ("1. No se valida el tipo: un str como '12345678' debería lanzar ValueError.\n"
                    "2. No se comprueban negativos ni números de más de 8 cifras.\n"
                    "3. Propuesta: validar con isinstance(numero, int) y 0 <= numero <= 99_999_999 "
                    "antes de calcular.")
        self.intentos_generador += 1
        ya_aprendido = "Lecciones de intentos anteriores" in usuario  # la memoria evita repetir el error
        if self.intentos_generador == 1 and not ya_aprendido:  # 1.ª versión: caso feliz, sin validar
            return ("```python\ndef letra_dni(numero):\n"
                    "    return 'TRWAGMYFPDXBNJZSQVHLCKE'[numero % 23]\n```")
        return ("```python\ndef letra_dni(numero):\n"
                "    if not isinstance(numero, int) or isinstance(numero, bool):\n"
                "        raise ValueError('El número debe ser un entero')\n"
                "    if not 0 <= numero <= 99_999_999:\n"
                "        raise ValueError('El número debe tener como máximo 8 cifras y no ser negativo')\n"
                "    return 'TRWAGMYFPDXBNJZSQVHLCKE'[numero % 23]\n```")


# ---------------------------------------------------------------- piezas del bucle
def extraer_codigo(respuesta: str) -> str:
    bloque = re.search(r"```(?:python)?\s*\n(.*?)```", respuesta, re.S)
    return bloque.group(1) if bloque else respuesta


def verificar(codigo: str) -> tuple[bool, str]:
    """Verificación externa: ejecuta los tests en un proceso aparte con tiempo límite."""
    with tempfile.TemporaryDirectory() as carpeta:
        Path(carpeta, "solucion.py").write_text(codigo, encoding="utf-8")
        Path(carpeta, "test_solucion.py").write_text(TESTS, encoding="utf-8")
        try:
            r = subprocess.run([sys.executable, "-I", "test_solucion.py"], cwd=carpeta,
                               capture_output=True, text=True, timeout=10)
        except subprocess.TimeoutExpired:
            return False, "Los tests superaron el tiempo límite (¿bucle infinito?)."
        return r.returncode == 0, (r.stderr or r.stdout)[-2000:]


def criticar(llm, codigo: str, salida_tests: str) -> str:
    sistema = ("Eres un crítico de código exigente. No reescribas el código: "
               "señala errores concretos y cómo arreglarlos, en una lista numerada.")
    usuario = (f"Tarea:\n{TAREA}\n\nCódigo:\n```python\n{codigo}\n```\n\n"
               f"Resultado de los tests:\n{salida_tests}")
    return llm(sistema, usuario)


def generar(llm, critica: str | None, codigo_previo: str | None, lecciones: str) -> str:
    sistema = "Eres un programador Python cuidadoso."
    usuario = TAREA
    if lecciones:
        usuario += f"\n\nLecciones de intentos anteriores:\n{lecciones}"
    if critica:
        usuario += (f"\n\nTu versión anterior:\n```python\n{codigo_previo}\n```\n"
                    f"Crítica recibida:\n{critica}\nCorrige el código teniendo en cuenta la crítica.")
    return extraer_codigo(llm(sistema, usuario))


def guardar_leccion(iteracion: int, critica: str) -> None:
    with MEMORIA.open("a", encoding="utf-8") as f:
        f.write(f"\n## {datetime.now():%Y-%m-%d %H:%M} · iteración {iteracion}\n{critica}\n")


# ---------------------------------------------------------------- bucle principal
def bucle_reflection(llm) -> str | None:
    lecciones = MEMORIA.read_text(encoding="utf-8")[-1500:] if MEMORIA.exists() else ""
    if lecciones:
        print(f"Memoria cargada: se usan las lecciones guardadas en {MEMORIA}")
    codigo, critica = None, None
    for i in range(1, MAX_ITERACIONES + 1):
        codigo = generar(llm, critica, codigo, lecciones)
        ok, salida = verificar(codigo)
        print(f"\n--- Iteración {i}: {'tests OK' if ok else 'tests FALLAN'} ---")
        print(codigo)
        if ok:
            return codigo
        critica = criticar(llm, codigo, salida)
        print("Crítica:\n" + critica)
        guardar_leccion(i, critica)
    print(f"\nSin solución válida tras {MAX_ITERACIONES} iteraciones: revisa a mano.")
    return None


if __name__ == "__main__":
    if "--demo" not in sys.argv and "OPENROUTER_API_KEY" not in os.environ:
        sys.exit("Falta OPENROUTER_API_KEY. Usa --demo para probar sin API.")
    modelo = LLMSimulado() if "--demo" in sys.argv else llamar_llm
    final = bucle_reflection(modelo)
    sys.exit(0 if final else 1)
