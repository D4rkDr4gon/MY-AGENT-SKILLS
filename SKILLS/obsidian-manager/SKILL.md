---
name: obsidian-manager
description: Use when the user asks about managing their Obsidian vault, taking notes, creating notes from templates, searching, managing tasks, daily notes, or syncing their Personal-Vault at /files/Personal-Vault via the obsidian CLI.
---

# obsidian-manager

## Contexto del Vault

**Vault**: Personal-Vault
**Path**: `/files/Personal-Vault`
**CLI**: `obsidian vault=Personal-Vault <command>`
**Remote**: `https://github.com/<usuario>/<vault>.git`
**Git user**: `<usuario>`

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

## CLI de Obsidian

### Uso basico

```bash
obsidian vault=Personal-Vault <comando> [opciones]
```

### Sintaxis general

| Parametro | Descripcion |
|-----------|-------------|
| `file=<name>` | Resuelve por nombre (como wikilinks) |
| `path=<path>` | Ruta exacta (`folder/note.md`) |
| `content=<text>` | Contenido (usar `\n` para saltos, `\t` para tabs) |
| `format=json\|tsv\|csv` | Formato de salida |
| `total` | Devuelve solo el conteo |
| `verbose` | Info detallada |

---

### Comandos por categoria

#### Creacion y edicion

| Comando | Descripcion |
|---------|-------------|
| `create name=<n> path=<p> content=<t>` | Crear nota |
| `create name=<n> template=<t>` | Crear desde template |
| `unique name=<n> content=<t>` | Crear nota unica (evita duplicados) |
| `append file=<n> content=<t>` | Agregar contenido al final |
| `prepend file=<n> content=<t>` | Agregar contenido al inicio |
| `rename file=<n> name=<new>` | Renombrar archivo |
| `move file=<n> to=<path>` | Mover a otra carpeta |
| `delete file=<n>` | Eliminar archivo |

#### Lectura y consulta

| Comando | Descripcion |
|---------|-------------|
| `read file=<n>` | Leer contenido |
| `file file=<n>` | Info del archivo |
| `files folder=<p>` | Listar archivos |
| `folders` | Listar carpetas |
| `search query=<text>` | Buscar en el vault |
| `search:context query=<t>` | Buscar con contexto |
| `wordcount file=<n>` | Contar palabras |
| `outline file=<n>` | Mostar encabezados |
| `properties file=<n>` | Ver propiedades (frontmatter) |
| `tags file=<n>` | Ver tags |
| `aliases file=<n>` | Ver alias |
| `backlinks file=<n>` | Ver backlinks |
| `links file=<n>` | Ver outgoing links |

#### Propiedades (Frontmatter)

| Comando | Descripcion |
|---------|-------------|
| `property:read name=<p> file=<n>` | Leer propiedad |
| `property:set name=<p> value=<v> file=<n>` | Establecer propiedad |
| `property:remove name=<p> file=<n>` | Eliminar propiedad |
| `properties total` | Contar propiedades en el vault |

#### Daily Notes

| Comando | Descripcion |
|---------|-------------|
| `daily` | Abrir daily note |
| `daily:read` | Leer daily note |
| `daily:path` | Ruta de la daily |
| `daily:append content=<t>` | Agregar a la daily |
| `daily:prepend content=<t>` | Poner al inicio de la daily |

#### Tasks

| Comando | Descripcion |
|---------|-------------|
| `tasks` | Listar tareas |
| `tasks todo` | Tareas pendientes |
| `tasks done` | Tareas completadas |
| `tasks file=<n>` | Tareas de un archivo |
| `task line=<n> file=<n> done` | Marcar como hecha |
| `task line=<n> file=<n> todo` | Marcar como pendiente |
| `task line=<n> file=<n> toggle` | Alternar estado |

#### Tags

| Comando | Descripcion |
|---------|-------------|
| `tags` | Listar tags |
| `tags counts` | Tags con conteo |
| `tag name=<tag>` | Info de un tag especifico |

#### Templates

| Comando | Descripcion |
|---------|-------------|
| `templates` | Listar templates |
| `template:read name=<n>` | Leer contenido del template |
| `template:read name=<n> resolve` | Resolver variables del template |
| `template:insert name=<n>` | Insertar en archivo activo |

#### Busqueda y navegacion

| Comando | Descripcion |
|---------|-------------|
| `search query=<t>` | Busqueda basica |
| `search:context query=<t>` | Busqueda con contexto |
| `search:open query=<t>` | Abrir panel de busqueda |
| `random` | Nota aleatoria |
| `random:read` | Leer nota aleatoria |
| `recents` | Archivos recientes |
| `open file=<n>` | Abrir archivo |
| `open file=<n> newtab` | Abrir en nueva pestania |

#### Plugin management

| Comando | Descripcion |
|---------|-------------|
| `plugins` | Listar plugins instalados |
| `plugins:enabled` | Plugins habilitados |
| `plugin id=<id>` | Info del plugin |
| `plugin:enable id=<id>` | Habilitar plugin |
| `plugin:disable id=<id>` | Deshabilitar plugin |
| `plugin:install id=<id> enable` | Instalar y habilitar |

#### Vault & Sync

| Comando | Descripcion |
|---------|-------------|
| `vault` | Info del vault |
| `vault info=files\|folders\|size` | Info especifica |
| `reload` | Recargar vault |
| `restart` | Reiniciar Obsidian |
| `sync status` | Estado de sync |
| `sync on\|off` | Reanudar/pausar sync |

#### Bookmarking

| Comando | Descripcion |
|---------|-------------|
| `bookmark file=<p>` | Marcar archivo |
| `bookmark folder=<p>` | Marcar carpeta |
| `bookmark search=<q>` | Marcar busqueda |
| `bookmarks` | Listar marcadores |

#### Developer

| Comando | Descripcion |
|---------|-------------|
| `eval code=<js>` | Ejecutar JavaScript |
| `dev:dom selector=<css>` | Query DOM |
| `dev:css selector=<css>` | Inspeccionar CSS |
| `dev:screenshot path=<f>` | Capturar pantalla |
| `devtools` | Abrir DevTools |

---

## Templates disponibles

| Template | File | Uso |
|----------|------|-----|
| Daily note | `TEMPLATES/Daily note.md` | Nota diaria con secciones de resumen, importante, reflexiones, aprendizaje, estado |
| Notas generales | `TEMPLATES/Notas generales.md` | Nota de conocimiento general (tag `KNOWLEDGE`) |
| MOCs | `TEMPLATES/MOCs.md` | Mapas de contenido (tag `INDEX`, `MOCs`) |
| NOTA FACULTAD | `TEMPLATES/NOTA FACULTAD.md` | Nota de la facultad (tag `ciberseguridad`, `UNIVERSIDAD`) |
| Ticket | `TEMPLATES/Ticket - {{DATE}}.md` | Ticket tecnico con RCA, resolucion, lecciones (incluye HTML para OsTicket) |

### Crear nota desde template

```bash
obsidian vault=Personal-Vault create name="Mi nota" template="Notas generales"
```

### IDs de templates (frontmatter)

| Template | ID prefix |
|----------|-----------|
| Daily note | `DAY-` |
| Notas generales | `MAN-` |
| MOCs | `MOC-` |
| NOTA FACULTAD | `UFA-` |
| Ticket | (sin prefijo fijo) |

---

## Flujos de trabajo comunes

### 1. Captura rapida (INBOX)

```bash
obsidian vault=Personal-Vault create name="Idea rapida" \
  path="INBOX/General" \
  content="# ${1:titulo}\n\n"
```

### 2. Daily note

```bash
# Leer la daily de hoy
obsidian vault=Personal-Vault daily:read

# Agregar algo a la daily
obsidian vault=Personal-Vault daily:append content="- Compre pan\n- Pase por el banco"
```

### 3. Buscar y leer

```bash
# Buscar en todo el vault
obsidian vault=Personal-Vault search query="algoritmos"

# Buscar en una carpeta especifica
obsidian vault=Personal-Vault search query="tarea" path="WORK"

# Leer archivo
obsidian vault=Personal-Vault read file="Mi nota"
```

### 4. Tareas

```bash
# Ver tareas pendientes en todo el vault
obsidian vault=Personal-Vault tasks todo

# Ver tareas de un archivo especifico
obsidian vault=Personal-Vault tasks file="PENDIENTES TRABAJO"

# Marcar tarea como pendiente
obsidian vault=Personal-Vault task line=42 file="nota.md" done
```

### 5. Propiedades (Frontmatter)

```bash
# Ver todas las propiedades de un archivo
obsidian vault=Personal-Vault properties file="nota.md"

# Leer una propiedad especifica
obsidian vault=Personal-Vault property:read name="tags" file="nota.md"

# Setear propiedad
obsidian vault=Personal-Vault property:set name="estado" value="revisado" file="nota.md"
```

### 6. Tags

```bash
# Listar todos los tags
obsidian vault=Personal-Vault tags counts

# Ver info de un tag especifico
obsidian vault=Personal-Vault tag name="ciberseguridad"
```

### 7. Git Sync

```bash
# Pull desde GitHub
bash ~/dotfiles/automat/vault-pull.sh

# Push a GitHub (commitea con fecha)
bash ~/dotfiles/automat/vault-push.sh
```

### 8. Nota de facultad

```bash
obsidian vault=Personal-Vault create name="Clase 5 - SQL Injection" \
  template="NOTA FACULTAD"
```

### 9. Ticket tecnico

```bash
obsidian vault=Personal-Vault create name="INCIDENTE-1234" \
  template="Ticket - {{DATE}}"
```

---

## Notas importantes

- El CLI requiere que Obsidian este **abierto** para la mayoria de los comandos
- `file=<name>` resuelve por nombre (como wikilinks), no por ruta exacta
- Usar `path=<path>` para rutas exactas: `path="WORK/00-CLIENTE-A/nota.md"`
- Los valores con espacios van entre comillas: `name="Mi nota"`
- Las variables de template se resuelven automaticamente con `resolve`
- Si no se especifica `file` o `path`, los comandos operan sobre el **archivo activo**
- El vault usa `useMarkdownLinks: true` — los links internos son rutas relativas `.md`
- `trashOption: none` — los archivos borrados se pierden permanentemente

---

## Aliases recomendados para `.zshrc`

```zsh
alias ov='obsidian vault=Personal-Vault'
alias ovd='obsidian vault=Personal-Vault daily'
alias ovs='obsidian vault=Personal-Vault search'
alias ovt='obsidian vault=Personal-Vault tasks'
alias ovpush='bash ~/dotfiles/automat/vault-push.sh'
alias ovpull='bash ~/dotfiles/automat/vault-pull.sh'
```
