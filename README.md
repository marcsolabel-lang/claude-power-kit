# Power kit para Claude Code — arranque

Un kit portátil de skills, agentes y permisos para Claude Code. Pensado para que **empieces a
trabajar HOY en Windows** con lo que ya funciona, y desbloquees el resto **el sábado en CachyOS**.

El objetivo inmediato: montar el **catálogo de encargos** de un artista o creador (escritura/literatura + arte)
en `project-comisiones/`.

---

## 1. Qué es esto

Una carpeta con cuatro piezas:

- `commands/` → skills que se invocan con `/slug` (planificar, verificar, diseñar…).
- `agents/` → subagentes especializados que usan algunas skills.
- `council/` → el consejo: un panel de revisores expertos para criticar una decisión o un diseño.
- `doctrine/` → plantillas y método (la forma de un `spec.md`, etc.).
- `.claude/settings.json` → permisos: lo permitido (dev genérico) y la red de seguridad (lo denegado).
- `project-comisiones/` → tu primer proyecto real, con contexto (`CLAUDE.md`) y spec (`spec.md`).

El kernel del kit (cómo trabajamos) está en `CLAUDE.md`.

---

## 2. Qué funciona HOY (Windows) vs. qué espera al SÁBADO (CachyOS)

### CHUCHES AHORA — funcionan tal cual en Windows

Todo esto es Claude Code puro (skills en Markdown + permisos JSON), no depende del sistema operativo:

- **Skills de diseño** — `taste-skill` (frontend anti-slop: landings, portfolios, catálogos) y
  `emil-design-eng` (pulido de UI y animación). Son las que le dan buen gusto al catálogo.
- **`/plan`** — ciclo disciplinado para cualquier cambio no trivial: aclara → explora → diseña →
  planifica → ejecuta → verifica.
- **`/cdx`** — bucle de preguntas afiladas que baja la ambigüedad a cero antes de tocar nada, y
  deja un contexto compartido escrito.
- **`/check`** — segunda lectura / verificación cruzada de un análisis o una decisión.
  (Nota: necesita una clave de API propia configurada en tu entorno; si aún no la tienes, sáltala.)
- **El consejo (`council/`)** — convocas revisores expertos para que critiquen antes de dar algo
  por bueno.
- **La doctrina (`doctrine/`)** — plantillas y método reutilizables.
- **Los permisos (`.claude/settings.json`)** — la red de seguridad que bloquea comandos
  destructivos; ver sección 5.

### TRABAJO DURO — espera al sábado en CachyOS

Estas piezas dependen del sistema (Linux) y las montamos cuando migres:

- **La mascota / panel de estado del escritorio** — el indicador visual de "trabajando / requiere
  atención". Es integración de escritorio Linux.
- **El shell** — funciones de terminal (atajos, navegación, git) sobre fish.
- **Los timers de systemd** — mantenimiento autónomo en segundo plano.
- **La voz (salida)** — lectura por TTS cuando Claude termina una respuesta.
- **El dictado (entrada)** — hablarle a Claude por micrófono con atajos globales.

Nada de esto hace falta para construir el catálogo. Son comodidad, no camino crítico.

---

## 3. Instalación en Windows (hoy)

Claude Code lee las skills y agentes desde tu carpeta de usuario. Los pasos:

1. **Copia las skills** — el contenido de `commands\` va a:

   ```
   %USERPROFILE%\.claude\commands\
   ```

2. **Copia los agentes** — el contenido de `agents\` va a:

   ```
   %USERPROFILE%\.claude\agents\
   ```

3. **Fusiona los permisos** — abre `.claude\settings.json` de este kit y `%USERPROFILE%\.claude\settings.json`
   (créalo si no existe). Copia los bloques `permissions.allow` y `permissions.deny`. Si ya tienes
   un `settings.json`, no lo sobrescribas: añade las entradas que falten.

4. **Reinicia Claude Code** para que cargue las skills y los permisos nuevos.

Comprueba que ha ido bien: abre Claude Code y escribe `/` — deberían aparecer las skills del kit
(`/plan`, `/cdx`, `taste-skill`…).

---

## 4. El detalle de los symlinks en Windows

En Linux es cómodo enlazar (`~/.claude/commands` → la carpeta del kit) para tener **una sola fuente
de verdad**: editas el kit y Claude Code lo ve al instante. En Windows los symlinks son más
delicados:

- Necesitan **Modo Desarrollador** activado (Configuración → Privacidad y seguridad → Para
  desarrolladores), o crear la unión con `mklink /J` desde una consola:

  ```
  mklink /J "%USERPROFILE%\.claude\commands" "C:\ruta\al\kit\commands"
  ```

  (`/J` crea una *junction* de directorio, que no exige permisos de administrador.)

- **Lo más simple: copia los archivos reales** (sección 3) y olvídate de enlazar. Cuando quieras
  actualizar el kit, vuelves a copiar. Menos magia, cero sorpresas.

El sábado, en CachyOS, ya podrás enlazar con `ln -s` sin fricción.

---

## 5. Los permisos (la red de seguridad)

`.claude/settings.json` trae dos listas:

- **`allow`** — dev genérico: `git`, `npm`/`node`/`npx`/`bun`/`yarn`/`pnpm`, `python`/`pip`,
  utilidades de shell (`ls`, `cat`, `jq`…) y `gh` de solo lectura. Es lo que Claude puede hacer sin
  pedirte permiso cada vez.
- **`deny`** — la red de seguridad. Bloquea lo irreversible aunque se lo pidas por error:
  `git push --force`, `git reset --hard`, `git clean -f`, `rm -rf` de home/raíz, `mkfs`/`dd`/
  `parted`/`fdisk`/`cryptsetup`, tuberías `curl … | sh` y `wget … | bash`, `DROP TABLE`/
  `DROP DATABASE`, y leer `.env*` o `~/.ssh/**`.

**Nota para CachyOS (sábado):** en Linux conviene añadir a `deny` tres reglas de desinstalación de
paquetes de Arch que aquí se han omitido por no aplicar en Windows:

```
"Bash(pacman -R*)",
"Bash(sudo pacman -R*)",
"Bash(paru -R*)"
```

---

## 6. Primer movimiento

1. Entra en la carpeta del proyecto:

   ```
   cd project-comisiones
   ```

2. Abre Claude Code ahí y lee su `CLAUDE.md` y `spec.md` (los tienes ya escritos).

3. Lanza:

   ```
   /plan
   ```

   Dile que construya la **v1 del catálogo** siguiendo `spec.md`. `/plan` aclarará lo que falte,
   diseñará y ejecutará por pasos verificables. El diseño lo conduce `taste-skill`; al final,
   `/verify` comprueba que el build funciona de verdad.
