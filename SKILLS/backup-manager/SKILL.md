---
name: backup-manager
description: Use when creating, managing, or restoring backups — restic, borg, rsync, 3-2-1 strategy, snapshot management, backup automation with systemd timers/cron, and restore testing.
---

# backup-manager

Guía de estrategias de backup para sistemas Linux y Windows. Orientada a administración de sistemas y protección de datos.

## Contexto del usuario

- **SO:** Arch Linux (primary) + Windows 11
- **Herramientas Linux:** `restic`, `rsync`, `borg`, `systemd-timers`
- **Herramientas Windows:** `robocopy`, `Windows Backup`, `restic`
- **Destinos:** Disco local, USB externo, servidor remoto (SFTP/S3)
- **Datos críticos:** `~/dotfiles/`, `~/projects/`, `~/lab/`, Obsidian vault, `/files/Personal-Vault/`, GPG keys, SSH keys

---

## 1. Restic — Backup moderno y cifrado

### Setup
```bash
# Instalar
sudo pacman -S restic

# Inicializar repositorio
restic init --repo /mnt/backup/restic-repo
restic init --repo sftp:user@server:/backup/restic-repo    # Remoto
restic init --repo rclone:cloud:backup/restic-repo          # Cloud (via rclone)
```

### Backup
```bash
# Backup básico
restic --repo /mnt/backup/restic-repo backup /home/lcampassi/projects

# Con exclusiones
restic --repo /mnt/backup/restic-repo backup \
  --exclude="*.tmp" \
  --exclude="__pycache__" \
  --exclude="node_modules" \
  --exclude=".cache" \
  --exclude="target" \
  /home/lcampassi

# Backup de directorios específicos
restic backup \
  /home/lcampassi/dotfiles \
  /home/lcampassi/.config \
  /home/lcampassi/.ssh \
  /files/Personal-Vault

# Taggear snapshot
restic backup --tag dotfiles /home/lcampassi/dotfiles
restic backup --tag vault /files/Personal-Vault
```

### Gestión y restore
```bash
# Listar snapshots
restic snapshots
restic snapshots --tag dotfiles

# Ver diferencias entre snapshots
restic diff latest <snapshot-id>

# Restore completo
restic restore latest --target /tmp/restore

# Restore de archivos específicos
restic restore latest --target /tmp/restore \
  --include /home/lcampassi/dotfiles/.gitconfig

# Montar repositorio como FUSE
mkdir /tmp/restic-mount
restic mount /tmp/restic-mount
```

### Automatización
```bash
# Script — /home/lcampassi/scripts/backup.sh
#!/bin/bash
REPO="/mnt/backup/restic-repo"
export RESTIC_PASSWORD="<pass>"

restic -r $REPO backup \
  --tag automated \
  --exclude-file=/home/lcampassi/.restic-excludes \
  /home/lcampassi/dotfiles \
  /home/lcampassi/.config \
  /home/lcampassi/.ssh \
  /files/Personal-Vault

# Olvidar snapshots viejos (retention)
restic -r $REPO forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune

# Verificar integridad
restic -r $REPO check
```

### Systemd timer (diario)
```bash
# /etc/systemd/system/restic-backup.service
[Unit]
Description=Restic backup
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
ExecStart=/home/lcampassi/scripts/backup.sh
User=lcampassi
Nice=19
IOSchedulingClass=idle

# /etc/systemd/system/restic-backup.timer
[Unit]
Description=Daily restic backup

[Timer]
OnCalendar=daily
Persistent=true
RandomizedDelaySec=1800

[Install]
WantedBy=timers.target

sudo systemctl enable --now restic-backup.timer
```

---

## 2. Borg — Backup con deduplicación

```bash
# Instalar
sudo pacman -S borg

# Inicializar repo
borg init --encryption=repokey /mnt/backup/borg-repo

# Backup
borg create --stats --progress \
  /mnt/backup/borg-repo::{hostname}-{now:%Y-%m-%d} \
  /home/lcampassi/dotfiles \
  /home/lcampassi/.config \
  --exclude '*.cache' \
  --exclude '*/node_modules/*'

# Listar archivos
borg list /mnt/backup/borg-repo

# Restore
borg extract /mnt/backup/borg-repo::<archive-name>

# Prune (retention)
borg prune --keep-daily 7 --keep-weekly 4 --keep-monthly 6 \
  /mnt/backup/borg-repo

# Compactar (liberar espacio)
borg compact /mnt/backup/borg-repo
```

---

## 3. Rsync — Backup rápido local/remoto

```bash
# Backup local
rsync -avh --delete /home/lcampassi/dotfiles/ /mnt/backup/dotfiles/

# Backup remoto (SSH)
rsync -avh --delete -e ssh \
  /home/lcampassi/dotfiles/ \
  user@server:/backup/dotfiles/

# Con exclusiones
rsync -avh --delete \
  --exclude=".cache" \
  --exclude="node_modules" \
  --exclude="__pycache__" \
  /home/lcampassi/projects/ /mnt/backup/projects/

# Snapshot incremental con hardlinks
rsync -avh --delete --link-dest=/mnt/backup/daily/yesterday \
  /home/lcampassi/projects/ /mnt/backup/daily/$(date +%Y%m%d)
```

---

## 4. Estrategia 3-2-1

```
3 copias de los datos
2 medios diferentes (SSD + HDD, local + cloud)
1 copia fuera del sitio (off-site / cloud)
```

### Implementación práctica
```bash
# Backup local (diario)
restic backup --tag local /home/lcampassi

# Backup a USB externo (semanal)
# Conectar USB en /mnt/usb-backup
restic -r /mnt/usb-backup/restic-repo backup --tag usb /home/lcampassi

# Backup remoto (diario)
restic -r sftp:server:/backup/restic-repo backup --tag remote /home/lcampassi
```

### Rotación recomendada
```
Diario:   últimos 7 días
Semanal:  últimas 4 semanas
Mensual:  últimos 6 meses
Anual:    1 por año (forever)
```

---

## 5. Backup de GPG y SSH keys (crítico)

```bash
# Exportar GPG keys y cifrar con age
gpg --export-secret-keys --armor > /tmp/gpg-keys.asc
gpg --export-ownertrust > /tmp/gpg-trust.txt
cp -r ~/.ssh /tmp/ssh-keys

# Cifrar con age
tar czf /tmp/crypto-keys.tar.gz /tmp/gpg-keys.asc /tmp/gpg-trust.txt /tmp/ssh-keys
age -p -o /mnt/backup/crypto-keys.tar.gz.age /tmp/crypto-keys.tar.gz

# Backup separado (mínimo 2 copias físicas)
cp /mnt/backup/crypto-keys.tar.gz.age /mnt/usb-backup/
```

---

## 6. Windows Backup

### Robocopy (built-in)
```powershell
# Backup de dotfiles
robocopy C:\Users\lcampassi\.config C:\Backup\.config /MIR /R:3 /W:5 /LOG:C:\Backup\logs\config.log

# Backup de proyectos
robocopy "C:\Users\lcampassi\source\repos" "D:\Backup\repos" /MIR /R:3 /W:5 /XD node_modules __pycache__

# Parámetros clave
# /MIR = mirror (borra archivos que ya no existen en origen)
# /R:3 = 3 reintentos
# /W:5 = esperar 5 seg entre reintentos
# /XD = excluir directorios
# /LOG = log a archivo
```

### Windows Task Scheduler
```powershell
# Crear tarea programada
$action = New-ScheduledTaskAction -Execute "robocopy" -Argument "C:\Users\lcampassi\.config D:\Backup\.config /MIR /R:3 /W:5"
$trigger = New-ScheduledTaskTrigger -Daily -At "03:00"
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -RunLevel Highest
Register-ScheduledTask -TaskName "Backup-Config" -Action $action -Trigger $trigger -Principal $principal
```

### Restic on Windows
```powershell
# restic funciona nativo en Windows
restic.exe init --repo D:\Backup\restic-repo
restic.exe backup C:\Users\lcampassi\source\repos
```

---

## 7. Verificación y restore testing

```bash
# Verificar integridad del repo
restic check
borg check /mnt/backup/borg-repo

# Restore de prueba (sin sobrescribir)
restic restore latest --target /tmp/restore-test

# Verificar que los archivos están completos
diff -r /home/lcampassi/dotfiles /tmp/restore-test/home/lcampassi/dotfiles

# Probar restore de un archivo específico
restic restore latest --target /tmp/restore-single \
  --include /home/lcampassi/.ssh/id_ed25519
```

---

## 8. Buenas prácticas

1. **3-2-1 siempre** — 3 copias, 2 medios, 1 off-site
2. **Automatizar** — si requiere acción manual, no se va a hacer
3. **Cifrar backups** — restic/borg ya cifran, rsync requiere cifrado de disco
4. **Probar restores** — un backup que no se puede restore no es backup
5. **Monitorear** — verificar que los backups se ejecutan, alertar si fallan
6. **Documentar** — qué se backupa, dónde, cómo restorear
7. **Keys críticas** — GPG, SSH, age keys merecen backup especial aparte
8. **No confiar en un solo medio** — SSD + HDD + cloud
9. **Retention policy** — no guardar todo forever, tener política de rotación
10. **Check periódico** — `restic check` semanal para detectar corrupción
