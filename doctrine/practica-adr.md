# Práctica de ADR — decisiones que se explican solas dentro de seis meses

Un ADR (Architecture Decision Record) es la memoria durable de un "por qué". Cuando tú —o
tu yo de dentro de seis meses— te preguntes por qué decidiste X, el ADR responde sin tener
que reconstruir la conversación original. Son ligeros a propósito: uno útil cabe en una
pantalla.

## Cuándo escribir uno
Cualquier decisión con **consecuencias a más de 3 meses**: la arquitectura del sitio,
convenciones que afectan a varios sitios, políticas de datos, o compromisos de proceso. Si
dudas si algo necesita ADR, la respuesta segura es **sí**: es barato y te ahorra una
conversación dentro de medio año. Lo que NO necesita ADR: decisiones reversibles de un solo
archivo, gustos que puedes cambiar mañana sin coste.

## Numeración
`ADR-NNNN-titulo-en-kebab.md` — correlativa, cuatro dígitos con ceros a la izquierda (0001,
0002, …), **sin huecos**. El número se reserva al crear el archivo aunque la decisión quede
en `propuesto`. Los números de ADR **rechazados no se reutilizan** (para no reabrir la misma
discusión sin contexto).

## Estados posibles
- `propuesto` — borrador en discusión, no vincula.
- `aceptado` — vigente y vinculante hasta que otro ADR lo sustituya.
- `superseded-by-NNNN` — sustituido por uno posterior. El archivo se queda **intacto**; solo
  cambia la línea de estado.
- `rechazado` — evaluado y descartado.

## Cómo escribirlo
1. Copia `templates/adr.md` al siguiente número libre.
2. Rellénalo conciso — cabe en una pantalla.
3. Quien **cierra** la decisión la redacta, no necesariamente quien la propuso.

## Regla de oro: un ADR aceptado no se edita
Congelado tras aceptarse. Si la decisión cambia, se crea un ADR **nuevo** que pone el anterior
en `superseded-by-NNNN` — preserva la historia auditable en lugar de reescribir el pasado. La
verdad es la cadena entera, no la última entrada. Única excepción: erratas/formato, en un
commit aparte (`docs: typo en el ADR NNNN`).

## Un solo sitio los enumera
Manténlos todos en una carpeta (p. ej. `doctrine/decisions/` o `docs/adr/`) con un índice que
los liste. Que ningún otro doc mantenga su propia lista de ADR en paralelo: se desincroniza.
Un solo sitio es la fuente de verdad; el resto apunta a él.
