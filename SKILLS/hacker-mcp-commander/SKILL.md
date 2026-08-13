---
name: hacker-mcp-commander
description: >
  Guía de uso del MCP server HACKER-MCP-COMMANDER: pentesting con Kali Linux
  en Docker. Usar cuando se necesite ejecutar herramientas ofensivas (nmap,
  gobuster, ffuf, sqlmap, hydra, etc.), hacer reconocimiento, enumeración,
  explotación, o documentar evidencia de un engagement. Carga esta skill
  ANTES de usar cualquier tool del MCP server.
---

# HACKER-MCP-COMMANDER — Skill de pentesting

MCP server que expone herramientas de Kali Linux corriendo en un contenedor
Docker aislado. Este skill define el flujo de trabajo correcto para usarlo.

## 1. Verificación del entorno

Antes de usar cualquier tool MCP, verificar que el contenedor esté corriendo:

```bash
docker ps --filter "name=hacker-mcp-commander"
```

Si no está corriendo:
```bash
cd /files/VMs/DOCKER/kali-mcp && make up
```

Si no existe (primera vez):
```bash
cd /files/VMs/DOCKER/kali-mcp && make build && make up
```

## 2. Reglas de seguridad (obligatorias)

1. **Solo targets autorizados**: el usuario debe confirmar explícitamente el
   target y el alcance antes de iniciar cualquier scan.
2. **Siempre crear una sesión** con `session_create` al empezar un engagement:
   queda registrado el target autorizado y la evidencia se guarda por sesión.
3. **No DoS**: usar presets conservadores (quick/standard), timeouts razonables,
   y no lanzar scans agresivos sin pedir confirmación.
4. **Evidencia**: guardar outputs importantes con `save_output` en la sesión.
5. **Credenciales**: usar `credential_store` para credenciales descubiertas
   (nunca en el chat).
6. **Modo libre**: `run` tiene allowlist por defecto. Si se necesita un binario
   no permitido, avisar al usuario (requiere ALLOW_FREE_COMMAND=true en .env).

## 3. Flujo de pentesting recomendado

### Fase 1 — Reconocimiento
```
session_create(name="<lab>-<maquina>", target="<IP/dominio>")
port_scan(target=<IP>, scan_type=quick)          # puertos abiertos
dns_enum(domain=<dominio>)                       # si aplica
network_discovery(target=<rango>)                # descubrir hosts
subdomain_enum(domain=<dominio>)                 # si aplica
```

### Fase 2 — Enumeración
```
port_scan(target=<IP>, scan_type=service)        # versiones de servicios
web_enumeration(target=http://<IP>, enumeration_type=basic)
whatweb / header_analysis(url=...)               # fingerprinting
enum_shares / smbclient                          # si hay 139/445
ssl_analysis(host=<IP>)                          # si hay 443
```

### Fase 3 — Explotación
```
searchsploit <servicio> <version>                # buscar exploits
vulnerability_scan(target=<IP>, scan_type=quick) # nikto
sqlmap / hydra_attack(...)                       # según hallazgos
payload_generate / reverse_shell(...)            # si se logra RCE
```

### Fase 4 — Post-explotación y evidencia
```
save_output(session_id, "nmap_full.txt", <output>)
parse_nmap(filepath=...)                         # output estructurado
credential_store(action=add, ...)                # credenciales
create_report(session_id, title, summary, findings)
```

### Fase 5 — Cierre
```
session_close(session_id)
```

## 4. Mapa de tools por necesidad

| Necesidad | Tool MCP |
|---|---|
| Escanear puertos | `port_scan` (presets: quick/full/stealth/udp/service/aggressive) |
| Enumerar DNS | `dns_enum` |
| Descubrir hosts | `network_discovery` |
| Subdominios | `subdomain_enum` |
| Recon automático | `recon_auto` (depth: quick/standard/deep) |
| Vulns web | `vulnerability_scan` |
| Directorios web | `web_enumeration` |
| Cabeceras HTTP | `header_analysis` |
| SSL/TLS | `ssl_analysis` |
| Crawling | `spider_website` |
| Fuerza bruta | `hydra_attack` |
| Identificar hash | `hash_identify` |
| Payloads | `payload_generate`, `reverse_shell` |
| Buscar exploits | `exploit_search` |
| Parsear nmap | `parse_nmap` |
| Parsear output | `parse_tool_output` |
| Codificar/decodificar | `encode_decode` |
| Analizar archivo | `file_analysis` |
| Descargar archivo | `download_file` |
| Comando libre | `run` (allowlist) |
| Sesiones | `session_create/list/switch/status/history/close/delete` |
| Evidencia | `save_output`, `list_files`, `read_file` |
| Reporte | `create_report` |

## 5. Buenas prácticas

- **Sesión por engagement**: no mezclar targets en la misma sesión.
- **Output grande**: si un scan genera mucho output, guardarlo con `save_output`
  y leerlo con `read_file` en vez de traerlo todo al contexto.
- **Timeouts**: scans largos (full, aggressive) pueden tardar minutos — usar
  timeouts generosos (300-900s) en esas tools.
- **Workspace**: los archivos se comparten con el host en
  `/files/VMs/DOCKER/kali-mcp/workspace/` — los resultados quedan accesibles
  para el usuario.
- **Documentar**: al terminar, documentar hallazgos en el vault Babilonia
  (cargar `obsidian-manager`) con evidencia de los outputs.

## 6. Troubleshooting

| Problema | Solución |
|---|---|
| "Container not running" | `make up` en /files/VMs/DOCKER/kali-mcp |
| Tool no responde | Verificar `docker ps`; `make logs` |
| Binario no en allowlist | Usar tool específica o activar ALLOW_FREE_COMMAND |
| Workspace no writable | `docker exec -u root <ctr> chown -R pentester:pentester /workspace` |
| Rebuild tras cambios | `make build && make up` |