---
name: dotfiles-manager
description: Use when the user asks about managing, updating, documenting, testing or extending their real Arch Linux dotfiles at ~/dotfiles (Hyprland + Qtile) - themes and theme shape fields, the Settings TUI and its sections, the Textual TUIs built on dtui.py (keymaps, workers, set_rows), workspaces count, night light, firewall, VPN/Tailscale, updates/CVEs/firmware, waybar, keybindings, docs - and when porting those changes to the public D4rkFiles repo. Provides the repo layout, safety rules, conventions and the porting map.
---

# dotfiles-manager

Contexto y reglas para trabajar en los dotfiles **reales** del usuario (`$DOTFILES` = `~/dotfiles`) y para
portar lo genérico al repo público **D4rkFiles** (`/files/D4rkFiles`). El contrato detallado vive en
`$DOTFILES/AGENTS.md` (lo carga `CLAUDE.md`): **leelo primero**; esta skill es el mapa y las recetas.

## Contexto

| | |
|---|---|
| Repo | `$DOTFILES` · remote `git@github.com:${DOTFILES_REPO}.git` · branch `main` |
| Sistema | Arch Linux · **Hyprland** (WM en uso) · Qtile/X11 como alternativa |
| Enlaces | `~/.config/<app>` → `$DOTFILES/<app>` (hypr, waybar, kitty, rofi, dunst, qtile, walker, swayosd, gtklock, hyprshell, opencode, Thunar, zsh…) · `~/.zshrc` → `zsh/zshrc` · `~/.claude/statusline-command.sh` → `claude/` |
| Idioma | Español rioplatense en código, comentarios, docs y commits; **textos visibles de las TUIs en inglés** |
| Punto de entrada | **Settings** (`recursos/settings/settings_tui.py`, `Super+Shift+Space`, logo de waybar) |

Stack: Hyprland + waybar · kitty + zsh (p10k) · rofi/walker · dunst · swayosd · gtklock · hypridle ·
hyprsunset · hyprshell · Thunar/HyprFM · Neovim (LazyVim) / Sublime · TUIs propias en Python + Textual.

## Reglas que no se rompen (resumen de AGENTS.md)

1. **Todo cambia en vivo**: `~/.config/<app>` apunta al repo. Cambios no destructivos; ante algo estructural,
   primero una vía que no toque el sistema y pedir OK.
2. **Nunca editar en el lugar un script que puede estar corriendo** (bash lee a medida que ejecuta; waybar
   llama a `vpn_tui.py --waybar-status` y a `hypr-workspaces.py` cada pocos segundos). Escribir a un temporal
   **en el mismo filesystem** y `os.replace`/`mv` (inode nuevo). `/tmp` es otro filesystem: copiar al lado y
   reemplazar desde ahí. Revisar con `ps -eo args | grep '[n]ombre'` (ojo: `pgrep -f` se encuentra a sí mismo).
3. **`hyprland.conf` en vivo**: validar antes con `Hyprland --verify-config -c <copia>` y, después de
   reemplazar, `hyprctl configerrors` (vacío = bien) y `hyprctl binds -j` si tocaste atajos.
4. **Pruebas sin efectos**: nada que recargue componentes (`theme-switch.sh`, `launch.sh`, `pkill waybar`,
   aplicar un modo, conectar una VPN, prender servicios). Ver "Probar sin tocar la sesión".
5. **Nada outward-facing sin OK**: push, PRs, GitHub, subir a Proton Drive. `sudo` pide contraseña/huella: el
   usuario lo corre con `! <comando>` (sin TTY no se puede contestar `[Y/n]`: usar `--noconfirm`).
6. Hay cambios del usuario sin commitear a veces: no pisarlos; al commitear, revisar el diff y separar o avisar.

## Estructura

```
~/dotfiles/
├── AGENTS.md / CLAUDE.md        contrato para agentes (CLAUDE.md = @AGENTS.md)
├── <app>/                       una carpeta por app (hypr, waybar, kitty, rofi, dunst, qtile, walker…)
│   └── hypr/
│       ├── hyprland.conf        config principal (source de workspaces.conf)
│       ├── workspaces.conf      GENERADO por Settings → Workspaces (atajos 1..N + "# count: N")
│       ├── hypridle.conf        GENERADO por Settings → Power
│       ├── hyprsunset.conf      GENERADO por Settings → Displays (luz nocturna)
│       └── scripts/             move-and-focus-workspace.sh, move-window-to-workspace.sh,
│                                workspace-cycle.sh (Ctrl+Tab/rueda en 1..N), hypr-workspaces.py (indicador waybar)
├── scripts/                     theme-switch.sh (orquestador de temas), dotfiles-update.sh, proton-backup.sh,
│                                mode-switch.sh, webapps.sh, wallpaper-set.sh, lock-screen.sh, wayland/…
├── recursos/
│   ├── tui/dtui.py              base común de TUIs (+ keymap.json: teclas reasignadas)
│   ├── settings/settings_tui.py Settings (menú, CATEGORIES, section_views(), binding_catalog())
│   │   └── sections/            una sección por archivo (common.py = helpers)
│   ├── vpn/ shortcuts/ modes/ webapps/ clipboard/ agents/ proton-backup/   TUIs sueltas (vista + app)
│   ├── PROTON/ OPENVPN/ WIREGUARD/ CITRIX/ FORTI/   perfiles VPN (fuera de git)
│   └── wallpapers/
├── themes/<nombre>/theme.json   17 temas (+ _design-tokens.json)
└── docs/                        overview, installation, keybindings, themes, design-system, requirements,
                                 automations, configuration/*.md (una por componente)
```

## Settings y sus secciones

`Super+Shift+Space`. Menú por categorías a la izquierda (`CATEGORIES`), sección a la derecha. `tab`/`enter`
entran, `esc` vuelve al menú, `q` sale. Tabla completa: `docs/configuration/settings.md`.

| Categoría | Secciones (archivo) |
|---|---|
| Connectivity | Wi-Fi, Bluetooth (en settings_tui.py) · VPN (`recursos/vpn/vpn_tui.py`: Forti, Proton, WireGuard, OpenVPN, **Tailscale**, Citrix) · **Firewall** (`sections/firewall.py`) · Phone · Network tools |
| System | Services · Startup apps · Logs · Snapshots · Backup (Proton Drive) · System · **Update** (`sections/update.py`) |
| Tools | Notifications · Clipboard · Screenshots · Color picker · AI Agents |
| Hardware | **Displays** (`sections/displays.py` + `nightlight.py`) · Audio · Input · **Power** (`sections/power.py`) · Battery · Storage |
| Desktop | Modes · **Workspaces** (`sections/workspaces.py`) · **Desktop widgets** (`sections/deskwidgets.py`) · Webapps · Default apps · **Shortcuts** |
| Look & feel | Themes · Theme editor · **Appearance** (forma del tema) · **Fonts & cursor** (`sections/fonts.py`) · Backgrounds |

Lo más reciente:

- **Firewall** — firewalld: on/off, zona por defecto, servicios/puertos (`a`/`d`), zona por conexión de NM.
  Estado por `systemctl` (con firewalld parado `firewall-cmd` espera ~10 s a D-Bus), zonas/servicios/puertos de
  los XML de `/usr/lib/firewalld`; cambios con `sudo` en la terminal (`--permanent` + `--reload`). Prenderlo corta
  KDE Connect / VNC si no se permiten (`kdeconnect`, `5900/tcp`).
- **Displays** — mapa de monitores (`hyprctl monitors -j`), **luz nocturna** (hyprsunset: `←/→` temperatura,
  `-/+` brillo en vivo por IPC `hyprctl hyprsunset …`, franja de 24 h, `s` horario, `l` al login;
  `hyprsunset.service`), tablet por VNC.
- **Update** — estado (pendientes cacheados 15 min en `~/.local/state/dotfiles-settings/update.json`, última
  actualización de `pacman.log`, snapshot, kernel, CVEs, firmware), acciones agrupadas, **Pending** y
  **Installed** estilo pacseek (`v`; `/` buscar, `e` a mano, `s` tamaño, `x` desinstalar con vista previa
  `pacman -Rs --print`). Modos del script: `check all snapshot rollback pacman aur clean orphans audit firmware`.
- **Power** — batería (upower), perfil, brillo pantalla/teclado, idle actions con línea de tiempo (hypridle),
  sesión (lock/suspend/logout/reboot/poweroff).
- **Desktop widgets** — widgets en los workspaces vacíos (`desktop-widgets/`: daemon GTK3 + layer-shell,
  `dwlib.py` sin GTK, `agenda.py` con parser ICS propio). Prender/apagar, zona de una grilla 3×3 por widget (`p`),
  orden en la zona (`K`/`J`), presets, mapa, **Options** (clima, agenda Obsidian Full Calendar / `.ics`, pomodoro,
  teléfono KDE Connect, red) y todo. Config `desktop-widgets/widgets.conf`; el daemon la relee sola (reiniciarlo
  por PID si cambia un `.py`). En D4rkFiles: `config/desktop-widgets/`, config en
  `~/.config/dotfiles/desktop-widgets.conf`, CSS desde `style.css.tpl`, sin backup en la tarjeta de estado.
- **Workspaces** — cantidad 1–10 (`←/→`, `enter`): genera `hypr/workspaces.conf` y `hyprctl reload`; ofrece mover
  ventanas que quedan afuera. Lo leen waybar, `workspace-cycle.sh` y `rofi/scripts/workspace-switcher.sh`.
- **Appearance / Fonts & cursor** — campos de forma del tema y vista previa real de fuentes/íconos/cursor (PIL).
- **Shortcuts** — atajos de Hyprland, kitty, herdr, Qtile, Obsidian, LazyVim y pestaña **Settings**: las 130+
  teclas de las TUIs, reasignables.

## TUIs: `recursos/tui/dtui.py`

Todas se ven como impala/bluetui y usan solo estas piezas (sin CSS ni colores propios):

| Pieza | Uso |
|---|---|
| `DApp` / `DView` / `ViewApp` | App base; contenido de una TUI (se monta suelta o como sección); `FOCUS`, `hints()`, `update_hints()`, `visible_now` |
| `Panel` | Borde redondeado, título y `border_subtitle` de estado; el que tiene foco va en `primary` |
| `Table` | Fila completa; `j/k`; filas `hdr:`/`gap:` que el cursor saltea; **`set_rows()`** redibuja solo si cambió y conserva la selección por clave |
| `Card` | Contenido rich que recibe foco (paneles que no son tablas: mapa de monitores, luz nocturna) |
| Popups | `FormModal` (`Field` con `choices`, `password`, `files`), `ConfirmModal`, `PickModal`, `TextModal` |
| Barras / imágenes | `bar`, `meter10`, `charge10`, `ImagePreview` (kitty graphics), `swatches` |
| Teclas | Cada `Binding` de una `DView`/`DApp` recibe id `Clase.acción`; `keymap.json` las reasigna (`App.set_keymap`); `remap_hints` traduce el pie; `bindings_of()` las lista |

Reglas aprendidas:
- **Todo lo que llama a procesos va en `@work(thread=True, exclusive=True)`** y la UI solo pinta
  (`call_from_thread`). VPN trababa 0.5 s cada 5 s por hacerlo en el hilo de la UI.
- **No usar `self.loading`** como bandera: es una propiedad de Textual y muestra un spinner. Usar `_busy`.
- Un método `render` en un widget pisa el de Textual: no nombrar así métodos propios.
- Dar `description` a los `Binding` con `show=False` (se ven en Shortcuts → Settings).
- `hints()` con la tecla por defecto tal cual (`"a"`, `"/"`, `"←/→"`): se traducen solas si se reasignan.
- `run()` de `settings_tui.py` ya fija `timeout`; no pasarle otro.

Sección nueva de Settings: archivo en `recursos/settings/sections/` con su `DView` (helpers de `common.py`:
`run`, `detach`, `DOTFILES`, `STATE`, `HYPRLAND`, `hypr_block_get/set`), import en `settings_tui.py`, entrada en
`CATEGORIES` y en `section_views()`. Una TUI suelta nueva: `recursos/<x>/`, lanzador en
`waybar/scripts/<x>-launch.sh` → `float-tui-launch.sh` / `center-tui-launch.sh`, `windowrule` en
`hyprland.conf` (y `FLOAT_GEOMETRY` en Qtile), doc.

## Temas

`themes/<nombre>/theme.json` plano: 14 claves de color (`name`, `icon`, `wallpaper`, `primary`, `secondary`,
`background`, `foreground`, `chip_battery`→`chip_bluetooth`→`chip_wlan`→`chip_audio` como rampa oscuro→claro,
`status_ok/warn/error`). `theme <nombre>` → `scripts/theme-switch.sh` es el **único** orquestador: escribe
`qtile/current_theme.json` (fuente del tema activo para runtime), genera cada config en su formato y recarga.

Campos de forma opcionales (defaults = como se veía todo antes; tabla en `docs/themes.md`; `shape_field` respeta
`false` explícitos): `radius`, `opacity`, `inactive_opacity`, `dim_inactive`, `dim_strength`, `blur_enabled`,
`blur_size`, `blur_passes`, `blur_noise`, `blur_contrast`, `blur_brightness`, `blur_vibrancy`, `blur_popups`,
`shadow_enabled`, `shadow_style` (dark/glow), `shadow_range`, `shadow_power`, `border_size`, `border_style`
(solid/gradient/rotating), `border_angle`, `gaps_in`, `gaps_out`, `animations` (smooth/snappy/bouncy/off),
`font_mono`, `font_size`, `font_ui`, `icon_theme`, `opencode_theme`. Se editan en Settings → Appearance y Fonts &
cursor. Un color nuevo sale de las 14 claves con `hex_blend()`, **nunca** un campo nuevo. Los 17 temas:
atom-dark, brown-at-at, catppuccin-mocha, chill-lofi, ciberpunk, data-center, everforest, gray-terminal,
green-geek, gruvbox, kanagawa-dragon, nord, oxocarbon-dark, purple-sky, red-dark, solarized-dark, tokyo-night.

## Probar sin tocar la sesión

- **TUIs headless**: `app.run_test(size=(170, 48))`, `pilot.press(...)`, `app.save_screenshot("x.svg")`. Para ver
  el SVG: `sed 's/<svg /<svg xml:space="preserve" /'` y `rsvg-convert` (sin eso rsvg colapsa los espacios y la
  captura parece rota aunque no lo esté). Las imágenes de kitty no salen en el SVG.
- **Leer lo que dibuja un widget**: `"".join(s.text for s in w.render_line(y))`.
- **Sandbox**: `bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind <scratch> <scratch>
  --unshare-ipc` sin `WAYLAND_DISPLAY`/`DBUS_SESSION_BUS_ADDRESS`/`HYPRLAND_INSTANCE_SIGNATURE` (agregar
  `--unshare-pid` salvo que la prueba necesite ver procesos reales).
- **Binarios falsos** en un `PATH` antepuesto para simular estados (`firewall-cmd`, `tailscale`, `hyprctl`,
  `arch-audit`, `fwupdmgr`, `nmcli`, `systemctl`); no pulsar teclas que ejecuten acciones reales.
- **Copias de config**: `DTUI_KEYMAP`, `PROTON_BACKUP_CONF/STATE`, `MODES_CONF`, `WEBAPPS_CONF`, `GASTOS_DB`.
  Con `HOME` falso, `PYTHONUSERBASE=$HOME_REAL/.local` para no perder `rich`/`textual`.
- **Lag de la UI**: medir con una tarea asyncio que duerme 10 ms y registra el máximo atraso mientras se navega.
- zsh no separa palabras en `set -- $var`: los scripts de prueba con bucles, en bash.

## Instrucciones

### 0. Mantener D4rkFiles sincronizado

D4rkFiles (`/files/D4rkFiles`, github.com/D4rkDr4gon/D4rkFiles) es la versión genérica y pública. **Lo genérico que
se cambia acá se porta allá**, adaptado (nunca copiado): sin rutas, nombres, VPNs de trabajo, redes ni credenciales.

| `~/dotfiles` | D4rkFiles |
|---|---|
| `<app>/` | `config/<app>/` (lo que depende del tema, como plantilla `.tpl` con tokens `@nombre@`) |
| `recursos/tui/dtui.py` | `tools/dtui.py` |
| `recursos/settings/` | `tools/settings/` (rutas por `sections/common.py`: `CONF_DIR`, `STATE`, `HYPR_USER_DIR`…) |
| `recursos/<tui>/<tui>_tui.py` | `tools/<tui>_tui.py` (`load_view(módulo, atributo)`, sin carpeta) |
| `qtile/current_theme.json` | `~/.local/state/dotfiles/current_theme.json` |
| `recursos/tui/keymap.json` | `~/.config/dotfiles/keymap.json` |
| `hypr/workspaces.conf` (source, todos los atajos) | `~/.config/dotfiles/hypr/workspaces.conf` (el repo trae 1..9; el override hace `unbind` de los que sobran, el bind del 10 y `# count: N`) |
| `hypr/hypridle.conf`, `hyprsunset.conf` (versionados) | `config/hypr/…` generados y en `.gitignore` |
| `sed` sobre configs en `theme-switch.sh` | tokens en `scripts/lib/theme.sh` + plantillas (`config/hypr/theme.conf.tpl` lleva la forma; `config/hypr/animations/<preset>.conf`) |
| `lazy-nvim/`, `zsh/`, `sddm/`, `systemd/user/` | `config/nvim/`, `home/zsh/`, `system/` |

Método que funcionó: **merge a tres vías por archivo** (`git merge-file -p ours base theirs`, base = dotfiles en el
commit en que D4rkFiles estaba al día), resolver conflictos con la convención de D4rkFiles, y archivos nuevos
portados a mano. Después:

- `Hyprland --verify-config -c` sobre una **copia** renderizada (`theme-switch.sh --render-only` escribe en
  Firefox/HyprFM/estado del home: correrlo con `HOME`/`XDG_*` falsos) y probar varias combinaciones de forma.
- Settings y TUIs headless con `XDG_CONFIG_HOME`/`XDG_STATE_HOME`/`DTUI_KEYMAP` en el scratchpad.
- `scripts/check-docs.sh` (0 problemas) y `scripts/dotfiles-doctor.sh configs repo` (0 errores).
- `git diff | grep -iE '<usuario>|/home/|<empresa>|citrix|forti|proton'` antes de commitear.
- Paquetes nuevos en `install/packages/*.txt`; docs de D4rkFiles (`docs/settings.md`, `themes.md`, `scripts.md`,
  `keybindings.md`, `customization.md`, `components.md`, `design-system.md`, `ai-skill.md`) y su skill
  `skills/d4rkfiles/` (`SKILL.md` + `references/recetas.md`).
- Confirmar con el usuario antes del push (salvo que lo haya pedido explícitamente).

### 1. Actualizar documentación tras un cambio

Cada cambio de comportamiento actualiza su doc en el mismo commit: `docs/configuration/settings.md` (secciones),
`docs/configuration/<componente>.md`, `docs/themes.md` (campos/tabla de apps), `docs/keybindings.md` y
`docs/configuration/hyprland.md` (atajos), `docs/configuration/updates.md` (modos de dotfiles-update),
`docs/configuration/shortcuts.md`, `docs/design-system.md` (piezas de TUI) y `AGENTS.md` (si cambia una
convención o una pieza de `dtui.py`). Y esta skill, si cambia algo de lo que describe.

### 2. Crear un tema

1. `themes/<nombre>/theme.json` con las 14 claves (+ forma opcional) y `preview.png`.
2. Wallpaper en `recursos/wallpapers/`.
3. `theme <nombre>` (recarga componentes: solo con OK del usuario) o Settings → Themes.
4. Fila en `docs/themes.md`.

### 3. Agregar una app tematizada o un componente

Carpeta en `$DOTFILES/<app>`, symlink a `~/.config/<app>`, bloque en `apply_theme_config` de `theme-switch.sh`
(y en `reload_components` si se recarga en vivo), fila en `docs/themes.md` y `docs/configuration/<app>.md`.
Los archivos generados llevan cabecera "generado, no editar".

### 4. Commits

Conventional commits en español (`feat(scope): …`), cuerpo con viñetas del porqué, `Co-Authored-By` y
`Claude-Session` si el entorno los da. Sin `git add -A` a ciegas cuando hay cambios ajenos; si el usuario pide
"todo en un commit", nombrar en el cuerpo los cambios suyos que entran.

### 5. Ubicación

Esta skill: `$HOME/MY-AGENT-SKILLS/SKILLS/dotfiles-manager/SKILL.md` (enlazada en `~/.claude/skills/`; opencode
la lee por `skills.paths`). La skill pública del repo genérico es `/files/D4rkFiles/skills/d4rkfiles/`.
