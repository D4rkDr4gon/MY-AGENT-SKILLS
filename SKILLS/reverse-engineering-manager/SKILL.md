---
name: reverse-engineering-manager
description: Use when performing reverse engineering of binaries — radare2/rizin, Ghidra (headless), binary analysis (PE/ELF/Mach-O), GDB debugging, unpacking, anti-debugging detection, YARA integration, and firmware RE.
---

# reverse-engineering-manager

Guía para ingeniería reversa de binarios, orientada a análisis de malware y vulnerabilidades.

## Contexto del usuario

- **SO:** Arch Linux (primario) + Windows 11 (VM/FLARE)
- **RE tools en Arch:** `radare2`, `rizin`, `gdb`, `binutils`, `file`, `strings`, `xxd`
- **Ghidra:** `ghidra` (AUR) o headless
- **Windows RE:** x64dbg, Process Hacker, PeStudio, Detect It Easy (DIE)
- **Sandbox:** Docker/Podman (ver `docker-manager`)
- **YARA:** `yara`, `yargen` para detección de malware

---

## 1. Reconocimiento inicial del binario

### File type y metadata
```bash
file malware.exe
file malware.elf
file firmware.bin

# Hashes (IOC)
sha256sum malware.exe
md5sum malware.exe

# Strings (los clasicos)
strings malware.bin
strings -n 8 malware.bin          # Strings de al menos 8 caracteres
strings -e l malware.exe          # Unicode (little-endian)
strings -e b malware.bin          # Unicode (big-endian)

# Strings con contexto de offset
rabin2 -z malware.elf             # radare2: strings en secciones de datos
rizin -q -c "izz~..." malware.elf # rizin: strings con filtro
```

### Detección de compilador/packer
```bash
# Detect It Easy (diec — CLI)
diec malware.exe

# rabin2 info
rabin2 -I malware.exe             # Información general
rabin2 -E malware.exe             # Entries
rabin2 -S malware.exe             # Secciones
rabin2 -l malware.exe             # Librerías importadas
rabin2 -s malware.exe             # Símbolos

# Binutils clasicos
objdump -p malware.exe            # PE header
objdump -f malware.elf            # ELF header
objdump -t malware.elf            # Symbol table
readelf -a malware.elf            # TODO ELF
nm -C malware.elf                 # Símbolos (C++ demangled)
```

### Análisis de secciones sospechosas
```bash
# Secciones con permisos extraños (W+E)
rabin2 -S malware.exe | grep -E 'rwx|wx'

# Verificar entropy por sección (alta entropía = packed/encrypted)
# Usando diec o script propio
diec -d entropy malware.exe

# Secciones inusuales (no estándar)
rabin2 -S malware.exe | grep -vE '\.text|\.data|\.rdata|\.bss|\.idata|\.rsrc'
```

---

## 2. radare2 / rizin

### Comandos esenciales
```bash
# Abrir binario
r2 malware.exe                    # radare2
rizin malware.exe                 # rizin (fork moderno)

# Modo análisis
r2 -A malware.exe                 # Analizar automáticamente
rizin -A malware.exe

# Comandos básicos dentro de r2/rizin
[0x00401000]> aaa                # Análisis completo (autorecon)
[0x00401000]> afl                # Listar funciones
[0x00401000]> afl~main           # Filtrar funciones por nombre
[0x00401000]> s main             # Seek a función main
[0x00401000]> pdf                # Disassembly de función actual
[0x00401000]> V                  # Modo visual (q para salir)
[0x00401000]> VV                 # Modo graph (call graph)
[0x00401000]> iz                 # Strings en data sections
[0x00401000]> izz                # Strings en todo el binario
[0x00401000]> is                 # Símbolos
[0x00401000]> il                 # Importaciones
[0x00401000]> ie                 # Entrypoints
[0x00401000]> iS                 # Secciones
[0x00401000]> oo+                # Abrir en modo escritura (para patches)
[0x00401000]> wa nop             # Patch: escribir NOP en la posición actual
[0x00401000]> wc                 # Escribir en el cursor

# Búsqueda de patrones
[0x00401000]> /R xor             # Buscar instrucciones 'xor'
[0x00401000]> /v 1234            # Buscar valor 0x1234
[0x00401000]> /x 90              # Buscar bytes (NOP)
[0x00401000]> /a jmp eax         # Buscar patrón assembly

# Cross-references
[0x00401000]> axt 0x00402000     # Qué referencias a esta dirección
[0x00401000]> axf 0x00401000     # Adónde apunta esta dirección

# Debugging simple (modo debug)
r2 -d malware.exe
[0x7f...]> db main               # Breakpoint en main
[0x7f...]> dc                    # Continue
[0x7f...]> dr                    # Registros
[0x7f...]> dbt                   # Backtrace
[0x7f...]> ds                    # Step (single instruction)
[0x7f...]> dso                   # Step over
[0x7f...]> dri                   # Register info

# Análisis de llamadas a API
[0x00401000]> is~WinExec         # Buscar importación específica
[0x00401000]> il~CreateFile      # Buscar en imports
[0x00401000]> /R call.*Create    # Buscar calls a Create functions
```

### Scripting en r2pipe (Python)
```python
import r2pipe

r2 = r2pipe.open("malware.exe")
r2.cmd("aaa")  # Analyze all
functions = r2.cmd("afl").split("\n")
imports = r2.cmd("il").split("\n")
strings = r2.cmd("izz").split("\n")

print(f"Funciones: {len(functions)}")
print(f"Strings: {len(strings)}")
print("API calls sospechosas:")
for api in imports:
    if any(x in api.lower() for x in ['socket', 'connect', 'write', 'readfile', 'createfile']):
        print(f"  {api}")
```

---

## 3. Ghidra Headless

### Análisis desde CLI
```bash
# Analizar binario sin abrir GUI
ghidraHeadless /tmp/ghidra-proj MalwareAnalysis \
  -import malware.exe \
  -postScript AnalyzeFunctionID.xml \
  -postScript AnalyzeSymbols.xml \
  -postScript /path/to/custom-script.py

# Exportar resultados
ghidraHeadless /tmp/ghidra-proj MalwareAnalysis \
  -import malware.exe \
  -scriptPath /path/to/scripts \
  -postScript ExportToCsv.java \
  -deleteProject
```

### Scripts útiles en Python (para Ghidra)
```python
# ghidra_scripts/extract_iocs.py
from ghidra.program.model.listing import Function
from ghidra.program.model.address import AddressSet

def run():
    program = getCurrentProgram()
    listing = program.getListing()
    fm = program.getFunctionManager()
    
    print(f"Binary: {program.getName()}")
    print(f"Functions: {fm.getFunctionCount()}")
    
    # Buscar strings
    for string in getData().getDefinedData(True):
        if string.isString():
            text = string.getDefaultValueRepresentation()
            if len(text) > 4 and len(text) < 256:
                print(f"String @ {string.getAddress()}: {text}")
    
    # Listar funciones importadas
    for ext_ref in getExternalReferences():
        print(f"Import: {ext_ref.getExternalLocation().getSymbolName()}")
```

---

## 4. GDB — GNU Debugger (Linux ELF)

```bash
# Básicos
gdb ./malware.elf
gdb -q ./malware.elf             # Quiet mode
gdb -q -ex "set pagination off" -ex "r" ./malware.elf

# Puntos de interrupción
(gdb) break main
(gdb) break *0x00401234
(gdb) break read
(gdb) info breakpoints

# Ejecución
(gdb) run < args.txt
(gdb) run < input.txt
(gdb) continue
(gdb) nexti                     # Next instruction
(gdb) stepi                     # Step instruction (entra en calls)
(gdb) finish                    # Salir de función actual

# Inspección
(gdb) info registers
(gdb) info frame
(gdb) x/10i $rip               # 10 instrucciones desde RIP
(gdb) x/10x $rsp               # 10 palabras desde RSP (stack)
(gdb) x/s 0x404000             # String en dirección
(gdb) print $rdi               # Primer argumento (x86_64 SysV ABI)
(gdb) print $rsi               # Segundo argumento
(gdb) print $rdx               # Tercer argumento

# Stack
(gdb) bt                       # Backtrace
(gdb) bt full                  # Backtrace con variables locales

# Análisis de llamadas a syscalls (strace + gdb)
(gdb) catch syscall write      # Break en syscall write
(gdb) catch syscall 59         # Break en execve (59 = x64)

# Debugging de fork
(gdb) set follow-fork-mode child
(gdb) set detach-on-fork off
```

---

## 5. Detección de Packers

### Packers comunes y señales

| Packer | Señales | Herramientas de detección |
|--------|---------|--------------------------|
| **UPX** | Secciones UPX0/UPX1, alta entropía, poco imports reales | `upx -t`, `diec`, `rabin2 -S` |
| **Themida** | Secciones `.themida`, `.vmp`, .data rwx | `diec`, `peid` |
| **VMProtect** | Secciones `.vmp0`, `.vmp1`, saltos indirectos | `diec` |
| **ASPack** | Sección `.aspack`, OEP al final | `diec` |
| **ConfuserEx** | .NET obfuscado, muchos métodos virtuales | `de4dot`, `dnSpy` |
| **Enigma Protector** | Sección `.enigma1`, API hooking | `diec` |
| **MPRESS** | Sección `.MPRESS`, compresión | `diec` |

### Detección de packed binaries
```bash
# Alta entropía en secciones sospechosas
diec malware.exe

# Verificar si se puede desempaquetar UPX
upx -t malware.exe

# Anomalías en secciones
rabin2 -S malware.exe | awk '$3 ~ /rwx/ {print $0}'   # Secciones W+X (sospechoso)
rabin2 -S malware.exe | awk '$2 ~ /[0-9]/ { if ($2 > 0.6) print $0 }'  # Alta entropía

# Poco imports pero tamaño grande
rabin2 -l malware.exe | wc -l
rabin2 -S malware.exe | grep TOTAL
```

### Desempaquetado manual (UPX)
```bash
# UPX: desempaquetar
upx -d malware.exe -o malware_unpacked.exe

# UPX: si falla, dump manual con breakpoint en OEP
# 1. Ejecutar hasta OEP (original entry point)
# 2. Dump con:
#    - Linux: gdb + gcore
#    - Windows: x64dbg + Scylla plugin
upx -d malware.exe -k   # -k: mantener backup
```

### Herramientas de unpacking
```bash
# UNPACME (automatizado, requiere API key)
unpacme -k APIKEY analyze malware.exe

# Ultimate Packer for executables (UPX)
upx -t malware.exe              # Test
upx -l malware.exe              # List files in archive

# Detect It Easy (CLI)
diec malware.exe                # Detectar packer/compiler
diec -d entropy malware.exe     # Análisis de entropía
```

---

## 6. Análisis de PE (Windows)

```bash
# CFF Explorer CLI (wine)
cff_explorer.exe malware.exe

# pecheck (radare2)
rabin2 -r malware.exe           # Recurso
rabin2 -d malware.exe           # Debug info
rabin2 -O malware.exe           # Relocations
rabin2 -x malware.exe           # Extract resources

# pe-tree (Python)
# pip install pefile
python3 -c "
import pefile
pe = pefile.PE('malware.exe')
for section in pe.sections:
    print(f'{section.Name.decode().strip()}: '
          f'vaddr=0x{section.VirtualAddress:x} '
          f'size=0x{section.SizeOfRawData:x} '
          f'chars=0x{section.Characteristics:08x}')
# Imports
for entry in pe.DIRECTORY_ENTRY_IMPORT:
    print(f'\n[+] {entry.dll.decode()}')
    for imp in entry.imports:
        print(f'  {imp.name.decode() if imp.name else hex(imp.address)}')
"

# Análisis de recursos (iconos, manifest, version info)
rabin2 -r malware.exe           # Resources list
# Extraer recursos con Resource Hacker (Windows) o 7z
```

---

## 7. Análisis de ELF (Linux)

```bash
# Información básica
file malware.elf
readelf -h malware.elf          # ELF header
readelf -S malware.elf          # Section headers
readelf -l malware.elf          # Program headers (segments)
readelf -d malware.elf          # Dynamic section
readelf -s malware.elf          # Symbol table

# objdump
objdump -d malware.elf          # Disassembly
objdump -d malware.elf | head -50
objdump -t malware.elf          # Symbols
objdump -R malware.elf          # Relocations
objdump -p malware.elf          # Private headers

# Buscar gadgets ROP
ROPgadget --binary malware.elf
ROPgadget --binary malware.elf | grep "int 0x80"

# Análisis de syscalls (sin ejecutar)
strace -e trace=openat,read,write ./malware.elf 2>&1 | head -20

# LIEF (Library to Instrument Executable Formats)
python3 -c "
import lief
binary = lief.parse('malware.elf')
print(f'Entry: {hex(binary.entrypoint)}')
print(f'Sections: {len(binary.sections)}')
for s in binary.sections:
    print(f'  {s.name}: {hex(s.size)} flags={hex(s.flags)}')
print('Dynamic libs:', binary.libraries)
"
```

---

## 8. Análisis de Firmware

```bash
# Identificar firmware
file firmware.bin
hexdump -C firmware.bin | head -20

# binwalk (instalar: sudo pacman -S binwalk  o pip install binwalk)
binwalk firmware.bin                    # Detectar archivos embebidos
binwalk -Me firmware.bin                # Extraer automáticamente

# strings + grep
strings firmware.bin | grep -iE 'version|model|build|gcc|linux'

# Entropía (identificar compressed/encrypted regions)
binwalk -E firmware.bin                 # Entropy graph

# fdisk (si es imagen de disco)
fdisk -l firmware.bin

# mount (si es filesystem)
sudo mount -o loop,ro firmware.bin /mnt/fw

# Firmware Mod Kit (descompresión de firmwares comunes)
# https://github.com/rampageX/firmware-mod-kit
./extract-firmware.sh firmware.bin

# JH7110 / RISC-V / ARM firmwares
# Usar corresponding toolchain para cross-disassembly
arm-none-eabi-objdump -b binary -m arm -D firmware.bin
```

---

## 9. YARA Integration

```yaml
# rule_malware_common.yara
rule Malware_Generic_Packed {
    meta:
        description = "Detecta binarios packed con alta entropía"
        author = "lcampassi"
        date = "2026-06"
    strings:
        $upx_magic = "UPX!" 
        $high_entropy_section = /\.(upx|themida|vmp|aspack|MPRESS)\d*/
    condition:
        $upx_magic or $high_entropy_section
}

rule Malware_Suspicious_API {
    meta:
        description = "Binarios con APIs sospechosas"
    strings:
        $a1 = "CreateRemoteThread" nocase
        $a2 = "VirtualAllocEx" nocase
        $a3 = "WriteProcessMemory" nocase
        $a4 = "SetWindowsHookEx" nocase
        $a5 = "RegCreateKeyEx" nocase
    condition:
        2 of them
}

rule IOC_C2_Domain {
    meta:
        description = "IOC: dominio de C2 embebido"
    strings:
        $domain = /https?:\/\/([a-z0-9-]+\.)+[a-z]{2,}(:[0-9]+)?\/[^\s]{1,64}/
    condition:
        #domain > 0
}
```

```bash
# Escanear binario
yara -s rule_malware_common.yara malware.exe

# Escanear directorio
yara -r rule_malware_common.yara /samples/

# YARA + binario específico con metadatos
yara -s -m rule_malware_common.yara malware.exe
```

---

## 10. Debugging avanzado

### Anti-debugging detection
```bash
# Señales de anti-debug en binario
strings malware.exe | grep -iE 'IsDebuggerPresent|NtGlobalFlag|PEB|BeingDebugged|CheckRemoteDebuggerPresent|OutputDebugString'

# En radare2, buscar llamadas sospechosas
r2 -A malware.exe
[0x...]> /R call.*IsDebuggerPresent
[0x...]> axt~NtQueryInformationProcess

# Técnicas anti-debug comunes
# - IsDebuggerPresent()     -> Parchar: mov eax, 0; ret
# - NtGlobalFlag            -> PEB flag
# - Timing checks           -> rdtsc antes/después
# - INT 3 / int3            -> Software breakpoint detection
# - TLS callbacks           -> Se ejecutan antes de entrypoint
# - Process debug flags     -> NtSetInformationProcess
```

### Patch de binario
```bash
# En radare2
r2 -w malware.exe
[0x...]> s 0x00401234          # Seek a dirección del check
[0x...]> wa nop                # Parchar con NOPs
[0x...]> wc                    # Escribir

# Con python/pefile
python3 -c "
import pefile
pe = pefile.PE('malware.exe')
# Parchar bytes en una dirección
pe.set_bytes_at_rva(0x1234, b'\x90\x90\x90\x90')
pe.write('malware_patched.exe')
"

# Con xxd
xxd malware.exe | sed 's/1234: 7540/1234: eb40/' | xxd -r > malware_patched.exe
```

---

## 11. Herramientas complementarias

### Linux
```bash
# Syscall tracing
strace -f -e trace=network ./malware.elf           # Syscalls de red
strace -f -e trace=file ./malware.elf               # Syscalls de archivos
strace -f -e trace=process ./malware.elf            # Syscalls de procesos
ltrace -e malloc+free+calloc ./malware.elf          # Library calls

# Process monitoring (live)
htop                                        # Recursos
lsof -p <PID>                               # File descriptors
ls -la /proc/<PID>/fd/                      # FDs abiertos
/proc/<PID>/maps                            # Memory mappings
/proc/<PID>/root/                           # Root FS namespace

# Network
tcpdump -i lo port 4444                     # Captura de tráfico local
netstat -tulpn | grep <PID>                 # Conexiones activas
ss -tulpn | grep malware                    # Sockets

# Binary diffing
vbindiff malware.exe malware_patched.exe    # Visual binary diff
radiff2 malware.exe malware_patched.exe     # r2 binary diff
diasm malware.exe                           # Differ assembly
```

### Windows (FLARE VM / REMnux)
```powershell
# Herramientas recomendadas en Windows
# - x64dbg: Debugging gráfico con plugins ScyllaHide, xAnalyzer
# - Process Hacker 2: Process explorer + memory viewer
# - PeStudio: Análisis rápido de PE
# - Detect It Easy (DIE): Identificación de packers
# - HxD: Hex editor
# - API Monitor: Intercepción de API calls
# - Process Monitor (ProcMon): Filesystem, registry, process activity
# - CFF Explorer: PE structure
# - dnSpy: .NET decompiler
# - ILSpy: .NET decompiler alternativo
```

---

## 12. Buenas prácticas

1. **Siempre en sandbox** — nunca ejecutar malware en el host. Usar Docker/VMs
2. **Snapshot antes de ejecutar** — poder revertir el análisis dinámico
3. **Documentar IOCs** — hashes, dominios, IPs, paths, mutexes en la vault de Obsidian
4. **YARA desde el inicio** — identificar muestras relacionadas por similitud
5. **Aislar red** — el sandbox no debe tener acceso a internet ni a la LAN
6. **Cadena de custodia** — mantener hashes originales antes de cualquier modificación
7. **Checklist de análisis**:
   - [ ] File type + hash (sha256)
   - [ ] Detección de packer (diec, entropy)
   - [ ] Strings analysis
   - [ ] Import table / API calls
   - [ ] Disassembly inicial (entrypoint, main)
   - [ ] Identificar C2 (domains, IPs, protocols)
   - [ ] Extraer config (decryption keys, URLs)
   - [ ] Analisis dinámico (strace, tcpdump, procmon)
   - [ ] YARA rules
   - [ ] Documentar en Obsidian

---

## Referencias

- radare2 docs: `r2 -h` / https://book.rada.re
- rizin docs: https://rizin.re
- Ghidra: https://ghidra-sre.org
- PE format: https://docs.microsoft.com/en-us/windows/win32/debug/pe-format
- ELF spec: https://refspecs.linuxfoundation.org/elf/elf.pdf
- YARA: https://yara.readthedocs.io
- Practical Malware Analysis (Sikorski): Referencia definitiva de RE
- OALabs / MalwareUnicorn: YouTube channels de RE y unpacking
