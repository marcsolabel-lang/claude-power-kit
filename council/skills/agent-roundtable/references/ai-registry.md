# ai-registry — contratos de asiento del consejo

Contrato de cada IA externa del consejo: cómo se la llama, cómo se hace su
health-check gratuito, qué modelo debe observarse, y qué significa cada estado del
sobre. Lo lee `/agent-roundtable` (pasos 2–4) y `/master-plan` (peldaños medium+).

## Regla del sobre (todas las respuestas)

Toda respuesta de un consejero se guarda envuelta en un **sobre**:

```
{ provider, modelo_observado, duracion_ms, status }
```

- `provider` — el asiento: `openai-codex`, `gemini`, `notebooklm`.
- `modelo_observado` — el modelo que **de verdad** respondió (leído de la salida o
  del comando de versión), **no** el que se pidió de palabra.
- `duracion_ms` — cuánto tardó desde el envío.
- `status` — uno de: `OK`, `ABSENT`, `DEGRADED`, `NOT_APPLICABLE`.

**Respuestas tardías se descartan.** Si un consejero contesta después de cerrar la
ventana de recogida, su voz **no entra** en el contraste.

## Guarda de sustitución

Si `modelo_observado ≠ modelo_pedido`, el status es **`ABSENT`**. No importa que la
respuesta parezca buena: si el asiento sirvió otro modelo distinto al pactado, esa
voz **no cuenta** en el consejo. Se registra en el acta como ABSENT y se sigue con
los que sí cumplieron. Nunca se "acepta igualmente" un modelo sustituido.

## Estados

| Status | Significado | Qué se hace |
|---|---|---|
| `OK` | Respondió, a tiempo, con el modelo pedido. | Entra al contraste (paso 5). |
| `ABSENT` | No respondió, tarde, o modelo sustituido. | No cuenta. Se anota en el acta. |
| `DEGRADED` | Respondió pero incompleto/truncado/con error parcial. | Entra con **peso reducido**; se marca la incertidumbre alta. |
| `NOT_APPLICABLE` | El asiento no aplica a esta pregunta (p. ej. NotebookLM sin corpus relevante). | Se omite sin penalizar el consejo. |

## Health-check gratuito (paso 2, antes del payload real)

Antes de mandar el prompt real, se hace una llamada **trivial y barata** a cada
asiento para confirmar dos cosas: (a) está **vivo**, y (b) **qué modelo es
realmente**. Nunca se manda el payload real a un asiento cuyo health-check no
confirma el modelo esperado.

---

## Asiento 1 — OpenAI / ChatGPT vía `codex`

**Cómo se llama:**

```
codex exec --sandbox read-only "<PROMPT NEUTRAL>"
```

- **`--sandbox read-only`**: el CLI no puede escribir nada. Obligatorio.
- **cwd NEUTRO**: se ejecuta desde un **directorio vacío y con `git init`**, aparte
  del proyecto real. Así el sandbox de codex no tiene a mano los ficheros del
  catálogo ni nada privado, aunque intentara leerlos. Ejemplo de preparación:

  ```
  # crear una vez un cwd neutro y usarlo SIEMPRE para el consejo
  mkdir -p "%USERPROFILE%\council-neutral"   # Windows ahora
  cd "%USERPROFILE%\council-neutral"
  git init -q
  codex exec --sandbox read-only "<PROMPT>"
  ```

  En Linux (más adelante) es el mismo patrón con `~/council-neutral`. La regla no
  cambia: **el prompt lleva todo el contexto necesario; el cwd no aporta nada.**

**Health-check gratis:** `codex --version` (confirma que el CLI responde). El modelo
observado se lee de la cabecera/salida de la propia ejecución.

**Modelo observado:** el que codex reporte en su salida. Si difiere del pactado →
`ABSENT` (guarda de sustitución).

**Requisito previo:** `codex login` hecho una vez (ver `council/README.md`).

---

## Asiento 2 — Gemini (clave de AI Studio)

**Cómo se llama:** vía el script de contraste:

```
python council/scripts/contrastar.py --repo . "<TEXTO A CONTRASTAR>"
```

o para una segunda lectura de un fichero concreto:

```
python council/scripts/contrastar.py --archivo docs/plan.md
```

- Clave leída de `GEMINI_API_KEY` (variable de entorno) o del fichero
  `~/.claude/gemini-api-key.txt`. La clave **nunca** se pega en el prompt ni sale en
  ningún payload (es clase prohibida en egress).
- Modelo pedido: `gemini-2.5-flash` (ver el script).

**Health-check gratis:** una generación mínima (un "ping") con el mismo modelo, que
confirma clave válida y modelo. El script imprime a stderr el modelo que usa.

**Modelo observado:** el `MODEL` con el que responde la API. Distinto del pedido →
`ABSENT`.

---

## Asiento 3 — NotebookLM (pegado MANUAL)

**Cómo se llama:** NotebookLM **no tiene API** en este consejo. El usuario abre su
cuaderno, pega **a mano** el prompt neutral, y copia la respuesta de vuelta al acta.

- Por eso su respuesta puede llegar **más tarde** en el flujo (paso 3 lo contempla).
- Su valor es el **corpus**: lo que dicen las fuentes que el usuario ha cargado
  (referencias de escritura/literatura, guías de estilo, ejemplos de catálogos de
  arte). Aporta "qué dicen las fuentes", no opinión libre.

**Health-check:** no aplica (es manual). Si el usuario no tiene un cuaderno relevante
para la pregunta, el asiento es `NOT_APPLICABLE` y se omite sin penalizar.

**Modelo observado:** no se controla el modelo interno; se trata como fuente de
corpus citado, no como voz de modelo con guarda de sustitución.

---

## Asiento 4 — Claude (orquestador, nativo)

No es un consejero externo: es quien **orquesta y decide el último**. Publica su
posición independiente **antes** de leer las respuestas de los demás (anti-anclaje,
paso 3), construye la tabla de contraste (paso 5), aplica el filtro de veredicto y
escribe el acta. No pasa por egress consigo mismo (es local), pero **todo lo que
salga de él hacia otro asiento sí** pasa la checklist.

---

## El quinto asiento: ausente por diseño

El roster es de **cuatro asientos y ninguno más**. Un sistema anterior incluía un
quinto asiento (un modelo extra) que aquí se ha **retirado por completo,
deliberadamente**. No forma parte de este consejo y **no debe re-añadirse** sin
rehacer los contratos de asiento, el egress y el filtro de veredicto. Añadir un
asiento es un **meta-cambio** → CRUCIAL → decide el usuario.

## Recordatorio de contaminación

En el paso 5 **nunca** se pegan las salidas crudas de varios asientos juntas para
resumirlas. De cada sobre `OK`/`DEGRADED` se **extraen afirmaciones atribuidas** y
se llevan a la tabla. Concatenar textos crudos de distintas fuentes en un mismo
buffer es contaminación y está prohibido.
