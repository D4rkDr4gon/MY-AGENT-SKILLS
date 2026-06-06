---
name: homelab-manager
description: Use when managing pentesting homelab — VMs (KVM/VirtualBox), snapshots, networking, HTB/THM tracking, VulnHub, writeups. Cross-platform (Arch Linux + Windows 11).
---

# Homelab Manager

Guía integral para la gestión del laboratorio de pentesting de **Lucciano Campassi (D4rkDr4g0n)**.

## Descripción general

El homelab está diseñado para tres propósitos principales:

| Propósito | Descripción | Plataformas |
|-----------|-------------|-------------|
| **Pentesting practice** | Máquinas HTB, THM, VulnHub para práctica ofensiva | Arch Linux |
| **Malware analysis** | Sandbox aislado para análisis de muestras | Arch Linux (KVM) |
| **Development testing** | Entornos de prueba para exploits, scripts, herramientas | Linux + Windows |

### Estructura de directorios

```
~/lab/
├── htb/              # Máquinas de Hack The Box
├── thm/              # Máquinas de TryHackMe
├── vulnhub/          # Máquinas VulnHub offline
├── vpn/              # Perfiles OpenVPN
├── vms/              # Discos e imágenes de VMs
├── writeups/         # Writeups de máquinas resueltas
├── tools/            # Herramientas y scripts propios
└── shares/           # Directorios compartidos entre host y VMs
```

### Cross-platform

| Recurso | Linux (Arch) | Windows 11 |
|---------|-------------|------------|
| Hypervisor | KVM/QEMU + libvirt | VirtualBox / Hyper-V (ocasional) |
| CLI | `virsh`, `virt-install`, `VBoxManage` | `VBoxManage.exe` |
| GUI | `virt-manager` | VirtualBox GUI |
| Snapshots | `virsh snapshot-*` | `VBoxManage snapshot` |
| Redes | `virsh net-*` | `VBoxManage natnetwork` / Hyper-V Switch |

---

## Gestión de VMs

### KVM / libvirt (Arch Linux — primario)

#### Crear VM con virt-install

```bash
# VM Linux básica
virt-install \
  --name debian-lab \
  --ram 2048 \
  --vcpus 2 \
  --disk path=/var/lib/libvirt/images/debian-lab.qcow2,size=20 \
  --os-variant debian12 \
  --network network=default \
  --graphics vnc,listen=0.0.0.0 \
  --cdrom /home/lcampassi/iso/debian-12.iso

# VM Windows (con drivers virtio)
virt-install \
  --name win10-lab \
  --ram 4096 \
  --vcpus 4 \
  --disk path=/var/lib/libvirt/images/win10-lab.qcow2,size=60 \
  --disk path=/home/lcampassi/iso/virtio-win.iso,device=cdrom \
  --os-variant win10 \
  --network network=isolated-lab \
  --graphics spice \
  --cdrom /home/lcampassi/iso/Win10.iso
```

#### Gestión con virsh

```bash
# Listar VMs
virsh list --all

# Iniciar / apagar / reiniciar
virsh start <vm-name>
virsh shutdown <vm-name>
virsh reboot <vm-name>
virsh destroy <vm-name>          # Forzar apagado

# Conectar por consola (serial)
virsh console <vm-name>

# Información detallada
virsh dominfo <vm-name>
virsh vcpuinfo <vm-name>
virsh dommemstat <vm-name>

# Editar configuración XML
virsh edit <vm-name>

# Clonar VM
virt-clone --original debian-lab --name debian-lab-clone --auto-clone

# Migrar a otro host (cold migration)
virsh migrate --offline --persistent <vm> qemu+ssh://<host>/system
```

#### Plantilla de VM para pentesting (XML snippet)

Configuración recomendada para máquinas de ataque (Kali/Parrot):

```bash
# Crear VM con especificaciones de ataque
virt-install \
  --name kali-lab \
  --ram 4096 \
  --vcpus 4 \
  --disk path=/var/lib/libvirt/images/kali-lab.qcow2,size=40,bus=virtio \
  --os-variant linux2022 \
  --network network=lab-net \
  --graphics spice \
  --video virtio \
  --sound none \
  --channel unix,target_type=virtio,name=org.qemu.guest_agent \
  --cdrom /home/lcampassi/iso/kali-linux.iso
```

#### Template XML personalizado

```xml
<!-- /etc/libvirt/qemu/templates/pentest-vm.xml -->
<domain type='kvm'>
  <name>pentest-vm</name>
  <memory unit='GiB'>4</memory>
  <vcpu placement='static'>4</vcpu>
  <os>
    <type arch='x86_64' machine='pc-q35-8.0'>hvm</type>
  </os>
  <features>
    <acpi/><apic/><hyperv>
      <relaxed state='on'/>
      <vapic state='on'/>
    </hyperv>
  </features>
  <cpu mode='host-passthrough'/>
  <devices>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='/var/lib/libvirt/images/pentest-vm.qcow2'/>
      <target dev='vda' bus='virtio'/>
    </disk>
    <interface type='network'>
      <source network='lab-net'/>
      <model type='virtio'/>
    </interface>
    <graphics type='spice' port='-1' autoport='yes'/>
    <video><model type='virtio'/></video>
  </devices>
</domain>
```

### VirtualBox (Linux + Windows)

#### Comandos VBoxManage

```bash
# Crear VM desde CLI
VBoxManage createvm --name "Win10-Analysis" --ostype Windows10_64 --register

# Asignar recursos
VBoxManage modifyvm "Win10-Analysis" --memory 4096 --cpus 2 --vram 128

# Crear disco
VBoxManage createmedium disk --filename "$HOME/VirtualBox VMs/Win10-Analysis/Win10-Analysis.vdi" --size 51200

# Agregar controlador SATA y attach disco
VBoxManage storagectl "Win10-Analysis" --name SATA --add sata --controller IntelAhci
VBoxManage storageattach "Win10-Analysis" --storagectl SATA --port 0 --device 0 --type hdd --medium "$HOME/VirtualBox VMs/Win10-Analysis/Win10-Analysis.vdi"

# Agregar ISO
VBoxManage storageattach "Win10-Analysis" --storagectl SATA --port 1 --device 0 --type dvddrive --medium "$HOME/iso/Win10.iso"

# Configurar red
VBoxManage modifyvm "Win10-Analysis" --nic1 natnetwork --nat-network1 "lab-net"

# Iniciar VM (headless)
VBoxManage startvm "Win10-Analysis" --type headless

# Listar VMs
VBoxManage list vms
VBoxManage list runningvms

# Apagar / guardar estado
VBoxManage controlvm "Win10-Analysis" acpipowerbutton
VBoxManage controlvm "Win10-Analysis" savestate

# Información
VBoxManage showvminfo "Win10-Analysis" | less
```

#### En Windows (PowerShell)

```powershell
# Los mismos comandos anteponiendo la ruta si no está en PATH
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" list vms

# O si está en PATH:
VBoxManage list runningvms
```

---

## Snapshots y rollbacks

### KVM / libvirt

Los snapshots en KVM pueden ser **disk-only** (solo disco) o **full system** (disco + RAM + estado de devices).

```bash
# Crear snapshot (disk-only, sin RAM)
virsh snapshot-create-as debian-lab \
  --name "clean-install" \
  --description "Estado post-instalación limpia"

# Crear snapshot con estado completo de RAM
virsh snapshot-create-as win10-lab \
  --name "ready-with-tools" \
  --description "VM lista con herramientas instaladas" \
  --atomic

# Listar snapshots
virsh snapshot-list debian-lab

# Ver detalles de un snapshot
virsh snapshot-info debian-lab --snapshotname clean-install
virsh snapshot-dumpxml debian-lab --snapshotname clean-install

# Revertir a snapshot (VM debe estar apagada o usarla --force si running)
virsh snapshot-revert debian-lab --snapshotname clean-install
virsh snapshot-revert debian-lab --snapshotname clean-install --running  # Reanudar tras revert

# Eliminar snapshot
virsh snapshot-delete debian-lab --snapshotname clean-install
virsh snapshot-delete debian-lab --snapshotname clean-install --children  # Con hijos

# Flujo típico de rollback (máquina comprometida)
# 1. Apagar VM comprometida
virsh destroy vulnerable-vm
# 2. Revertir al último snapshot limpio
virsh snapshot-revert vulnerable-vm --snapshotname "pre-exploit"
# 3. Re-iniciar
virsh start vulnerable-vm
```

#### Disk-only vs Full system

| Tipo | Contenido | Tamaño | Velocidad | Uso típico |
|------|-----------|--------|-----------|------------|
| Disk-only | Solo disco (qcow2) | Pequeño | Rápido | Snapshots frecuentes, bajo espacio |
| Full system | Disco + RAM + device state | Grande (RAM incluida) | Lento | Estado exacto pre-exploit (con procesos en memoria) |

Para snapshots de malware analysis, **siempre usar disk-only** — el estado completo puede consumir
GBs innecesariamente.

### VirtualBox

```bash
# Crear snapshot
VBoxManage snapshot "Kali-Lab" take "base-install" --description "Kali recién instalado"

VBoxManage snapshot "Kali-Lab" take "with-tools" --description "Con nmap, metasploit, burp"

# Listar snapshots
VBoxManage snapshot "Kali-Lab" list
VBoxManage snapshot "Kali-Lab" list --details

# Restaurar snapshot
VBoxManage snapshot "Kali-Lab" restore "base-install"

# Restaurar snapshot actual (sin nombrarlo)
VBoxManage snapshot "Kali-Lab" restorecurrent

# Eliminar snapshot
VBoxManage snapshot "Kali-Lab" delete "with-tools"

# Flujo: restaurar y arrancar en un solo comando
VBoxManage snapshot "Kali-Lab" restore "base-install" && \
VBoxManage startvm "Kali-Lab" --type headless
```

#### En Windows (PowerShell)

```powershell
VBoxManage snapshot "Win10-Analysis" take "clean-tools-installed"
VBoxManage snapshot "Win10-Analysis" list --details
VBoxManage snapshot "Win10-Analysis" restore "clean-tools-installed"
```

### Estrategia de snapshots para pentesting

1. **Base install** — SO recién instalado + updates
2. **Tools** — Herramientas de pentesting instaladas (nmap, metasploit, burp, etc.)
3. **Pre-exploit** — Antes de atacar una máquina específica (punto de rollback si algo sale mal)
4. **Post-exploit** — Después de obtener acceso (para preservar el estado del compromiso)

---

## Redes de laboratorio

### Conceptos

| Tipo de red | Descripción | Caso de uso |
|-------------|-------------|-------------|
| **NAT** | VMs comparten IP del host, salida a internet | VMs que necesitan internet para updates |
| **Bridged** | VM en la misma subred que el host | Servicios expuestos en LAN, co-pentesting |
| **Host-only** | VM solo se comunica con el host | Aislamiento total, malware analysis |
| **Internal** | VMs se comunican entre sí pero no con host ni internet | Red de laboratorio aislada |

### Redes KVM (libvirt)

```bash
# Listar redes definidas
virsh net-list --all

# Información de una red
virsh net-info default
virsh net-dumpxml default

# Red NAT por defecto (192.168.122.0/24)
# Ya creada al instalar libvirt, las VMs tienen salida a internet

# Crear red interna aislada (sin NAT, sin DHCP)
cat > /tmp/isolated-lab.xml << 'EOF'
<network>
  <name>isolated-lab</name>
  <forward mode='none'/>
  <bridge name='virbr1' stp='on' delay='0'/>
  <ip address='10.10.0.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='10.10.0.10' end='10.10.0.100'/>
    </dhcp>
  </ip>
</network>
EOF

virsh net-define /tmp/isolated-lab.xml
virsh net-start isolated-lab
virsh net-autostart isolated-lab

# Crear red host-only (solo comunicación con host)
cat > /tmp/hostonly-lab.xml << 'EOF'
<network>
  <name>hostonly-lab</name>
  <forward mode='nat'/>
  <bridge name='virbr2' stp='on' delay='0'/>
  <ip address='10.10.1.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='10.10.1.10' end='10.10.1.100'/>
    </dhcp>
  </ip>
</network>
EOF

virsh net-define /tmp/hostonly-lab.xml
virsh net-start hostonly-lab

# Conectar VM a una red específica
virsh attach-interface debian-lab --type network --source isolated-lab --config --live

# Desconectar interfaz
virsh detach-interface debian-lab --type network --mac 52:54:00:xx:xx:xx --config
```

### Redes VirtualBox

```bash
# NAT por defecto (la VM sale a internet automáticamente)

# Host-only
VBoxManage hostonlyif create
VBoxManage hostonlyif ipconfig vboxnet0 --ip 192.168.56.1 --netmask 255.255.255.0
VBoxManage modifyvm "Kali-Lab" --nic2 hostonly --hostonlyadapter2 vboxnet0

# Internal network (solo VMs, sin host)
VBoxManage modifyvm "Target-VM" --nic3 intnet --intnet3 "pentest-net"

# NAT network (red NAT completa sin depender del host)
VBoxManage natnetwork add --netname "lab-net" --network "10.10.0.0/24" --enable
VBoxManage natnetwork start --netname "lab-net"
VBoxManage modifyvm "Kali-Lab" --nic1 natnetwork --nat-network1 "lab-net"
VBoxManage modifyvm "Target-VM" --nic1 natnetwork --nat-network1 "lab-net"

# Port forwarding (NAT network)
VBoxManage natnetwork modify --netname "lab-net" \
  --port-forward-4 "ssh:tcp:[127.0.0.1]:2222:10.10.0.10:22"
```

### Routing entre VMs

Para que VMs en diferentes redes se comuniquen:

```bash
# En el host, habilitar IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1
# Persistente: descomentar net.ipv4.ip_forward=1 en /etc/sysctl.d/99-sysctl.conf

# Agregar rutas estáticas en la VM de ataque
ip route add 10.10.2.0/24 via 10.10.0.1
```

---

## HTB / THM Tracking

### Estructura de tracking

Las máquinas se trackean en `~/lab/<plataforma>/<maquina>/` con la siguiente estructura:

```
~/lab/htb/Atomic/
├── notes.md         # Notas de reconocimiento y explotación
├── flags.txt        # Flags encontradas (user/root)
├── walkthrough.md   # Writeup completo
├── scans/           # Outputs de nmap, gobuster, etc.
│   ├── nmap-inicial.txt
│   ├── nmap-full.txt
│   └── gobuster.txt
├── loot/            # Evidencia (screenshots, hashes, shells)
├── exploits/        # Scripts/exploits usados
└── .status          # Estado actual
```

### Template de estado

```
Máquina:   <nombre>
Plataforma: HTB | THM | VulnHub
OS:        Linux | Windows | BSD | Other
Dificultad: Easy | Medium | Hard | Insane
IP:        <target_ip>
Estado:    Recon | Foothold | User | Root | Writeup | Retired

User flag:  <hash> | encontrada en <path>
Root flag:  <hash> | encontrada en <path>

Vector inicial: <servicio/exploit usado>
Lateral:        <técnica de movimiento lateral (si aplica)>
Escalada:       <técnica de escalada de privilegios>

Herramientas: nmap, gobuster, metasploit, burp, ...
Tags:         sqli, rce, kernel-exploit, ...
```

### Automatización de setup para nueva máquina

```bash
# Script para crear estructura de una nueva máquina HTB/THM
setup_machine() {
    local platform="$1"
    local machine="$2"
    local ip="$3"

    mkdir -p ~/lab/$platform/$machine/{scans,loot,exploits}
    echo "Máquina: $machine" > ~/lab/$platform/$machine/notes.md
    echo "IP: $ip" >> ~/lab/$platform/$machine/notes.md
    echo "Estado: Recon" >> ~/lab/$platform/$machine/.status
    echo "Estructura creada en ~/lab/$platform/$machine/"
    echo "Target: $ip"
}

# Uso: setup_machine "htb" "Atomic" "10.10.10.147"
```

---

## Lab documentation

Las notas del laboratorio se almacenan en la bóveda de Obsidian:

| Plataforma | Ruta en Obsidian (Linux) | Ruta en Obsidian (Windows) |
|------------|-------------------------|---------------------------|
| HTB | `Personal-Vault/HTB/<Maquina>/` | `Personal-Vault\HTB\<Maquina>\` |
| THM | `Personal-Vault/THM/<Maquina>/` | `Personal-Vault\THM\<Maquina>\` |
| VulnHub | `Personal-Vault/VulnHub/<Maquina>/` | `Personal-Vault\VulnHub\<Maquina>\` |
| General | `Personal-Vault/Lab/Notas/` | `Personal-Vault\Lab\Notas\` |

### Template de nota Obsidian

```markdown
---
machine: <nombre>
platform: HTB | THM | VulnHub
os: <os>
difficulty: <dificultad>
completed: <fecha>
tags: [pentesting, <tags>]
---

# <Nombre de la máquina>

## Reconocimiento

- IP: `10.10.x.x`
- Puertos abiertos: `22, 80, 443`

## Enumeración

```nmap
# nmap -sC -sV -oN scans/nmap-inicial.txt <IP>
...
```

## Explotación

### Vector de entrada
...

### Shell de baja privilegiada
...

## Escalada de privilegios

### User -> Root
...

## Flags
- **User**: `hash`
- **Root**: `hash`

## Resumen
Breve resumen de la máquina.
```

---

## Offline labs

### VulnHub

Las máquinas VulnHub se descargan como `.ova` u `.iso` y se importan localmente:

```bash
# Importar OVA a VirtualBox
VBoxManage import ~/lab/vulnhub/Kioptrix-Level-1/Kioptrix.ova

# Importar OVA a KVM (convertir primero)
qemu-img convert -O qcow2 Kioptrix-disk1.vmdk kioptrix.qcow2
virt-install --name kioptrix --ram 512 --vcpus 1 \
  --disk path=kioptrix.qcow2,format=qcow2 \
  --import --os-variant linux2022 \
  --network network=isolated-lab

# Máquina ya con disco (sin ISO)
virt-install --name metasploitable2 --ram 1024 --vcpus 1 \
  --disk path=/var/lib/libvirt/images/metasploitable2.qcow2,format=qcow2 \
  --import --os-variant ubuntu18.04 \
  --network network=isolated-lab --graphics none
```

### Catálogo de máquinas offline

| Máquina | Propósito | Tipo | Dificultad |
|---------|-----------|------|------------|
| Metasploitable 2 | Práctica de exploits básicos | Linux | Easy |
| Metasploitable 3 | Explotación Windows | Windows | Medium |
| DVWA | Web app pentesting | Linux (LAMP) | Easy |
| Kioptrix series | Escalada de privilegios | Linux | Easy-Medium |
| VulnOS 2 | OSCP-style enumeration | Linux | Medium |
| SickOs 1.2 | CTO enumeration | Linux | Medium |
| DC-1 a DC-9 | Wordpress/Drupal recon | Linux | Medium |
| Mr-Robot | Web + privesc | Linux | Medium |

### Recomendaciones de red para offline labs

- Conectar todas las VMs offline a la red **`isolated-lab`** (sin salida a internet)
- La VM de ataque (Kali) y la VM objetivo deben estar en la misma red interna
- Desde Kali, atacar a la IP de la VM objetivo directamente
- No exponer las VMs vulnerables a la LAN física

```bash
# Verificar conectividad entre VMs en red aislada
# Desde la VM de ataque:
ping -c 2 10.10.0.20    # IP de la VM objetivo
nmap -sn 10.10.0.0/24   # Descubrir VMs en la red
```

---

## Writeup automation

### Template markdown para writeups

```markdown
# <Nombre Máquina> — Writeup

## Información general

| Campo | Valor |
|-------|-------|
| Máquina | `<nombre>` |
| Plataforma | `HTB` / `THM` / `VulnHub` |
| OS | `Linux` / `Windows` |
| Dificultad | `Easy` / `Medium` / `Hard` / `Insane` |
| IP | `10.10.x.x` |
| Fecha | `2025-01-15` |
| Tiempo | `3h 25m` |
| Estado | `User` / `Root` / `Retired` |

## Reconocimiento

```
nmap -sC -sV -oN scans/nmap-inicial.txt <IP>
```

**Puertos abiertos:**
| Puerto | Servicio | Versión |
|--------|----------|---------|
| 22/tcp | SSH | OpenSSH x.x |
| 80/tcp | HTTP | Apache x.x.x |

## Enumeración

### HTTP (puerto 80)
- Gobuster: `/admin`, `/uploads`, `/backup`
- WordPress 5.x detectado con wpscan

## Explotación

### Vector de entrada
...
**Comandos ejecutados:**
```bash
...
```

**Evidencia:**
<!-- Screenshot aquí -->

## Escalada de privilegios

### User → Root
...
**Comandos ejecutados:**
```bash
...
```

## Flags

- **User**: `hash_del_flag_user`
- **Root**: `hash_del_flag_root`

## Lecciones aprendidas

- Punto clave 1
- Punto clave 2

## Herramientas usadas

- nmap, gobuster, metasploit, burpsuite, ...
```

### Export workflow

```bash
# Convertir writeup markdown a PDF con pandoc
pandoc ~/lab/htb/<maquina>/walkthrough.md \
  -o ~/lab/writeups/<maquina>-writeup.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  --highlight-style=tango

# Con template personalizado
pandoc ~/lab/htb/<maquina>/walkthrough.md \
  -o ~/lab/writeups/<maquina>-writeup.html \
  --self-contained \
  --css=css/writeup.css

# Script para generar writeup con fecha
generate_writeup() {
    local machine="$1"
    local date=$(date +%Y-%m-%d)
    local template=~/lab/templates/writeup-template.md
    local outfile=~/lab/writeups/${machine,,}-${date}.md

    [[ -f "$template" ]] && cp "$template" "$outfile" || touch "$outfile"
    sed -i "s/<nombre>/$machine/g" "$outfile"
    sed -i "s/<fecha>/$date/g" "$outfile"
    echo "Writeup creado: $outfile"
}
```

### Embedding de evidencia (screenshots)

Para incluir screenshots en los writeups:

```markdown
<!-- En el writeup markdown -->
![nmap scan](./loot/nmap-inicial.png)

<!-- O ruta absoluta -->
![Puerto 80](file:///home/lcampassi/lab/htb/Maquina/loot/web-login.png)
```

En Obsidian, usar `![[imagen.png]]` para embed automático desde el vault.

---

## Herramientas por plataforma

### Linux (Arch) — KVM/libvirt

| Herramienta | Comando | Propósito |
|-------------|---------|-----------|
| virsh | `virsh list`, `virsh start`, `virsh create` | Gestión de VMs (CLI principal) |
| virt-install | `virt-install --name ...` | Crear VMs desde CLI |
| virt-manager | `virt-manager &` | GUI para gestión de VMs |
| virt-clone | `virt-clone --original ... --auto-clone` | Clonar VMs |
| virt-viewer | `virt-viewer <vm>` | Consola gráfica SPICE/VNC |
| qemu-img | `qemu-img create -f qcow2 ...` | Crear/convertir discos |
| qemu-system-x86_64 | (uso directo no recomendado) | Ejecutar QEMU sin libvirt |
| VBoxManage | (si VirtualBox instalado) | Gestión de VMs VirtualBox |

### Linux (Arch) — VirtualBox

```bash
# Verificar instalación
VBoxManage --version

# Comandos clave ya cubiertos arriba.
# VBoxManage coexiste con KVM, pero no ejecutar ambas al mismo tiempo
# o puede haber conflicto de módulos del kernel
```

### Windows 11 — VirtualBox

```powershell
# PowerShell (Administrador)
$vbox = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

# Listar VMs
& $vbox list vms

# Crear VM desde PowerShell
& $vbox createvm --name "Win10-Analysis" --ostype Windows10_64 --register
& $vbox modifyvm "Win10-Analysis" --memory 4096 --cpus 2
& $vbox createmedium disk --filename "C:\Users\lcampassi\VirtualBox VMs\Win10-Analysis.vdi" --size 51200
& $vbox startvm "Win10-Analysis"

# Función helper para no escribir la ruta completa cada vez
function VBox { & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" @args }
VBox list runningvms
VBox snapshot "Win10-Analysis" take "clean-state"
```

### Windows — Hyper-V (conceptual)

Si en algún momento se usa Hyper-V en lugar de VirtualBox:

```powershell
# Listar VMs
Get-VM

# Crear VM
New-VM -Name "Kali-Linux" -MemoryStartupBytes 4GB -BootDevice VHD

# Iniciar / apagar
Start-VM "Kali-Linux"
Stop-VM "Kali-Linux"

# Checkpoints (snapshots en Hyper-V)
Checkpoint-VM -Name "Kali-Linux" -SnapshotName "Clean-Install"
Restore-VMSnapshot -Name "Kali-Linux" -SnapshotName "Clean-Install" -Confirm:$false

# Red interna
New-VMSwitch -Name "Lab-Switch" -SwitchType Internal
```

**Nota:** Hyper-V y VirtualBox **no pueden ejecutarse simultáneamente** en Windows.
Hyper-V requiere deshabilitar la virtualización anidada para VBox.

### Comparativa rápida de comandos

| Acción | KVM (virsh) | VirtualBox (VBoxManage) | Hyper-V (PowerShell) |
|--------|-------------|------------------------|----------------------|
| Listar VMs | `virsh list --all` | `VBoxManage list vms` | `Get-VM` |
| Iniciar VM | `virsh start <vm>` | `VBoxManage startvm <vm>` | `Start-VM <vm>` |
| Apagar VM | `virsh shutdown <vm>` | `VBoxManage controlvm <vm> acpipowerbutton` | `Stop-VM <vm>` |
| Snapshot | `virsh snapshot-create-as <vm> --name <snap>` | `VBoxManage snapshot <vm> take <snap>` | `Checkpoint-VM -Name <vm> -SnapshotName <snap>` |
| Restaurar | `virsh snapshot-revert <vm> --snapshotname <snap>` | `VBoxManage snapshot <vm> restore <snap>` | `Restore-VMSnapshot -Name <vm> -SnapshotName <snap>` |
| Crear VM | `virt-install --name <vm> ...` | `VBoxManage createvm --name <vm> ...` | `New-VM -Name <vm> ...` |
| Red NAT | `virsh net-start default` | (NatNetwork por defecto) | `New-VMSwitch -SwitchType NAT` |
| Red interna | `virsh net-define red.xml && net-start` | `VBoxManage modifyvm <vm> --nic2 intnet` | `New-VMSwitch -SwitchType Internal` |

---

## Buenas prácticas

1. **Siempre tomar snapshot antes de exploitar** una máquina nueva
2. **Redes aisladas** para VMs vulnerables — nunca conectarlas a la LAN física
3. **Nomenclatura consistente**: `plataforma-maquina-rol` (ej: `htb-atomic-target`)
4. **Documentar todo** en Obsidian mientras se resuelve la máquina
5. **Rotar snapshots viejos** — mantener solo los esenciales para ahorrar espacio
6. **Respaldar configuraciones** XML de libvirt: `virsh dumpxml <vm> > backup.xml`
7. **No usar KVM y VirtualBox simultáneamente** en el mismo host (conflicto de módulos)
8. **Estandarizar IPs** en redes de laboratorio (ej: atacante .10, objetivo .20, servidor .30)
9. **Purgar VMs viejas** que ya no se usan para liberar espacio en disco
10. **Mantener ISOs y templates** organizados en `~/lab/isos/` y `~/lab/templates/`
