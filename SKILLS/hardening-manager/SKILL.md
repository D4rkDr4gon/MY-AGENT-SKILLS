---
name: hardening-manager
description: Use when hardening Linux or Windows systems — CIS benchmarks, lynis, OpenSCAP, kernel hardening, SSH hardening, firewall rules, service minimization, AppArmor/SELinux, and security auditing.
---

# hardening-manager

Guía de hardening para sistemas Linux y Windows. Orientada a blue team y administración de sistemas.

## Contexto del usuario

- **Linux:** Arch Linux (systemd, nftables, AppArmor)
- **Windows:** Windows 11 Pro (Windows Defender, Windows Firewall)
- **Propósito:** Hardening de sistemas personales y de laboratorio
- **Herramientas:** `lynis`, `openscap`, `sysctl`, `nft`, `ufw`, `chkrootkit`, `rkhunter`

---

## 1. Lynis — Auditoría de seguridad general

```bash
# Instalar
sudo pacman -S lynis

# Auditoría completa
sudo lynis audit system

# Auditoría sin root (limitada)
lynis audit system

# Ver perfil de hardening
sudo lynis show details

# Reporte HTML
sudo lynis audit system --report-file /tmp/lynis-report.html
```

### Interpretar resultados
```bash
# Puntajes
# 60-69: Mejorable
# 70-79: Aceptable
# 80-89: Bueno
# 90-100: Excelente

# Ver sugerencias
sudo grep "suggestion\|warning" /var/log/lynis.log
sudo lynis show suggestions
```

---

## 2. Hardening de Kernel (sysctl)

```bash
# Ver configuración actual
sudo sysctl -a | grep -E 'net\.ipv4|net\.ipv6|kernel\.(exec-shield|randomize)'

# Hardening básico de red — /etc/sysctl.d/99-hardening.conf
cat > /tmp/99-hardening.conf << 'EOF'
# -- IPv4 Hardening --
net.ipv4.ip_forward = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.secure_redirects = 0
net.ipv4.conf.default.secure_redirects = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_rfc1337 = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.icmp_ignore_bogus_error_responses = 1

# -- IPv6 Hardening --
net.ipv6.conf.all.accept_source_route = 0
net.ipv6.conf.default.accept_source_route = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0
net.ipv6.conf.all.accept_ra = 0
net.ipv6.conf.default.accept_ra = 0

# -- Kernel Hardening --
kernel.kptr_restrict = 2
kernel.dmesg_restrict = 1
kernel.printk = 3 3 3 3
kernel.unprivileged_bpf_disabled = 1
net.core.bpf_jit_harden = 2
kernel.yama.ptrace_scope = 2
kernel.randomize_va_space = 2
kernel.exec-shield = 1
EOF

# Aplicar
sudo cp /tmp/99-hardening.conf /etc/sysctl.d/
sudo sysctl -p /etc/sysctl.d/99-hardening.conf
```

---

## 3. Hardening de servicios systemd

```bash
# Listar servicios activos
systemctl list-units --type=service --state=running

# Servicios comúnmente innecesarios para desktop
sudo systemctl disable --now bluetooth.service     # Si no usás BT
sudo systemctl disable --now cups.service          # Si no imprimís
sudo systemctl disable --now avahi-daemon.service  # mDNS/Bonjour
sudo systemctl mask --now pcscd.service            # Smart card (si no usás)

# Hardening por servicio (override)
sudo systemctl edit sshd
# [Service]
# PrivateTmp=yes
# ProtectSystem=full
# ProtectHome=yes
# NoNewPrivileges=yes
# CapabilityBoundingSet=CAP_NET_BIND_SERVICE
```

---

## 4. Hardening de SSH

```bash
# /etc/ssh/sshd_config — recomendado
cat >> /etc/ssh/sshd_config << 'EOF'
Port 2222                              # Puerto no estándar
PermitRootLogin no
MaxAuthTries 3
MaxSessions 2
PubkeyAuthentication yes
PasswordAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no
UsePAM yes
X11Forwarding no
AllowUsers lcampassi                  # Solo este usuario
ClientAliveInterval 300
ClientAliveCountMax 2
Protocol 2
MACs hmac-sha2-512,hmac-sha2-256
KexAlgorithms curve25519-sha256,diffie-hellman-group-exchange-sha256
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
EOF

# Verificar config antes de reiniciar
sudo sshd -t

# Reiniciar
sudo systemctl restart sshd
```

---

## 5. OpenSCAP — Automatización de benchmarks

```bash
# Instalar
sudo pacman -S openscap

# Escanear contra benchmark CIS
oscap xccdf eval \
  --profile xccdf_org.ssgproject.content_profile_cis \
  --results /tmp/oscap-results.xml \
  --report /tmp/oscap-report.html \
  /usr/share/openscap/ssg-content/ssg-archlinux-ds.xml  # Si existe, o usar genérico

# Para Arch (no hay profile oficial, se puede usar genérico)
oscap xccdf eval \
  --profile xccdf_org.ssgproject.content_profile_cis_server_l1 \
  --results /tmp/oscap-results.xml \
  --report /tmp/oscap-report.html \
  /usr/share/openscap/scap-xccdf.xml
```

---

## 6. AppArmor (Arch Linux)

```bash
# Ver estado
sudo aa-status

# Cargar perfiles
sudo aa-enforce /path/to/profile   # Modo enforce
sudo aa-complain /path/to/profile  # Solo logging

# Perfiles comunes
sudo pacman -S apparmor
sudo systemctl enable --now apparmor

# Generar perfil para un binario
sudo aa-genprof /bin/mi-binary
# Seguir wizard: S (scan), A (allow), D (deny), F (finish)
```

---

## 7. Rootkit detection

```bash
# chkrootkit
sudo pacman -S chkrootkit
sudo chkrootkit

# rkhunter
sudo pacman -S rkhunter
sudo rkhunter --check --skip-keypress

# Actualizar DB de rkhunter antes del scan
sudo rkhunter --update
sudo rkhunter --propupd
```

---

## 8. Hardening de firewall (nftables)

```bash
# Ver reglas actuales
sudo nft list ruleset

# Configuración básica — /etc/nftables.conf
cat > /tmp/nftables.conf << 'EOF'
#!/usr/sbin/nft -f

flush ruleset

table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;
        
        # Loopback
        iif lo accept
        iif != lo ip daddr 127.0.0.0/8 drop
        
        # Conexiones establecidas
        ct state established,related accept
        
        # SSH (puerto personalizado)
        tcp dport 2222 accept
        
        # ICMP limitado
        ip protocol icmp icmp type { echo-request } limit rate 10/second accept
        
        # Log y drop
        log prefix "NFTABLES-DROP: " counter drop
    }
    
    chain forward {
        type filter hook forward priority 0; policy drop;
    }
    
    chain output {
        type filter hook output priority 0; policy accept;
    }
}
EOF

sudo cp /tmp/nftables.conf /etc/
sudo systemctl enable --now nftables

# Verificar reglas
sudo nft list ruleset
```

---

## 9. Windows Hardening

### Windows Defender
```powershell
# Ver estado
Get-MpComputerStatus

# Configurar proteccion en tiempo real
Set-MpPreference -EnableRealtimeMonitoring $true
Set-MpPreference -PUAProtection Enabled
Set-MpPreference -CloudBlockLevel High
Set-MpPreference -CloudTimeout 50
Set-MpPreference -SubmitSamplesConsent Always

# Exclusiones (solo si necesario)
Add-MpPreference -ExclusionPath "C:\lab\"
Add-MpPreference -ExclusionExtension ".vhd"

# Escaneo rápido
Start-MpScan -ScanType QuickScan
Start-MpScan -ScanType FullScan

# Exploit Guard
Set-ProcessMitigation -System -Enable DEP,SEHOP,ForceRelocateImages
Set-ProcessMitigation -Name cmd.exe -Enable BlockLowLabel
```

### Windows Firewall
```powershell
# Bloquear todo entrante por defecto
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
Set-NetFirewallProfile -DefaultInboundAction Block

# Permitir solo lo necesario
New-NetFirewallRule -DisplayName "SSH" -Direction Inbound -Protocol TCP -LocalPort 2222 -Action Allow

# Logging
Set-NetFirewallProfile -LogFileName "%SystemRoot%\System32\LogFiles\Firewall\pfirewall.log" -LogMaxSize 4096
```

### Windows Services (hardening)
```powershell
# Deshabilitar servicios innecesarios
Set-Service -Name RemoteRegistry -StartupType Disabled
Set-Service -Name RemoteDesktopConfiguration -StartupType Disabled  # Si no usás RDP

# Ver servicios con riesgo
Get-Service | Where-Object {$_.StartType -eq "Automatic" -and $_.Status -eq "Running"} | Select Name,DisplayName
```

### Windows Update
```powershell
# Forzar actualizaciones
Install-Module -Name PSWindowsUpdate -Force
Get-WUInstall -MicrosoftUpdate -AcceptAll -AutoReboot
```

---

## 10. Buenas prácticas

1. **Principio de mínimo privilegio** — cada servicio/usr con solo lo que necesita
2. **Menos superficie** — deshabilitar servicios no necesarios (cups, bluetooth, avahi)
3. **Firewall por defecto deny** — bloquear todo lo entrante, permitir explícitamente
4. **Actualizaciones al día** — `sudo pacman -Syu` semanal, Windows Update automático
5. **Auditar periódicamente** — lynis semanal, oscap mensual
6. **No ejecutar como root** — usar sudo con configuración restrictiva
7. **Logs centralizados** — journalctl persistente + forwarded a SIEM si aplica
8. **Hardening de SSH ante todo** — es la puerta de entrada principal
9. **AppArmor/SELinux** — perfiles para servicios críticos (nginx, sshd, docker)
10. **Documentar cambios** — qué se hardenizó y por qué (en Obsidian)
