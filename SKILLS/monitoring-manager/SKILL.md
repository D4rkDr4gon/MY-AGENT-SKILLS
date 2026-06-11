---
name: monitoring-manager
description: Use when the user asks about system monitoring — health checks, resource metrics, alerting, performance baselines, log monitoring, and automated monitoring loops. Cross-platform (Linux + Windows).
---

# monitoring-manager

## Descripción general

Filosofía de monitoreo **proactiva**: detectar problemas antes de que afecten la operación. El monitoreo **reactivo** es el plan B.

### Qué monitorear

| Categoría | Qué medir | Por qué |
|-----------|-----------|---------|
| CPU | Carga, temperatura, frecuencia | Sobrecalentamiento, throttling |
| RAM | Uso, swap/zram, OOM | Fugas de memoria |
| Disco | Uso, I/O, latencia, SMART | Fallo inminente |
| Red | Throughput, latencia, errores | Congestión, interfaces caídas |
| Servicios | Estado systemd/Windows Services | Servicios críticos caídos |
| Temperatura | CPU, GPU, NVMe, HDD | Throttling térmico |
| Logs | Errores, warning, OOM killer | Diagnóstico temprano |

## System health checks

### Linux

```bash
# CPU
htop                             # Monitor interactivo
mpstat -P ALL 1 3                # Por núcleo
uptime                           # Load average (1/5/15 min)

# RAM
free -ht                         # Total, usado, disponible, swap
vmstat 1 5                       # Memoria, swap, I/O

# Disco
df -h                            # Uso de particiones
df -i                            # Inodos
iostat -xz 1 3                   # I/O detallado

# SMART
sudo smartctl -a /dev/nvme0n1   # Todo SMART
sudo smartctl -H /dev/nvme0n1   # Health summary
sudo nvme smart-log /dev/nvme0n1  # NVMe específico

# Temperatura
sensors                          # lm-sensors — CPU/motherboard
sudo nvme smart-log /dev/nvme0n1  # NVMe incluye temp

# Red
ip -s link                       # Estadísticas por interfaz
ss -tuln                         # Puertos escuchando
ping -c 5 1.1.1.1                # Latencia

# Servicios
systemctl --failed               # Servicios fallados
systemd-analyze blame            # Tiempos de arranque
```

### Windows (PowerShell)

```powershell
# CPU
Get-Counter "\Processor(_Total)\% Processor Time"
Get-Process | Sort-Object CPU -Descending | Select -First 10

# RAM
Get-Counter "\Memory\Available MBytes"
Get-Process | Sort-Object WorkingSet -Descending | Select -First 10

# Disco
Get-Volume | Format-Table DriveLetter, SizeRemaining, Size
Get-PhysicalDisk | Select FriendlyName, MediaType, HealthStatus

# Red
Get-NetAdapterStatistics | Select Name, ReceivedBytes, SentBytes
Get-NetTCPConnection | Group-Object State | Format-Table Name, Count

# Servicios
Get-Service | Where-Object Status -eq 'Running'
Get-Service | Where-Object Status -eq 'Stopped' | Where-Object StartType -eq Automatic
```

### Interpretación de métricas

| Métrica | Saludable | Atención | Crítico |
|---------|-----------|----------|---------|
| CPU load | < 70% | 70-90% | > 90% sostenido |
| RAM disponible | > 20% | 10-20% | < 10% |
| SWAP/ZRAM uso | < 10% | 10-50% | > 50% |
| Disco uso | < 80% | 80-90% | > 90% |
| Disco I/O wait | < 5% | 5-15% | > 15% |
| Temp CPU | < 70°C | 70-85°C | > 85°C |
| Temp NVMe | < 60°C | 60-75°C | > 75°C |
| SMART Reallocated | 0 | 1-10 | > 10 |

## Resource monitoring

### Tiempo real

| Herramienta | Linux | Windows | Función |
|-------------|-------|---------|---------|
| `btop` | `pacman -S btop` | — | Dashboard TUI completo |
| `htop` | `pacman -S htop` | — | Procesos interactivo |
| `glances` | `pacman -S glances` | `pip install glances` | Dashboard web + TUI |
| `nvtop` | `pacman -S nvtop` | — | Monitor GPU |
| `sensors` | `pacman -S lm_sensors` | HWMonitor | Temperatura |
| Task Manager | — | Ctrl+Shift+Esc | GUI nativa |
| Process Explorer | — | Sysinternals | Árbol de procesos |
| `Get-Counter` | — | PowerShell nativo | Contadores rendimiento |

```bash
# Linux — glances modo servidor
glances -w                       # Web UI en http://localhost:61208
```

### Histórico con sysstat

```bash
sudo systemctl enable --now sysstat
sar -u                           # CPU histórico
sar -r                           # RAM histórico
sar -b                           # I/O histórico
sar -n DEV                       # Red histórico
```

### Windows — PerfMon logging

```powershell
logman create counter monitor -n "SystemHealth" `
  -c "\Processor(_Total)\% Processor Time" "\Memory\Available MBytes" `
  -si 00:00:30 -o "C:\PerfLogs\SystemHealth.blg"
```

## Performance baselines

```bash
# Linux — baseline rápido
#!/bin/bash
OUTPUT="$HOME/monitoring/baseline-$(date +%Y%m%d).txt"
{
  echo "=== CPU ==="; mpstat -P ALL 1 3
  echo "=== RAM ==="; free -h
  echo "=== Disco ==="; df -h | grep -v tmpfs; iostat -x 1 3
  echo "=== Temperatura ==="; sensors -u | grep temp
  echo "=== SMART ==="; sudo nvme smart-log /dev/nvme0n1
} > "$OUTPUT"
```

```powershell
# Windows — baseline
$output = "$env:USERPROFILE\monitoring\baseline-$(Get-Date -Format yyyyMMdd).txt"
@"
CPU: $(Get-CimInstance Win32_Processor | Select Name, MaxClockSpeed | Format-Table | Out-String)
RAM: $(Get-CimInstance Win32_OperatingSystem | Select TotalVisibleMemorySize, FreePhysicalMemory | Format-Table | Out-String)
Disco: $(Get-Volume | Select DriveLetter, SizeRemaining, Size | Format-Table | Out-String)
"@ | Out-File $output
```

### Anomaly detection

```bash
# ~/dotfiles/scripts/health-check.sh
CPU=$(awk '{print $1*100}' /proc/loadavg | cut -d. -f1)
RAM=$(free | awk '/Mem/{printf "%d", $3/$2 * 100}')
DISK=$(df / | awk 'NR==2{print $5}' | tr -d %)
TEMP=$(sensors -u | grep -A1 "temp1_input" | tail -1 | awk '{print $2}' | cut -d. -f1)

[ "$CPU" -gt 80 ] && echo "ALERTA: CPU al ${CPU}%"
[ "$RAM" -gt 85 ] && echo "ALERTA: RAM al ${RAM}%"
[ "$DISK" -gt 90 ] && echo "ALERTA: Disco / al ${DISK}%"
[ "$TEMP" -gt 85 ] && echo "ALERTA: Temperatura ${TEMP}°C"
```

## Alerting

### Linux — notify-send

```bash
notify-send -u critical -t 0 "ALERTA" "CPU al 95%" -i dialog-warning

# Script con niveles
cat << 'EOF' > ~/dotfiles/scripts/alerter.sh
send_alert() {
  local level="$1" title="$2" message="$3"
  local icon="dialog-warning"
  [ "$level" = "critical" ] && icon="dialog-error"
  notify-send -u "$level" "$title" "$message" -i "$icon"
  echo "[$(date)] [$level] $title — $message" >> "$HOME/monitoring/alerts.log"
}
# Uso: send_alert "critical" "🔥 CPU OVERHEAT" "Temp: 92°C"
EOF
```

### Windows — BurntToast / BalloonTip

```powershell
# BurntToast (Install-Module -Name BurntToast -Force)
New-BurntToastNotification -Text "ALERTA", "RAM al 92%" -Silent

# BalloonTip (sin módulos externos)
Add-Type -AssemblyName System.Windows.Forms
$b = New-Object System.Windows.Forms.NotifyIcon
$b.Icon = [System.Drawing.SystemIcons]::Warning
$b.BalloonTipTitle = "ALERTA"
$b.BalloonTipText = "Disco C: al 95%"
$b.Visible = $true
$b.ShowBalloonTip(10000)
```

### Escalation

| Nivel | Condición | Acción |
|-------|-----------|--------|
| Info | Uso > 70% | Log + notify low |
| Warning | Uso > 85% | Notificación normal + log |
| Critical | Uso > 95% | notify critical + sonido |
| Emergency | Servicio caído | Reintentar inicio automático |

## Log monitoring

### Linux — journalctl

```bash
journalctl -p err -b --no-pager              # Errores del boot
journalctl -p crit -b                        # Críticos
journalctl -k -p err                         # Errores kernel
journalctl -u sshd --since "1 hour ago"      # Servicio específico
journalctl --vacuum-size=500M                # Limitar espacio
journalctl -p err -b | grep -i "oom"         # OOM kills
```

### Linux — logwatch (resumen diario)

```bash
sudo pacman -S logwatch
sudo logwatch --detail High --mailto $USER --service All --range yesterday
# Config: /usr/share/logwatch/default.conf/logwatch.conf
```

### Windows — EventLog

```powershell
Get-WinEvent -LogName System -MaxEvents 50 | Where-Object LevelDisplayName -eq 'Error'
Get-WinEvent -LogName System | Where-Object { $_.Id -eq 41 }  # Unexpected shutdown
Get-WinEvent -LogName Application -MaxEvents 100 | Export-Csv C:\PerfLogs\app-logs.csv
```

### Log rotation

```bash
# /etc/logrotate.d/custom-monitoring
$HOME/monitoring/*.log {
    weekly
    rotate 4
    compress
    delaycompress
    missingok
    notifempty
    create 0644 $USER $USER
}
```

## Automated monitoring loops

### Linux — systemd timer (c/5 min)

```bash
# /etc/systemd/system/health-check.service
[Unit]
Description=Health check monitor
[Service]
Type=oneshot
ExecStart=$HOME/dotfiles/scripts/health-check.sh
User=$USER

# /etc/systemd/system/health-check.timer
[Unit]
Description=Ejecuta health check cada 5 minutos
[Timer]
OnCalendar=*:0/5
Persistent=true
[Install]
WantedBy=timers.target

sudo systemctl daemon-reload && sudo systemctl enable --now health-check.timer
```

### Linux — cron

```bash
crontab -e
*/5 * * * * $HOME/dotfiles/scripts/health-check.sh
0 */6 * * * $HOME/dotfiles/scripts/baseline.sh
0 0 * * 0 /usr/bin/logwatch --detail High --mailto lcampassi
```

### Windows — Scheduled Task

```powershell
$action = New-ScheduledTaskAction -Execute "Powershell.exe" `
  -Argument "-File $env:USERPROFILE\dotfiles\scripts\health-check.ps1"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) `
  -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration ([TimeSpan]::MaxValue)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType S4U
Register-ScheduledTask -TaskName "SystemHealthCheck" -Action $action -Trigger $trigger -Principal $principal
```

### Windows — PS Background Job

```powershell
$job = Register-ScheduledJob -Name "MonitorRAM" -ScriptBlock {
  while ($true) {
    $freePct = ((Get-Counter "\Memory\Available MBytes").CounterSamples.CookedValue /
      ((Get-CimInstance Win32_OperatingSystem).TotalVisibleMemorySize / 1MB)) * 100
    if ($freePct -lt 10) {
      Write-EventLog -LogName Application -Source "Monitoring" `
        -EntryType Error -EventId 1001 -Message "RAM crítica: ${freePct}% libre"
    }
    Start-Sleep -Seconds 120
  }
} -Trigger (New-JobTrigger -AtStartup)
```

## Instalación rápida

### Arch Linux

```bash
sudo pacman -S btop htop glances nvtop lm_sensors smartmontools nvme-cli \
  sysstat collectl nethogs iftop iotop logwatch
sudo sensors-detect --auto
sudo systemctl enable --now sysstat
```

### Windows

```powershell
Install-Module -Name BurntToast -Force
Invoke-WebRequest -Uri "https://download.sysinternals.com/files/SysinternalsSuite.zip" `
  -OutFile "$env:TEMP\SysinternalsSuite.zip"
Expand-Archive "$env:TEMP\SysinternalsSuite.zip" -DestinationPath "C:\Tools\Sysinternals"
[Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Tools\Sysinternals", "User")
```
