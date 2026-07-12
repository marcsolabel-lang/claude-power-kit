---
name: master-plan
description: Planificación disciplinada con ESCALERA DE ESFUERZO. Convierte un objetivo en un plan por fases con una cantidad de llamadas externas calibrada al peldaño (low = Claude solo, sin llamadas; medium = una segunda lectura con codex; high = además una ronda de consejo; xhigh/ultracode = más contraste interno). Anuncia peldaño + llamadas + techos ANTES de la primera llamada externa. Produce el plan; NUNCA lo ejecuta. Manual: se invoca a mano, nunca en segundo plano.
disable-model-invocation: true
---

# master-plan — planificar con escalera de esfuerzo

Convierte un objetivo en un **plan** ordenado por fases, gastando en consulta
externa **solo lo que el problema merece**. El esfuerzo se elige por **peldaño**, se
anuncia antes de gastar, y no se auto-escala. La skill **produce el plan; nunca lo
ejecuta.**

Es **manual**: `disable-model-invocation: true`. Nunca corre sola ni en segundo
plano (headless). La lanzas tú cuando quieres un plan pensado, no una acción.

## Regla de oro: produce, no ejecuta

`/master-plan` entrega **un plan** — fases, decisiones, riesgos, criterio de "hecho".
No escribe código de producción, no despliega, no borra, no publica. Cuando el plan
esté listo, la ejecución es un paso aparte que decides tú.

## La escalera de esfuerzo

Cada peldaño fija cuántas **llamadas externas** se permiten. Antes de la **primera
llamada externa**, Claude **anuncia**: `peldaño elegido + nº de llamadas previstas +
techos`. Nunca se auto-escala de un peldaño al siguiente por su cuenta: si el
problema pide más, se te dice y **tú** subes el peldaño.

| Peldaño | Llamadas externas | Qué hace |
|---|---|---|
| **low** | **0** | Claude planifica **solo**. Cero llamadas al exterior. |
| **medium** | 1 | Borrador → **egress** → **una** segunda lectura con `codex` (read-only, cwd neutro). |
| **high** *(por defecto)* | 1 + ronda | medium **más** una ronda de `/agent-roundtable` sobre la decisión clave. |
| **xhigh** | interno | Como high **más** fan-out **interno** (más contraste de Claude consigo mismo por fases), sin multiplicar el egress. |
| **ultracode** | interno++ | El techo. Máximo contraste interno, misma disciplina de egress. |

**Por defecto = high.** Si no dices peldaño, se planifica en `high`.

### Cómo se anuncia (obligatorio, antes de la 1ª llamada externa)

```
Peldaño: high
Llamadas externas previstas: 1 codex (medium) + 1 ronda roundtable
Techos: máx 3 ciclos de reformulación · egress obligatorio por cada salida
```

Si el peldaño es **low**, se dice igual: "Peldaño low — 0 llamadas externas".

## Flujo de la skill

1. **Encuadrar el objetivo.** Una frase: qué se quiere lograr y por qué. Si falta
   contexto material, **una** pregunta antes de seguir.
2. **Elegir peldaño** (o usar `high` por defecto) y **anunciarlo** con llamadas y
   techos.
3. **Borrador del plan** (Claude solo): fases, decisiones abiertas, riesgos.
4. **Contraste según peldaño**:
   - `low`: nada externo.
   - `medium`: pasa el borrador por **egress**, luego **una** segunda lectura con
     `codex` (`references/ai-registry.md`).
   - `high`: además dispara **una** ronda de `/agent-roundtable` sobre la decisión
     que más pesa.
   - `xhigh`/`ultracode`: más contraste **interno** de Claude, mismo egress.
5. **Filtro de veredicto** sobre el plan resultante:
   - **PASA** → entregar el plan.
   - **NO PASA** → reformular con el fallo concreto (**máx 3 ciclos**).
   - **CRUCIAL** → parar y preguntarte (hacia fuera / irreversible,
     confidencial, meta-cambio, o disidencia material sin resolver; en la duda,
     CRUCIAL).
6. **Entregar el plan** + un acta breve: peldaño usado, llamadas hechas, veredicto.
   Sin payloads literales.

## Egress: siempre, antes de cada salida

Toda llamada externa (codex, Gemini, o el fan-out de `/agent-roundtable`) pasa
**antes** por la checklist de egress sobre los bytes exactos:
`../agent-roundtable/references/egress-checklist.md`. Clase prohibida → parada dura.

## Guarda de recursión

`/master-plan` **no se llama a sí misma** ni encadena ronda sobre ronda de forma
automática. Una ronda de consejo por decisión clave, y el resultado vuelve a Claude.
El fan-out de `/agent-roundtable` es **hub-and-spoke**: los consejeros no re-lanzan a
otros consejeros. Si un peldaño no basta, se escala **a ti**, no a otra vuelta.

## Reglas duras

1. **Produce el plan; nunca lo ejecuta.**
2. **Anuncia peldaño + llamadas + techos ANTES** de la primera llamada externa.
3. **No auto-escala** de peldaño: lo subes tú.
4. **Egress antes de cada salida**; clase prohibida = parada dura.
5. **Máx 3 ciclos** de reformulación; luego CRUCIAL.
6. **Manual siempre**: nunca headless, nunca auto-invocada.

## Relación con el consejo

`/master-plan` es la capa de **planificación**; `/agent-roundtable` es la capa de
**consulta de una pregunta**. En `high`, master-plan **usa** roundtable para la
decisión que más pesa. Ambas comparten la misma puerta de egress y el mismo filtro
de veredicto.
