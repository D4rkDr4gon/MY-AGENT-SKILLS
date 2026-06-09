---
name: forensic-manager
description: Use when performing digital forensics — disk forensics (dd, guymager, sleuthkit, autopsy), memory forensics (volatility), file carving (foremost, scalpel), Windows artifacts (registry, prefetch, event logs, USN journal), and forensic imaging. Cross-platform (Linux + Windows).
---

# forensic-manager

Guía de forense digital para CSIRT y blue team. Complementa `hecate`, `apolo` y `hermes` con el enfoque de adquisición y análisis forense de disco y memoria.

## Contexto del usuario

- **Rol:** CSIRT / Blue Team / DFIR
- **SO primario:** Arch Linux (con herramientas forenses)
- **SO secundario:** Windows 11 (FLARE VM si aplica)
- **Herramientas Linux:** `dd`, `guymager`, `sleuthkit`, `autopsy`, `volatility3`, `foremost`, `scalpel`, `photorec`
- **Herramientas Windows:** `FTK Imager`, `Volatility`, `RegRipper`, `Zimmerman's Tools`

---

## 1. Adquisición forense

### Disco completo (dd)
```bash
# Identificar disco
sudo fdisk -l
sudo lsblk

# Adquisición forense (bit-for-bit)
sudo dd if=/dev/sda of=/mnt/evidence/case001/disk.dd bs=4M conv=noerror,sync status=progress

# Comprimido (más rápido, menos espacio)
sudo dd if=/dev/sda bs=4M conv=noerror,sync status=progress | gzip -c > /mnt/evidence/case001/disk.dd.gz

# Verificar integridad
sha256sum /mnt/evidence/case001/disk.dd > /mnt/evidence/case001/disk.dd.sha256

# Con hash inline (ddrescue, más robusto ante errores)
sudo pacman -S ddrescue
sudo ddrescue -d /dev/sda /mnt/evidence/case001/disk.img /mnt/evidence/case001/disk.log
```

### Partición específica
```bash
# Adquirir solo una partición
sudo dd if=/dev/sda2 of=/mnt/evidence/case001/part_sda2.dd bs=4M status=progress
```

### Memoria RAM
```bash
# Linux — liME (Linux Memory Extractor)
git clone https://github.com/504ensicsLabs/LiME.git
cd LiME/src
make
sudo insmod lime.ko "path=/mnt/evidence/case001/memory.lime format=lime"
sudo insmod lime.ko "path=/mnt/evidence/case001/memory.raw format=raw"

# Con avml (alternativa moderna)
sudo pacman -S avml  # o descargar de GH
sudo avml /mnt/evidence/case001/memory.raw

# Windows — winpmem (desde Linux)
# Descargar winpmem de GitHub
# Ejecutar en la máquina Windows objetivo como Admin
winpmem_mini_x64_rc2.exe memory.raw
```

### Cadena de custodia
```bash
# Calcular hashes ANTES de cualquier modificación
sha256sum /dev/sda > /mnt/evidence/case001/disk_original.sha256
md5sum /dev/sda >> /mnt/evidence/case001/disk_original.md5

# Registrar en documento
cat > /mnt/evidence/case001/custodia.txt << 'EOF'
CASO: CASE-001
FECHA: 2026-06-05
ADQUIRIENTE: Lucciano Campassi
DISPOSITIVO: /dev/sda (SSD 1TB)
HASH SHA256: <hash>
METODO: dd bs=4M conv=noerror,sync
DESTINO: /mnt/evidence/case001/disk.dd
NOTAS: Equipo apagado, adquisición en frío
EOF

# Cifrar evidencia
age -p -o /mnt/evidence/case001.tar.gz.age /mnt/evidence/case001/
```

---

## 2. Sleuth Kit — Análisis de disco

```bash
# Instalar
sudo pacman -S sleuthkit

# Información del disco
mmls /mnt/evidence/case001/disk.dd               # Tabla de particiones
fsstat /mnt/evidence/case001/disk.dd              # Filesystem info
fsstat -o 2048 /mnt/evidence/case001/disk.dd     # Partición con offset

# Análisis de archivos
fls -o 2048 /mnt/evidence/case001/disk.dd        # Listar archivos (partición)
fls -o 2048 -r /mnt/evidence/case001/disk.dd     # Recursivo
fls -o 2048 -d /mnt/evidence/case001/disk.dd     # Solo archivos eliminados

# Recuperar archivo por inodo
icat -o 2048 /mnt/evidence/case001/disk.dd 12345 > /tmp/recovered_file

# Timeline del filesystem
fls -o 2048 -m / /mnt/evidence/case001/disk.dd > /tmp/bodyfile.txt
mactime -b /tmp/bodyfile.txt -d > /tmp/timeline.csv

# Verificar actividad de archivos
find /mnt/evidence/case001 -name "*.dd" -exec stat {} \;
```

---

## 3. Autopsy — GUI Forense

```bash
# Instalar
sudo pacman -S autopsy

# Iniciar (corre como servidor web en localhost:9999)
sudo autopsy

# Workflow:
# 1. New Case → nombrar y describir
# 2. Add Host → identificar origen
# 3. Add Image → seleccionar .dd o .img
# 4. Análisis automático (file type, hash db, keyword search)
# 5. Revisar resultados en la UI
```

---

## 4. File Carving

```bash
# foremost
sudo pacman -S foremost

# Carving por tipo de archivo
foremost -t jpg,png,doc,pdf -i /mnt/evidence/case001/disk.dd -o /tmp/carved/

# Carving todos los tipos
foremost -i /mnt/evidence/case001/disk.dd -o /tmp/carved-all/

# scalpel (más configurable)
sudo pacman -S scalpel
# Editar /etc/scalpel/scalpel.conf (descomentar tipos de archivo)
scalpel /mnt/evidence/case001/disk.dd -o /tmp/scalped/

# photorec (recuperación de fotos/media)
sudo pacman -S testdisk
photorec /d /tmp/photorec/ /mnt/evidence/case001/disk.dd
```

---

## 5. Windows Artifacts Analysis

### Registry
```bash
# Registry (usando tools de Linux)
sudo pacman -S regripper  # si está disponible

# O con python-registry
pip install python-registry

# Extraer hive del disco montado
fls -o 2048 /mnt/evidence/case001/disk.dd | grep -i "ntuser.dat\|SAM\|SYSTEM\|SOFTWARE\|SECURITY"

# Analizar SAM (contraseñas)
python3 -c "
from Registry import Registry
reg = Registry.Registry('/path/to/SAM')
# Users
for key in reg.open('SAM\\Domains\\Account\\Users\\Names').subkeys():
    print(f'User: {key.name()}')
"

# Analizar NetworkList (redes conocidas)
# SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces
```

### Event Logs
```bash
# Extraer .evtx de la imagen
fls -o 2048 disk.dd | grep "\.evtx"

# Analizar con python-evtx
pip install python-evtx
python3 -m evtx_dump /path/to/Security.evtx > security.xml

# Timeline de eventos
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('security.xml')
for event in tree.findall('.//Event'):
    id = event.find('.//EventID')
    time = event.find('.//TimeCreated')
    print(f'[{time.get("SystemTime")}] EventID: {id.text}')
"
```

### Prefetch
```bash
# Extraer prefetch de la imagen
fls -o 2048 disk.dd | grep -i "\.pf$"
icat -o 2048 disk.dd <inode> > /tmp/app.pf

# Analizar con python-prefetch (si existe) o PECmd (Windows)
```

### USN Journal
```bash
# Extraer USN Journal
icat -o 2048 disk.dd <usnjrnl_inode> > /tmp/usnjrnl

# Analizar con herramientas
# $MFT, $LogFile, $USNJrnl: $J
# En Windows: MFTEcmd.exe, UsnJrnl2CSV (Zimmerman's tools)
```

---

## 6. Memory Forensics — Volatility 3

```bash
# Instalar volatility3
git clone https://github.com/volatilityfoundation/volatility3.git
cd volatility3
python3 -m pip install -r requirements.txt

# Identificar perfil (Windows)
python3 vol.py -f memory.raw windows.info
python3 vol.py -f memory.raw windows.envars

# Procesos
python3 vol.py -f memory.raw windows.pslist
python3 vol.py -f memory.raw windows.psscan      # Procesos ocultos
python3 vol.py -f memory.raw windows.pstree       # Árbol de procesos

# Conexiones de red
python3 vol.py -f memory.raw windows.netscan
python3 vol.py -f memory.raw windows.netstat

# DLLs cargados
python3 vol.py -f memory.raw windows.dlllist
python3 vol.py -f memory.raw windows.cmdline      # Command line por proceso

# Handles
python3 vol.py -f memory.raw windows.handles
python3 vol.py -f memory.raw windows.filescan     # Archivos abiertos

# Registry (memory)
python3 vol.py -f memory.raw windows.registry.hiveslist
python3 vol.py -f memory.raw windows.registry.printkey -K "Microsoft\\Windows\\CurrentVersion\\Run"

# Malware detection
python3 vol.py -f memory.raw windows.malfind      # Inyección de código
python3 vol.py -f memory.raw windows.modscan      # Módulos del kernel (rootkits)
python3 vol.py -f memory.raw windows.ssdt         # SSDT hooks (rootkits)
python3 vol.py -f memory.raw windows.driverscan   # Driver sospechosos

# Dump de procesos para análisis
python3 vol.py -f memory.raw windows.dumpfiles --pid 1234 -o /tmp/dumped/
python3 vol.py -f memory.raw windows.memdump --pid 1234 -o /tmp/dumped/

# Timeline
python3 vol.py -f memory.raw windows.mftscan      # MFT desde memoria
python3 vol.py -f memory.raw windows.timeliner    # Timeline completo
```

### Volatility 3 en Linux
```bash
# Linux memory analysis
python3 vol.py -f memory.lime linux.info
python3 vol.py -f memory.lime linux.pslist
python3 vol.py -f memory.lime linux.bash          # Bash history
python3 vol.py -f memory.lime linux.netstat
python3 vol.py -f memory.lime linux.malfind
python3 vol.py -f memory.lime linux.proc.Malfind
```

---

## 7. Timeline Forense

```bash
# Crear timeline con múltiples fuentes
# 1. Filesystem MAC times (sleuthkit)
fls -o 2048 -m / /mnt/evidence/case001/disk.dd > body_fls.txt

# 2. Event Logs (convertir a timeline)
# 3. Memory (volatility timeliner)
python3 vol.py -f memory.raw windows.timeliner > memory_timeline.csv

# 4. Logs de sistema
# 5. Browser history

# Unificar timeline
# Ordenar por timestamp
sort -t, -k1 all_events.csv > sorted_timeline.csv

# Formato CSV recomendado
# Timestamp,Source,EventType,Description,User,Path,Hash
```

---

## 8. Buenas prácticas forenses

1. **Cadena de custodia** — documentar cada paso desde la adquisición
2. **Hashes** — sha256 antes de tocar cualquier evidencia
3. **No modificar el original** — trabajar siempre sobre copias/imágenes
4. **Write blocker** — usar hardware/software write blocker durante adquisición
5. **Orden de volatilidad** — RAM > procesos > conexiones > disco
6. **Imagen forense, no copia** — dd/dc3dd, no cp/robocopy
7. **Cifrar evidencia** — age/gpg para almacenar imágenes
8. **Herramientas validadas** — usar herramientas forenses no solo scripts caseros
9. **Documentar tools** — versión, parámetros, output en el reporte
10. **Reporte ejecutivo + técnico** — ambos públicos objetivo
