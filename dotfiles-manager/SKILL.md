---
name: dotfiles-manager
description: Use when the user asks about managing, updating, documenting, or creating themes for their dotfiles at ~/dotfiles. Helps with documentation, theme creation, and provides full context of the dotfiles structure.
---

# dotfiles-manager

## Contexto del Repositorio

**Ubicacion**: `~/dotfiles`
**Remote**: `git@github.com:D4rkDr4g0n/dotfiles.git` (branch: `main`)
**Autor**: Lucciano Campassi (D4rkDr4g0n) -- Ciberseguridad & Desarrollo
**Distro**: Arch Linux / Kali Linux
**WM**: Qtile (Python)
**License**: MIT

### Stack Tecnologico

```
WM:          Qtile (Python)
Barra:       Polybar
Terminal:    Kitty
Shell:       Zsh + powerlevel10k
Launcher:    Rofi
Compositor:  Picom (GLX + dual_kawase blur)
Editores:    Neovim (LazyVim) / Sublime Text
File Mgr:    Thunar
Info:        Fastfetch
AI:          opencode (skills personalizadas)
```

### Enlaces Simbolicos

```
~/.zshrc              -> ~/dotfiles/zsh/zshrc
~/.config/qtile       -> ~/dotfiles/qtile/
~/.config/polybar     -> ~/dotfiles/polybar/
~/.config/picom       -> ~/dotfiles/picom/
~/.config/rofi        -> ~/dotfiles/rofi/
~/.config/kitty       -> ~/dotfiles/kitty/
~/.config/Thunar      -> ~/dotfiles/Thunar/
~/.config/zsh         -> ~/dotfiles/zsh/
~/.config/automat     -> ~/dotfiles/automat/
~/.config/opencode    -> ~/dotfiles/opencode/
```

---

## Estructura Completa del Repositorio

```
dotfiles/
├── README.md
├── docs/                              # Documentacion modular
│   ├── overview.md, installation.md, keybindings.md, themes.md, automations.md
│   └── configuration/
│       ├── qtile.md, polybar.md, kitty.md, zsh.md, rofi.md
│       ├── picom.md, editors.md, fastfetch.md, thunar.md, extras.md
│
├── qtile/                             # Window Manager
│   ├── config.py                      # Entry point
│   ├── current_theme.json             # Tema activo
│   └── modules/
│       ├── groups.py                  # 5 workspaces: NOTES, FILES, DEV, SYS, WEB
│       ├── keys.py                    # Keybindings (mod4 = Super)
│       ├── layouts.py                 # Columns, MonadTall, Stack
│       ├── mouse.py                   # Mouse bindings
│       ├── screens.py                 # Dual screen + wallpapers
│       └── hooks.py                   # Autostart (nitrogen, polybar, picom)
│
├── polybar/                           # Status bar
│   ├── config.ini                     # 98% width, 28px, rounded 10px
│   ├── colors.ini                     # Dinamico por tema
│   ├── launch.sh                      # Kill + launch por monitor
    │   └── modules/ (battery, bluetooth, brillo, date, logo, pulseaudio, vpn, wlan, xworkspaces)
│
├── kitty/                             # Terminal
│   ├── kitty.conf                     # Hack Nerd Font 10pt, 80% opacity
│   └── colors.conf                    # Dinamico por tema
│
├── zsh/                               # Shell modular
│   ├── zshrc                          # Entry point
│   └── modules/
│       ├── aliases.zsh                # theme, vi, cat, ls, c, q, .., vpnup/down, etc.
│       ├── history.zsh                # 100k lines, shared, inc_append
│       ├── paths.zsh                  # ~/.local/bin, ~/.opencode/bin
│       ├── plugins.zsh                # zsh-autosuggestions, zsh-syntax-highlighting
│       ├── startup.zsh                # ASCII banner rojo D4rkDr4g0n
│       ├── theme.zsh                  # powerlevel10k + colores dinamicos
│       └── tools.zsh                  # extractPorts, hex-encode/decode, rot13
│
├── rofi/                              # Launcher
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
│       ├── settings-menu.sh           # Themes, Workspaces, Web search, Backgrounds
│       └── web-search.sh              # Google, abre Firefox en WEB workspace
│
├── picom/                             # Compositor
│   └── picom.conf                     # GLX, vsync, 12px radius, dual_kawase blur (6)
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
├── themes/                            # 8 temas dinamicos
│   ├── at-at/         (theme.json + wallpaper)
│   ├── city/
│   ├── city-sci-fi/
│   ├── creativity-room/
│   ├── data-center/
│   ├── hacker/
│   ├── hacker-setup/
│   └── kali-red/
│
├── scripts/
│   ├── theme-switch.sh                # Cambia polybar/kitty/zsh/qtile/fastfetch
│   └── vpn-replace.sh                 # Reemplazar config de Wireguard VPN
│
├── automat/
│   ├── display-monitors.sh            # xrandr laptop + HDMI
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

| # | Nombre | Icono | Uso |
|---|--------|-------|-----|
| 1 | NOTES | 󰠮 | Notas y documentacion |
| 2 | FILES | 󰉋 | Gestion de archivos |
| 3 | DEV | 󰘦 | Desarrollo / coding |
| 4 | SYS | 󰣇 | Sistema, terminales |
| 5 | WEB | 󰖟 | Navegador, web |

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
| `Mod + Q` | Cerrar ventana |
| `Mod + Shift + F` | Fullscreen |
| `Mod + T` | Float toggle |
| `Mod + Shift + Arrows` | Mover ventana |
| `Mod + Ctrl + Arrows` | Redimensionar |
| `Mod + Ctrl + R` | Recargar Qtile |
| `Mod + L` | Action menu |
| `Mod + Shift + Space` | Settings menu |
| `Mod + 1-5` | Ir a workspace |
| `Mod + Shift + 1-5` | Mover ventana a workspace |
| `Print` / `Mod + Shift + S` | Flameshot |

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
| `theme` | `~/dotfiles/scripts/theme-switch.sh` |
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
| `polybarupdate` | Relaunch polybar |
| `hosts` | `sudo nvim /etc/hosts` |

---

## Temas Disponibles

8 temas en `themes/<nombre>/theme.json`:

| Tema | Wallpaper | Paleta |
|------|-----------|--------|
| AT-AT | at-at.png | Marron/gris calido |
| Kali Red | wallpaper_dark_spaceship.jpg | Rojo oscuro |
| Hacker | wallpaper hacker.jpg | Verde matrix |
| Hacker Setup | hacker-setup-dark.jpg | Beige/teal |
| City | wallpaper_city.jpg | Rosa/purpura |
| City Sci-Fi | wallpaper_city_sci-fi.jpg | Teal/gris |
| Creativity Room | wallpaper_Creativity_Room.jpg | Tierra calido |
| Data Center | Wallpaper data center.jpg | Cian/verde |

### Estructura de theme.json

```json
{
  "name": "AT-AT",
  "wallpaper": "/home/lcampassi/dotfiles/recursos/wallpapers/at-at.png",
  "colors": {
    "primary": "#a0522d",
    "secondary": "#8b4513",
    "background": "#1a1a1a",
    "foreground": "#d4c5a9",
    "chip": {
      "battery": "#a0522d",
      "bluetooth": "#4a90d9",
      "wlan": "#4a90d9",
      "audio": "#a0522d"
    }
  }
}
```

### Componentes que actualiza theme-switch.sh

- `polybar/colors.ini`
- `kitty/colors.conf`
- `~/.zsh_colors`
- `qtile/current_theme.json`
- `qtile/modules/screens.py` (wallpaper)
- Recarga: polybar, kitty, qtile

---

## Documentacion

La documentacion vive en `docs/` y cubre:

| Archivo | Contenido |
|---------|-----------|
| `docs/overview.md` | Arquitectura, file tree, enlaces |
| `docs/installation.md` | Guia de instalacion |
| `docs/keybindings.md` | Todos los atajos |
| `docs/themes.md` | Sistema de temas |
| `docs/automations.md` | Scripts automat/install |
| `docs/configuration/qtile.md` | Qtile detalle |
| `docs/configuration/polybar.md` | Polybar modulos |
| `docs/configuration/kitty.md` | Kitty config |
| `docs/configuration/zsh.md` | Zsh modulos |
| `docs/configuration/rofi.md` | Rofi scripts |
| `docs/configuration/picom.md` | Picom efectos |
| `docs/configuration/editors.md` | Neovim + Sublime |
| `docs/configuration/fastfetch.md` | Fastfetch display |
| `docs/configuration/thunar.md` | Thunar accels/uca |
| `docs/configuration/opencode.md` | opencode AI config |
| `docs/configuration/extras.md` | OneDrive, wallpapers, gastos.py |

---

## Instrucciones

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
5. La ruta del wallpaper debe ser absoluta: `/home/lcampassi/dotfiles/recursos/wallpapers/<archivo>`
6. Definir colores: primary, secondary, background, foreground, y chip (battery, bluetooth, wlan, audio)
7. Verificar que el tema funcione: `theme <nombre>`
8. Actualizar `docs/themes.md` con la nueva entrada en la tabla
9. Actualizar la tabla de temas en este SKILL.md

### 3. Agregar un nuevo componente

1. Crear la carpeta en `~/dotfiles/` con su configuracion
2. Agregar el enlace simbolico en la seccion de estructura
3. Crear el enlace real: `ln -sf ~/dotfiles/<carpeta> ~/.config/<carpeta>`
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

Este skill vive en `/home/lcampassi/MY-AGENT-SKILLS/dotfiles-manager/SKILL.md`.
Para que opencode lo cargue, debe estar registrado en `skills.paths` del `opencode.json`.
