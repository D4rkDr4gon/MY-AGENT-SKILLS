---
name: arch-manager
description: Use when the user asks about managing their Arch Linux system — packages, systemd services, kernel, bootloader, networking, hardware, users, locale, dotfiles deployment. Provides full system context for post-install management and maintenance.
---

# Arch Linux System Manager

## System Context

- **Distro:** Arch Linux
- **Kernel:** linux (current)
- **CPU:** AMD Ryzen 7 5825U (amd-ucode)
- **GPU:** AMD Radeon (Barcelo) — `xf86-video-amdgpu`, `vulkan-radeon`
- **RAM:** 22 GB
- **Storage:** NVMe x2 (OS + Data)
- **Boot:** systemd-boot (EFI), dual boot with Windows 11
- **Initramfs:** mkinitcpio
- **Swap:** zram-generator (zstd, 11 GB)
- **Audio:** PipeWire (pipewire-pulse, pipewire-alsa, pipewire-jack)
- **Bluetooth:** Bluez
- **Fingerprint:** Goodix — `libfprint-2-tod1-goodix`
- **Shell:** Zsh + Powerlevel10k
- **WM:** Qtile (X11)
- **Display Manager:** LightDM
- **Dotfiles:** `~/dotfiles/` (Git repo at `github.com/D4rkDr4g0n/dotfiles`)

---

## 1. Package Management

**Official packages:** `pacman`  
**AUR helper:** `yay`

### Useful commands

```bash
# System upgrade
sudo pacman -Syu
yay -Syu              # includes AUR

# List explicitly installed
pacman -Qe --quiet | sort

# List AUR packages
pacman -Qm --quiet | sort

# Find package owner of a file
pacman -Qo <file>

# Orphan cleanup
sudo pacman -Rns $(pacman -Qdtq)

# Package info
pacman -Qi <pkg>
yay -Si <pkg>         # includes AUR

# Search
pacman -Ss <term>
yay -Ss <term>        # includes AUR

# Cache cleanup
sudo pacman -Sc       # keep current only
paccache -r           # keep last 3 versions
```

### AUR Packages Installed

`betterlockscreen`, `conan`, `cura-bin`, `forticlient-vpn`, `i3lock-color`, `n8n`, `onedrive-abraunegg`, `onedriver`, `onlyoffice-bin`, `polyclipping`, `proton-drive-sync-bin`, `proton-mail`, `sigma-file-manager-bin`, `spotify`, `sublime-text-4`, `zoom`

### Repositories

```
[core], [extra], [multilib] — official
[blackarch]                 — pentesting (optional)
```

---

## 2. System Services

### Enabled services

| Service | Controls |
|---|---|
| `lightdm.service` | Display manager |
| `NetworkManager.service` | Network |
| `bluetooth.service` | Bluetooth stack |
| `systemd-resolved.service` | DNS resolver |
| `systemd-timesyncd.service` | NTP sync |
| `ollama.service` | Local LLM server |

### Custom services (`/etc/systemd/system/`)

```bash
# Vault git sync
vault-pull.service    # git pull on boot (multi-user.target)
vault-push.service    # git commit+push on shutdown (shutdown.target)

# Enable/disable
sudo systemctl enable vault-pull.service vault-push.service
sudo systemctl disable vault-pull.service vault-push.service
```

### Timers

```bash
fstrim.timer                    # weekly — SSD trim
systemd-tmpfiles-clean.timer    # daily
shadow.timer                    # daily
archlinux-keyring-wkd-sync.timer # weekly
```

### Service management

```bash
sudo systemctl status <svc>
sudo systemctl start/stop/restart <svc>
sudo systemctl enable/disable <svc>
sudo journalctl -u <svc> --no-pager -n 50
```

---

## 3. User & Groups

```bash
# Primary user
groups: wheel, uucp, docker
shell: /bin/zsh

# Add to groups
sudo usermod -aG docker $USER
```

---

## 4. Network

**Manager:** NetworkManager  
**WiFi backend:** iwd  
**DNS:** systemd-resolved  

### Common tasks

```bash
# List connections
nmcli connection show
nmcli device status

# WiFi
nmcli device wifi list
nmcli device wifi connect <SSID> --ask

# VPN toggle
nmcli connection up <name>
nmcli connection down <name>

# Edit connections
nm-connection-editor
sudo systemctl restart NetworkManager
```

---

## 5. Display

| Component | Config |
|---|---|
| Display Manager | LightDM (`/etc/lightdm/lightdm.conf`) |
| WM | Qtile (`~/.config/qtile/config.py`) |
| Compositor | Picom (`~/.config/picom/picom.conf`) |
| Wallpaper | Nitrogen / Qtile built-in |
| Dual monitors | `xrandr` managed by `display-monitors.sh` |

### Picom features

```
backend: glx
corner-radius: 12
blur: dual_kawase (strength 6)
shadow: disabled
vsync: true
opacity-by-rule for kitty, rofi, dunst, sublime
```

### LightDM

```bash
# Status
systemctl status lightdm

# Greeter config
/etc/lightdm/lightdm-gtk-greeter.conf
```

---

## 6. Locale & Keyboard

```bash
LANG=en_US.UTF-8
KEYMAP=es
XKBLAYOUT=es
FONT=default8x16

# File locations
/etc/locale.conf
/etc/vconsole.conf
/etc/locale.gen
```

### Change keyboard layout

```bash
sudo localectl set-keymap <layout>
sudo localectl set-x11-keymap <layout>
```

---

## 7. Bootloader (systemd-boot)

```bash
# Config
/boot/loader/loader.conf
/boot/loader/entries/<entry>.conf

# Update after kernel changes
sudo mkinitcpio -p linux
```

### machine-id for dual boot entry

Windows entry points to `/boot/EFI/Microsoft/Boot/bootmgwf.efi`.

---

## 8. Kernel & Initramfs

```bash
# mkinitcpio hooks (order matters):
# base udev autodetect microcode modconf kms keyboard keymap consolefont block filesystems fsck

# Regenerate initramfs
sudo mkinitcpio -p linux

# Check kernel version
uname -a
```

---

## 9. ZRAM (Compressed RAM Swap)

```bash
# Config: /etc/systemd/zram-generator.conf
# 11 GB, zstd compression

# Check status
zramctl
swapon --show
```

---

## 10. Audio (PipeWire)

```bash
# Status
systemctl --user status pipewire pipewire-pulse wireplumber

# Volume controls
pactl set-sink-volume @DEFAULT_SINK@ +5%
pactl set-sink-mute @DEFAULT_SINK@ toggle

# GUI
pavucontrol
```

---

## 11. Bluetooth

```bash
# Status
systemctl status bluetooth

# TUI client
bluetui

# CLI
bluetoothctl
  power on
  scan on
  devices
  pair <mac>
  connect <mac>
  trust <mac>
```

---

## 12. Fingerprint Reader

```bash
# Enroll fingerprint(s)
fprintd-enroll

# Verify
fprintd-verify

# List enrolled
fprintd-list

# Remove
fprintd-delete <username>
```

---

## 13. Partition Layout

```
nvme0n1 (system disk):
  p1: EFI (Windows)
  p2-p4: NTFS (Windows partitions)
  p5: /boot — vfat
  p6: / — ext4

nvme1n1 (data disk):
  p2: NTFS (shared storage)
  p3: /files — ext4
```

### /etc/fstab summary

```fstab
/dev/nvme0n1p6  /     ext4  rw,relatime          0 1
UUID=xxxx-xxxx  /boot vfat  fmask=0022,dmask=... 0 2
/dev/nvme1n1p3  /files ext4  rw,relatime          0 2
```

---

## 14. Dotfiles Deployment

### Clone & stow

```bash
git clone https://github.com/D4rkDr4g0n/dotfiles ~/dotfiles
cd ~/dotfiles

# Install stow
sudo pacman -S stow

# Create symlinks component by component:
stow -t ~/.config qtile polybar picom kitty rofi Thunar dunst fastfetch
stow -t ~/.config onedrive opencode
stow -t ~/.config/sublime-text sublime-text
stow -t ~/ zsh  # creates ~/.zshrc

# For Neovim (LazyVim):
stow -t ~/.config lazy-nvim
nvim  # auto-installs plugins

# Autostart directory
ln -sf ~/dotfiles/automat/ ~/.config/automat
```

Or use the install scripts in `~/dotfiles/automat/install/` in order.

### Verification

```bash
# Check all symlinks
ls -la ~/dotfiles/qtile ~/dotfiles/polybar ~/.config/qtile ~/.config/polybar

# Verify Qtile config
qtile check

# Launch components
polybar ~/.config/polybar/launch.sh
picom --config ~/.config/picom/picom.conf
dunst -config ~/.config/dunst/dunstrc

# Verify fonts
fc-list | grep "Hack.*Nerd"
```

---

## 15. Theme Management

8 themes in `~/dotfiles/themes/<name>/theme.json`.

```bash
# List themes
theme --list
ls ~/dotfiles/themes/

# Apply theme
theme at-at
theme city-sci-fi
theme hacker

# Verify current theme
cat ~/.config/qtile/current_theme.json
```

### Creating a new theme

1. Create `~/dotfiles/themes/<name>/`
2. Create `theme.json`:
   ```json
   {
     "name": "Theme Name",
     "wallpaper": "/path/to/wallpaper",
     "primary": "#hex",
     "secondary": "#hex",
     "background": "#hex",
     "foreground": "#hex",
     "chip_battery": "#hex",
     "chip_bluetooth": "#hex",
     "chip_wlan": "#hex",
     "chip_audio": "#hex"
   }
   ```
3. Copy wallpaper to `~/dotfiles/recursos/wallpapers/`
4. Update `docs/themes.md` table
5. Test: `theme <name>`

### Theme components updated

- `polybar/colors.ini`
- `kitty/colors.conf`
- `~/.zsh_colors`
- `qtile/current_theme.json`
- `qtile/modules/screens.py` (wallpaper path)
- Polybar + Qtile are reloaded automatically

---

## 16. Filesystem Locations

### Important paths

```
~/dotfiles/                    # Dotfiles Git repository
~/dotfiles/recursos/wallpapers/ # Wallpaper collection (18+ images)
~/dotfiles/recursos/finnancials/gastos.py  # Expense manager TUI
~/dotfiles/automat/install/    # Installation scripts (13 scripts)
~/dotfiles/scripts/            # theme-switch.sh, vpn-replace.sh
~/dotfiles/docs/               # Documentation
~/dotfiles/themes/             # Dynamic themes
```

### Data partitions

```
/files     — bulk storage (music, videos, projects, etc.)
~/OneDrive — cloud sync (OneDrive + Obsidian vault)
```

---

## 17. OneDrive & Cloud Sync

```bash
# OneDrive CLI
onedrive --synchronize
onedrive --monitor

# OneDrive FUSE (on demand mount)
onedriver mount ~/OneDrive

# Config: ~/.config/onedrive/config
#   sync_dir = "~/OneDrive"
#   skip_file = "~*|.~*|*.tmp|*.swp|*.partial"
```

### Obsidian Vault Git Sync

```
~/OneDrive/vault/ — Git repo
vault-pull.service  → pulls on boot
vault-push.service  → commits "D4 - YYYY-MM-DD" + pushes force on shutdown
```

---

## 18. Development Environment

| Tool | Config path |
|---|---|
| Neovim (LazyVim) | `~/.config/nvim/` or `~/dotfiles/lazy-nvim/` |
| Sublime Text 4 | `~/.config/sublime-text/` or `~/dotfiles/sublime-text/` |
| Git | `~/.gitconfig` |
| Python | `~/.local/bin/`, pip |
| Node.js | n8n global (`/usr/lib/node_modules/n8n`) |
| Go | Go 1.26 |
| D (DMD) | DMD v2.x |
| Ollama | Service + models at `/usr/share/ollama/` |

### Node global packages

```bash
n8n@2.2.6
node-gyp@12.3.0
npm@11.14.1
```

### Python (system + pip)

Notable packages: `aiohttp`, `cairocffi`, `conan`, `cryptography`, `dbus-fast`, `ollama`, `pillow`, `pynvim`, `requests`

---

## 19. Networking & VPN

```bash
# List VPN connections
nmcli connection show | grep vpn

# Toggle VPN
nmcli connection up <vpn-name>
nmcli connection down <vpn-name>

# Polybar has a vpn_status.sh + vpn_toggle.sh module
# Proton VPN has CLI + GTK interfaces
```

---

## 20. Security

```bash
# SSH key
# ed25519 key in ~/.ssh/

# Fingerprint (fprintd)
fprintd-enroll

# Docker
# User must be in docker group
sudo usermod -aG docker $USER
```

---

## 21. System Maintenance Tasks

```bash
# Full system update
yay -Syu

# Clean pacman cache (keep last 3)
sudo paccache -r

# Remove orphan packages
sudo pacman -Rns $(pacman -Qdtq)

# Check disk health
sudo smartctl -a /dev/nvme0n1
sudo smartctl -a /dev/nvme1n1

# Check disk usage
ncdu /
df -h

# Check ZRAM
zramctl

# Check journal for errors
journalctl -p err -b --no-pager | tail -30

# Regenerate initramfs after config change
sudo mkinitcpio -p linux

# Update systemd-boot entries
sudo bootctl update

# Check systemd-boot
bootctl status

# Trim manually
sudo fstrim -v /
sudo fstrim -v /files
```

---

## 22. Troubleshooting

### Display / Qtile issues

```bash
# Check Qtile config
qtile check

# Restart Qtile without logout
Mod+Ctrl+R

# Check Xorg logs
cat ~/.local/share/xorg/Xorg.0.log | grep -iE "(error|fail)"

# Picom issues
pkill picom && picom --config ~/.config/picom/picom.conf

# Polybar issues
pkill polybar && bash ~/.config/polybar/launch.sh
```

### Network issues

```bash
# Restart NetworkManager
sudo systemctl restart NetworkManager

# Check WiFi
nmcli device wifi list

# Check DNS
resolvectl status

# Check connections
nmcli connection show --active
```

### Audio issues

```bash
# Restart PipeWire
systemctl --user restart pipewire pipewire-pulse wireplumber

# Check sinks
pactl list sinks short

# Test audio
speaker-test -c 2 -l 1
```

### Bluetooth issues

```bash
sudo systemctl restart bluetooth
bluetoothctl
  power on
  scan on
```

---

## 23. Post-Install Checklist

- [ ] Install yay
- [ ] Install all fonts (`install-fonts.sh`)
- [ ] Install Zsh + change shell (`install-zsh.sh`)
- [ ] Install Qtile (`install-qtile.sh`)
- [ ] Install Polybar (`install-polybar.sh`)
- [ ] Install Picom (`install-picom.sh`)
- [ ] Install Kitty (`install-kitty.sh`)
- [ ] Install Rofi (`install-rofi.sh`)
- [ ] Install Neovim + LazyVim (`install-neovim.sh`)
- [ ] Install productivity tools (`install-tools.sh`)
- [ ] Install Ollama (`install-ollama.sh`)
- [ ] Install n8n (`install-n8n.sh`)
- [ ] Apply theme (`theme city-sci-fi`)
- [ ] Set up online accounts
- [ ] Configure dual monitors
- [ ] Configure VPN
- [ ] Set up fingerprint reader
- [ ] Enable vault services
- [ ] Verify Docker access
- [ ] Sync OneDrive
- [ ] Create Timeshift snapshot
- [ ] Reboot and verify
