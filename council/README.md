# El consejo multi-IA — cómo montarlo (Windows ahora)

Un **consejo de cuatro IAs** para decidir mejor. Claude **orquesta y decide el
último**; las otras tres **aconsejan** (riesgos y contra-argumentos), nunca deciden
ni ejecutan. Todo lo que sale a una IA externa pasa antes por una **puerta de
salida (egress)**.

Dos skills, ambas **manuales** (nunca se disparan solas):

- **`/master-plan`** — planificar con una escalera de esfuerzo (gastas en consulta
  externa solo lo que el problema merece).
- **`/agent-roundtable`** — consultar UNA pregunta a todo el consejo de un disparo.

Todo esto funciona **ya en Windows**, antes de pasar a CachyOS el sábado. Nada de
lo de aquí depende de Linux; el sábado se migra el mismo montaje sin cambios.

---

## Los cuatro asientos

| Asiento | Rol | Necesita |
|---|---|---|
| **Claude** | Orquestador, decide el último | Esta sesión (nativo) |
| **OpenAI / ChatGPT** | Consejero, vía CLI `codex` | `codex login` (una vez) |
| **Gemini** | Consejero, segunda lectura | Clave de AI Studio + Python |
| **NotebookLM** | Consejero de corpus | Pegado **manual** (sin API) |

Son **cuatro y ninguno más**: el roster está cerrado por diseño.

---

## 1. Asiento OpenAI/ChatGPT — el CLI `codex`

Ya tienes el CLI `codex`. Solo hay que iniciar sesión una vez:

```
codex login
```

El consejo **siempre** llama a codex así, en modo solo-lectura y desde un
**directorio neutro y vacío**:

```
codex exec --sandbox read-only "<PROMPT>"
```

**Por qué un cwd neutro:** codex puede leer ficheros de su carpeta de trabajo. Si lo
lanzaras desde tu repo del catálogo, tendría a mano tus ficheros. Lanzándolo desde
una carpeta vacía con `git init`, el prompt lleva **todo** el contexto y el disco no
aporta nada. Prepáralo una vez:

```
mkdir "%USERPROFILE%\council-neutral"
cd "%USERPROFILE%\council-neutral"
git init
```

Y usa **siempre esa carpeta** para lanzar codex dentro del consejo.

---

## 2. Asiento Gemini — clave de AI Studio + Python

**Clave (gratis):** créala en https://aistudio.google.com/apikey y guárdala de una
de estas dos formas (la segunda es la cómoda):

- Variable de entorno `GEMINI_API_KEY`, **o**
- Fichero de una línea en `~/.claude/gemini-api-key.txt` (en Windows,
  `%USERPROFILE%\.claude\gemini-api-key.txt`) con solo la clave dentro.

La clave **nunca** se pega en un prompt ni sale en ningún envío (es clase prohibida
en la puerta de salida).

**Python:** el asiento Gemini usa `council/scripts/contrastar.py`, que necesita:

```
pip install google-genai
```

(Python 3.9+.) Es lo **único** que necesita Python en todo el consejo. codex y
NotebookLM no lo requieren.

**Probarlo:**

```
python council\scripts\contrastar.py --sin-docs "un texto cualquiera para ver que responde"
```

Uso normal, contrastando contra los docs de un repo (auto-detecta la raíz git del
directorio actual; prefiere `./docs` si existe):

```
cd C:\repos\mi-catalogo
python C:\ruta\a\council\scripts\contrastar.py --repo . "el texto o decisión a revisar"
```

Devuelve un contraste con veredicto (consistencia ALTA/MEDIA/BAJA, contradicciones,
lagunas y una recomendación directa).

---

## 3. Asiento NotebookLM — pegado manual

NotebookLM **no tiene API** en este consejo: se opera **a mano**.

1. Abre tu cuaderno de NotebookLM con las fuentes cargadas (referencias de
   escritura/literatura, guías de estilo, ejemplos de catálogos de arte).
2. Pega el **prompt neutral** que te dé el consejo.
3. Copia la respuesta de vuelta al acta cuando la tengas.

Por eso su respuesta puede llegar más tarde en el flujo — está previsto. Si no
tienes un cuaderno relevante para la pregunta, ese asiento simplemente no participa
en esa ronda.

---

## Lo que hace falta, en corto

| Asiento | Requisito | ¿Python? |
|---|---|---|
| Claude | Esta sesión | No |
| codex | `codex login` una vez + carpeta neutra con `git init` | No |
| Gemini | Clave AI Studio (env o fichero) + `pip install google-genai` | **Sí** |
| NotebookLM | Un cuaderno con fuentes | No (manual) |

---

## Las reglas que nunca cambian

- **Claude decide el último.** Los consejeros aconsejan; no son puerta ni ejecutor.
- **Todo egress pasa la puerta de salida** antes de enviar, sobre los bytes exactos.
  Secretos, datos privados, la config del propio consejo y las mezclas de confianza
  peligrosas **no salen** (parada dura). Detalle:
  `skills/agent-roundtable/references/egress-checklist.md`.
- **Anti-anclaje:** el prompt no revela hacia dónde se inclina Claude, y Claude
  publica su posición antes de leer las respuestas de los demás.
- **Se pesan argumentos, no se cuentan cabezas.**
- **Filtro de veredicto:** PASA → adelante · NO PASA → reformular con el fallo (máx
  3 vueltas) · CRUCIAL → parar y preguntarte a ti (todo lo irreversible, hacia
  fuera, confidencial o con desacuerdo serio sin resolver; en la duda, CRUCIAL).
- **Manuales siempre:** ni `/master-plan` ni `/agent-roundtable` se ejecutan solas.

## Estructura

```
council/
  README.md                        ← este fichero
  skills/
    master-plan/SKILL.md           ← planificar con escalera de esfuerzo
    agent-roundtable/SKILL.md      ← consultar UNA pregunta al consejo
    agent-roundtable/references/
      ai-registry.md               ← contratos de asiento, sobre, health-check
      egress-checklist.md          ← la puerta de salida
  scripts/
    contrastar.py                  ← segunda lectura por Gemini
commands/
  master-plan.md                   ← comando de entrada (thin)
  agent-roundtable.md              ← comando de entrada (thin)
```
