---
name: obsidian-manager
description: >
  Gestión completa del vault Obsidian Personal-Vault (Babilonia).
  Opera en 3 modos (REST API, MCP, Filesystem), usa templates con ID registry,
  búsqueda semántica multi-estrategia, y respeta permisos estrictos por zona.
  Único skill autorizado para leer/escribir en el vault desde agentes.
---

# obsidian-manager ⚡

## ⚡ Resumen Ejecutivo

Este skill es la **única puerta de entrada autorizada** para que cualquier agente de OpenCODE interactúe con el vault Babilonia. Opera en **3 modos**, en orden de preferencia:

| Modo | Canal | Ideal para |
|------|-------|------------|
| **1. Filesystem** | `cat`, `rg`, lectura/escritura directa de archivos | Leer/escribir archivos completos, búsquedas masivas con `rg` |
| **2. REST API** | `curl -k https://127.0.0.1:27124/vault/...` | CRUD + Abrir en UI + Search estructurado (1 request) |
| **3. MCP** | `POST /mcp/` (con session ID, 2 requests) | Tags, patches quirúrgicos, nota activa, búsqueda JsonLogic |

**Regla de decisión:**
- Si es **leer o escribir un archivo completo** → **Filesystem** (sin red, instantáneo)
- Si es **CRUD + abrir en UI + search** → **REST API** (1 request, sin sesión)
- Si es **tags + patches + nota activa + search estructurado** → **MCP** (requiere sesión)
- Si no responde REST API ni MCP → **Filesystem** como fallback universal

---

## 🧩 Variables de Entorno — Único Origen de Verdad

> ⚠️ **No existe ninguna ruta absoluta hardcodeada en este skill.**
> TODO se resuelve vía env vars definidas en `~/.zshenv`.

| Variable | Valor | Propósito |
|----------|-------|-----------|
| `$BABILONIA` | Raíz del vault | Path base para TODAS las operaciones |
| `$BABILONIA_OPENCODE` | `$BABILONIA/.../03-OPENCODE-AGENTS-SKILLS` | Docs de agentes, skills, ID registry |
| `$OBSIDIAN_API_KEY` | API key | Autenticación REST API y MCP |
| `$DOTFILES` | `~/dotfiles` | Scripts auxiliares (git sync, etc.) |
| `$GITHUB_USER` | Usuario GitHub | Remote del vault |

**Derivadas (si no existen, se construyen en el momento):**

```bash
OBSIDIAN_URL="${OBSIDIAN_URL:-https://127.0.0.1:27124}"
TEMPLATE_NOTA="${TEMPLATE_NOTA:-$BABILONIA/TEMPLATES/Notas generales.md}"
TEMPLATE_MOC="${TEMPLATE_MOC:-$BABILONIA/TEMPLATES/MOCs.md}"
ID_REGISTRY="${ID_REGISTRY:-$BABILONIA_OPENCODE/ID-REGISTRY.md}"
NEXT_ID_SCRIPT="${NEXT_ID_SCRIPT:-$BABILONIA/BIBLIOTECA-DE-BABEL/05-PRACTICAL-RESOURCES/01-SCRIPTS/PYTHON/next-id.py}"
```

> Cualquier referencia a paths dentro del vault **siempre** usa `$BABILONIA/...`.  
> Cualquier referencia a scripts **siempre** usa su env var correspondiente.

---

## 🔌 Detección Automática de Conectividad

Antes de operar, verificá qué canales están disponibles:

```bash
# 1. REST API disponible?
REST_OK=$(curl -sk -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "${OBSIDIAN_URL}/" 2>/dev/null)

# 2. Filesystem disponible? (siempre que $BABILONIA exista)
FS_OK=$([ -d "$BABILONIA" ] && echo "yes" || echo "no")
```

---

## 📝 Templates Obligatorios

Toda nota o MOC que se cree **debe** usar el template correspondiente.  
No se crean notas sin template — el contenido se adapta del template al caso concreto.

### Template: Nota General

**Ubicación:** `$TEMPLATE_NOTA` → `$BABILONIA/TEMPLATES/Notas generales.md`

```markdown
---
id: MAN-XXXXXX
nombre: "{{title}}"
tags:
  - KNOWLEDGE
  - KNOWLEDGE/IT
Fecha de creación: "{{date}}"
---
# OBJETIVO
>[!tip] 

# DESCRIPCIÓN
```

**Reglas de uso:**
- El `id:` se genera con `next-id MAN` (ver sección ID Registry)
- `nombre:` debe ser descriptivo, en español, con el título real de la nota
- `tags:` mantener `KNOWLEDGE` + agregar tags específicos del dominio
- La sección `OBJETIVO` debe responder: *¿Qué problema resuelve o qué concepto explica esta nota?*
- La sección `DESCRIPCIÓN` debe ser clara, estructurada y fácil de entender para alguien que la lea 6 meses después

### Template: MOC (Map of Content)

**Ubicación:** `$TEMPLATE_MOC` → `$BABILONIA/TEMPLATES/MOCs.md`

```markdown
---
id: MOC-XXXXXX
nombre: "{{title}}"
tags:
  - INDEX
  - MOCs
Fecha de creación: "{{date}}"
---
# {{TITLE}}
>[!tip] Descripcion de la carpeta
# INDICE
%% WAYPOINT %%
>Borrar esto y cambiar WAYPOINT a Waypoint
```

**Reglas de uso:**
- El `id:` se genera con `next-id MOC`
- `nombre:` debe reflejar el dominio/área que indexa
- La descripción en `[!tip]` debe resumir qué agrupa este MOC
- El `%% WAYPOINT %%` se reemplaza por `%% Waypoint %%` (activa el plugin)

---

## 🆔 Sistema de IDs — ID Registry

**Documentación completa:** `$ID_REGISTRY`  
**Script:** `$NEXT_ID_SCRIPT` (o alias global `next-id` si está configurado)

### Cómo generar un ID

```bash
# Para una NOTA general → prefijo MAN
next-id MAN
# → MAN-001237

# Para un MOC → prefijo MOC
next-id MOC
# → MOC-000018

# Para un prefijo nuevo (se auto-descubre)
next-id MI_PROYECTO
# → MI_PROYECTO-000001
```

### Reglas de asignación

| Tipo de contenido | Prefijo | Formato |
|------------------|---------|---------|
| Nota de conocimiento general | `MAN` | `MAN-######` |
| Map of Content (MOC) | `MOC` | `MOC-######` |
| Nota de facultad | `UFA` | `UFA-######` |
| Nota diaria (journal) | `JOURNAL` | `JOURNAL-####` |
| Otro (auto-descubierto) | *cualquiera* | `PREFIJO-######` |

> ⚠️ Los prefijos de clientes/ trabajo no se listan en este skill por privacidad. Se resuelven via `next-id <prefijo>` en el momento.

> **Siempre** ejecutar `next-id <PREFIJO>` justo antes de crear la nota para obtener el ID actualizado.

---

## 🔍 Estrategias de Búsqueda Semántica

El skill soporta **4 estrategias** para buscar información, ordenadas de la más a la menos eficiente según el caso:

### Estrategia 1: `rg` (recomendada para búsquedas rápidas y precisas)

```bash
# Búsqueda por palabra clave exacta en todos los .md
rg -i "firewall" "$BABILONIA/" -g "*.md"

# Búsqueda por frase exacta
rg -i "política de backup" "$BABILONIA/" -g "*.md"

# Búsqueda en frontmatter (tags, id, nombre)
rg -i "tags:.*MOCs" "$BABILONIA/" -g "*.md" --no-heading

# Búsqueda combinando múltiples términos (líneas que contengan ambos)
rg -i "windows" "$BABILONIA/" -g "*.md" | rg -i "registry"

# Contar ocurrencias
rg -c "linux" "$BABILONIA/" -g "*.md"
```

**Cuándo usarla:** Búsqueda rápida, offline (Obsidian cerrado), resultados sin filtro.

### Estrategia 2: REST API Search (recomendada para búsqueda desde Obsidian abierto)

```bash
# Búsqueda full-text simple
curl -sk -X POST \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "${OBSIDIAN_URL}/search/simple/?query=firewall+config"

# Búsqueda con filtro por path (solo en una carpeta)
curl -sk -X POST \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "${OBSIDIAN_URL}/search/simple/?query=firewall&path=BIBLIOTECA-DE-BABEL"
```

**Cuándo usarla:** Obsidian abierto, se necesita resultado estructurado JSON, paths limpios.

### Estrategia 3: MCP Search (recomendada para búsqueda semántica estructurada)

```bash
# Inicializar sesión MCP (si no se tiene una activa)
SID=$(curl -sk -i -X POST "${OBSIDIAN_URL}/mcp/" \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"opencode","version":"1.0.0"}}}' \
  | grep -ia "mcp-session-id" | head -1 | sed 's/.*: //' | tr -d '\r\n')

# Búsqueda JsonLogic (estructurada, potente)
curl -sk -X POST "${OBSIDIAN_URL}/mcp/" \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: ${SID}" \
  -d '{
    "jsonrpc":"2.0",
    "id":2,
    "method":"tools/call",
    "params":{
      "name":"search_query",
      "arguments":{
        "query": {
          "and": [
            {"or": [{"path": {"contains": "BIBLIOTECA-DE-BABEL"}}, {"path": {"contains": "EL-EMPORIO"}}]},
            {"content": {"contains": "firewall"}}
          ]
        }
      }
    }
  }'
```

**Cuándo usarla:** Búsqueda con múltiples condiciones (path + contenido + tags), filtros anidados.

### Estrategia 4: Tags (recomendada para navegación por categorías)

```bash
# Listar todos los tags con su frecuencia
curl -sk -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "${OBSIDIAN_URL}/tags/"

# Buscar notas con un tag específico vía rg (filesystem)
rg "tags:.*KNOWLEDGE" "$BABILONIA/" -g "*.md" --no-heading -l
```

**Cuándo usarla:** Para entender la estructura temática del vault, o filtrar por dominio.

### Tabla de ruteo de búsqueda

| Situación | Estrategia | Comando |
|-----------|-----------|---------|
| Offline, búsqueda rápida | `rg` (FS) | `rg "término" $BABILONIA -g "*.md"` |
| Online, quiero JSON estructurado | REST API Search | `POST /search/simple/?query=...` |
| Búsqueda compleja (path + content + tags) | MCP JsonLogic | `tools/call search_query` |
| Quiero explorar categorías | Tags | `GET /tags/` |
| Quiero abrir el resultado en UI | REST API + Open | Search → `POST /open/{path}` |

---

## 📖 Flujo Completo: Crear una Nota de Conocimiento

```bash
# 1. Obtener ID único
NOTE_ID=$(next-id MAN)
# → MAN-001237

# 2. Obtener el template
TEMPLATE=$(cat "$TEMPLATE_NOTA")

# 3. Adaptar el template
#    - Reemplazar MAN-XXXXXX por $NOTE_ID
#    - Reemplazar {{title}} por el título real
#    - Reemplazar {{date}} por la fecha actual
#    - Completar OBJETIVO y DESCRIPCIÓN con contenido descriptivo

CONTENT=$(echo "$TEMPLATE" | sed \
  -e "s/MAN-XXXXXX/$NOTE_ID/" \
  -e "s/{{title}}/Mi título descriptivo/" \
  -e "s/{{date}}/$(date '+%Y-%m-%d')/" \
  -e '/^# OBJETIVO/a\
> Entender cómo funciona X concepto para aplicarlo en Y contexto.' \
  -e '/^# DESCRIPCIÓN/a\
\
## ¿Qué es?\
Breve definición.\
\
## ¿Cómo funciona?\
Explicación del mecanismo.\
\
## Ejemplo práctico\
Código o caso de uso.\
\
## Referencias\
Links a notas relacionadas.')

# 4. Guardar la nota (elegir método)
# Opción A: Filesystem
echo "$CONTENT" > "$BABILONIA/BIBLIOTECA-DE-BABEL/00-FUNDAMENTALS/mi-nota.md"

# Opción B: REST API
curl -sk -X PUT \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  -H "Content-Type: text/markdown" \
  --data-raw "$CONTENT" \
  "${OBSIDIAN_URL}/vault/BIBLIOTECA-DE-BABEL/00-FUNDAMENTALS/mi-nota.md"

# 5. Abrir en UI (para verificar)
curl -sk -X POST \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "${OBSIDIAN_URL}/open/BIBLIOTECA-DE-BABEL/00-FUNDAMENTALS/mi-nota.md"

# 6. Ofrecer resumen al usuario
echo "✅ Nota creada: $NOTE_ID — Mi título descriptivo"
echo "📂 $BABILONIA/BIBLIOTECA-DE-BABEL/00-FUNDAMENTALS/mi-nota.md"
echo "🔗 Abierta en Obsidian UI"
```

---

## 📖 Flujo Completo: Crear un MOC

```bash
# 1. Obtener ID único
MOC_ID=$(next-id MOC)
# → MOC-000018

# 2. Obtener el template
TEMPLATE=$(cat "$TEMPLATE_MOC")

# 3. Adaptar el template
CONTENT=$(echo "$TEMPLATE" | sed \
  -e "s/MOC-XXXXXX/$MOC_ID/" \
  -e "s/{{title}}/Mapa de Contenido - Mi Dominio/" \
  -e "s/{{TITLE}}/Mapa de Contenido - Mi Dominio/" \
  -e "s/{{date}}/$(date '+%Y-%m-%d')/" \
  -e 's/%% WAYPOINT %%/%% Waypoint %%' \
  -e 's/Descripcion de la carpeta/Índice de todos los recursos relacionados con Mi Dominio/')

# 4. Guardar
echo "$CONTENT" > "$BABILONIA/BIBLIOTECA-DE-BABEL/mi-dominio/_MOC_.md"

# 5. Abrir en UI
curl -sk -X POST \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "${OBSIDIAN_URL}/open/BIBLIOTECA-DE-BABEL/mi-dominio/_MOC_.md"
```

---

## 📖 Flujo: Buscar y Mostrar en UI (Obligatorio al Responder)

> **Cada vez que un usuario pregunte por información que existe en el vault, el agente DEBE:**
> 1. Buscar la nota en el vault
> 2. Leer su contenido
> 3. **Ofrecer activamente abrirla en la UI** (`POST /open/{path}`)
> 4. Presentar un resumen de lo encontrado

```bash
# 1. Buscar
RESULTADOS=$(rg -i "firewall" "$BABILONIA/" -g "*.md" -l)
# o via REST API:
# RESULTADOS=$(curl -sk -X POST ... /search/simple/?query=firewall)

# 2. Si hay resultado único → leer y mostrar
if [ -f "$RESULTADOS" ]; then
  # 3. Abrir en UI
  REL_PATH=${RESULTADOS#$BABILONIA/}
  ENCODED_PATH=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$REL_PATH'))")
  
  curl -sk -X POST \
    -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
    "${OBSIDIAN_URL}/open/${ENCODED_PATH}"
  
  # 4. Leer y mostrar resumen
  echo "### 📄 Encontrado: $REL_PATH"
  echo "🔗 Abierto en Obsidian UI"
  head -30 "$RESULTADOS"
fi
```

---

## 🔒 Permisos y Restricciones

### Zonas del Vault

Este skill es el **único autorizado** para acceder al vault. Cualquier agente que necesite leer/escribir notas **debe pasar por este skill**.

| Zona | Acceso por defecto | Acción permitida | Excepción |
|------|-------------------|------------------|-----------|
| `$BABILONIA/BIBLIOTECA-DE-BABEL/**` | ✅ **Allow** | CRUD total (crear, leer, modificar, borrar) | — |
| `$BABILONIA/TEMPLATES/**` | ✅ **Allow** | Solo lectura (los templates no se modifican) | — |
| `$BABILONIA/EL-EMPORIO/**` | ✅ **Allow** | CRUD total en notas de trabajo | — |
| `$BABILONIA/EL-OBSERVATORIO-DE-BABILONIA/**` | ✅ **Allow** | CRUD total en notas de facultad | — |
| `$BABILONIA/LA-VIA-PROCESIONAL/**` | ✅ **Allow** | Lectura de imágenes y capturas adjuntas | — |
| `$BABILONIA/INBOX/**` | ❌ **ASK** | **No accesible sin permiso explícito del usuario** | Preguntar siempre |
| `$BABILONIA/.obsidian/**` | ❌ **Deny** | Config interna de Obsidian | Solo si el usuario lo pide explícitamente |
| `$BABILONIA/.git/**` | ❌ **Deny** | Directorio git | Solo si el usuario lo pide explícitamente |
| Cualquier otra ruta no listada | ❓ **ASK** | Preguntar al usuario antes de acceder | — |

### Reglas para Agentes que usan este skill

1. **Nunca** accedas a `$BABILONIA/INBOX/` sin preguntar primero al usuario.
2. **Nunca** modifiques `.obsidian/` ni `.git/` a menos que el usuario lo ordene explícitamente.
3. **Siempre** que leas una nota del vault, ofrecé abrirla en la UI de Obsidian.
4. **Siempre** que crees una nota, usá el template correspondiente y generá el ID con `next-id`.
5. **Siempre** priorizá rutas relativas a `$BABILONIA` — nunca absolutas.

---

## ⚙️ Cross-Platform

| Recurso | Linux | Windows |
|---------|-------|---------|
| Vault root | `$BABILONIA` | `$BABILONIA` (definido en el entorno) |
| REST API | `https://127.0.0.1:27124` | `https://127.0.0.1:27124` |
| CLI Obsidian | `obsidian vault=Personal-Vault ...` | `obsidian vault=Personal-Vault ...` |
| Git sync scripts | `$DOTFILES/automat/vault-pull.sh` / `vault-push.sh` | *(idem si existe)* |

---

## 📋 Tabla de Ruteo Completa: Operación → Canal

| Operación | Canal preferente | Por qué | Fallback |
|-----------|-----------------|---------|----------|
| **Leer nota** | 🥇 Filesystem | `cat` instantáneo, sin red | REST API |
| **Listar directorio** | 🥇 Filesystem | `ls` directo, sin dep | REST API |
| **Buscar keyword (rg)** | 🥇 Filesystem | `rg` masivo, offline | REST API search |
| **Buscar por tags** | 🥇 REST API | `GET /tags/` + filtro | MCP tag_list |
| **Crear nota** | 🥇 REST API | `PUT` + validación | Filesystem |
| **Editar nota completa** | 🥇 REST API | `PUT` reemplazo completo | Filesystem |
| **Abrir nota en UI** | 🥇 REST API | `POST /open/{path}` (1 request) | MCP open_file |
| **Patch quirúrgico** | 🥇 MCP | `vault_patch` preciso | REST API PATCH |
| **Nota activa** | 🥇 MCP | `active_file_get_path` | REST API `/active/` |
| **Notas periódicas** | 🥇 REST API | `GET /periodic/daily/` | MCP |
| **Ejecutar comandos** | 🥇 REST API | `POST /commands/{id}/` | MCP command_execute |
| **Búsqueda JsonLogic** | 🥇 MCP | `search_query` con filtros | — |
| **Document map** | 🥇 MCP | `vault_get_document_map` | — |

---

## ⚠️ Notas y Consideraciones

- **Obsidian debe estar abierto** para usar REST API y MCP. Filesystem funciona siempre.
- **URL encoding:** Los espacios en paths se escapan con `%20` o usando:
  ```bash
  python3 -c "import urllib.parse; print(urllib.parse.quote('$REL_PATH'))"
  ```
- **Trash:** El vault usa `trashOption: none` — los borrados son permanentes. Confirmar siempre antes de borrar.
- **Links:** El vault usa `useMarkdownLinks: true` — los links internos son rutas relativas `.md`.
- **IOps:** Para operaciones batch (múltiples archivos), preferir **Filesystem**. Para operaciones interactivas, preferir **REST API**.

---

## 🩺 Healthcheck Rápido

```bash
echo "=== Healthcheck Obsidian Manager ==="

# 1. Filesystem
[ -d "$BABILONIA" ] && echo "✅ Filesystem: $BABILONIA" || echo "❌ Filesystem: no encontrado"

# 2. REST API
HTTP=$(curl -sk -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "${OBSIDIAN_URL}/" 2>/dev/null)
[ "$HTTP" = "200" ] && echo "✅ REST API: ${OBSIDIAN_URL}" || echo "❌ REST API: no disponible"

# 3. Tags
curl -sk -H "Authorization: Bearer ${OBSIDIAN_API_KEY}" \
  "${OBSIDIAN_URL}/tags/" 2>/dev/null | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f'   Tags: {len(d.get(\"tags\",[]))}')" 2>/dev/null

# 4. next-id disponible
NEXTID=$(command -v next-id 2>/dev/null || echo "$NEXT_ID_SCRIPT")
[ -n "$NEXTID" ] && echo "✅ next-id: $NEXTID" || echo "⚠️ next-id: no encontrado (usar script directo)"

# 5. Templates
[ -f "$TEMPLATE_NOTA" ] && echo "✅ Template nota: ok" || echo "⚠️ Template nota: no encontrado"
[ -f "$TEMPLATE_MOC" ] && echo "✅ Template MOC: ok" || echo "⚠️ Template MOC: no encontrado"
```

---

## 📚 Referencias Rápidas

- **ID Registry completo:** `$ID_REGISTRY`
- **Script next-id:** `$NEXT_ID_SCRIPT`
- **Alias útil (agregar a zshrc):**
  ```zsh
  alias ov='obsidian vault=Personal-Vault'
  alias ob='curl -sk -H "Authorization: Bearer ${OBSIDIAN_API_KEY}"'
  alias ob-open='ob -X POST "${OBSIDIAN_URL}/open"'
  alias ob-read='ob "${OBSIDIAN_URL}/vault"'
  alias ob-tags='ob "${OBSIDIAN_URL}/tags"'
  alias ob-search='ob -X POST "${OBSIDIAN_URL}/search/simple/?query"'
  ```
