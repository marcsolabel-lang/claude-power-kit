---
name: master-plan
description: Planificación disciplinada con escalera de esfuerzo (low = Claude solo · medium = una segunda lectura con codex · high = además una ronda de consejo · xhigh/ultracode = más contraste interno). Anuncia peldaño + llamadas + techos antes de la primera llamada externa. Produce el plan; nunca lo ejecuta. Manual.
disable-model-invocation: true
---

# /master-plan

Comando de entrada. Carga y sigue la skill:

**`../council/skills/master-plan/SKILL.md`**

Manual siempre (`disable-model-invocation: true`): se invoca a mano, nunca en
segundo plano ni auto-invocada.

Egress y filtro de veredicto compartidos con el consejo:
- Puerta de salida: `../council/skills/agent-roundtable/references/egress-checklist.md`
- Contratos de asiento: `../council/skills/agent-roundtable/references/ai-registry.md`
