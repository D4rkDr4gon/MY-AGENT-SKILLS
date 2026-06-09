# MY-AGENT-SKILLS

Skills, Agents y MCP Servers personalizados para Agentes de IA (opencode).
Ecosistema **cross-platform**: Arch Linux 🐧 + Windows 11 🪟

## Skills

Skills que cargan contexto especializado en opencode.

| Skill | Plataforma | Descripción |
|-------|-----------|-------------|
| [arch-manager](./SKILLS/arch-manager/SKILL.md) | 🐧 Linux | Gestión del sistema Arch Linux: paquetes, servicios, kernel, red, hardware |
| [windows-manager](./SKILLS/windows-manager/SKILL.md) | 🪟 Windows | Gestión del sistema Windows 11: servicios, procesos, disco, red, seguridad, WSL |
| [dotfiles-manager](./SKILLS/dotfiles-manager/SKILL.md) | 🐧 Linux | Gestión de dotfiles: documentación, temas, estructura del repo `~/dotfiles` |
| [obsidian-manager](./SKILLS/obsidian-manager/SKILL.md) | 🐧🪟 Cross | Manejo del vault Obsidian: notas, templates, búsqueda, tasks, sync. Paths dinámicos según SO |
| [ollama-manager](./SKILLS/ollama-manager/SKILL.md) | 🐧 Linux | Gestión de modelos locales Ollama: ejecución, GPU, API REST |
| [agent-creator](./SKILLS/agent-creator/SKILL.md) | 🐧🪟 Cross | Instrucciones para crear, configurar y optimizar agents personalizados |
| [openvpn-manager](./SKILLS/openvpn-manager/SKILL.md) | 🐧🪟 Cross | Conexiones OpenVPN para pentesting labs (HTB, THM). Linux + Windows |
| [docker-manager](./SKILLS/docker-manager/SKILL.md) | 🐧🪟 Cross | Docker/Podman cross-platform: containers, images, compose, sandboxing malware |
| [mcp-ollama](./SKILLS/mcp-ollama/SKILL.md) | 🐧 Linux | MCP server para modelos locales Ollama — tools de IA local sin consumir tokens |

## Agents

Archivos de configuración de agentes (nombres de dioses griegos). Copiar a `~/.config/opencode/agents/` o `.opencode/agents/`.

### Primarios (mode: primary)

| Agent | Plataforma | Propósito |
|-------|-----------|-----------|
| [atlas](./AGENTS/atlas.md) | 🐧 Linux | Administración del sistema Arch Linux |
| [hestia](./AGENTS/hestia.md) | 🪟 Windows | Administración del sistema Windows 11 |
| [atenea](./AGENTS/atenea.md) | 🐧🪟 Cross | CSIRT, Forense Digital, Blue Team |
| [ares](./AGENTS/ares.md) | 🐧🪟 Cross | Pentesting, Bug Bounty, Red Team, CTF |
| [prometeo](./AGENTS/prometeo.md) | 🐧🪟 Cross | Desarrollo: Python, Shell, JavaScript, Rust, Go, D, C |
| [hefesto](./AGENTS/hefesto.md) | 🐧🪟 Cross | Creador de agentes opencode con contexto completo del usuario |

### Subagentes (mode: subagent)

| Agent | Padre | Plataforma | Propósito |
|-------|-------|-----------|-----------|
| [iris](./AGENTS/iris.md) | atlas | 🐧 Linux | Investigación, diagnóstico, fixes en Linux |
| [clio](./AGENTS/clio.md) | atlas | 🐧 Linux | Documentación de dotfiles |
| [mnemosina](./AGENTS/mnemosina.md) | atlas | 🐧 Linux | Documentación Linux en Obsidian |
| [angelos](./AGENTS/angelos.md) | hestia | 🪟 Windows | Investigación, diagnóstico, fixes en Windows |
| [polimnia](./AGENTS/polimnia.md) | hestia | 🪟 Windows | Documentación Windows en Obsidian |
| [hecate](./AGENTS/hecate.md) | atenea | 🐧🪟 Cross | Análisis de malware — estático, dinámico, YARA, reversing, IOC extraction |
| [apolo](./AGENTS/apolo.md) | atenea, atlas, hestia | 🐧🪟 Cross | Análisis de logs y SIEM — parseo, correlación, reglas Sigma, timeline forense |
| [hermes](./AGENTS/hermes.md) | atenea | 🐧🪟 Cross | Forense de red y PCAP — tshark, tcpdump, Zeek, captura y procesamiento de tráfico |
| [argos](./AGENTS/argos.md) | atenea, ares | 🐧🪟 Cross | OSINT — dominios, emails, redes sociales, breaches, footprinting |
| [proteo](./AGENTS/proteo.md) | atenea | 🐧🪟 Cross | Criptografía — estudio, implementación y herramientas criptográficas |
| [temis](./AGENTS/temis.md) | atenea | 🐧🪟 Cross | Auditoría y cumplimiento normativo |
| [nemesis](./AGENTS/nemesis.md) | atenea | 🐧🪟 Cross | Forense digital — disco, memoria, file carving, Windows artifacts |
| [eris](./AGENTS/eris.md) | ares | 🐧🪟 Cross | Seguridad web ofensiva — Burp Suite, ZAP, OWASP Top 10, fuzzing |
| [zeus](./AGENTS/zeus.md) | atenea | 🐧🪟 Cross | Orquestación de respuesta a incidentes |
| [dolos](./AGENTS/dolos.md) | atenea | 🐧🪟 Cross | Análisis de phishing — headers email, URLs, attachments, IOCs |
| [epimeteo](./AGENTS/epimeteo.md) | atenea, atlas, hestia | 🐧🪟 Cross | Gestión de vulnerabilidades — CVE tracking, escaneo, patch management |
| [quiron](./AGENTS/quiron.md) | ares, atenea | 🐧🪟 Cross | Gestión de laboratorios — HTB/THM/VulnHub, VMs, tracking, writeups |
| [caliope](./AGENTS/caliope.md) | atenea, ares | 🐧🪟 Cross | Reportes profesionales — pentest, forense, auditoría, executive summary |
| [eos](./AGENTS/eos.md) | Todos (cross) | 🐧🪟 Cross | Asistente personal diario — rutina, tareas, aprendizaje, daily notes |
| [eolo](./AGENTS/eolo.md) | Cualquiera | 🐧 Linux | Subagente local ultrarrápido (qwen3:1.7b) via MCP — sin consumir tokens |
| [crono](./AGENTS/crono.md) | Cualquiera | 🐧 Linux | Subagente local de razonamiento (qwen2.5:7b, fallback whiterabbit-neo:13b) via MCP — sin consumir tokens |

## MCP Servers

Servidores MCP (Model Context Protocol) que exponen herramientas locales
a los agentes de opencode.

| Server | Descripción | Tools expuestas |
|--------|-------------|-----------------|
| [ollama-mcp-server](./MCP/ollama-server/README.md) | Modelos locales de IA vía Ollama | `ollama_generate`, `ollama_chat`, `ollama_list_models`, `ollama_ps`, `ollama_embed`, `ollama_pull` |

### Instalación de MCP servers

Cada servidor tiene su propio README con instrucciones. En general:

1. Instalar dependencias (usar `requirements.txt` del server)
2. Agregar la entrada en `opencode.jsonc` bajo `mcp:`
3. Reiniciar opencode

Ver [MCP/ollama-server/README.md](./MCP/ollama-server/README.md) para
el server de Ollama.

## Estructura

```
MY-AGENT-SKILLS/
├── README.md
├── LICENSE
├── AGENTS/
│   ├── hefesto.md                # 🐧🪟 Cross — Creador de agentes
│   ├── atlas.md                  # 🐧 Linux — Sysadmin Arch
│   ├── hestia.md                 # 🪟 Windows — Sysadmin Windows
│   ├── atenea.md                 # 🐧🪟 Cross — CSIRT, Blue Team
│   ├── ares.md                   # 🐧🪟 Cross — Pentesting, Red Team
│   ├── prometeo.md               # 🐧🪟 Cross — Desarrollo
│   ├── iris.md                   # 🐧 Linux — Delegado atlas
│   ├── clio.md                   # 🐧 Linux — Dotfiles
│   ├── mnemosina.md              # 🐧 Linux — Docs Linux en Obsidian
│   ├── angelos.md                # 🪟 Windows — Delegado hestia
│   ├── polimnia.md               # 🪟 Windows — Docs Windows en Obsidian
│   ├── hecate.md                 # 🐧🪟 Cross — Malware analysis
│   ├── apolo.md                  # 🐧🪟 Cross — Logs & SIEM
│   ├── hermes.md                 # 🐧🪟 Cross — Network forensics
│   ├── argos.md                  # 🐧🪟 Cross — OSINT
│   ├── proteo.md                 # 🐧🪟 Cross — Criptografía
│   ├── temis.md                  # 🐧🪟 Cross — Auditoría
│   ├── nemesis.md                # 🐧🪟 Cross — Forense digital
│   ├── eris.md                   # 🐧🪟 Cross — Web security
│   ├── zeus.md                   # 🐧🪟 Cross — IR orchestrator
│   ├── dolos.md                  # 🐧🪟 Cross — Phishing analysis
│   ├── epimeteo.md               # 🐧🪟 Cross — Vulnerability mgmt
│   ├── quiron.md                 # 🐧🪟 Cross — Labs (HTB/THM)
│   ├── caliope.md                # 🐧🪟 Cross — Reportes
│   ├── eos.md                    # 🐧🪟 Cross — Daily assistant
│   ├── eolo.md                   # 🐧 Linux — IA local (qwen3:1.7b)
│   └── crono.md                  # 🐧 Linux — IA local (qwen2.5:7b)
├── SKILLS/
│   ├── agent-creator/
│   │   └── SKILL.md              # 🐧🪟 Cross
│   ├── arch-manager/
│   │   └── SKILL.md              # 🐧 Linux
│   ├── windows-manager/
│   │   └── SKILL.md              # 🪟 Windows
│   ├── dotfiles-manager/
│   │   └── SKILL.md              # 🐧 Linux
│   ├── obsidian-manager/
│   │   └── SKILL.md              # 🐧🪟 Cross
│   ├── ollama-manager/
│   │   └── SKILL.md              # 🐧 Linux
│   ├── openvpn-manager/
│   │   └── SKILL.md              # 🐧🪟 Cross
│   ├── docker-manager/
│   │   └── SKILL.md              # 🐧🪟 Cross
│   └── mcp-ollama/
│       └── SKILL.md              # 🐧 Linux — MCP + Ollama
└── MCP/
    └── ollama-server/
        ├── server.py             # MCP server — Ollama bridge
        ├── requirements.txt      # Dependencias
        └── README.md             # Docs del server
```

## Instalación en opencode

Para que opencode cargue estos skills, agregar en `opencode.json`:

```json
{
  "skills": {
    "paths": ["$HOME/MY-AGENT-SKILLS"]
  }
}
```

Los agents se instalan copiando el `.md` correspondiente a `~/.config/opencode/agents/` y reiniciando opencode.

Los MCP servers se instalan registrándolos bajo `mcp:` en `opencode.jsonc` (ver docs de cada server).

### Windows

En Windows los paths son:
- Skills: `C:\Users\lcampassi\Proton Drive\D4rkDr4g0n19\My files\MY-AGENT-SKILLS` (configurado en opencode.jsonc)
- Agents: `C:\Users\lcampassi\.config\opencode\agents\`

### Linux

En Linux los paths son:
- Skills: `~/MY-AGENT-SKILLS`
- Agents: `~/.config/opencode/agents/`

## Documentación en Vault

La documentación detallada del ecosistema se mantiene en el vault Babilonia (Obsidian):
`Manuales/04-SPECIALIZED-DOMAINS/03-AI/03-OPENCODE-AGENTS-SKILLS/`
