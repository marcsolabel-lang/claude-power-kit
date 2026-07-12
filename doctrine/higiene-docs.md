# Higiene de docs — antes de comprimir, mover o borrar

Mantener docs no es reescribir a gusto: es un procedimiento acotado que protege el rastro
auditable. Es la hermana de la [escalera de simplicidad](escalera-simplicidad.md): esa poda
lo que construyes, esta poda lo que ya está escrito, sin perder señal.

## Niveles de protección — mira el nivel ANTES de tocar
- **Nivel 0 — intocable.** ADRs aceptados, logs de sesión, actas y bitácoras con fecha. No se
  editan; si la decisión cambia, ADR **nuevo** que la sustituye. Única excepción: erratas, en
  commit aparte.
- **Nivel 1 — preservar sin pérdida de señal.** Doctrina viva (esta carpeta `doctrine/`,
  plantillas, notas de conocimiento estable). Se edita para corregir o actualizar, NUNCA para
  "resumir" perdiendo matices. Consolidar antes que borrar.
- **Nivel 2 — comprimir agresivo.** Borradores, notas de trabajo, scratch. Aquí sí se poda.

## Regla Cero
No se reescribe la historia. ADRs, logs y actas son **add-only**. Lo que envejece se **marca
histórico** (un banner "⚠️ HISTÓRICO", y se mueve a una carpeta `archivo/` si aplica), no se
borra en silencio.

## Señal vs ruido
- Borra **duplicación**, no contenido único. Si un dato vive en dos sitios, deja UNO (el
  canónico) y que el otro apunte a él (regla de fuente única).
- Un doc que nadie carga, nada referencia y no es bitácora → candidato a `archivo/`, no a la
  papelera.

## Sin borrado silencioso
Mover o retirar algo deja **un puntero** a dónde fue. El lector futuro (tú, en seis meses)
nunca debe toparse con un enlace muerto.

## Checklist pre-commit (higiene de docs)
1. ¿Toqué algo de **Nivel 0**? → para; no se edita (salvo errata en commit aparte).
2. ¿Borré contenido único o solo **duplicación**? → solo duplicación.
3. ¿Lo retirado deja **puntero**? → sí.
4. ¿Queda algún **enlace roto**? → repáralo. Haz `grep` de las referencias ANTES de mover un
   archivo, no después.
5. ¿El dato canónico sigue en **un solo sitio**? → sí.
