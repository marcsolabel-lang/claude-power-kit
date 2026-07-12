# ADR-NNNN: [título corto y descriptivo]

## Estado
[Propuesto | Aceptado | Obsoleto | Sustituido por ADR-XXXX]

## Fecha
AAAA-MM-DD

## Contexto y problema
[El problema y las fuerzas en juego. ¿Por qué hay que decidir ahora?]

## Opciones consideradas
- Opción A — pros / contras
- Opción B — pros / contras

## Decisión
[Qué se elige y por qué esa, frente a las otras.]

## Consecuencias
- Positivas:
- Negativas / costes:   ← obligatorio, fuerza honestidad sobre el coste
- Reversión: [git revert + borrar/editar qué]

## Qué toca (si aplica)
- [convenciones, secretos, otra decisión que sustituye…]

## Modelado de amenazas (solo si cruzas una frontera de confianza)
[Datos que salen del sitio, credenciales, superficie pública, un formulario que recibe input
de desconocidos → las 4 preguntas: ¿en qué trabajamos? · ¿qué puede salir mal? · ¿qué hacemos
al respecto? · ¿lo hicimos bien? + ¿puede un input hostil torcerlo? Si no se cruza frontera,
borra esta sección.]

> Inmutable una vez **Aceptada**: si aparece algo mejor, se escribe un ADR nuevo que la
> sustituye. La verdad es la cadena entera, no la última.
