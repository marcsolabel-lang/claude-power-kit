---
name: check
description: Automatic second reading via the Gemini API. Cross-checks any text or analysis against the docs of the active project — the repo is auto-detected. Invoke after producing an analysis or decision (or before publishing something) to cross-check it. Zero copy/paste between tools.
---

You are the trigger for the second-reading cross-check system.

---

## What it does

Toma un texto (salida de la sesión, un análisis, una decisión) y lo manda a Gemini junto con los
docs del proyecto en el que estás trabajando. Gemini actúa como una segunda voz independiente y
devuelve un veredicto de consistencia aquí mismo.

Autodetección: escanea los `.md` del repo actual. Sin repo → contrasta solo con criterio general.

**Qué sale de tu máquina:** solo el texto que le pasas + los docs que apuntas. Nada más. El free
tier de la API de Gemini no garantiza que tu contenido no se use para entrenar, así que manda solo
lo que no te importe compartir; para material sensible, fragmentos escogidos, no el repo entero.

---

## How to invoke

El motor es el script `council/scripts/contrastar.py` (lo construye otro agente del kit). Córrelo
con un Python que tenga `google-genai` instalado.

**Texto directo (lo más común — contrasta la salida de la sesión):**
```bash
python council/scripts/contrastar.py "pega aquí el texto a contrastar"
```

**Contrastar un fichero generado durante la sesión:**
```bash
python council/scripts/contrastar.py --archivo "ruta/al/fichero.md"
```

**Proyecto explícito:**
```bash
python council/scripts/contrastar.py --proyecto nombre-proyecto "texto"
```

**Cualquier repo externo como fuente de docs:**
```bash
python council/scripts/contrastar.py --repo "ruta/a/otro-proyecto" "texto"
```

**Sin docs (solo criterio general de Gemini):**
```bash
python council/scripts/contrastar.py --sin-docs "texto"
```

(Las rutas son relativas a la raíz del kit; si corres desde `commands/`, antepón `../`.)

---

## When to invoke it

- Tras un análisis o una decisión → contrasta que no contradice los docs del repo.
- Antes de publicar algo hacia fuera (una página del catálogo, un texto que verá otra persona) →
  verifica que el encuadre es correcto y no se contradice con lo ya escrito.
- En cualquier repo del proyecto.

Alcance: `/check` es la segunda lectura INSTANTÁNEA, gratis y de un solo modelo (consistencia). No
crece hacia consulta deliberativa multi-modelo — para una decisión con coste de error material,
eso es otra herramienta.

---

## Prerequisite — Gemini API key

El script lee tu clave de un fichero local (convención del kit: `council/gemini-api-key.txt`,
fuera de git). Pega ahí tu clave (gratis en https://aistudio.google.com/apikey).

El free tier (Gemini 2.5 Flash · 1M tokens · 1500 llamadas/día) sobra para este uso.

**Intérprete:** corre siempre con un Python que tenga `google-genai` instalado (idealmente un
venv), no el Python del sistema pelado, o dará `ModuleNotFoundError`.

---

## Verdict que devuelve Gemini

El veredicto viene en castellano:

```
✓  consistente  — respaldado por [doc]
✗  contradice   — [doc] dice: [cita exacta]
?  no cubierto  — no está en los docs

RESUMEN
Consistencia: ALTA / MEDIA / BAJA
Contradicciones: N — cómo resolverlas
Lagunas: N — si son abiertas o no documentadas
Recomendación: [una frase directa]
```
