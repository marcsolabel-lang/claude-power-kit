# CLAUDE.md — proyecto Catálogo de Encargos

Contexto de este proyecto. El kernel del kit (cómo trabajamos) está en el `CLAUDE.md` de la raíz.

---

## Qué estamos construyendo

Un **sitio web tipo catálogo (HTML estático)** para gestionar y seguir los **encargos** de un
artista o creador: encargos de **escritura/literatura** (relatos, textos por encargo, corrección…) y de
**arte** (ilustración, comisiones visuales…).

Hoy los lleva de cabeza y en notas sueltas. Queremos un único sitio donde se vea, de un vistazo:
qué encargos hay, en qué estado están, qué se debe entregar y cuándo, y qué está cobrado.

Dos vistas posibles (la v1 se centra en la de gestión; ver `spec.md`):

- **Gestión (privada)** — el tablero de trabajo: todos los encargos por estado, con fechas y pagos.
- **Catálogo (pública, opcional)** — escaparate de lo que ofrece y de trabajos terminados.

---

## Modelo de datos: un encargo

Cada encargo es un registro con estos campos:

| Campo | Tipo | Notas |
|---|---|---|
| `id` | texto/número | Identificador único y estable. |
| `cliente` | objeto | `{ nombre, contacto? }`. El contacto es opcional. |
| `tipo` | enum | `escritura` \| `arte`. (Se pueden añadir subtipos luego.) |
| `titulo` | texto | Nombre corto del encargo. |
| `descripcion` | texto | Qué se pide, en una o dos frases. |
| `estado` | enum | `solicitado` \| `aceptado` \| `en_progreso` \| `entregado` \| `cancelado`. |
| `precio` | número (€) | Importe acordado. |
| `pago` | enum | `pendiente` \| `parcial` \| `pagado`. |
| `fecha_solicitud` | fecha | Cuándo entró el encargo. |
| `fecha_entrega_prevista` | fecha | Compromiso de entrega. |
| `fecha_entrega_real` | fecha? | Se rellena al entregar. |
| `entregables` | lista | Qué se entrega (p. ej. "relato 2.000 palabras", "ilustración A4 + versión web"). |
| `notas` | texto | Libre: referencias, cambios pedidos, incidencias. |

Los datos viven en un **archivo de datos editable a mano** (JSON, o Markdown con front-matter si
usamos content collections). Nada de base de datos ni backend: el sitio se genera desde ese archivo.

---

## Stack sugerido

Manténlo simple. Dos opciones, de menor a mayor:

- **HTML + CSS a pelo** — si la v1 es un tablero pequeño, un `index.html` que renderiza tarjetas
  desde un `datos.json` con un poco de JS. Cero build, cero dependencias.
- **Astro + Tailwind** — cuando quieras varias páginas, colecciones de contenido y buenas prácticas
  de sitio estático sin complicarte. Es la opción por defecto si dudas: buen tooling, salida
  estática, fácil de desplegar.

No metas frameworks pesados ni estado de servidor: es un catálogo estático que lee un archivo.

---

## Cómo se trabaja aquí

- **El diseño lo conduce `taste-skill`** (con `emil-design-eng` para el pulido de detalle). El
  catálogo tiene que verse bien: jerarquía clara, estados legibles de un vistazo, nada de plantilla
  genérica.
- **`/verify` comprueba el build** — que el sitio compila, que las tarjetas salen y que los estados
  y fechas se pintan bien antes de darlo por hecho.
- **La v1 está especificada en `spec.md`.** Empieza por ahí, no por el CSS.
