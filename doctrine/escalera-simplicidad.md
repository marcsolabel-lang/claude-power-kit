# Escalera de simplicidad — antes de construir nada

El mejor código (o comando, o script, o doc) es el que no se escribe. Antes de proponer
construir algo, baja la escalera: el PRIMER peldaño que se satisface, ahí te detienes.
No es lineal — cada peldaño decide si sigues bajando o paras.

1. ¿Hace falta construirlo? (YAGNI) → si no resuelve un problema real YA, no se hace.
2. ¿Lo hace ya algo que tienes? → un comando, un script, una plantilla, un componente existente.
3. ¿Lo cubre una capacidad nativa? → un hook, un ajuste de Claude Code, la shell, git, HTML/CSS nativo.
4. ¿Lo resuelve una dependencia ya instalada? → no añadas una nueva para algo que ya está.
5. ¿Cabe en una línea / un alias? → la solución mínima antes que el módulo.
6. Solo entonces: lo mínimo que funciona. Custom como último recurso, porque es esencial.

## Innegociables — NUNCA se recortan con la escalera
La escalera poda complejidad superflua, no robustez. Estos no son "opcionales":
- Validación de entrada y manejo de errores que evita pérdida de datos.
- Secretos y seguridad: las claves, tokens y credenciales nunca entran en git.
- Reversibilidad (git) y tu gate para lo irreversible u outward (publicar, borrar algo
  externo, un force-push): eso espera tu OK, no corre solo.
- Specs explícitas: si lo pediste tú a propósito, no se "simplifica" quitándolo.

> Ejemplo: antes de meter una librería JS para un lightbox de la galería, mira si el
> elemento `<dialog>` nativo + cuatro líneas de CSS ya lo hacen. Casi siempre sí.

## Si construyes: ¿de qué tipo?
Si pasaste la escalera y toca construir, elige el tipo **más ligero** que sirva:

| Necesidad | Tipo | Cuándo |
|---|---|---|
| Conocimiento estable que se relee | **doc / plantilla** | la respuesta no cambia entre sesiones |
| Un gesto que tecleas a menudo | **alias / función de shell** | una línea, sin método ni contexto |
| Una rutina con pasos y criterio | **comando / skill** (`/x`) | se repite y necesita método, no solo un comando |
| Trabajo profundo especializado | **agente** | razonamiento largo, lectura de muchos ficheros |
| Algo que corre solo, sin ti | **hook / tarea programada** | disparado por evento o reloj (respeta tu gate) |

**Regla de tres para comandos/skills:** no se crea una skill hasta que el gesto se ha hecho
a mano **tres veces**. Antes, es un alias o una nota. La fábrica se extrae del producto, no
al revés.
