---
name: windows-manager
description: Use when managing Windows 11 system — services, packages, processes, disk, network, security, WSL, performance. Provides full Windows system context.
---

# Windows 11 System Manager

## System Context

- **OS:** Microsoft Windows 11 Pro
- **Build:** 10.0.26200 (Insider Preview / Release Preview)
- **Edition:** Windows 11 Pro
- **CPU:** AMD Ryzen 7 5825U (8 cores, 16 threads)
- **GPU:** AMD Radeon Graphics (integrated)
- **RAM:** 22.8 GB
- **Storage:**
  - `C:` — Micron MTFDKCD512TFK (512 GB SSD) — OS
  - `D:` — KINGSTON SNV2S1000G (1 TB SSD) — Data
- **Dual Boot:** Windows 11 + Arch Linux (systemd-boot)

### Important Paths

| Resource | Path |
|---|---|
| Vault Obsidian | `$BABILONIA` (se resuelve por SO desde `~/.zshenv`) |
| Windows docs in vault | dentro de `$BABILONIA` |
| MY-AGENT-SKILLS | `$HOME/MY-AGENT-SKILLS` (o `%USERPROFILE%\MY-AGENT-SKILLS` en Windows) |
| Dotfiles (git) | `$DOTFILES` (en Linux; en Windows usa `git clone` donde corresponda) |
| PROGRESS.md | `%USERPROFILE%\Downloads\opencode\windows-progress.md` |
| Temp dir | `%TEMP%\opencode` |

---

## 1. Package Management (winget)

```powershell
# Search
winget search <term>

# Install
winget install <id>

# List installed (may need --accept-source-agreements first)
winget list

# Upgrade
winget upgrade --all
winget upgrade <id>

# Uninstall
winget uninstall <id>

# Export/Import
winget export -o packages.json
winget import -i packages.json
```

---

## 2. Service Management

```powershell
# List all services
Get-Service

# Filter by status
Get-Service | Where-Object Status -eq 'Running'
Get-Service | Where-Object StartType -eq 'Automatic'

# Get specific service
Get-Service <name>
Get-Service <pattern>*   # wildcard

# Start/Stop/Restart
Start-Service <name>
Stop-Service <name>
Restart-Service <name>

# Set startup type
Set-Service -Name <name> -StartupType Automatic
Set-Service -Name <name> -StartupType Manual
Set-Service -Name <name> -StartupType Disabled

# Legacy sc.exe (useful for some services)
sc.exe query <name>
sc.exe config <name> start=auto
```

---

## 3. Process Management

```powershell
# List processes
Get-Process
Get-Process | Sort-Object CPU -Descending | Select -First 10
Get-Process | Sort-Object WorkingSet64 -Descending | Select -First 10

# Find specific process
Get-Process -Name <name>
Get-Process | Where-Object Name -like '*<pattern>*'

# Kill process
Stop-Process -Name <name>
Stop-Process -Id <pid>

# Process details
Get-Process -Id <pid> | Select-Object *
```

---

## 4. Disk & Volume Management

```powershell
# List volumes
Get-Volume
Get-PSDrive -PSProvider FileSystem

# Disk info
Get-PhysicalDisk
Get-Disk

# Partition info
Get-Partition

# Disk usage
Get-WmiObject Win32_LogicalDisk | Select-Object DeviceID, @{N='SizeGB';E={[math]::Round($_.Size/1GB,2)}}, @{N='FreeGB';E={[math]::Round($_.FreeSpace/1GB,2)}}

# Check disk health
Get-PhysicalDisk | Select FriendlyName, HealthStatus, OperationalStatus

# TRIM (optimize SSD)
Optimize-Volume -DriveLetter C -ReTrim -Verbose
Optimize-Volume -DriveLetter D -ReTrim -Verbose

# CHKDSK (read-only first)
chkdsk C:
chkdsk D:

# Clean disk (cleanmgr)
cleanmgr /sageset:1   # configure
cleanmgr /sagerun:1   # run
```

---

## 5. Network Management

```powershell
# Network adapters
Get-NetAdapter
Get-NetAdapter | Where-Object Status -eq 'Up'

# IP configuration
Get-NetIPAddress -AddressFamily IPv4
Get-NetIPConfiguration

# Legacy
ipconfig /all
ipconfig /flushdns
ipconfig /release
ipconfig /renew

# DNS cache
Clear-DnsClientCache
Get-DnsClientCache

# Network connections
Get-NetTCPConnection
Get-NetUDPEndpoint

# WiFi profiles
netsh wlan show profiles
netsh wlan show profile name="<SSID>" key=clear

# Firewall rules
Get-NetFirewallRule | Where-Object Enabled -eq 'True' | Select DisplayName, Direction, Action
New-NetFirewallRule -DisplayName "<name>" -Direction Inbound -Protocol TCP -LocalPort <port> -Action Allow
Remove-NetFirewallRule -DisplayName "<name>"
```

---

## 6. Windows Update

```powershell
# Check for updates (built-in)
Get-WUInstall -MicrosoftUpdate -AcceptAll -AutoReboot

# List pending updates
Get-WUList -MicrosoftUpdate

# Install updates
Install-WUUpdates -Updates $(Get-WUList -MicrosoftUpdate)

# Note: PSWindowsUpdate module may need install first:
# Install-Module PSWindowsUpdate
```

---

## 7. Windows Security (Defender)

```powershell
# Get Defender status
Get-MpComputerStatus
Get-MpPreference

# Scan
Start-MpScan -ScanType QuickScan
Start-MpScan -ScanType FullScan

# Update signatures
Update-MpSignature

# Add exclusion
Add-MpPreference -ExclusionPath "C:\path\to\exclude"
Add-MpPreference -ExclusionExtension ".ext"

# Remove exclusion
Remove-MpPreference -ExclusionPath "C:\path\to\exclude"

# Real-time monitoring
Set-MpPreference -DisableRealtimeMonitoring $false
Set-MpPreference -DisableRealtimeMonitoring $true
```

---

## 8. Event Logs

```powershell
# List available logs
Get-WinEvent -ListLog * | Where-Object RecordCount -gt 0

# Get recent errors
Get-WinEvent -LogName System -MaxEvents 50 | Where-Object LevelDisplayName -eq 'Error'
Get-WinEvent -LogName Application -MaxEvents 50

# Filter by time
Get-WinEvent -LogName System -FilterXPath "*[System[TimeCreated[timediff(@SystemTime) <= 86400000]]]"

# Filter by Event ID
Get-WinEvent -LogName System | Where-Object Id -eq 41    # unexpected shutdown
Get-WinEvent -LogName System | Where-Object Id -eq 6008   # unexpected shutdown (old)
Get-WinEvent -LogName Security -MaxEvents 50 | Where-Object Id -eq 4625  # failed login

# Export log
wevtutil epl System C:\temp\system.evtx
```

---

## 9. Registry

```powershell
# Query
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion"
Get-ItemProperty -Path "HKCU:\Control Panel\Desktop"

# Set value
Set-ItemProperty -Path "HKLM:\SOFTWARE\..." -Name "<name>" -Value "<value>"

# Legacy
reg query "HKLM\SOFTWARE\..."
reg add "HKLM\SOFTWARE\..." /v <name> /t REG_DWORD /d <value> /f
```

---

## 10. Performance Monitoring

```powershell
# CPU, Memory, Disk counters
Get-Counter "\Processor(_Total)\% Processor Time"
Get-Counter "\Memory\Available MBytes"
Get-Counter "\LogicalDisk(C:)\% Free Space"

# Resource usage snapshot
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name, CPU, WorkingSet64, Id

# System info
systeminfo

# Tasklist (legacy)
tasklist
tasklist /svc   # show services per process
```

---

## 11. Scheduled Tasks

```powershell
# List tasks
Get-ScheduledTask
Get-ScheduledTask | Where-Object State -eq 'Ready'

# Get task details
Get-ScheduledTask -TaskName "<name>" | Get-ScheduledTaskInfo

# Enable/Disable
Enable-ScheduledTask -TaskName "<name>"
Disable-ScheduledTask -TaskName "<name>"

# Start task
Start-ScheduledTask -TaskName "<name>"
```

---

## 12. WSL (Windows Subsystem for Linux)

```powershell
# Status
wsl --status

# List distros
wsl --list --verbose

# Shutdown all
wsl --shutdown

# Set default distro
wsl --set-default <distro>

# Export/Import distro
wsl --export <distro> <file.tar>
wsl --import <distro> <install-dir> <file.tar>

# Terminate specific distro
wsl --terminate <distro>
```

---

## 13. Startup Programs

```powershell
# Via Task Manager startup tab
Get-CimInstance Win32_StartupCommand | Select Name, Command, Location

# Via registry
Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run"
Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
```

---

## 14. User & System Info

```powershell
# Current user
whoami
[System.Environment]::UserName

# Environment variables
Get-ChildItem Env:
$env:USERPROFILE
$env:TEMP
$env:APPDATA

# System info
systeminfo | Select-String "OS Name","OS Version","System Type","Total Physical Memory"

# Installed programs (registry)
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | Select DisplayName, DisplayVersion, Publisher
Get-ItemProperty HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | Select DisplayName, DisplayVersion, Publisher
```

---

## 15. Proton Drive Sync

```powershell
# Check Proton Drive status (if CLI available)
# Proton Drive syncs automatically via the desktop app
# Manual pause/resume via system tray or:
# Look for Proton Drive process
Get-Process ProtonDrive*

# Sync location (ruta específica del usuario, consultar env vars)
# %USERPROFILE%\Proton Drive\...\My files\
```

---

## 16. Common Troubleshooting

```powershell
# Check disk for errors
chkdsk C: /scan   # online scan (no reboot)
chkdsk C: /f      # offline (requires reboot)

# System File Checker
sfc /scannow

# DISM repair
DISM /Online /Cleanup-Image /CheckHealth
DISM /Online /Cleanup-Image /ScanHealth
DISM /Online /Cleanup-Image /RestoreHealth

# Reset network stack
netsh int ip reset
netsh winsock reset
ipconfig /flushdns

# Clear temp files
Remove-Item "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue

# Restart Windows Explorer (fix UI issues)
Stop-Process -Name explorer -Force
# Explorer auto-restarts

# Power efficiency report
powercfg /energy
powercfg /batteryreport
```
