---
name: automation-manager
description: Use when managing system automation — systemd timers, cron jobs, PowerShell Scheduled Tasks, and shell scripting. Cross-platform (Linux + Windows). For sysadmin, devops, and CSIRT automation workflows.
---

# automation-manager

## Descripción general

La automatización de tareas es el pilar de un sistema bien administrado. Este skill cubre las cuatro herramientas fundamentales para **Linux (Arch)** y **Windows 11**, con énfasis en patrones **idempotentes**, **logging estructurado** y **manejo de errores**.

### Principios

| Principio | Descripción |
|-----------|-------------|
| **Idempotencia** | Ejecutar N veces produce el mismo resultado que ejecutarlo una vez |
| **Logging** | Todo script debe loguear inicio, fin, errores y warnings con timestamp |
| **Notificaciones** | Fallos deben notificar al admin (notify-send, email, webhook) |
| **Fallos silenciosos no existen** | Si algo falla, debe ser detectable |

### Logging function (bash — reusable)

```bash
LOGFILE="${HOME}/logs/automation-$(date +%Y%m).log"
mkdir -p "$(dirname "$LOGFILE")"

log() {
    local level="$1" msg="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [${level}] ${msg}" | tee -a "$LOGFILE"
}

info()  { log "INFO"  "$1"; }
warn()  { log "WARN"  "$1"; }
error() { log "ERROR" "$1"; }
```

---

## systemd timers

Son el reemplazo moderno de cron en Linux. Consisten en dos archivos: `.timer` (configuración del disparo) y `.service` (la tarea a ejecutar).

### Estructura básica

`~/.config/systemd/user/backup.service`:
```ini
[Unit]
Description=Backup diario de datos críticos

[Service]
Type=oneshot
ExecStart=/home/lcampassi/scripts/backup.sh
StandardOutput=journal
StandardError=journal
```

`~/.config/systemd/user/backup.timer`:
```ini
[Unit]
Description=Timer de backup diario — 03:00 AM

[Timer]
OnCalendar=daily
Persistent=true
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
```

### Tipos de calendario

| Expresión | Significado |
|-----------|-------------|
| `daily` | Todos los días a medianoche |
| `*-*-* 03:00:00` | Todos los días a las 03:00 |
| `Mon..Fri 09:30:00` | Lunes a viernes 09:30 |
| `*-*-1..7 02:00:00` | Primeros 7 días del mes |
| `0/15 * * * *` | Cada 15 minutos (notación cron) |

### Timers monotónicos

Se ejecutan transcurrido X tiempo desde el boot:

```ini
[Timer]
OnBootSec=5min
OnUnitActiveSec=1h
```

### Instalación y gestión

```bash
systemctl --user daemon-reload
systemctl --user enable --now backup.timer
systemctl --user list-timers
systemctl --user status backup.timer
systemctl --user start backup.service   # Ejecutar manualmente
journalctl --user -u backup.service -f  # Logs en vivo
```

### Timers del sistema (root)

Para tareas del sistema usar `/etc/systemd/system/` y sin `--user`:

```bash
sudo systemctl enable --now cleanup.timer
```

### Persistent timers

`Persistent=true` en el timer ejecuta la tarea olvidada si el sistema estaba apagado. Esencial para notebooks y desktops que no están 24/7.

### Ejemplo completo: rotación de logs

`~/.config/systemd/user/logrotate.service`:
```ini
[Unit]
Description=Rotar logs personales

[Service]
Type=oneshot
ExecStart=/home/lcampassi/scripts/rotate-logs.sh
Nice=19
IOSchedulingClass=idle
```

`~/.config/systemd/user/logrotate.timer`:
```ini
[Unit]
Description=Timer semanal de logrotate

[Timer]
OnCalendar=weekly
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
systemctl --user enable --now logrotate.timer
```

---

## Cron jobs

Para entornos donde systemd timers no están disponibles o se prefiere crontab clásico.

### Sintaxis

```
* * * * * comando
┬ ┬ ┬ ┬ ┬
│ │ │ │ └ día de semana (0-7, 0=domingo)
│ │ │ └── mes (1-12)
│ │ └──── día del mes (1-31)
│ └────── hora (0-23)
└──────── minuto (0-59)
```

### Expresiones comunes

| Expresión | Se ejecuta |
|-----------|-----------|
| `0 3 * * *` | Todos los días 03:00 |
| `*/15 * * * *` | Cada 15 minutos |
| `0 9-17 * * 1-5` | Cada hora 9-17, lunes-viernes |
| `@daily` | Una vez al día |
| `@reboot` | Al iniciar el sistema |

### Crontab del usuario

```bash
crontab -e                                    # Editar crontab del usuario
crontab -l                                    # Listar tareas actuales
CRON_LOG="${HOME}/logs/cron-$(date +%Y%m).log"
```

Ejemplo de entrada en crontab:
```
# ──────────────────────────────────────────────
# Backup diario — 03:00
# ──────────────────────────────────────────────
0 3 * * * /home/lcampassi/scripts/backup.sh >> "${HOME}/logs/cron-$(date +\%Y\%m).log" 2>&1

# ──────────────────────────────────────────────
# Health check — cada 5 minutos
# ──────────────────────────────────────────────
*/5 * * * * /home/lcampassi/scripts/health-check.sh
```

### Variables de entorno en cron

Cron ejecuta con un entorno mínimo (`SHELL=/bin/sh`, `PATH` reducido). Siempre definir:

```bash
# Al inicio del crontab
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin:/home/lcampassi/.local/bin
HOME=/home/lcampassi
MAILTO=lcampassi@localhost
```

### Anacron para desktops

Si el equipo no está 24/7, cron puede saltarse ejecuciones. Anacron resuelve esto:

```bash
sudo pacman -S anacron
```

Config en `/etc/anacrontab`:
```
# period delay job-identifier command
@daily  10  backup.daily   /home/lcampassi/scripts/backup.sh
@weekly 20  cleanup.weekly /home/lcampassi/scripts/cleanup.sh
```

- **period**: frecuencia en días (`@daily` = 1, `@weekly` = 7)
- **delay**: minutos de espera antes de ejecutar
- **identifier**: archivo timestamp en `/var/spool/anacron/`

---

## PowerShell Scheduled Tasks

En Windows 11, las tareas programadas se manejan con PowerShell o el Task Scheduler GUI.

### Crear tarea básica

```powershell
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "-NoProfile -File C:\Scripts\backup.ps1"

$trigger = New-ScheduledTaskTrigger -Daily -At "03:00am"

$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" `
    -LogonType ServiceAccount -RunLevel Highest

Register-ScheduledTask -TaskName "BackupDiario" `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Description "Backup diario de datos críticos"
```

### Triggers avanzados

```powershell
# Cada 30 minutos
$trigger = New-ScheduledTaskTrigger -Once -At "00:00" `
    -RepetitionInterval (New-TimeSpan -Minutes 30) `
    -RepetitionDuration ([TimeSpan]::MaxValue)

# Al iniciar sesión
$trigger = New-ScheduledTaskTrigger -AtLogOn

# En evento del sistema (ej: USB insertado)
$trigger = New-ScheduledTaskTrigger -Custom -RepetitionInterval "PT5M"
```

### Tareas con condiciones

```powershell
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries $false `
    -DontStopIfGoingOnBatteries $true `
    -StartWhenAvailable $true `
    -RunOnlyIfNetworkAvailable $true

Register-ScheduledTask -TaskName "BackupRed" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal
```

### Gestión de tareas

```powershell
Get-ScheduledTask -TaskName "Backup*"
Start-ScheduledTask -TaskName "BackupDiario"
Stop-ScheduledTask -TaskName "BackupDiario"
Unregister-ScheduledTask -TaskName "BackupDiario" -Confirm:$false
Export-ScheduledTask -TaskName "BackupDiario" | Out-File "BackupDiario.xml"
```

### Desde el Task Scheduler GUI

`taskschd.msc` → Create Task → General (Run whether user is logged on or not) → Triggers → Actions → Conditions → Settings.

### PowerShell workflow script completo

```powershell
# C:\Scripts\automated-task.ps1
param(
    [string]$TaskName,
    [string]$ScriptPath,
    [string]$TriggerTime = "03:00am"
)

$ErrorActionPreference = "Stop"
$logFile = "C:\Logs\scheduler-$(Get-Date -Format yyyyMM).log"

function Write-Log {
    param([string]$Level, [string]$Message)
    $line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] [$Level] $Message"
    Add-Content -Path $logFile -Value $line
    Write-Host $line
}

try {
    $action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
        -Argument "-NoProfile -ExecutionPolicy Bypass -File $ScriptPath"
    $trigger = New-ScheduledTaskTrigger -Daily -At $TriggerTime
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" `
        -LogonType ServiceAccount -RunLevel Highest

    Register-ScheduledTask -TaskName $TaskName `
        -Action $action `
        -Trigger $trigger `
        -Principal $principal `
        -Force

    Write-Log "INFO" "Tarea '$TaskName' registrada — $ScriptPath a las $TriggerTime"
} catch {
    Write-Log "ERROR" "Falló registro de tarea: $_"
    exit 1
}
```

---

## Shell scripting best practices

### Idempotency patterns

```bash
#!/bin/bash
set -euo pipefail

SCRIPT_NAME="$(basename "$0")"
LOCKFILE="/tmp/${SCRIPT_NAME}.lock"

cleanup() {
    rm -f "$LOCKFILE"
    info "Script finalizado"
}
trap cleanup EXIT
trap 'error "Interrumpido por señal"; exit 1' INT TERM

# Evitar ejecución concurrente
if [[ -f "$LOCKFILE" ]]; then
    pid=$(cat "$LOCKFILE")
    if kill -0 "$pid" 2>/dev/null; then
        error "Ya está en ejecución (PID $pid)"
        exit 1
    fi
    warn "Lockfile huérfano del PID $pid, continuando"
fi
echo $$ > "$LOCKFILE"

# Idempotencia: verificar si ya se hizo
SEMAPHORE_DIR="${HOME}/.semaphores/$(date +%Y%m%d)/${SCRIPT_NAME}"
mark_done() {
    mkdir -p "$(dirname "$SEMAPHORE_DIR")"
    date > "$SEMAPHORE_DIR"
}
is_done() {
    [[ -f "$SEMAPHORE_DIR" ]]
}

# ── Ejecución condicional ──
if is_done; then
    info "Tarea ya ejecutada hoy, saltando"
    exit 0
fi

# ── Lógica principal ──
main() {
    info "Iniciando ${SCRIPT_NAME}"
    # ... tareas ...
    mark_done
    info "Completado exitosamente"
}
main "$@"
```

### Argument parsing

```bash
DRY_RUN=false
VERBOSE=false
CONFIG_FILE="${HOME}/.config/automation/config.ini"

usage() {
    cat <<EOF
Uso: $0 [opciones]
Opciones:
  -c, --config FILE   Archivo de configuración
  -n, --dry-run       Simular sin ejecutar
  -v, --verbose       Modo verboso
  -h, --help          Mostrar ayuda
EOF
    exit 0
}

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -c|--config) CONFIG_FILE="$2"; shift 2 ;;
        -n|--dry-run) DRY_RUN=true; shift ;;
        -v|--verbose) VERBOSE=true; shift ;;
        -h|--help) usage ;;
        *) error "Opción desconocida: $1"; usage ;;
    esac
done

run() {
    if $DRY_RUN; then
        info "[DRY-RUN] $*"
    else
        "$@"
    fi
}
```

### Config files con fallback

```bash
load_config() {
    local cfg="$1"
    if [[ -f "$cfg" ]]; then
        info "Cargando configuración: $cfg"
        source "$cfg"
    else
        warn "No existe $cfg, usando defaults"
        # Defaults
        BACKUP_DEST="${HOME}/backups"
        RETENTION_DAYS=30
        LOG_LEVEL="INFO"
    fi
}
```

Ejemplo de `~/.config/automation/backup.ini`:
```bash
# Configuración de backup
BACKUP_DEST="/mnt/backup"
RETENTION_DAYS=45
EXCLUDE_DIRS=("node_modules" ".cache" "tmp")
COMPRESS=true
```

---

## Automation patterns

### Backup automation

```bash
#!/bin/bash
set -euo pipefail

BACKUP_DEST="${BACKUP_DEST:-${HOME}/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DEST}/home-${DATE}.tar.zst"

mkdir -p "$BACKUP_DEST"

info "Iniciando backup → ${BACKUP_FILE}"

tar --zstd \
    --exclude="node_modules" \
    --exclude=".cache" \
    --exclude=".local/share/Trash" \
    -cf "$BACKUP_FILE" \
    -C / home/lcampassi/Documents \
    -C / home/lcampassi/.config \
    -C / home/lcampassi/scripts

# Rotación: eliminar backups más viejos que RETENTION_DAYS
find "$BACKUP_DEST" -name "home-*.tar.zst" -mtime "+${RETENTION_DAYS}" -delete

# Verificar integridad
tar --zstd -tf "$BACKUP_FILE" > /dev/null 2>&1
if [[ $? -eq 0 ]]; then
    info "Backup verificado: OK"
else
    error "Backup corrupto!"
    exit 1
fi
```

### Cleanup jobs

```bash
#!/bin/bash
# ~/scripts/cleanup.sh — Limpieza de temporales y cachés
set -euo pipefail

declare -a TARGETS=(
    "${HOME}/.cache/*"
    "${HOME}/tmp/*"
    "${HOME}/Downloads/*.tmp"
    "/tmp/*"
)

for pattern in "${TARGETS[@]}"; do
    count=$(find "$(dirname "$pattern")" -name "$(basename "$pattern")" 2>/dev/null | wc -l)
    if [[ "$count" -gt 0 ]]; then
        info "Limpiando: ${pattern} (${count} archivos)"
        find "$(dirname "$pattern")" -name "$(basename "$pattern")" -mtime +7 -delete
    fi
done

# Vaciar trash
if command -v trash-empty &>/dev/null; then
    trash-empty 30
    info "Trash vaciado (retención 30 días)"
fi

# Docker cleanup (si corre)
if command -v docker &>/dev/null; then
    docker system prune -f --filter "until=24h" 2>/dev/null || true
fi
```

### Health checks

```bash
#!/bin/bash
# ~/scripts/health-check.sh — Verificación del sistema
set -euo pipefail

FAILURES=0
REPORT=""

check_service() {
    local service="$1"
    if systemctl --user is-active --quiet "$service" 2>/dev/null; then
        info "✓ $service activo"
    else
        warn "✗ $service inactivo"
        FAILURES=$((FAILURES + 1))
        REPORT="${REPORT}\n  - Servicio: $service (inactivo)"
    fi
}

check_disk() {
    local usage
    usage=$(df / | awk 'NR==2 {print $5}' | tr -d '%')
    if [[ "$usage" -gt 90 ]]; then
        warn "Discos: / al ${usage}% !"
        FAILURES=$((FAILURES + 1))
        REPORT="${REPORT}\n  - Disco / al ${usage}%"
    else
        info "Disco / al ${usage}% OK"
    fi
}

check_network() {
    if ping -c1 -W3 1.1.1.1 &>/dev/null; then
        info "Red: conectado"
    else
        warn "Red: sin conexión"
        REPORT="${REPORT}\n  - Sin conexión a internet"
    fi
}

info "=== Health Check ==="
check_disk
check_network
check_service "backup.timer"
check_service "syncthing.service"

if [[ "$FAILURES" -gt 0 ]]; then
    error "Health check: ${FAILURES} fallo(s) —${REPORT}"
    notify-send -u critical "Health check" "${FAILURES} fallos detectados"
    exit 1
else
    info "Health check: TODO OK"
fi
```

### Notification script (notify-send + webhook)

```bash
#!/bin/bash
# ~/scripts/notify.sh
NOTIFY_WEBHOOK="${NOTIFY_WEBHOOK:-https://hooks.example.com/alert}"

send_notification() {
    local subject="$1" body="$2" urgency="${3:-normal}"

    # Desktop notification
    notify-send -u "$urgency" "$subject" "$body"

    # Webhook (JSON)
    if [[ -n "$NOTIFY_WEBHOOK" ]]; then
        curl -s -X POST "$NOTIFY_WEBHOOK" \
            -H "Content-Type: application/json" \
            -d "{\"subject\": \"$subject\", \"body\": \"$body\", \"host\": \"$(hostname)\"}" \
            &>/dev/null || true
    fi
}

send_notification "Backup completado" "Backup diario finalizado OK" "low"
```

---

## Herramientas por plataforma

### Linux (Arch)

| Herramienta | Propósito | Comando |
|-------------|-----------|---------|
| **systemd timers** | Tareas programadas (reemplazo de cron) | `systemctl --user list-timers` |
| **cron/anacron** | Compatibilidad clásica, equipos no 24/7 | `crontab -e` |
| **journald** | Logging centralizado de servicios | `journalctl -u servicio` |
| **notify-send** | Notificaciones desktop (libnotify) | `notify-send "Título" "Cuerpo"` |
| **at** | Ejecución única en el tiempo | `echo "comando" | at now + 1 hour` |
| **logrotate** | Rotación de logs del sistema | `logrotate /etc/logrotate.conf` |

### Windows 11

| Herramienta | Propósito | Comando/Acceso |
|-------------|-----------|----------------|
| **Task Scheduler** | GUI de tareas programadas | `taskschd.msc` |
| **PowerShell Scheduled Tasks** | Creación programática | `Register-ScheduledTask` |
| **schtasks.exe** | CLI clásica (CMD) | `schtasks /create /tn "Tarea" /tr ...` |
| **Event Viewer** | Logs del sistema | `eventvwr.msc` |
| **BurntToast** | Notificaciones toast PowerShell | `New-BurntToastNotification` |
| **Task Scheduler Scripting** | COM objects desde scripts | `$sch = New-Object -ComObject Schedule.Service` |

### Ejemplo schtasks.exe (CMD)

```cmd
schtasks /create /tn "BackupDiario" /tr "powershell.exe -File C:\Scripts\backup.ps1" /sc daily /st 03:00 /ru SYSTEM /rl HIGHEST
```

### BurntToast (notificaciones Windows)

```powershell
Install-Module -Name BurntToast -Force
New-BurntToastNotification -Text "Backup completado", "Backup diario finalizado OK" -AppLogo C:\icons\ok.png
```

### Equivalencias cross-platform

| Acción | Linux | Windows |
|--------|-------|---------|
| Programar tarea diaria | systemd timer / cron | `Register-ScheduledTask -Daily` |
| Ver logs de tarea | `journalctl -u servicio` | `Get-WinEvent -LogName Microsoft-Windows-TaskScheduler/Operational` |
| Notificar al usuario | `notify-send` | `New-BurntToastNotification` |
| Ejecutar script al boot | systemd service + `Wants=network-online.target` | Task trigger `AtStartup` |
| Ver tareas activas | `systemctl --user list-timers` | `Get-ScheduledTask \| Where State -eq Ready` |

---

## Buenas prácticas generales

1. **Toda tarea automatizada debe tener logging** — sin logging no hay debugging
2. **Usar timers persistentes o anacron** en equipos que no están 24/7
3. **Idempotencia siempre** — ejecutar N veces debe ser seguro
4. **Notificar fallos** — si el script falla silenciosamente, no existe
5. **Probar manualmente antes de programar** — ejecutar el `.service` o el script directo antes de asociarlo a un timer
6. **Documentar cada tarea** — en el crontab o en los comentarios del timer/service
7. **Timeout en scripts** — usar `timeout 3600 ./script.sh` para evitar procesos zombies
8. **Lockfiles** para evitar ejecución concurrente del mismo script
9. **Rotación de logs** — los logs sin rotation llenan el disco
10. **Versionar los scripts** — mantener los scripts en git (tu dotfiles repo)
