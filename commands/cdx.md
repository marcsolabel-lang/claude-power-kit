---
name: cdx
description: Interrogation loop that drives ambiguity to zero before working — rounds of sharp questions until you and the assistant are LOCKED (fully contextualized), then writes a persisted context lock aligned to what you're building. Two grains — `/cdx <task>` (per-prompt, fast) and `/cdx` (per-session, deep). Clarifies only; it does NOT execute.
---

# /cdx — interrogate until LOCKED, then close the context

> **Nota:** el artefacto que persiste esta skill es un **"cierre de contexto"** (context lock),
> NO el CLI de OpenAI Codex. `cdx` es el bucle de aclaración; no tiene nada que ver con `codex`.

Tu trabajo: llevar la **ambigüedad material a cero** antes de cualquier trabajo real,
interrogando en rondas que convergen, y luego escribir un **cierre de contexto** — un candado
persistido y compartido al que ambos os referís. El cierre es la respuesta a "¿estamos los dos
claros, alineados y cerrados antes de empezar?". Toda la salida es en castellano; tus notas,
telegráficas.

**Esta skill ACLARA, no ejecuta.** Termina haciendo hand-off (a `/plan`, o simplemente "ahora
trabajamos"). Nunca empieces a construir desde dentro de `/cdx`.

**Frontera con `/plan`:** usa `/cdx` cuando el bloqueo es la **ambigüedad** (aún no sabes QUÉ
construir — el porqué/el qué están abiertos); usa la fase *clarify* de `/plan` cuando ya sabes QUÉ
y solo falta el CÓMO (diseño/pasos). `/cdx` PRECEDE a `/plan`, no lo duplica.

**Anti-rumiación (innegociable):** el bucle debe CONVERGER, no dar vueltas. Pregunta solo lo que,
respondido distinto, **cambiaría el trabajo**. Si una ronda no saca nada nuevo y material, declara
`🔒 LOCKED` y para — no fabriques dudas ni persigas la certeza perfecta.

## Two grains (detéctalo del argumento)
- **`/cdx <tarea>`** → **grano PROMPT**: aclara la tarea inmediata. Rápido (normalmente 1-2 rondas).
- **`/cdx`** (solo) → **grano SESIÓN**: aclara el contexto de toda la sesión. Más hondo.

## Phase 1 — Read first (nunca preguntes lo que el repo ya responde)
Ánclate antes de interrogar:
- Grano SESIÓN: los docs del proyecto (README / notas de estado, la carpeta de decisiones/ADRs),
  cualquier plan activo en `.plans/`.
- Grano PROMPT: lee lo que la propia tarea toca; `grep -ri` en la carpeta de decisiones + el repo
  objetivo, buscando precedente.
Saca de los ficheros todo hecho respondible — gasta las preguntas solo en lo que no puedan
responder.

## Phase 2 — The interrogation loop (until LOCKED)
1. Lista las **incógnitas materiales** — las que, respondidas distinto, cambian alcance, enfoque,
   el "hecho" o el riesgo. Descarta lo trivial y lo que el repo ya responde.
2. Pregúntalas en **tandas vía AskUserQuestion** — afiladas, priorizadas, cada opción abriendo con
   una recomendación (nada de volcados sin priorizar). Esto es el "interrogatorio".
3. Tras cada ronda, dibuja el **tablero de convergencia** para que ambos veáis dónde estáis:
   ```
   CDX — [grano] · ronda [N]
   🔒 LOCKED:  [lo que ya está cerrado]
   ❓ FUZZY:   [lo que sigue abierto y por qué importa]
   ```
4. Repite hasta que nada material siga FUZZY, O tú lo des por cerrado. Regla de convergencia: una
   ronda que no añade respuesta material nueva ⇒ declara LOCKED. Máximo dos rondas para el grano
   prompt salvo que quieras cavar más.

## Phase 3 — Close the lock (persist)
Escribe el cierre en `.plans/lock-<slug>.md` y dibújalo. Recuerda:
- es el **candado de contexto compartido** para esta tarea/sesión;
- para conservarlo tras una compactación, dilo explícitamente al compactar;
- el **siguiente paso** (hand-off): `/plan` (build no trivial) o "ahora trabajamos" (bastante
  claro como para arrancar).

### Lock format
```
CIERRE DE CONTEXTO — [tarea o sesión] · [fecha]
Objetivo:        [qué se persigue, una frase]
Hecho cuándo:    [el criterio de aceptación = el test, verificable]
Fuera de alcance:[lo que explícitamente NO se hace]
Innegociables:   [reversibilidad, secretos, criterio supremo]
Decisiones cerradas: [- lo acordado en el interrogatorio]
Encaje:          [¿sirve a lo que estás construyendo? ✓/✗ por qué]
Abierto:         [lo que queda fuzzy a propósito, o "nada"]
Siguiente paso:  [/plan · trabajar]
```

## Rules
- Aclara solo — nunca ejecutes. Hand-off al final.
- Solo preguntas materiales — converge, no des vueltas. Nada nuevo material en una ronda → LOCK.
- No preguntes lo que el repo, el código o los ADR ya responden — léelos primero.
- Cada opción de AskUserQuestion abre con una recomendación.
- El cierre es el artefacto; declarar LOCKED es decisión tuya, no del asistente — el asistente lo
  propone, tú lo confirmas.
