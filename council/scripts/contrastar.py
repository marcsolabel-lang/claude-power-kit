#!/usr/bin/env python3
"""
contrastar.py — Segunda lectura automática via Gemini API.

Contrasta cualquier texto contra los docs de un repo. Genérico: auto-detecta el
repo (raíz git del directorio actual) o acepta uno explícito con --repo.

Uso:
  python contrastar.py "texto a contrastar"
  python contrastar.py --archivo docs/plan.md
  python contrastar.py --repo C:/repos/mi-catalogo "texto"      # Windows ahora
  python contrastar.py --repo ~/repos/mi-catalogo "texto"       # Linux luego
  python contrastar.py --todo "texto"                           # todos los .md, sin filtro de carpeta
  python contrastar.py --sin-docs "texto"                       # solo criterio general
  echo "texto" | python contrastar.py

Detección automática (sin --repo):
  1. Raíz git del directorio actual → usa sus docs (prefiere ./docs si existe).
  2. Si no hay repo git → contraste solo con el criterio general (con aviso).

Clave de Gemini (obtén una gratis en https://aistudio.google.com/apikey):
  - variable de entorno GEMINI_API_KEY, o
  - fichero ~/.claude/gemini-api-key.txt (una línea con la clave).
La clave NUNCA se pega en el prompt ni sale en ningún payload.

Requiere: pip install google-genai
"""

import os
import sys
import argparse
import glob
import subprocess
import textwrap
from pathlib import Path

# ── Configuración ──────────────────────────────────────────────────────────────
KEY_FILE       = os.path.expanduser("~/.claude/gemini-api-key.txt")
MODEL          = "gemini-2.5-flash"
MAX_DOC_CHARS  = 800_000   # límite suave para no saturar el contexto
IGNORAR        = ["node_modules", ".git", "__pycache__", "dist/", "build/", ".venv"]


# ── Detección del repo y sus docs ──────────────────────────────────────────────

def detectar_repo(cwd):
    """Devuelve (nombre, ruta) de la raíz git que contiene el CWD, o (None, cwd)."""
    cwd = os.path.realpath(cwd)
    try:
        raiz = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd, stderr=subprocess.DEVNULL, text=True
        ).strip()
        return os.path.basename(raiz), raiz
    except Exception:
        return None, cwd


def encontrar_docs(ruta_repo, todo=False):
    """
    Busca los .md del repo. Preferencia:
      - si existe ./docs y no se pidió --todo → solo los .md bajo ./docs
      - en otro caso → todos los .md del repo (filtrando node_modules, .git, etc.)
    Devuelve (lista_de_rutas, carpeta_origen).
    """
    ruta_repo = os.path.expanduser(ruta_repo)
    if not os.path.isdir(ruta_repo):
        return [], None

    docs_dir = os.path.join(ruta_repo, "docs")
    if not todo and os.path.isdir(docs_dir):
        base = docs_dir
    else:
        base = ruta_repo

    patron = os.path.join(base, "**", "*.md")
    archivos = sorted(glob.glob(patron, recursive=True))
    archivos = [f for f in archivos if not any(p in f for p in IGNORAR)]
    return archivos, (base if archivos else None)


def cargar_docs(rutas, limite_chars=MAX_DOC_CHARS):
    """Carga y concatena docs hasta el límite de caracteres."""
    partes = []
    total = 0
    cargados = 0
    for ruta in rutas:
        try:
            contenido = Path(ruta).read_text(encoding="utf-8", errors="replace")
            if total + len(contenido) > limite_chars:
                partes.append(f"[... {len(rutas) - cargados} docs omitidos por límite de contexto ...]")
                break
            nombre = os.path.basename(ruta)
            partes.append(f"### FUENTE: {nombre}\n\n{contenido}")
            total += len(contenido)
            cargados += 1
        except Exception:
            pass
    return "\n\n---\n\n".join(partes), cargados


# ── Prompt de contraste ────────────────────────────────────────────────────────

def construir_prompt(texto, corpus, nombre_proyecto, criterio=""):
    proyecto_ctx = f"del proyecto **{nombre_proyecto}**" if nombre_proyecto else ""

    if corpus:
        bloque_docs = textwrap.dedent(f"""\
            ════════════════════════════════════════
            DOCUMENTOS {proyecto_ctx.upper()} (fuente de verdad)
            ════════════════════════════════════════

            {corpus}

        """)
        instruccion_docs = textwrap.dedent("""\
            Para cada afirmación principal del texto, indica:

              ✓  consistente  — respaldado por [nombre del doc]
              ✗  contradice   — [nombre del doc] dice exactamente: [cita]
              ?  no cubierto  — no está en los docs disponibles

            Si el texto ignora algo relevante que SÍ está en los docs, indícalo.
            Si un punto no está en los docs, di "no está en los docs" — no rellenes
            con conocimiento general.
        """)
    else:
        bloque_docs = "(No se han proporcionado documentos del proyecto.)\n\n"
        instruccion_docs = textwrap.dedent("""\
            No tienes documentos del proyecto. Evalúa solo con criterios generales:
            coherencia interna, supuestos implícitos, riesgos no mencionados.
            Indica claramente que el contraste es sin documentos de referencia.
        """)

    # Verificador contra criterio de aceptación: si se pasa un "definición de hecho"
    # con --instruccion, se verifica el borrador punto por punto y se emite un
    # veredicto PASA/FALLA — sin embarcar el corpus a ningún otro sitio.
    bloque_criterio = ""
    linea_veredicto = ""
    if criterio:
        bloque_criterio = textwrap.dedent(f"""\
            ════════════════════════════════════════
            CRITERIO DE ACEPTACIÓN (definición de «hecho»)
            ════════════════════════════════════════

            {criterio}

            Verifica el TEXTO A REVISAR contra ESTE criterio, punto por punto: por
            cada punto di si lo CUMPLE o NO, citando la evidencia del propio texto.

        """)
        linea_veredicto = "Veredicto criterio: PASA / FALLA — [qué punto(s) del criterio quedan sin cumplir]\n"

    return textwrap.dedent(f"""\
        Eres un analista de segunda lectura. Tu trabajo es contrastar si el TEXTO
        A REVISAR es consistente con los documentos de referencia disponibles.
        No tienes otra fuente: lo que no está en los docs, no lo sabes.

        {bloque_docs}
        ════════════════════════════════════════
        TEXTO A REVISAR
        ════════════════════════════════════════

        {texto}

        {bloque_criterio}
        ════════════════════════════════════════
        INSTRUCCIONES
        ════════════════════════════════════════

        {instruccion_docs}

        Al final, añade:

        RESUMEN
        -------
        {linea_veredicto}Consistencia general: ALTA / MEDIA / BAJA
        Contradicciones (✗): [N] — [cómo resolverlas si las hay]
        Lagunas (?): [N] — [si son decisiones abiertas o simplemente no documentadas]
        Recomendación: [una frase directa sobre si el texto es sólido o necesita revisión]
    """)


# ── API key ────────────────────────────────────────────────────────────────────

_PLACEHOLDER = "PEGA_AQUI_TU_API_KEY_DE_GEMINI"


def get_api_key():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key and key != _PLACEHOLDER:
        return key
    if os.path.exists(KEY_FILE):
        key = Path(KEY_FILE).read_text(encoding="utf-8").strip()
        if key and key != _PLACEHOLDER:
            return key
    print(
        "\nERROR: API key de Gemini no configurada.\n"
        "  Opción A: variable de entorno  GEMINI_API_KEY\n"
        f"  Opción B: fichero  {KEY_FILE}  (una línea con la clave)\n"
        "  Obtén una gratis en https://aistudio.google.com/apikey\n",
        file=sys.stderr
    )
    sys.exit(1)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="Contrasta un texto contra los docs de un repo via Gemini."
    )
    ap.add_argument("texto", nargs="?", help="Texto a contrastar")
    ap.add_argument("--archivo",     help="Archivo .md a contrastar en lugar de texto directo")
    ap.add_argument("--repo",        help="Ruta a un repo como fuente de docs (por defecto: raíz git del CWD)")
    ap.add_argument("--todo",        action="store_true", help="Usa todos los .md del repo, no solo ./docs")
    ap.add_argument("--sin-docs",    action="store_true", help="Contrasta solo con criterios generales, sin docs")
    ap.add_argument("--instruccion", help="Criterio de aceptación / definición de «hecho» a verificar")
    args = ap.parse_args()

    # ── Texto a contrastar
    if args.archivo:
        texto = Path(args.archivo).read_text(encoding="utf-8", errors="replace")
        print(f"[contrastar] Archivo: {args.archivo}", file=sys.stderr, flush=True)
    elif args.texto:
        texto = args.texto
    elif not sys.stdin.isatty():
        texto = sys.stdin.read()
    else:
        ap.print_help()
        sys.exit(1)

    if not texto.strip():
        print("ERROR: El texto a contrastar está vacío.", file=sys.stderr)
        sys.exit(1)

    # ── Determinar fuente de docs
    corpus = ""
    nombre_proyecto = None
    n_docs = 0

    if not args.sin_docs:
        if args.repo:
            ruta_repo = os.path.expanduser(args.repo)
            nombre_proyecto = os.path.basename(ruta_repo.rstrip("/\\")) or ruta_repo
        else:
            nombre_proyecto, ruta_repo = detectar_repo(os.getcwd())

        if nombre_proyecto:
            rutas, origen = encontrar_docs(ruta_repo, todo=args.todo)
            if rutas:
                corpus, n_docs = cargar_docs(rutas)
                print(f"[contrastar] Proyecto: {nombre_proyecto} | {n_docs} docs ({origen})", file=sys.stderr, flush=True)
            else:
                print(f"[contrastar] Sin docs .md para '{nombre_proyecto}' — contraste sin documentos", file=sys.stderr, flush=True)
        else:
            print("[contrastar] No se detectó repo git — contraste sin documentos", file=sys.stderr, flush=True)

    # ── Construir prompt y llamar a Gemini
    prompt = construir_prompt(texto, corpus, nombre_proyecto, criterio=(args.instruccion or ""))
    api_key = get_api_key()

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("ERROR: falta la librería. Instala con:  pip install google-genai", file=sys.stderr)
        sys.exit(2)

    cliente = genai.Client(api_key=api_key)
    print(f"[contrastar] Enviando a {MODEL}...", file=sys.stderr, flush=True)

    respuesta = cliente.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(max_output_tokens=32768),
    )

    sep = "═" * 62
    # Progreso/banner -> stderr; STDOUT solo el veredicto (así se puede capturar limpio).
    print(f"\n{sep}", file=sys.stderr)
    print(f"CONTRASTE — segunda lectura via Gemini {MODEL}", file=sys.stderr)
    if nombre_proyecto:
        print(f"Proyecto: {nombre_proyecto} | {n_docs} docs cargados", file=sys.stderr)
    print(f"{sep}\n", file=sys.stderr)
    print(respuesta.text)
    print(f"\n{sep}", file=sys.stderr)


if __name__ == "__main__":
    main()
