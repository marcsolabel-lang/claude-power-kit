# spec.md — Catálogo de Encargos (v1)

Especificación de la primera versión, construible en un fin de semana.

---

## Problema

Un artista o creador recibe encargos de escritura/literatura y de arte. Hoy los sigue en la cabeza y en notas
dispersas (chat, papel, correo). No hay un sitio único donde ver **qué hay pendiente, en qué estado
está, cuándo se entrega y qué está cobrado**. Se cuelan olvidos de plazos y de pagos.

La v1 resuelve una sola cosa: **un tablero visual, en HTML, que muestra todos los encargos por
estado** a partir de un archivo de datos que el creador edita a mano.

---

## Usuarios

- **Primaria: el artista o creador.** Edita el archivo de datos, mira el tablero para organizarse el día y no
  perder plazos ni pagos. No es técnico: editar el archivo tiene que ser sencillo y con ejemplos.
- **Secundario (opcional, no en v1): clientes.** Podrían ver una vista pública de catálogo/portfolio.
  Fuera del alcance de la v1 (ver más abajo).

---

## Flujo

1. El creador abre el **archivo de datos** (`datos.json`) y añade/edita un encargo con los campos del
   modelo (ver `CLAUDE.md`).
2. Genera el sitio (o simplemente abre `index.html` si es la versión sin build).
3. El **tablero** muestra los encargos agrupados por `estado`, en columnas:
   `solicitado → aceptado → en_progreso → entregado` (y `cancelado` recogido aparte).
4. Cada encargo es una **tarjeta** con: título, cliente, tipo (escritura/arte), precio, estado de
   pago, y la fecha de entrega prevista.
5. Las tarjetas con **plazo vencido** y aún no entregadas se marcan visualmente (badge "atrasado").
6. Al entregar, el creador cambia `estado` a `entregado` y rellena `fecha_entrega_real`; la tarjeta se
   mueve de columna al regenerar.

---

## Criterios de aceptación (como pruebas)

Cada criterio es un test que se puede comprobar a mano.

1. **Render por estado.** Dado un `datos.json` con 5 encargos en estados distintos, cuando se
   genera el sitio, entonces el tablero muestra 5 tarjetas, cada una en la columna de su `estado`.
2. **Tarjeta completa.** Dada una tarjeta, entonces muestra título, nombre de cliente, tipo, precio
   en euros, estado de pago y fecha de entrega prevista, todos legibles sin abrir nada.
3. **Badge de atraso.** Dado un encargo con `fecha_entrega_prevista` anterior a hoy y `estado`
   distinto de `entregado`/`cancelado`, entonces su tarjeta muestra un distintivo "atrasado".
   Si está `entregado` o la fecha es futura, NO lo muestra.
4. **Pago visible.** Dado un encargo con `pago = pendiente`, entonces la tarjeta lo distingue
   claramente de uno con `pago = pagado` (color o etiqueta), de un vistazo.
5. **Filtro por tipo.** Dado el tablero, cuando filtro por `tipo = arte`, entonces solo se ven los
   encargos de arte; al quitar el filtro, vuelven todos.
6. **Vacío con sentido.** Dado un `datos.json` sin encargos en una columna, entonces esa columna
   muestra un estado vacío ("sin encargos aquí"), no un hueco roto.
7. **Total visible.** Dado el tablero, entonces se ve el número total de encargos activos (no
   cancelados) y la suma de importes `pendiente`/`parcial` por cobrar.
8. **El build pasa.** El sitio compila/abre sin errores de consola y se ve correctamente en móvil y
   en escritorio (responsive, sin scroll horizontal).

---

## Casos límite

- **Fechas ausentes.** Un encargo recién `solicitado` puede no tener `fecha_entrega_prevista`: la
  tarjeta no debe romperse ni marcar atraso; muestra "sin fecha".
- **Cliente sin contacto.** `contacto` es opcional; la tarjeta se pinta igual.
- **Precio 0 o pendiente de presupuesto.** Mostrar "a presupuestar" en vez de "0 €".
- **Encargo cancelado.** No cuenta en totales ni en columnas activas; se recoge aparte para que
  quede el histórico.
- **Datos malformados.** Si el `datos.json` tiene un registro con un campo obligatorio ausente, el
  sitio no debe caer entero: se salta ese registro y avisa (en consola o con un aviso visible).
- **Muchos entregables o notas largas.** La tarjeta no debe desbordarse; recorta con "ver más" o
  limita altura.

---

## Fuera de alcance (v1)

- Vista pública de catálogo/portfolio para clientes (llega en una v2).
- Edición desde el navegador: en v1 los datos se editan en el archivo, no hay formularios ni
  guardado.
- Backend, base de datos, autenticación, o cualquier cosa dinámica de servidor.
- Notificaciones/recordatorios automáticos de plazos o cobros.
- Multi-idioma, multi-usuario o roles.

La v1 es un tablero estático que lee un archivo. Nada más. Si algo no cabe en un fin de semana,
va a la v2.
