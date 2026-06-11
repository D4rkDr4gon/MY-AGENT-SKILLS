# MY-AGENT-SKILLS

Skills y Agentes personalizados para opencode.
Ecosistema **cross-platform**: Arch Linux 🐧 + Windows 11 🪟

## 📁 Estructura

```
~/MY-AGENT-SKILLS/
├── AGENTS/          ← 7 agentes primarios (source of truth)
├── SKILLS/          ← Skills especializados
├── docs/            ← Documentación interna
├── README.md        ← Este archivo
└── .gitignore
```

Los agentes en `~/.config/opencode/agents/` son **symlinks** a `AGENTS/`.

## 🧠 Agentes

| Agente | Plataforma | Propósito |
|--------|-----------|-----------|
| `atlas` | 🐧 Linux | Administración Arch Linux |
| `hestia` | 🪟 Windows | Administración Windows 11 |
| `atenea` | 🐧🪟 | CSIRT, Forense, Blue Team |
| `ares` | 🐧🪟 | Pentesting, Red Team, CTF |
| `prometeo` | 🐧🪟 | Desarrollo de software |
| `hefesto` | 🐧🪟 | Creación de agentes |
| `dedalo` | 🐧🪟 | IDM/NAM laboral |

## 📚 Skills

Los skills se cargan via `/skill <nombre>` en opencode.

### Vault (todos los agentes)
| Skill | Propósito |
|-------|-----------|
| `obsidian-manager` | Gateway al vault Babilonia |

### Sistema
| Skill | Plataforma | Agentes |
|-------|-----------|---------|
| `arch-manager` | 🐧 | atlas |
| `windows-manager` | 🪟 | hestia |
| `dotfiles-manager` | 🐧 | atlas |
| `system-automation` | 🐧🪟 | atlas, hestia |
| `system-monitoring` | 🐧🪟 | atlas, hestia |
| `system-backup` | 🐧🪟 | atlas, hestia |
| `system-hardening` | 🐧🪟 | atlas, hestia, atenea |
| `network-manager` | 🐧🪟 | atlas |

### Ciberseguridad
| Skill | Agentes |
|-------|---------|
| `malware-analysis` | atenea |
| `log-analysis` | atenea |
| `network-forensics` | atenea |
| `osint-threat-intel` | atenea, ares |
| `cryptography` | atenea |
| `compliance-audit` | atenea |
| `forensic-analysis` | atenea |
| `incident-response` | atenea |
| `phishing-analysis` | atenea |
| `vulnerability-mgmt` | atenea |
| `secret-mgmt` | atenea, prometeo |
| `container-security` | atenea, prometeo |
| `web-security` | ares |
| `lab-mgmt` | ares |
| `openvpn-manager` | ares |

### Desarrollo
| Skill | Agentes |
|-------|---------|
| `git` | atlas, hestia, hefesto, ares, prometeo |
| `ci-cd` | prometeo |
| `database` | prometeo |
| `portfolio` | prometeo |
| `blog-writer` | prometeo |
| `document-processing` | prometeo |

### IDM/NAM
| Skill | Agentes |
|-------|---------|
| `enterprise-certificates` | dedalo |
| `IDM-workflow-forms` | dedalo |
| `IDM-identity-drivers` | dedalo |
| `IDM-identity-servers` | dedalo |
| `NAM-access-manager` | dedalo |

### Meta
| Skill | Agentes |
|-------|---------|
| `agent-creator` | hefesto |
| `orchestrator` | hefesto |

## 🔧 Setup

### Linux

1. Clonar el repo:
   ```bash
   git clone https://github.com/D4rkDr4g0n/dotfiles ~/MY-AGENT-SKILLS
   ```

2. Configurar variables de entorno en `~/.zshenv`:
   ```bash
   export BABILONIA="/ruta/a/tu/vault"
   export OBSIDIAN_API_KEY="tu-api-key"
   # Ver docs/ENV-VARS.md para la lista completa
   ```

3. Crear symlinks:
   ```bash
   mkdir -p ~/.config/opencode/agents
   for agent in ~/MY-AGENT-SKILLS/AGENTS/*.md; do
     ln -sf "$agent" ~/.config/opencode/agents/
   done
   ```

4. Configurar `opencode.jsonc` para apuntar a los skills:
   ```jsonc
   "skills": {
     "paths": ["/home/tu-usuario/MY-AGENT-SKILLS/SKILLS"]
   }
   ```

5. **Reiniciar opencode** para que los cambios surtan efecto.

### Windows

1. Clonar el repo en `C:\Users\<user>\MY-AGENT-SKILLS\`
2. Configurar variables de entorno en PowerShell `$PROFILE`:
   ```powershell
   $env:BABILONIA = "C:\Path\To\Your\Vault"
   $env:OBSIDIAN_API_KEY = "tu-api-key"
   ```
3. Configurar `opencode.jsonc` con la ruta a los skills
4. Crear symlinks en `%APPDATA%\opencode\agents\` apuntando a `AGENTS\`

## 🔐 Variables de Entorno

Las variables se definen en `~/.zshenv` (Linux) o `$PROFILE` (Windows). Ver [`docs/ENV-VARS.md`](./docs/ENV-VARS.md) para el listado completo.

| Variable | Obligatoria | Descripción |
|----------|:-----------:|-------------|
| `$BABILONIA` | ✅ | Ruta raíz del vault Obsidian |
| `$OBSIDIAN_API_KEY` | ✅ | API key para el plugin obsidian-local-rest-api |
| `$BABILONIA_*` | ❌ | Subpaths del vault (útiles para los skills) |

## 📖 Documentación en el Vault

La documentación detallada del ecosistema está en el vault Obsidian:
`$BABILONIA/Manuales/04-SPECIALIZED-DOMAINS/03-AI/03-OPENCODE-AGENTS-SKILLS/`

- `AGENTS.md` — Detalle de cada agente
- `SKILLS.md` — Detalle de cada skill
- `PERMISSIONS-MATRIX.md` — Matriz de permisos
- `CHANGELOG.md` — Historial de cambios

## 📝 Notas

- Los agentes **no contienen información confidencial** (paths reales, credenciales, nombres de clientes)
- Todo referencia al vault se hace via `$BABILONIA` y sus derivados
- Los archivos de configuración local (`opencode.jsonc`, `~/.zshenv`) están fuera del repo
