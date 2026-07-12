---
name: agent-roundtable
description: Consulta multi-IA de un solo disparo sobre UNA pregunta. Reúne un consejo de IAs externas (OpenAI/ChatGPT vía codex, Gemini, NotebookLM) para riesgos y contra-argumentos; Claude orquesta y decide el último. Todo egress pasa la puerta de salida. Manual.
disable-model-invocation: true
---

# /agent-roundtable

Comando de entrada. Carga y sigue la skill:

**`../council/skills/agent-roundtable/SKILL.md`**

Manual siempre (`disable-model-invocation: true`): se invoca a mano, nunca en
segundo plano ni auto-invocada.

Referencias que usa la skill:
- Contratos de asiento: `../council/skills/agent-roundtable/references/ai-registry.md`
- Puerta de salida: `../council/skills/agent-roundtable/references/egress-checklist.md`
- Segunda lectura Gemini: `../council/scripts/contrastar.py`
