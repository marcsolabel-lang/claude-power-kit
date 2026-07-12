---
name: plan
description: Disciplined planning & execution for any non-trivial change. Clarify → explore → design → plan → execute → verify, using the architect/adr-writer agents. Modes — `/plan <change>` (full cycle), `/plan audit <repo>` (read-only health report), `/plan design <question>` (stop at the design fork).
---

# /plan — planificación y ejecución disciplinada

Método de trabajo para los cambios que merece la pena hacer bien. La fuerza está en la
DISCIPLINA, no en los pasos: nada de código antes de acordar el enfoque, exploración real antes
de diseñar, pasos pequeños y reversibles, verificación antes de dar algo por "hecho".

**Idioma de salida:** todo el chat, las preguntas, las opciones y el fichero de plan se escriben
en **castellano**. Estas instrucciones van en inglés (convención de máquina). Sé frugal con los
tokens: lee cada plantilla o doc solo cuando llegues al gate que lo necesita.

**Modos** (el primer argumento elige uno; por defecto, el ciclo completo):
- `/plan <cambio>` — ciclo completo sobre un cambio.
- `/plan audit <repo>` — informe de salud de solo lectura, sin cambios (ver Modo auditoría).
- `/plan design <pregunta>` — para en la bifurcación de diseño: opciones + recomendación, sin ejecutar.
- `--ver` — muestra el plan de gates + preguntas de aclaración ANTES de correr; tú confirmas o ajustas.

---

## Phase 0 — Scope check (segundos, siempre)
¿Es trivial? Una línea, un typo, un fix obvio → **sáltate la ceremonia y hazlo**. El método es
para cambios con más de un paso o consecuencias reales. No burocratices el trabajo pequeño — eso
es fricción, no rigor.

## Phase 1 — Clarify (socrático, aún sin código — el único gate no saltable)
Lee primero, pregunta después. Saca a la luz las incógnitas reales, ancladas en el repo. Hazte (o
pregúntale al usuario) las 6 preguntas universales de arranque:
1. ¿Qué problema resuelve y cuánto tiempo/fricción ahorra?
2. ¿Quién lo usa y cómo? (el flujo de uso, no la implementación)
3. ¿Cómo se ve "hecho y bien"? ¿Cuál es el criterio de aceptación? (= el test)
4. ¿Qué casos límite hay? ¿Qué queda explícitamente FUERA de alcance?
5. ¿Qué innegociables aplican? (secretos, reversibilidad, criterio supremo)
6. ¿Hay decisiones que merezcan un ADR?

Fija también: ¿qué repo(s)? ¿reversible o destructivo? ¿hay precedente — un ADR o un patrón ya
existente? (`grep -ri` en la carpeta de decisiones/ADRs + el repo objetivo.) Usa
**AskUserQuestion** para las bifurcaciones reales. Nunca preguntes lo que el código ya responde.
La ambigüedad es lo que mata la finalización — no te saltes este gate. Si el bloqueo es la
ambigüedad de fondo (aún no está claro QUÉ construir, no solo el CÓMO), cierra el contexto con
`/cdx` primero y vuelve aquí.

## Phase 2 — Explore before designing (delega — esto es el motor)
Para cualquier cosa no obvia, lanza **subagentes Explore/Agent en paralelo** para mapear el
terreno real ANTES de proponer. Lee los ficheros que saquen. La mayoría de los planes malos
mueren aquí: diseñar contra suposiciones en vez de contra el código real. Explorar es barato;
planificar a ciegas es caro.

## Phase 3 — Design (opciones → una recomendación)
- Espacio de soluciones amplio → presenta **2-3 enfoques honestos** (trade-offs, esfuerzo) y
  **abre con una recomendación**. Nada de listas de opciones sin priorizar.
- Espacio estrecho → dilo, propón el único.
- **Necesidad primero:** antes de proponer CONSTRUIR nada, bájalo por la escalera de simplicidad —
  ¿hace falta? → ¿lo cubre algo que ya existe? → ¿capacidad nativa? → ¿una dependencia ya
  instalada? → ¿una línea? → solo entonces, lo mínimo. El primer peldaño satisfecho gana.
- Si la idea es estructural (toca estructura / dependencias / interfaces, o es la primera de su
  tipo), invoca al agente `architect` para sopesar opciones, y luego a `adr-writer` para escribir
  un ADR en `docs/decisions/` usando la plantilla de ADR del kit (`doctrine/`). Los ADR aceptados
  son ley — se sustituyen con un ADR nuevo, nunca se editan.
Consigue **acuerdo explícito** antes de escribir un plan. Nunca avances sobre el silencio.

## Phase 4 — Plan (granular, reversible, escrito)
Escribe el plan en `.plans/<slug>.md` (dentro del repo). Cada paso indica: el/los fichero(s) que
toca · qué cambia · cómo se revierte (git revert / qué commit) · cómo se verifica (`bash -n`, un
`grep`, un dry-run, un test). Pasos lo bastante pequeños como para verificarse de uno en uno. Si
un paso no se puede revertir o verificar, **márcalo**.
**Troceo por tracer bullets:** corta en pasos VERTICALES finos que crucen todas las capas de
punta a punta (primero un esqueleto ejecutable), no capas horizontales construidas enteras antes
de conectarse. El paso 1 debería producir algo demostrable de punta a punta, por mínimo que sea;
los pasos siguientes lo ensanchan. Es el antídoto contra el sobre-diseño: prefiere el corte que
cierra el bucle al que construye más infraestructura.
Para un proyecto de verdad, produce también la cola de issues (cada issue con ruta de fichero
exacta, un criterio de éxito observable y una verificación concreta) y pasa una checklist de
calidad rápida: ¿el spec es claro? · ¿cada issue es verificable? · ¿hay criterio de aceptación? ·
¿está el alcance cerrado? · ¿los pasos son reversibles? · ¿se respeta el precedente? · ¿algún
innegociable en riesgo? Si algún punto falla, NO empieces — arregla antes el spec/las issues. La
checklist para por calidad, no por permiso.

## Phase 5 — Execute + verify each step
**Re-verifica antes de ejecutar un plan escrito antes** (otra sesión/otro día): puede que la
necesidad se haya resuelto por el camino — confirma que la premisa de cada paso sigue en pie
contra el repo vivo. Si un hallazgo desapareció, tira ese paso y anota por qué; nunca ejecutes
trabajo caducado.
Un paso cada vez: **dry-run si es destructivo → cambio → verifica de inmediato → commit atómico**.
Método: explorar → planificar → cambio quirúrgico → verificar, con diffs pequeños. El trabajo
reversible y local fluye y auditas después; el gate salta solo en pasos hacia fuera/irreversibles.
Nunca acumules cambios sin verificar. Nunca un commit gigante. Si una verificación falla, **para
y repórtalo con honestidad** — no lo maquilles. Los mensajes de commit siguen la convención del
repo (cuerpo en inglés, prefijo `feat`/`docs`/`chore`).

## Phase 6 — Close
Actualiza el fichero de plan (`✓ hecho` / `⚠ bloqueado por X`). Haz push solo si te lo han pedido;
cualquier cosa hacia fuera/irreversible espera confirmación. Actualiza notas/memoria solo ante un
aprendizaje real y duradero — nunca por rutina.

---

## Audit mode (`/plan audit <repo>`)
Solo lectura. Reporta el estado vivo, anclado (nada de números inventados — léelos):
- `git -C <repo> log --oneline -20` · `git status` · commits sin subir · ramas.
- Cuenta los ADR reales (`ls docs/decisions/*.md`), comprueba la integridad de la cadena (estados,
  supersesiones).
- Notas o TODOs pendientes en los docs.
Disciplina de hallazgos: pásalos por un embudo — dedup por causa raíz, refutadores adversariales,
etiqueta `CONFIRMADO`/`PLAUSIBLE`, lo no verificado va a un anexo de cuarentena ("sospechas, no
hechos"), y cada hallazgo vivo cierra con un artefacto concreto. Cierra con un "¿siguiente paso?"
priorizado — sugiere, no actúes.

## Design mode (`/plan design <pregunta>`)
Corre las fases 1-3 y PARA en la bifurcación de diseño: opciones + una recomendación, sin fichero
de plan, sin ejecución.

## Guardrails (innegociables)
- **Verdad del terreno:** no edites el CONTENIDO de un doc por inferencia; git es la fuente de la
  verdad. Si algo contradice el repo vivo, para.
- **Deny-list:** nunca `push --force` / `push -f`, `rm -rf` de home o raíz, `reset --hard`,
  `clean -f`, `DROP TABLE/DATABASE`. Si un paso necesita uno → **para y pregunta**.
- **Hacia fuera:** cualquier acción irreversible o que salga del repo (publicar, borrar remoto,
  tocar datos reales) espera confirmación explícita.

## On plan mode — la mecánica real (sin magia)
Una skill son instrucciones, **no código**: no puede entrar en plan mode por ti. Dos caminos
honestos a la aprobación:
- **Entras tú en plan mode** (Shift+Tab). Este método moldea *cómo* planificas; presentas el plan
  terminado vía **ExitPlanMode** para su aprobación.
- **O** presentas el plan conversacionalmente y **esperas un "sí" explícito** antes de ejecutar.
En ambos casos: el fichero de plan es el artefacto, la aprobación es tuya, la ejecución nunca la
precede.

## Por qué merece la ceremonia
El contraste (una segunda perspectiva real antes de comprometerse) y la estructura son lo que
hacen fuerte a un plan. En una tarea del tamaño adecuado, esto convierte un encargo vago en un
cambio revisado, reversible y verificado. En una línea es pura fricción — por eso existe la
Phase 0. Ajusta el rigor a la tarea.
