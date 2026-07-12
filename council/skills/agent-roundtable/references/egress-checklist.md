# egress-checklist — la puerta de salida

Ningún byte sale a una IA externa (codex, Gemini, el fan-out del consejo) sin pasar
**antes** por esta checklist. La aplican `/agent-roundtable` (paso 1) y
`/master-plan` (peldaños medium+). Si aparece una **clase prohibida**: **parada
dura**, no sale nada.

## Principio

Lo que sale de tu máquina hacia un modelo de otra empresa **no vuelve**. La puerta
de egress existe para que nunca salga por accidente un secreto, un dato privado, la
config del propio consejo, ni una mezcla peligrosa de contextos. La checklist se
corre **sobre los bytes exactos ya ensamblados**, no sobre una intención.

## El manifiesto literal (se construye DESPUÉS de armar el prompt final)

1. **Ensambla el prompt final** completo (el prompt neutral + cualquier fragmento de
   contexto que lo acompañe). Nada de "más o menos": los **bytes exactos**.
2. **Resuelve los symlinks.** Si algo del payload es un enlace simbólico, se sigue
   hasta el fichero real y se audita **ese**. Un symlink no oculta su destino.
3. **Lista, uno a uno, cada elemento** que va dentro del payload: cada fragmento de
   texto, cada fichero incluido, cada ruta citada. Ese listado literal **es** el
   manifiesto.
4. **Ilegible o binario → falla CERRADO.** Si un elemento no se puede leer y
   verificar como texto (binario, ilegible, permiso denegado), **no se asume
   inocente**: se **aborta**. Fallar cerrado, nunca abierto.

Sin manifiesto no hay envío. El manifiesto se guarda (o se resume por hash) en el
acta; el **contenido literal no** se escribe en el acta.

## Clases prohibidas (parada dura — cualquiera aborta el envío)

### 1. Secretos y credenciales

- Claves de API, tokens, contraseñas, cookies de sesión, claves privadas.
- **El contenido de un `.env` — e incluso el nombre del fichero.** Si el payload
  menciona `.env`, para.
- La propia clave de Gemini nunca viaja dentro de un prompt (se pasa por variable de
  entorno o fichero de clave, jamás en el texto que sale).

### 2. Datos privados / personales / confidenciales

- Datos personales del usuario, de terceros o de clientes (nombres,
  correos, direcciones, datos de pago, mensajes privados).
- Cualquier cosa marcada o entendida como confidencial. Ante la duda de si un dato
  es privado: **es privado** → no sale (o se anonimiza antes).

### 3. Config del orquestador / de los agentes

- Ficheros de skill (`SKILL.md`, estos `references/*.md`), system prompts, `settings`,
  hooks, definiciones de agente, el propio contenido del consejo.
- **Razón:** exponer cómo está montado el consejo permite a un tercero aprender a
  manipularlo. La maquinaria no sale.

### 4. Mezcla de confianzas — la "trifecta letal"

- **Nunca** se combinan, en un mismo payload de salida, **contexto interno** (docs
  del proyecto, notas propias) **con contenido externo sin auditar** (texto pegado
  de una web, salida cruda de otra IA, un fichero de origen desconocido).
- Juntar datos internos + contenido externo no auditado + un canal de salida es la
  receta para una fuga o una inyección de instrucciones. **O se audita el trozo
  externo hasta confiar en él, o se parte el payload** y cada parte sale por
  separado con su propio manifiesto. Nunca mezclados.

## Qué SÍ puede salir (si el manifiesto está limpio)

- El **prompt neutral** del paso 0 (riesgos/contra-argumentos, sin la inclinación de
  Claude).
- Fragmentos de **contenido público o no sensible** estrictamente necesarios para
  entender la pregunta (un párrafo de copy que igualmente va a ser público, la
  estructura de una decisión de diseño, un dilema de arquitectura descrito en
  abstracto).
- **Texto que el usuario va a publicar de todas formas** (una descripción de obra, un
  texto de la web) — ya es público por destino.

## Procedimiento (resumen operativo)

1. Ensambla el prompt final → **bytes exactos**.
2. Construye el **manifiesto literal** (symlinks resueltos; ilegible/binario = falla
   cerrado).
3. Recorre el manifiesto contra las **4 clases prohibidas**.
4. ¿Alguna clase presente? → **PARADA DURA**, no sale nada; se le dice al usuario qué
   clase saltó.
5. ¿Limpio? → sigue al checkpoint humano (hash del payload + roster) y envía.
6. Registra en el acta el **hash** del payload, **no** su contenido literal.

## Relación con el filtro de veredicto

Egress y filtro de veredicto son puertas distintas:

- **Egress** vigila lo que **sale** (antes de enviar).
- **Filtro de veredicto** vigila lo que se **embarca** (después de decidir): PASA /
  NO PASA / CRUCIAL.

Una decisión de **abrir el egress a algo dudoso** (¿este fragmento es privado o no?)
es **hacia fuera** → si hay duda, es **CRUCIAL** → decide el usuario.
