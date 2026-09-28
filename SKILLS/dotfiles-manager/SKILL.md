---
name: dotfiles-manager
description: Use when the user asks about managing, updating, documenting, or creating themes for their dotfiles at ~/dotfiles. Helps with documentation, theme creation, and provides full context of the dotfiles structure.
---

# dotfiles-manager

## Contexto del Repositorio

**Ubicacion**: `$DOTFILES`
**Remote**: `git@github.com:${DOTFILES_REPO}.git` (branch: `main`)
**Autor**: D4rkDr4g0n — Ciberseguridad & Desarrollo
**Distro**: Arch Linux
**WM**: Qtile (Python, Wayland)
**License**: MIT

### Stack Tecnologico

```
WM:             Qtile (Python, Wayland)
Barra:          Waybar (Wayland)
Terminal:       Kitty (Wayland nativo)
Shell:          Zsh + powerlevel10k
Launcher:       Rofi (Wayland nativo)
Notifications:  Dunst
Compositor:     Qtile built-in (Wayland)
Lock Screen:    gtklock (Wayland)
Screenshots:    grim+slurp (Wayland)
Monitores:      wlr-randr (Wayland)
Editores:       Neovim (LazyVim) / Sublime Text
File Mgr:       Thunar
Info:           Fastfetch
AI:             opencode (skills personalizadas)
```

### Enlaces Simbolicos

```
~/.zshrc              -> $DOTFILES/zsh/zshrc
~/.config/qtile       -> $DOTFILES/qtile/
~/.config/waybar      -> $DOTFILES/waybar/
~/.config/gtklock     -> $DOTFILES/gtklock/
~/.config/dunst       -> $DOTFILES/dunst/
~/.config/rofi        -> $DOTFILES/rofi/
~/.config/kitty       -> $DOTFILES/kitty/
~/.config/Thunar      -> $DOTFILES/Thunar/
~/.config/zsh         -> $DOTFILES/zsh/
~/.config/automat     -> $DOTFILES/automat/
~/.config/opencode    -> $DOTFILES/opencode/
~/.config/herdr/config.toml -> $DOTFILES/herdr/config.toml  # solo el archivo, el resto es runtime (sockets/logs/session.json)
```

---

## Estructura Completa del Repositorio

```
dotfiles/
├── README.md
├── docs/                              # Documentacion modular
│   ├── overview.md, installation.md, keybindings.md, themes.md, automations.md
│   └── configuration/
│       ├── qtile.md, polybar.md, wayland.md, kitty.md, zsh.md, rofi.md
│       ├── picom.md, dunst.md, editors.md, fastfetch.md, thunar.md, extras.md, lock-screen.md
│
├── qtile/                             # Window Manager (X11 + Wayland)
│   ├── config.py                      # Entry point, wl_input_rules, cursor
│   ├── current_theme.json             # Tema activo
│   └── modules/
│       ├── groups.py                  # 6 workspaces con íconos (name numérico + label)
│       ├── keys.py                    # Keybindings (mod4 = Super), dual-backend scripts
│       ├── layouts.py                 # Columns, MonadTall, Stack
│       ├── mouse.py                   # Mouse bindings
│       ├── screens.py                 # Dual screen + wallpapers
│       └── hooks.py                   # Autostart dual-backend (Waybar vs Polybar+Picom)
│
├── polybar/                           # Status bar (X11 only)
│   ├── config.ini                     # 98% width, 28px, rounded 10px
│   ├── colors.ini                     # Dinamico por tema
│   ├── launch.sh                      # Kill + launch por monitor
    │   └── modules/ (battery, bluetooth, brillo, date, logo, pulseaudio, vpn, wlan, xworkspaces)
│
├── waybar/                            # Status bar (Wayland)
│   ├── config.jsonc                   # Modulos: logo, workspaces, clock, brillo, etc.
│   ├── style.css                      # CSS con @import theme.css para colores
│   ├── theme.css                      # @define-color generado por theme-switch.sh
│   ├── launch.sh                      # Kill + launch
│   ├── modules/
│   └── scripts/
│
├── gtklock/                           # Lock screen config (Wayland, GTK-based)
│   ├── config.ini                     # time-format, modules, style/layout paths
│   ├── style.css                      # GTK3 CSS: clock, auth form glass, etc.
│   └── layout.ui                      # Layout custom: clock bottom-left, auth bottom-right
│
├── kitty/                             # Terminal (X11 + Wayland nativo)
│   ├── kitty.conf                     # Hack Nerd Font 10pt, 80% opacity, linux_display_server wayland
│   └── colors.conf                    # Dinamico por tema
│
├── zsh/                               # Shell modular
│   ├── zshrc                          # Entry point
│   └── modules/
│       ├── aliases.zsh                # theme, vi, cat, ls, c, q, .., vpnup/down, barupdate, etc.
│       ├── history.zsh                # 100k lines, shared, inc_append
│       ├── paths.zsh                  # ~/.local/bin, ~/.opencode/bin
│       ├── plugins.zsh                # zsh-autosuggestions, zsh-syntax-highlighting
│       ├── startup.zsh                # ASCII banner rojo D4rkDr4g0n
│       ├── theme.zsh                  # powerlevel10k + colores dinamicos
│       └── tools.zsh                  # extractPorts, hex-encode/decode, rot13
│
├── rofi/                              # Launcher (X11 + Wayland nativo 2.0+)
│   ├── config.rasi                    # drun/run/window, fzf sort
│   ├── theme.rasi                     # Norte, 480px, 24px radius, semi-transparente
│   ├── favoritos.txt                  # Sublime, Burp, Wireshark, Bitwarden
│   ├── theme-drun.rasi                # Grid Android 5x4 para app launcher
│   ├── theme-action.rasi              # Grid 4x1 para action menu
│   └── scripts/
│       ├── launcher.sh                # Apps + Google search via "g <query>"
│       ├── emoji.sh                   # 800+ emojis, copia al clipboard
│       ├── qtile-action-menu.sh       # Suspend/Reboot/Poweroff/Logout
│       ├── qtile-workspace-switcher.sh
│       ├── notification-center.sh     # Notificaciones en Rofi (Dunst history) + entrada No Molestar
│       ├── dnd-menu.sh                # No Molestar: toggle global, timer (systemd-run --user), silenciar apps
│       ├── settings-menu.sh           # Themes, Workspaces, Web search, Backgrounds, Notifications
│       └── web-search.sh              # Google, abre Firefox en workspace 5 (dual-backend)
│
├── picom/                             # Compositor (X11 only)
│   └── picom.conf                     # GLX, vsync, 12px radius, dual_kawase blur (6)
│
├── dunst/                             # Notification daemon (X11 + Wayland)
│   ├── dunstrc                        # 16px radius, rofi-aligned colors; reglas de apps silenciadas autogeneradas al final
│   └── blocked-apps.conf              # Estado de apps silenciadas (enabled<TAB>appname), tracked en git
│
├── lazy-nvim/                         # Neovim (LazyVim)
│   ├── init.lua, lazy-lock.json
│   └── lua/config/ (lazy, options, keymaps, autocmds, colors, highlights)
│       └── lua/plugins/ (colorscheme, example)
│
├── sublime-text/Packages/User/
│   ├── Preferences.sublime-settings   # Kali-Red-Hack, Hack 10pt, caret #d32f2f
│   ├── Package Control.sublime-settings
│   └── Kali-Red-Hack.sublime-color-scheme
│
├── Thunar/
│   ├── accels.scm                     # Shortcuts por defecto
│   └── uca.xml                        # "Open Terminal Here" via exo-open
│
├── fastfetch/
│   ├── config.jsonc                   # OS/Kernel/DE/WM/Packages/Mem/CPU/GPU/etc
│   ├── ascii/ (arch.txt, cat.txt, rose.txt)
│   └── png/ (logos aleatorios)
│
├── onedrive/
│   ├── config                         # sync_dir=~/OneDrive, atomic writes
│   └── sync_list
│
├── opencode/                          # AI assistant (opencode)
│   ├── opencode.jsonc                 # Config: skills.paths -> MY-AGENT-SKILLS
│   ├── .gitignore                     # Ignora node_modules, lock files
│   ├── package.json                   # Plugin dependencies
│   └── node_modules/                  # Runtime (gitignored)
│
├── herdr/                             # Multiplexor de agentes IA (tmux-like)
│   ├── config.toml                    # prefix ctrl+space, theme.custom dinamico
│   └── launch.sh                      # kitty -e herdr (auto_detect_launch nativo)
│
├── themes/                            # 8 temas dinamicos
│   ├── brown-at-at/   (theme.json + wallpaper)
│   ├── purple-sky/
│   ├── ciberpunk/
│   ├── chill-lofi/
│   ├── data-center/
│   ├── green-geek/
│   ├── gray-terminal/
│   └── red-japan/
│
├── scripts/
│   ├── theme-switch.sh                # Cambia polybar/waybar/kitty/zsh/qtile/fastfetch
│   ├── barupdate.sh                   # Reinicia Polybar (X11) o Waybar (Wayland)
│   ├── screenshot.sh                  # grim+slurp (Wayland) o Flameshot (X11)
│   ├── lock-screen.sh                 # gtklock (Wayland) o lock-screen binary (X11)
│   ├── lock-screen                    # Compiled ELF (X11 i3lock-based)
│   ├── lock-screen.c                  # C source (X11)
│   └── vpn-replace.sh                 # Reemplazar config de Wireguard VPN
│
├── automat/
│   ├── display-monitors.sh            # xrandr (X11) / wlr-randr (Wayland) laptop + HDMI
│   ├── launch-logo.sh                 # ASCII dragon banner
│   ├── launchgemma.sh                 # Ollama + Gemma 3 en Kitty
│   ├── vault-pull.sh                  # Git pull en ~/OneDrive/vault
│   ├── vault-push.sh                  # Git commit "D4 - YYYY-MM-DD"
│   └── install/                       # 13 scripts de instalacion
│       ├── setup-yay.sh               # AUR helper
│       ├── install-fonts.sh           # Hack, JetBrains Mono, Font Awesome, Noto
│       ├── install-zsh.sh             # Zsh + p10k + symlinks
│       ├── install-qtile.sh           # Qtile + Python deps
│       ├── install-polybar.sh         # Polybar + stow
│       ├── install-picom.sh           # Picom + stow
│       ├── install-kitty.sh           # Kitty + stow
│       ├── install-rofi.sh            # Rofi + stow
│       ├── install-neovim.sh          # Neovim + LazyVim
│       ├── install-tools.sh           # Obsidian, Flameshot, Firefox, CopyQ, etc.
│       ├── install-ollama.sh          # Ollama + modelos
│       ├── install-n8n.sh             # n8n automation
│       ├── install-wayland.sh         # Paquetes Wayland (waybar, swaylock, grim, slurp, etc.)
│       └── setup-blackarch.sh         # BlackArch repos (opcional)
│
└── recursos/
    ├── wallpapers/                    # 18+ wallpapers cyberpunk/sci-fi/hacker
    ├── finnancials/gastos.py          # TUI expense manager (textual, SQLite)
    ├── logo-bloqueo.png               # Lock screen image
    ├── logo.txt                       # Dragon ASCII art
    ├── tux.txt                        # Tux ASCII
    └── Theme-Manager/Palettes/Fiery-Red-Sunset.theme
```

---

## Workspaces (Qtile Groups)

| # | Icono | Nombre |
|---|-------|--------|
| 1 |  | Workspace 1 |
| 2 |  | Workspace 2 |
| 3 |  | Workspace 3 |
| 4 |  | Workspace 4 |
| 5 |  | Workspace 5 |
| 6 |  | Workspace 6 |

---

## Keybindings Principales

### Qtile (mod4 = Super)

| Atajo | Accion |
|-------|--------|
| `Mod + Enter` | Terminal (Kitty) |
| `Mod + Space` | App launcher (Rofi) |
| `Mod + B` | Firefox |
| `Mod + F` | Thunar |
| `Mod + O` | Obsidian |
| `Mod + P` | Bitwarden |
| `Mod + S` | Sublime Text |
| `Mod + V` | CopyQ |
| `Mod + Shift + Return` | Herdr (multiplexor de agentes IA, prefix ctrl+space) |
| `Mod + Q` | Cerrar ventana |
| `Mod + Shift + F` | Fullscreen |
| `Mod + T` | Float toggle |
| `Mod + Shift + Arrows` | Mover ventana |
| `Mod + Ctrl + Arrows` | Redimensionar |
| `Mod + Ctrl + R` | Recargar Qtile + Waybar |
| `Mod + L` | Action menu (Lock/Reboot/Poweroff/Logout) |
| `Mod + Shift + Space` | Settings menu (incluye Notifications) |
| `Mod + 1-6` | Ir a workspace |
| `Mod + Shift + 1-6` | Mover ventana a workspace |
| `Print` / `Mod + Shift + S` | Screenshot (grim+slurp) |

### Kitty

| Atajo | Accion |
|-------|--------|
| `Ctrl+Shift+Enter` | Nueva tab |
| `Ctrl+Shift+W` | Cerrar tab |
| `Ctrl+Shift+N` | Renombrar tab |
| `Ctrl+Shift+Space` | Nueva ventana (split) |
| `Ctrl+Shift+Arrows` | Resize ±5px |

### Zsh Aliases

| Alias | Comando |
|-------|---------|
| `theme` | `$DOTFILES/scripts/theme-switch.sh` |
| `vi` | `nvim` |
| `cat` | `bat` |
| `ls`/`l`/`ll`/`la`/`lla` | `lsd` variants |
| `c` | `clear` |
| `q` | `exit` |
| `..`/`...`/`....`/`.....` | `cd` shortcuts |
| `top` | `btop` |
| `vpnup`/`vpndown` | Wireguard VPN |
| `launchgemma` | Ollama + Gemma |
| `n8nstart`/`n8nstop` | n8n service |
| `zshconfig` | `nvim ~/.zshrc` |
| `barupdate` | Relaunch Waybar |
| `hosts` | `sudo nvim /etc/hosts` |

---

## Temas Disponibles

17 temas en `themes/<nombre>/theme.json`:

| Tema | Wallpaper | Paleta |
|------|-----------|--------|
| Brown AT-AT | STAR-WARS-AT-AT.png | Marron/gris calido |
| Red Dark | RED-STONE.png | Rojo oscuro, minimalista |
| Gray Terminal | HACKER.jpg | Grises |
| Green Geek | HACKER-SETUP-DARK.jpg | Verde terminal |
| Purple Sky | CITY.jpg | Violeta |
| Ciberpunk | CITY-SCI-FI.jpg | Neon magenta/purple |
| Chill Lofi | CREATIVITY-ROOM.jpg | Tierra calido |
| Data Center | DATA-CENTER.jpg | Cian/verde |
| Gruvbox | CITYSCAPE-CYBER.png | Retro, tonos tierra, amarillo/verde mate |
| Everforest | CYBER-SPACE-CITY.png | Bosque neblinoso, verdes calidos |
| Solarized Dark | CODE.png | Cientifico, contraste calibrado |
| Atom Dark | INDUSTRIAL-CYBERPUNK-CITY.png | Grises oscuros, acento azul |
| Nord | DARK-SERVER-ROOM.png | Azul-gris artico |
| Catppuccin Mocha | DOG-ROOM.jpg | Pastel oscuro |
| Tokyo Night | CITY-DARK.jpg | Azul-violeta nocturno |
| Kanagawa Dragon | JAPAN-MYTHOLOGY.png | Neutros calidos tipo tinta sumi-e, acentos azul/malva |
| Oxocarbon Dark | CYBERPUNK-DATACENTER.png | IBM Carbon, negro carbon con neon purpura/azul |

### Estructura de theme.json

Schema **plano** (no anidado), leido con `jq`:

```json
{
  "name": "KANAGAWA DRAGON",
  "icon": "",
  "wallpaper": "$DOTFILES/recursos/wallpapers/JAPAN-MYTHOLOGY.png",
  "primary": "#8ba4b0",
  "secondary": "#a292a3",
  "background": "#181616",
  "foreground": "#c5c9c5",
  "chip_battery": "#282727",
  "chip_bluetooth": "#393836",
  "chip_wlan": "#625e5a",
  "chip_audio": "#7a8382",
  "status_ok": "#8a9a7b",
  "status_warn": "#c4b28a",
  "status_error": "#c4746e"
}
```

`chip_battery` → `chip_audio` es una rampa de 4 superficies oscuro→claro (reinterpretada como escala de elevacion para dunst, rofi, kitty, HyprFM, Obsidian, VPN TUI). `status_ok`/`status_warn`/`status_error` son colores semanticos (herdr, HyprFM, dunst, agents-tui, VPN TUI, y ahora tambien el statusline de Claude Code). Los tokens de forma (fuente, radios, opacidad, blur) viven como default en `themes/_design-tokens.json`, pero desde el piloto `atom-dark`/`tokyo-night`/`oxocarbon-dark` **sí pueden variar por tema** vía 8 campos opcionales (`radius`, `opacity`, `blur_enabled`, `blur_size`, `blur_passes`, `font_mono`, `icon_theme`, `opencode_theme`) — el resto de los temas todavía no los define y cae al default. Detalle completo en `docs/themes.md`.

### Componentes que actualiza theme-switch.sh

- `polybar/colors.ini` (X11, legacy)
- `waybar/theme.css` + `waybar/style.css` (radio/fuente)
- `kitty/colors.conf` + `kitty/kitty.conf` (fuente)
- `~/.zsh_colors`, `~/.zsh_banner_color`
- `qtile/current_theme.json`, `qtile/modules/screens.py` (wallpaper — legacy, el WM real en uso es Hyprland)
- `hypr/hyprland.conf`: colores de borde, `rounding`, opacidad por-app (`windowrule`), `decoration.blur` — **este es el WM que corre de verdad**, no Qtile/picom
- `rofi/theme*.rasi` (radio), `rofi/colors.rasi` (fuente), `dunst/dunstrc` (radio/transparencia/fuente/colores), `gtklock/style.css` (radio/fuente)
- `~/.config/gtk-3.0/gtk.css` (colores Thunar/GTK), `~/.config/gtk-3.0/settings.ini` (icon theme)
- `herdr/config.toml` ([theme.custom]), `opencode/opencode.jsonc` (colores de agente + campo `theme` built-in)
- `~/.claude/statusline-command.sh` (colores ANSI 24-bit de status_ok/warn/error/primary)
- Best-effort si existen: HyprFM, Obsidian (lc-red), Sublime Text, LazyVim, Walker
- Recarga: hyprctl, waybar, kitty, dunst, herdr, thunar

---

## Documentacion

La documentacion vive en `docs/` y cubre:

| Archivo | Contenido |
|---------|-----------|
| `docs/overview.md` | Arquitectura, file tree, enlaces, dual-backend |
| `docs/installation.md` | Guia de instalacion, paquetes Wayland |
| `docs/keybindings.md` | Todos los atajos, dual-backend |
| `docs/themes.md` | Sistema de temas, Polybar + Waybar |
| `docs/automations.md` | Scripts automat/install, dual-backend |
| `docs/configuration/qtile.md` | Qtile detalle, Wayland backend |
| `docs/configuration/polybar.md` | Polybar modulos (X11) |
| `docs/configuration/wayland.md` | Wayland architecture, Waybar, swaylock, grim+slurp |
| `docs/configuration/kitty.md` | Kitty config, Wayland flag |
| `docs/configuration/zsh.md` | Zsh modulos |
| `docs/configuration/rofi.md` | Rofi scripts |
| `docs/configuration/picom.md` | Picom efectos (X11) |
| `docs/configuration/dunst.md` | Dunst notification center |
| `docs/configuration/editors.md` | Neovim + Sublime |
| `docs/configuration/fastfetch.md` | Fastfetch display |
| `docs/configuration/lock-screen.md` | swaylock + betterlockscreen (dual-backend) |
| `docs/configuration/thunar.md` | Thunar accels/uca |
| `docs/configuration/opencode.md` | opencode AI config |
| `docs/configuration/extras.md` | OneDrive, wallpapers, gastos.py |
| `docs/configuration/herdr.md` | Herdr: prefix custom, launch, integracion de temas, por que solo se symlinkea config.toml |

---

## Instrucciones

### 0. AVISO: mantener D4rkFiles sincronizado

Estos dotfiles reales (`$DOTFILES`) tienen un homonimo generico y publico: **D4rkFiles** (`/files/D4rkFiles`,
github.com/D4rkDr4gon/D4rkFiles). **Si cambiamos algo en los dotfiles reales, actualizamos tambien D4rkFiles con
su equivalente generico** (sin rutas, nombres, VPNs, trabajo ni credenciales; lo dependiente del tema va como
plantilla `.tpl`). Equivalencias: `<app>/` -> `config/<app>/`, `lazy-nvim/` -> `config/nvim/`, `zsh/` -> `home/zsh/`,
`sddm/` y `systemd/user/` -> `system/`, `recursos/shortcuts/` -> `tools/`. Verificar con
`scripts/dotfiles-doctor.sh` y `scripts/check-docs.sh` de D4rkFiles, y confirmar con el usuario antes del push.

### 1. Actualizar documentacion tras un cambio

Cuando se modifique un archivo de configuracion, se agregue un nuevo componente, o se cambien atajos/alias:

1. Identificar que archivo/s de docs afecta el cambio
2. Leer el/los archivos actuales
3. Actualizar la informacion afectada (descripciones, atajos, rutas, etc.)
4. Si el cambio introduce algo completamente nuevo, evaluar si amerita un nuevo documento en `docs/configuration/`
5. Actualizar `docs/overview.md` si el file tree cambio
6. Actualizar `docs/keybindings.md` si se agregaron/eliminaron atajos
7. Actualizar este SKILL.md en la seccion correspondiente para mantener el contexto sincronizado

### 2. Crear un nuevo tema

Seguir estos pasos exactos:

1. Elegir nombre en kebab-case (ej: `matrix-rain`)
2. Buscar o crear wallpaper en `recursos/wallpapers/`
3. Crear directorio `themes/<nombre>/`
4. Crear `themes/<nombre>/theme.json` siguiendo la estructura de arriba
5. La ruta del wallpaper debe ser absoluta: `$HOME/dotfiles/recursos/wallpapers/<archivo>`
6. Definir colores: primary, secondary, background, foreground, y chip (battery, bluetooth, wlan, audio)
7. Verificar que el tema funcione: `theme <nombre>`
8. Actualizar `docs/themes.md` con la nueva entrada en la tabla
9. Actualizar la tabla de temas en este SKILL.md

### 3. Agregar un nuevo componente

1. Crear la carpeta en `$DOTFILES/` con su configuracion
2. Agregar el enlace simbolico en la seccion de estructura
3. Crear el enlace real: `ln -sf $DOTFILES/<carpeta> ~/.config/<carpeta>`
4. Crear `docs/configuration/<nombre>.md` con:
   - Proposito del componente
   - Archivos que contiene
   - Tabla de configuracion principal
   - Atajos si aplica
5. Actualizar `docs/overview.md` con el nuevo componente en file tree y tabla
6. Actualizar el README.md principal si el cambio es significativo
7. Si el componente requiere registro en opencode (skills, plugins, MCP), actualizar `opencode/opencode.jsonc`
8. Actualizar este SKILL.md manteniendo la estructura sincronizada

### 4. Ubicacion de los skills

Este skill vive en `$HOME/MY-AGENT-SKILLS/dotfiles-manager/SKILL.md`.
Para que opencode lo cargue, debe estar registrado en `skills.paths` del `opencode.json`.
