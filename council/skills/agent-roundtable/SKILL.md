---
name: agent-roundtable
description: Consulta multi-IA de un solo disparo sobre UNA pregunta. Reúne a un consejo de IAs externas (OpenAI/ChatGPT vía codex, Gemini, NotebookLM) para que aporten riesgos y contra-argumentos, mientras Claude orquesta y decide EL ÚLTIMO. Los consejeros aconsejan; nunca deciden ni ejecutan. Todo lo que sale a una IA externa pasa antes por la puerta de EGRESS. Manual: se invoca a mano, nunca en segundo plano.
disable-model-invocation: true
---

# agent-roundtable — el consejo multi-IA de un disparo

Reúne a un consejo de IAs externas para que critiquen UNA pregunta concreta y
devuelvan **riesgos y contra-argumentos**. Claude no delega el juicio: orquesta el
consejo, publica su propia posición y **decide el último**. Las IAs externas
aconsejan; **nunca deciden ni ejecutan** nada.

Esta skill es **manual**: `disable-model-invocation: true`. Nunca se dispara sola,
nunca corre en segundo plano (headless). La lanzas tú a mano cuando quieres una
segunda, tercera y cuarta opinión sobre una decisión que importa.

## Cuándo usarla

Una decisión con coste real donde una sola cabeza (la de Claude) no basta: elegir
arquitectura del catálogo, decidir el modelo de datos de las obras/comisiones,
validar un enfoque de accesibilidad, comparar dos diseños de navegación, revisar
un texto público antes de publicarlo. **Una** pregunta por ronda.

No la uses para: tareas mecánicas, cambios triviales, o cualquier cosa que Claude
ya puede resolver solo (para eso está `/master-plan` en peldaño bajo).

## El consejo (4 asientos)

| Asiento | Rol | Cómo se llama |
|---|---|---|
| **Claude** | Orquestador. Publica su posición, contrasta, sintetiza, decide. | Nativo, esta sesión |
| **OpenAI / ChatGPT** | Consejero. Segunda lectura crítica. | CLI `codex exec --sandbox read-only` desde un cwd neutro |
| **Gemini** | Consejero. Contra-argumentos y riesgos. | Clave de AI Studio (`council/scripts/contrastar.py`) |
| **NotebookLM** | Consejero de corpus. Lo que dicen las fuentes. | **Pegado manual** por ti |

El roster está fijado en cuatro asientos. Un sistema anterior tenía un quinto
asiento (un modelo extra) que aquí se ha eliminado **por diseño**: no forma parte
de este consejo y no debe re-añadirse. Contratos de cada asiento, regla del sobre
y guardas: **`references/ai-registry.md`**.

## El protocolo de siete pasos (0 → 6)

Se ejecutan **en orden**. No se salta ninguno. Los pasos 0–2 ocurren **antes** de
que salga un solo byte al exterior.

### Paso 0 — Redactar UN prompt neutral

Escribe **un único** prompt para todos los asientos que pida explícitamente
**riesgos y contra-argumentos**, y que **NO contenga la inclinación de Claude**. Si
el prompt filtra hacia dónde se inclina Claude, los consejeros se anclan a esa
respuesta y el consejo pierde su valor (anti-anclaje). El prompt describe el
problema y pide crítica; no insinúa la solución preferida.

### Paso 1 — Checklist de EGRESS sobre los bytes exactos

Ejecuta la checklist de egress (**`references/egress-checklist.md`**) sobre **los
bytes exactos ya ensamblados** que van a salir — no sobre una versión anterior ni
sobre "lo que pretendo enviar". Se construye un **manifiesto literal** después de
armar el prompt final: symlinks resueltos, y cualquier fichero ilegible o binario
**falla CERRADO** (se aborta, no se asume inocente). Si aparece una **clase
prohibida** (secretos, datos privados, config del orquestador, mezcla de confianzas
tipo "trifecta letal"), **parada dura**: no sale nada.

### Paso 2 — Roster, health-check gratis, checkpoint humano

Elige qué asientos participan. Haz un **health-check gratuito** de cada uno (una
llamada trivial que confirme que está vivo y **qué modelo es realmente**; ver
registry). Muestra al usuario un **checkpoint**: el **hash del payload** que va a
salir + el roster elegido. El usuario da luz verde. Sin checkpoint no se abre el
consejo.

### Paso 3 — Fan-out + publicar la posición de Claude ANTES de leer nada

Envía el mismo prompt a los consejeros. **Antes de leer ninguna respuesta**, Claude
escribe **su propia posición independiente** en el acta (transcript). Esto es
anti-anclaje: la opinión de Claude queda fijada antes de contaminarse con las de
los demás. NotebookLM se sirve por **pegado manual** del usuario (no hay API), así
que su respuesta puede llegar más tarde en el flujo.

### Paso 4 — Recoger cada respuesta en un sobre

Cada respuesta se envuelve en un **sobre**:

```
{ provider, modelo OBSERVADO, duración, status }
```

- **Respuestas tardías se descartan** (llegaron fuera de ventana → no cuentan).
- **modelo observado ≠ modelo pedido → status = ABSENT** (guarda de sustitución: si
  pediste un modelo y respondió otro, esa voz no está en el consejo).
- Estados posibles: `OK`, `ABSENT`, `DEGRADED`, `NOT_APPLICABLE`. Definiciones en el
  registry.

### Paso 5 — Contrastar afirmación por afirmación

**Nunca** se pegan las salidas externas crudas una detrás de otra para "resumirlas"
juntas: eso es **contaminación**. En su lugar, de cada respuesta se **extraen
afirmaciones atribuidas** y se vuelcan a una **tabla de contraste**:

| Afirmación | Evidencia | Riesgo único | Incertidumbre | Quién lo dice |
|---|---|---|---|---|

Se **pesan los argumentos, no se cuentan cabezas**: tres asientos de acuerdo no
ganan a un cuarto con la mejor evidencia. La síntesis se construye **solo** desde
las afirmaciones atribuidas y extraídas — jamás concatenando los textos crudos.

### Paso 6 — Veredicto, filtro y acta saneada

Claude emite el **veredicto citando la disidencia** (qué asiento discrepó y por
qué; el desacuerdo no se esconde). El veredicto pasa por el **filtro de veredicto**
(abajo). Finalmente se escribe un **acta saneada** (run-trace): qué se preguntó,
qué asientos participaron, hash del payload, afirmaciones clave, veredicto — **sin
el payload literal** y sin las salidas crudas.

## Filtro de veredicto (determinista, no es una IA)

Lo aplica Claude siguiendo reglas fijas. **No** es otro modelo:

- **PASA** → embarcar (ship). El resultado es sólido y reversible.
- **NO PASA** → reformular con **el fallo concreto** y volver a intentar. **Máximo
  3 ciclos.** Si a los 3 no pasa, escala como CRUCIAL.
- **CRUCIAL** → **parar y preguntarte**. Es CRUCIAL cuando la decisión es:
  - **hacia fuera / irreversible** (algo público, un borrado, un despliegue),
  - **juicio confidencial** (datos personales, de clientes/comisiones),
  - **meta-cambio** (tocar el propio consejo, sus skills o su config),
  - **disidencia material sin resolver** (dos asientos con buena evidencia en
    contra y no se puede decidir con lo que hay).
  - **En la duda, es CRUCIAL.**

## Reglas duras (no negociables)

1. **Claude decide el último.** Los consejeros nunca son puerta ni ejecutor.
2. **Todo egress pasa la checklist ANTES** de salir, sobre los bytes exactos.
3. **Anti-anclaje**: el prompt no filtra la inclinación de Claude; Claude publica su
   posición antes de leer respuestas.
4. **Nunca contaminación**: no se concatenan salidas crudas; se extraen y atribuyen
   afirmaciones.
5. **Pesar argumentos, no contar cabezas.**
6. **Manual siempre**: nunca headless, nunca auto-invocada.

## Ficheros de esta skill

- `references/ai-registry.md` — contratos de asiento, sobre, guarda de sustitución,
  health-check gratis, cwd neutro, estados.
- `references/egress-checklist.md` — la puerta de salida, manifiesto y clases
  prohibidas.
- `../../scripts/contrastar.py` — segunda lectura por Gemini (contraste con veredicto).
