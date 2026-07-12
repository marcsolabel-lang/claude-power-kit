# CLAUDE.md — kernel del kit

Instrucciones que se aplican en cualquier sesión de Claude Code dentro de este kit.
El contexto de cada proyecto concreto vive en su propio `CLAUDE.md` (p. ej. `project-comisiones/CLAUDE.md`).

---

## Quién soy

Desarrollador en solitario. Estoy montando un sitio web (catálogo en HTML) para
gestionar los encargos de escritura/literatura y arte de un artista o creador. Trabajo hoy en Windows;
el sábado paso a CachyOS (Linux).

No tengo un equipo detrás: soy yo y tú. Las decisiones son mías, la ejecución la repartimos.

---

## Cómo me gusta trabajar

- **Peticiones pequeñas y verificables.** Un cambio cada vez, que yo pueda comprobar antes de
  seguir. Prefiero tres pasos claros a un salto grande que no sé si funciona.
- **git es la red de seguridad.** Antes de un cambio grande, deja el árbol limpio (o proponme un
  commit). Si algo se rompe, se revierte y no se pierde nada. Nunca reescribas la historia.
- **Commits SOLO cuando lo pido explícitamente.** No hagas `git commit` ni `git push` por tu
  cuenta. Prepara el cambio, enséñamelo, y espera a que yo diga "commitea".
- **Castellano en lo que consumo yo** (respuestas de chat, docs, notas de proyecto).
  **Inglés en lo que consume la máquina**: mensajes de commit e identificadores/comentarios del
  código. El repo puede acabar siendo público. Los prefijos de commit (`feat`/`docs`/`chore`…)
  son interfaz estable, no se traducen.
- **Directo.** Sin preámbulos ("¡Buena pregunta!") ni resúmenes finales que repiten lo ya dicho.
  Profundo cuando el tema lo pide, corto cuando la pregunta es puntual.
- **Honestidad epistémica.** Distingue lo que sabes con certeza, lo que es estimación y lo que
  hay que verificar. Si digo algo incorrecto, corrígeme con argumentos. Si te falta contexto para
  responder bien, pídelo en una sola pregunta.

---

## Escalera de simplicidad (antes de construir nada)

Antes de proponer crear algo (un archivo, un script, una dependencia, una skill), baja la escalera:

1. ¿Hace falta de verdad?
2. ¿Lo cubre algo que ya tengo en el kit?
3. ¿Hay una capacidad nativa de Claude Code / del stack que lo haga?
4. ¿Una dependencia ya instalada?
5. ¿Se resuelve en una línea?
6. Solo entonces: lo mínimo que funcione.

Construir menos, reutilizar más. Lo que ya existe gana a lo que hay que crear.

---

## Qué hay en el kit (índice)

Este archivo es el índice; cada pieza tiene su fuente de verdad en su carpeta. No dupliques
listas aquí — enlaza al sitio canónico.

- **`commands/`** — skills invocables por slash (`/plan`, `/cdx`, `/check`, `taste-skill`,
  `emil-design-eng`…). Se copian a `~/.claude/commands/` para que Claude Code las vea.
- **`agents/`** — subagentes especializados que usan algunas skills. Se copian a `~/.claude/agents/`.
- **`council/`** — el consejo: un panel de revisores expertos que convocas para criticar una
  decisión o un diseño antes de darlo por bueno.
- **`doctrine/`** — plantillas y método (p. ej. la forma de un `spec.md`). El "cómo se hacen las
  cosas" del kit.
- **`.claude/settings.json`** — permisos: la lista de lo permitido (dev genérico) y la red de
  seguridad (lo denegado). Se fusiona con tu `~/.claude/settings.json`.
- **`project-comisiones/`** — el primer proyecto real: el catálogo de encargos. Su `CLAUDE.md`
  tiene el contexto y `spec.md` la especificación de la v1.

Arranque completo y pasos de instalación: **`README.md`**.

---

## Doctrina: fuente única de verdad + anti-inflación

- **Fuente única de verdad.** Cada hecho vive en UN solo sitio canónico. El catálogo de skills es
  `commands/`; la doctrina es `doctrine/`; el contexto de un proyecto es su `CLAUDE.md`. Si algo se
  lista o se cuenta a mano en dos sitios, driftea. Enlaza al canónico en vez de copiar.
- **Anti-inflación.** No crees skills, scripts ni docs "por si acaso". Si algo se puede resolver
  reutilizando lo que ya hay, se reutiliza. Un archivo nuevo tiene que justificar su existencia.
- **El agente corrige el drift, no lo reporta y espera.** Si al pasar por un doc ves un enlace roto
  o un dato desfasado y el arreglo es obvio y reversible, arréglalo en el momento; no me hagas una
  lista de cosas para que las corrija yo.
