# La escalera de sesiones — hábitos, no ceremonias

Tu unidad real de trabajo no es "el día". Es el **peldaño**: abres una sesión, trabajas un
rato, limpias y abres otra. Haces muchos peldaños. Si tratas cada uno como si fuera un ritual
completo, el ritual te frena; si no haces ninguno nunca, pierdes el hilo entre sesiones. La
solución es tallar el gesto a la altura correcta.

## Las cuatro alturas
| Altura | Qué es | Cada cuánto | El hábito |
|---|---|---|---|
| **Peldaño** | una sesión | muchas al día | abrir, trabajar, limpiar (`/compact`·`/clear`), guardar en git si hay commits. Casi gratis. |
| **Bloque** | un rato de trabajo real (≈1-4 h, varias sesiones) | pocas al día | ritual rico al **abrir** y al **cerrar**: repasar pendientes, guardar, anotar la lección si la hubo. |
| **Sprint** | ≤3 compromisos concretos | por resultado | abrir 3 cosas, cerrarlas, retro corta, reabrir. |
| **Plan** | un cambio no trivial | atraviesa varios peldaños | clarificar → diseñar → plan → ejecutar → verificar. |

La regla que evita el desgaste: **NO corras el ritual pesado en cada sesión.** Entre peldaños
basta con guardar en git lo que tenga commits y arrancar el siguiente. El ritual rico (repaso,
captura de pendientes, lección aprendida) es para **abrir o cerrar un bloque**, no cada vez.

> Hoy haces estos rituales a mano. Cuando un gesto se repita lo bastante (regla de tres), puedes
> convertirlo en un comando propio —p. ej. uno que llames `/hello` para abrir bloque y `/close`
> para cerrarlo—. No hace falta tenerlos para empezar: el hábito va primero, el comando después.

## Las tres salidas (cómo limpiar el contexto)
La ventana de contexto es finita y cada turno re-lee todo lo cargado. Arrastrar una conversación
larga a la siguiente tarea cuesta y la ensucia. Tres salidas, una regla:
- **`/compact`** → sigues en **la misma tarea** pero el contexto se llena. Resume conservando el
  hilo. Úsalo con preservación explícita: *"/compact pero conserva las decisiones sobre X"*.
- **`/clear`** → terminaste una tarea y empiezas **otra en el mismo proyecto**. Borra a cero y
  arranca limpio.
- **Pestaña / conversación nueva** → cambias de **proyecto**, quieres **conservar** esta
  conversación para consultarla, o la sesión se hizo tan larga que arrancar en paralelo sale mejor.

Resumen: *mismo hilo y lleno → `/compact`; otra tarea, mismo repo → `/clear`; otro proyecto o
conversación a guardar → pestaña nueva.*

## El sprint cierra por resultado, no por calendario
Un sprint no tiene fecha de fin. Son **≤3 compromisos** y cierra cuando están **hechos** — a tu
ritmo, eso es de una sesión a un par de días. Al completar los 3: retro corta (qué salió, qué
cambias en UN solo punto del proceso) y reabres. Mides *vueltas del bucle completadas*, no días
que pasan. Nada de "sprint de 14 días": el plazo fijo nunca coincide con el ritmo real.

## Verde / gate — cuánta autonomía das
La seguridad no son bloqueos-antes, es que el daño sea barato de deshacer:
- **Zona verde (corre sola):** todo lo reversible y local. git lo hace barato de revertir, así
  que editar archivos, escribir docs, refactorizar, probar → adelante sin pedir permiso.
- **Zona gate (espera tu OK):** lo irreversible o hacia fuera — publicar/desplegar, borrar algo
  externo, un force-push, mandar un correo, cualquier acto que git no pueda deshacer.
- **La única barrera dura: los secretos.** Claves, tokens y credenciales NUNCA entran en git ni
  se enseñan, porque una clave filtrada no se des-filtra revirtiendo. Todo lo demás es convención;
  esto es candado.
