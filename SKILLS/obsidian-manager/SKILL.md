---
name: obsidian-manager
description: Use when managing the Obsidian vault (Personal-Vault) — cross-platform. Create notes, search, manage tasks, daily notes, templates, or sync. Adapts paths automatically for Linux and Windows.
---

# obsidian-manager

## ⚡ Resumen ejecutivo

Este skill opera en **3 modos**, en orden de preferencia:

| Modo | Canal | Rápido | Requiere |
|------|-------|--------|----------|
| **1. REST API** | `curl -k https://127.0.0.1:27124/vault/...` | ✅ Instantáneo | Obsidian abierto + plugin REST API |
| **2. MCP** | `POST /mcp/` (con session ID) | ✅ Rápido (2 requests) | Obsidian abierto + plugin REST API |
| **3. Filesystem** | Lectura directa de archivos `.md` | ✅ Rapidísimo | Nada (sin dependencias) |

**Regla de oro**: Para cualquier operación, intentá en este orden:
1. Si es **leer/escribir archivo** → **Filesystem** (no requiere red, es lo más rápido)
2. Si es **CRUD + abrir en UI + search** → **REST API** (1 solo request, sin sesión)
3. Si es **tags + comandos + patches quirúrgicos + nota activa** → **MCP** (requiere sesión)
4. Si no responde REST API ni MCP → **Filesystem** como fallback

---

## Detección automática de conectividad

Antes de operar, verificá qué canales están disponibles:

```bash
# 1. ¿REST API disponible?
REST_OK=$(curl -sk -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  https://127.0.0.1:27124/ 2>/dev/null)
# 200 = OK

# 2. ¿MCP disponible? (requiere inicializar sesión)
MCP_OK=no
if [ "$REST_OK" = "200" ]; then
  MCP_SESSION=$(curl -sk -X POST "https://127.0.0.1:27124/mcp/" \
    -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"opencode","version":"1.0.0"}}}' \
    2>/dev/null | grep -o '"mcp-session-id": "[^"]*"' | cut -d'"' -f4)
  [ -n "$MCP_SESSION" ] && MCP_OK=yes
fi

# 3. Filesystem siempre disponible (es el fallback final)
FS_OK=yes
```

**Variables de configuración** (ya seteada en el entorno):
- `OBSIDIAN_API_KEY` = `7363b03610341c448ae340e556ea11ef644c54a0ddcbbd0e3b8fc0d1c8fadf8d`
- `OBSIDIAN_URL` = `https://127.0.0.1:27124`
- `OBSIDIAN_VAULT` = `/files/Personal-Vault` (Linux)
- `OBSIDIAN_BASE` = `https://127.0.0.1:27124/vault`

---

## Cross-Platform — Detección de SO

Este skill funciona en **Arch Linux** y **Windows 11**. Los paths cambian según el SO:

| Recurso | Linux | Windows |
|---|---|---|
| Vault root | `/files/Personal-Vault` | `C:\Users\lcampassi\Proton Drive\D4rkDr4g0n19\My files\Personal-Vault` |
| CLI | `obsidian vault=Personal-Vault <cmd>` | `obsidian vault=Personal-Vault <cmd>` (si está en PATH) |
| REST API | `https://127.0.0.1:27124` | `https://127.0.0.1:27124` |
| Scripts sync | `~/dotfiles/automat/vault-pull.sh` / `vault-push.sh` | *(no aplica)* |
| Ruta relativa base | `Manuales/` | `Manuales/` |

> **Regla**: Siempre operá con rutas **relativas al vault** cuando sea posible (ej: `Manuales/00-FUNDAMENTALS/...`). Solo usá paths absolutos cuando sea estrictamente necesario y detectá el SO automáticamente.

## Contexto del Vault

**Vault**: Personal-Vault
**Path**: 
  - **Linux**: `/files/Personal-Vault`
  - **Windows**: `C:\Users\lcampassi\Proton Drive\D4rkDr4g0n19\My files\Personal-Vault`
**CLI**: `obsidian vault=Personal-Vault <command>` (en ambos SO si está en PATH)
**Remote**: `https://github.com/D4rkDr4g0n/<vault>.git`
**Git user**: `D4rkDr4g0n`

### Estructura de carpetas

```
/files/Personal-Vault/
├── .obsidian/                 # Config de Obsidian
├── IMAGES/                    # Imagenes adjuntas
├── INBOX/                     # Captura rapida y bandeja de entrada
│   ├── DOCUMENTS/             # Documentos personales
│   │   ├── LABORAL/
│   │   ├── MIS-FINANZAS/
│   │   │   └── RECIBOS-DE-SUELDO/
│   │   └── OTROS/
│   │       └── Certificaciones/
│   ├── General/               # Notas generales
│   │   ├── fotos/
│   │   ├── LIST/
│   │   └── OTHER/
│   ├── HOME/                  # Cosas del hogar
│   ├── Journal/               # Daily notes
│   │   └── 2026/
│   ├── MAMO/                  # Notas de mama
│   └── TODOLIST/              # Listas de tareas
├── Manuales/                  # Manuales de referencia
├── TEMPLATES/                 # Plantillas
├── UFASTA/                    # Facultad
│   ├── 01-Introduccion a la informatica/
│   ├── 02-Introduccion a la programacion/
│   ├── 03-Taller de comunicacion eficaz/
│   ├── 04-Matematica y logica/
│   ├── 05-Aspectos Legales de la ciberseguridad/
│   ├── 06-CRIPTOGRAFIA/
│   ├── 07-ANTROPOLOGIA 1/
│   ├── 08-CIBERSEGURIDAD 1/
│   ├── 09-INGLES TECNICO/
│   ├── CALENDAR/
│   ├── Other/
│   └── PENDIENTES FACULTAD.md
├── WORK/                      # Trabajo (clientes anonimizados)
│   ├── 00-CLIENTE-A/
│   ├── 01-CLIENTE-B/
│   ├── 02-CLIENTE-C/
│   ├── 03-CLIENTE-D/
│   ├── 2026/
│   └── PENDIENTES TRABAJO.md
└── PENDIENTES FACULTAD.md
└── PENDIENTES TRABAJO.md
```

### Configuracion clave

| Setting | Value |
|---------|-------|
| Daily notes folder | `INBOX/Journal/2026` |
| Daily format | `DD MMMM` (ej: `24 mayo`) |
| Template | `TEMPLATES/Daily note` |
| Use markdown links | `true` |
| Attachment folder | `./attachments` |
| Trash option | none (permanent delete) |
| Prompt delete | false |

### Plugins instalados (19)

`advanced-canvas`, `beautitab`, `calendar`, `code-styler`, `file-explorer-note-count`, `folder-notes`, `full-calendar-remastered`, `highlightr-plugin`, `manual-sorting`, `nerdfont-icon-picker`, `obsidian-better-command-palette`, `obsidian-file-color`, `obsidian-icon-folder`, `obsidian-kanban`, `obsidian-smart-typography`, `ollama`, `oz-clear-unused-images`, `pdf-plus`, `waypoint`

---

## Modo 1: REST API (primer nivel, recomendado para CRUD + UI)

> **Endpoints base**: `https://127.0.0.1:27124`
> **Auth**: `Authorization: Bearer ${OBSIDIAN_API_KEY}`
> **SSL**: `-k` (certificado autofirmado)

### Healthcheck rápido

```bash
curl -sk -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  https://127.0.0.1:27124/
# → 200 si está vivo
```

### Operaciones disponibles

| Operación | Endpoint | Método | Descripción |
|-----------|----------|--------|-------------|
| **Listar vault** | `/vault/` | GET | Lista raíz del vault |
| **Listar carpeta** | `/vault/ruta/` | GET | Lista contenido de carpeta |
| **Leer nota** | `/vault/ruta/nota.md` | GET | Lee contenido completo |
| **Leer heading** | `/vault/ruta/nota.md/heading/Sección` | GET | Lee sección específica |
| **Crear nota** | `/vault/ruta/nota.md` | PUT | Crea o sobrescribe |
| **Editar nota** | `/vault/ruta/nota.md` | POST | Agrega contenido (append) |
| **Patch heading** | `/vault/ruta/nota.md` | PATCH | Edición quirúrgica |
| **Eliminar nota** | `/vault/ruta/nota.md` | DELETE | Borra la nota |
| **Abrir en UI** | `/open/ruta/nota.md` | POST | Abre en la interfaz gráfica |
| **Buscar texto** | `/search/simple/?query=...` | POST | Búsqueda full-text |
| **Buscar JsonLogic** | `/search/` | POST | Búsqueda estructurada |
| **Tags** | `/tags/` | GET | Todos los tags con counts |
| **Comandos** | `/commands/` | GET | Lista comandos disponibles |
| **Ejecutar comando** | `/commands/{id}/` | POST | Ejecuta un comando |
| **Nota activa** | `/active/` | GET | Nota abierta en UI |
| **Nota periódica** | `/periodic/daily/` | GET | Nota del día |

### Ejemplos concretos

```bash
# Leer nota
curl -sk -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "https://127.0.0.1:27124/vault/INBOX/General/OTHER/Clave%20de%20windows%2011%20PRO.md"

# Abrir nota en la UI
curl -sk -X POST \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "https://127.0.0.1:27124/open/INBOX/General/OTHER/Clave%20de%20windows%2011%20PRO.md"

# Crear nota (PUT)
curl -sk -X PUT \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  -H "Content-Type: text/markdown" \
  --data "# Mi nueva nota\n\nContenido" \
  "https://127.0.0.1:27124/vault/INBOX/General/mi-nota.md"

# Buscar texto
curl -sk -X POST \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "https://127.0.0.1:27124/search/simple/?query=windows+key"

# Listar tags
curl -sk -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "https://127.0.0.1:27124/tags/"

# Ejecutar comando (ej: guardar)
curl -sk -X POST \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "https://127.0.0.1:27124/commands/editor:save-file/"

# Patch quirúrgico: reemplazar frontmatter
curl -sk -X PATCH \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  -H "Operation: replace" \
  -H "Target-Type: frontmatter" \
  -H "Target: status" \
  -H "Content-Type: application/json" \
  --data '"done"' \
  "https://127.0.0.1:27124/vault/INBOX/mi-nota.md"
```

---

## Modo 2: MCP (segundo nivel, para operaciones avanzadas)

> **Endpoint**: `https://127.0.0.1:27124/mcp/`
> **Transporte**: Streamable HTTP (requiere inicializar sesión primero)
> **Usar solo cuando**: Tags, search estructurado, patches, nota activa, notas periódicas

### Protocolo MCP (Streamable HTTP)

El MCP requiere **2 requests**:

**Paso 1**: Inicializar sesión (obtener `mcp-session-id`)

```bash
RESP=$(curl -sk -i -X POST "https://127.0.0.1:27124/mcp/" \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"opencode","version":"1.0.0"}}}')

# Extraer session ID del header
MCP_SESSION=$(echo "$RESP" | grep -i "^mcp-session-id:" | awk '{print $2}' | tr -d '\r')
```

**Paso 2**: Usar la sesión para cualquier herramienta MCP

```bash
curl -sk -X POST "https://127.0.0.1:27124/mcp/" \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: ${MCP_SESSION}" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"NOMBRE_TOOL","arguments":{...}}}'
```

### MCP Tools disponibles (16 herramientas)

| Tool | Args | Descripción |
|------|------|-------------|
| `vault_list` | `path` (str) | Listar archivos en directorio |
| `vault_read` | `path` (str) | Leer nota (content + frontmatter + tags + stat) |
| `vault_write` | `path` (str), `content` (str) | Crear/sobrescribir nota |
| `vault_append` | `path` (str), `content` (str) | Agregar al final |
| `vault_patch` | `path` (str), `targetType` (str), `target` (str), `operation` (str), `content` (str), `targetScope` (int, opcional) | Patch quirúrgico |
| `vault_delete` | `path` (str) | Eliminar nota |
| `vault_move` | `from` (str), `to` (str) | Mover/renombrar |
| `vault_get_document_map` | `path` (str) | Headings, blocks, frontmatter |
| `active_file_get_path` | _(none)_ | Ruta de la nota activa |
| `periodic_note_get_path` | `period` (str: daily/weekly/monthly/quarterly/yearly) | Ruta de nota periódica |
| `search_query` | `query` (object, JsonLogic) | Búsqueda estructurada |
| `search_simple` | `query` (str) | Búsqueda full-text |
| `tag_list` | _(none)_ | Tags con counts |
| `command_list` | _(none)_ | Comandos registrados |
| `command_execute` | `commandId` (str) | Ejecutar comando |
| `open_file` | `path` (str) | Abrir en UI |

### Ejemplo MCP completo

```bash
# 1. Inicializar sesión
SESSION_RESP=$(curl -sk -i -X POST "https://127.0.0.1:27124/mcp/" \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"opencode","version":"1.0.0"}}}')

SID=$(echo "$SESSION_RESP" | grep -ia "mcp-session-id" | head -1 | sed 's/.*: //' | tr -d '\r\n')

# 2. Listar tags (solo MCP puede hacerlo con metadata completa)
curl -sk -X POST "https://127.0.0.1:27124/mcp/" \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: ${SID}" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"tag_list","arguments":{}}}'
```

---

## Modo 3: Filesystem (fallback universal, sin dependencias)

> Usar cuando Obsidian esté cerrado o para operaciones masivas.
> **Ventaja**: No requiere red, es lo más rápido para leer/escribir archivos completos.

### Operaciones básicas

```bash
# Leer archivo
cat "/files/Personal-Vault/ruta/nota.md"

# Buscar (grep/rg)
rg -r "patrón" "/files/Personal-Vault/" --include "*.md"

# Escribir archivo
cat > "/files/Personal-Vault/ruta/nota.md" << 'EOF'
---
tags: [ejemplo]
---
# Contenido
EOF

# Listar directorio
ls "/files/Personal-Vault/ruta/"
```

---

## Tabla de ruteo completa (qué usar y cuándo)

| Operación | Canal preferente | Por qué | Fallback |
|-----------|-----------------|---------|----------|
| **Leer nota** | 🥇 Filesystem | Sin red, instantáneo | REST API |
| **Listar directorio** | 🥇 Filesystem | `ls` / `rg` directo | REST API |
| **Buscar keyword** | 🥇 Filesystem | `rg` / `grep` masivo | REST API search |
| **Buscar por tags** | 🥇 REST API | `GET /tags/` + filtro | MCP |
| **Tags + counts** | 🥇 REST API | `GET /tags/` (1 request) | MCP tag_list |
| **Crear nota** | 🥇 REST API | `PUT` + validación | Filesystem |
| **Editar nota completa** | 🥇 REST API | `PUT` reemplazo completo | Filesystem |
| **Abrir nota en UI** | 🥇 REST API | `POST /open/{path}` (1 request) | MCP open_file |
| **Patch quirúrgico** | 🥇 MCP | `vault_patch` con targeting preciso | REST API PATCH |
| **Nota activa** | 🥇 MCP | `active_file_get_path` | REST API `/active/` |
| **Notas periódicas** | 🥇 REST API | `GET /periodic/daily/` | MCP |
| **Ejecutar comandos** | 🥇 REST API | `POST /commands/{id}/` | MCP command_execute |
| **Búsqueda JsonLogic** | 🥇 MCP | `search_query` con filtros complejos | — |
| **Document map** | 🥇 MCP | `vault_get_document_map` | — |

---

## Convenciones de namescape URL encoding

Al usar la REST API, los espacios y caracteres especiales en rutas deben escaparse:

| Carácter | Encoding |
|----------|----------|
| Espacio | `%20` |
| `#` | `%23` |
| `?` | `%3F` |
| `&` | `%26` |
| `ñ` | `%C3%B1` |
| `Ñ` | `%C3%91` |
| `áéíóú` | `%C3%A1%C3%A9%C3%AD%C3%B3%C3%BA` |

**Alternativa**: Usar `printf` para escapar automáticamente:
```bash
ENCODED_PATH=$(python3 -c "import urllib.parse; print(urllib.parse.quote('INBOX/General/OTHER/Clave de windows 11 PRO.md'))")
```

---

## Templates disponibles

| Template | File | Uso |
|----------|------|-----|
| Daily note | `TEMPLATES/Daily note.md` | Nota diaria con secciones de resumen, importante, reflexiones, aprendizaje, estado |
| Notas generales | `TEMPLATES/Notas generales.md` | Nota de conocimiento general (tag `KNOWLEDGE`) |
| MOCs | `TEMPLATES/MOCs.md` | Mapas de contenido (tag `INDEX`, `MOCs`) |
| NOTA FACULTAD | `TEMPLATES/NOTA FACULTAD.md` | Nota de la facultad (tag `ciberseguridad`, `UNIVERSIDAD`) |
| Ticket | `TEMPLATES/Ticket - {{DATE}}.md` | Ticket tecnico con RCA, resolucion, lecciones (incluye HTML para OsTicket) |

### Crear nota desde template vía REST API

```bash
# Primero leer template
TEMPLATE=$(curl -sk -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "https://127.0.0.1:27124/vault/TEMPLATES/Notas%20generales.md")

# Luego crear nota con ese contenido (adaptado)
curl -sk -X PUT \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  -H "Content-Type: text/markdown" \
  --data "${TEMPLATE}" \
  "https://127.0.0.1:27124/vault/INBOX/General/mi-nota.md"
```

---

## Flujos de trabajo comunes (versión optimizada)

### 1. Captura rápida (INBOX) — REST API

```bash
curl -sk -X PUT \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  -H "Content-Type: text/markdown" \
  --data "# Título\n\nContenido rápido" \
  "https://127.0.0.1:27124/vault/INBOX/General/mi-nota.md"
```

### 2. Leer daily note — REST API

```bash
curl -sk -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "https://127.0.0.1:27124/periodic/daily/"
```

### 3. Buscar y abrir — REST API

```bash
# 1. Buscar
RESULT=$(curl -sk -X POST \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "https://127.0.0.1:27124/search/simple/?query=clave+windows")

# 2. Abrir el primer resultado
FILE=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)[0]['filename'])")
curl -sk -X POST \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "https://127.0.0.1:27124/open/${FILE}"
```

### 4. Editar frontmatter de una nota — REST API PATCH

```bash
curl -sk -X PATCH \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  -H "Operation: replace" \
  -H "Target-Type: frontmatter" \
  -H "Target: estado" \
  -H "Content-Type: application/json" \
  --data '"revisado"' \
  "https://127.0.0.1:27124/vault/INBOX/mi-nota.md"
```

### 5. Ver tags y counts — REST API

```bash
curl -sk -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "https://127.0.0.1:27124/tags/"
```

### 6. Ejecutar comando de Obsidian — REST API

```bash
curl -sk -X POST \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "https://127.0.0.1:27124/commands/editor:save-file/"
```

### 7. Git Sync

```bash
# Pull desde GitHub
bash ~/dotfiles/automat/vault-pull.sh

# Push a GitHub (commitea con fecha)
bash ~/dotfiles/automat/vault-push.sh
```

---

## Healthcheck completo del stack

Script para verificar que todo funciona:

```bash
#!/bin/bash
# Verificar conectividad con Obsidian en todos los modos

API_KEY="${OBSIDIAN_API_KEY}"
BASE="https://127.0.0.1:27124"
VAULT="/files/Personal-Vault"

echo "=== Healthcheck Obsidian ==="

# 1. REST API
HTTP_CODE=$(curl -sk -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer ${API_KEY}" \
  "${BASE}/" 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
  echo "✅ REST API: OK (${BASE})"
  
  # 1b. Tags (operación clave)
  TAGS=$(curl -sk -H "Authorization: Bearer ${API_KEY}" \
    "${BASE}/tags/" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d.get(\"tags\",[]))} tags')" 2>/dev/null)
  echo "   Tags: ${TAGS:-error}"
  
  # 1c. Search
  SEARCH=$(curl -sk -X POST \
    -H "Authorization: Bearer ${API_KEY}" \
    "${BASE}/search/simple/?query=test" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d)} resultados')" 2>/dev/null)
  echo "   Search: ${SEARCH:-error}"
else
  echo "❌ REST API: No disponible"
fi

# 2. MCP
MCP_INIT=$(curl -sk -X POST "${BASE}/mcp/" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"opencode","version":"1.0.0"}}}' 2>/dev/null)
SID=$(echo "$MCP_INIT" | grep -ia "mcp-session-id" | head -1 | sed 's/.*: //' | tr -d '\r\n')
if [ -n "$SID" ]; then
  echo "✅ MCP: OK (session: ${SID})"
  
  # Probar tag_list via MCP
  MCP_TAGS=$(curl -sk -X POST "${BASE}/mcp/" \
    -H "Authorization: Bearer ${API_KEY}" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -H "Mcp-Session-Id: ${SID}" \
    -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"tag_list","arguments":{}}}' 2>/dev/null)
  echo "   MCP tags: OK"
else
  echo "❌ MCP: No disponible"
fi

# 3. Filesystem
if [ -d "$VAULT" ]; then
  echo "✅ Filesystem: OK (${VAULT})"
  echo "   Notas: $(find ${VAULT} -name '*.md' | wc -l)"
else
  echo "❌ Filesystem: No encontrado"
fi
```

---

## Notas importantes

- El REST API y MCP requieren que **Obsidian esté abierto**
- El filesystem **no requiere** Obsidian, pero no soporta tags, frontmatter queries, ni comandos
- Siempre codificar URLs con `%20` para espacios (o usar `python3 -c "import urllib.parse; print(urllib.parse.quote(path))"`)
- El vault usa `useMarkdownLinks: true` — los links internos son rutas relativas `.md`
- `trashOption: none` — los archivos borrados se pierden permanentemente
- Para **operaciones batch** (múltiples archivos), siempre preferir filesystem
- Para **operaciones interactivas** (abrir en UI, comandos), siempre preferir REST API
- Para **operaciones de metadata** (tags, frontmatter, patches), priorizar MCP

---

## Aliases recomendados para `.zshrc`

```zsh
# CLI de Obsidian
alias ov='obsidian vault=Personal-Vault'
alias ovd='obsidian vault=Personal-Vault daily'
alias ovs='obsidian vault=Personal-Vault search'
alias ovt='obsidian vault=Personal-Vault tasks'

# REST API directa
alias ob='curl -sk -H "Authorization: Bearer ${OBSIDIAN_API_KEY}"'
alias ob-open='ob -X POST "https://127.0.0.1:27124/open"'
alias ob-read='ob "https://127.0.0.1:27124/vault"'
alias ob-tags='ob "https://127.0.0.1:27124/tags"'
alias ob-search='ob -X POST "https://127.0.0.1:27124/search/simple/?query"'

# Git sync
alias ovpush='bash ~/dotfiles/automat/vault-push.sh'
alias ovpull='bash ~/dotfiles/automat/vault-pull.sh'
```
