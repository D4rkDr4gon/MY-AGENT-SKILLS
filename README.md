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

Archivos de configuración de agentes para copiar a `~/.config/opencode/agents/`.

### Primarios (mode: primary)

| Agent | Plataforma | Propósito |
|-------|-----------|-----------|
| [arch-sysadmin](./AGENTS/arch-sysadmin.md) | 🐧 Linux | Administración del sistema Arch Linux |
| [windows-sysadmin](./AGENTS/windows-sysadmin.md) | 🪟 Windows | Administración del sistema Windows 11 |
| [blue-copilot](./AGENTS/blue-copilot.md) | 🐧🪟 Cross | Copiloto de CSIRT, Forense Digital, Blue Team |
| [red-copilot](./AGENTS/red-copilot.md) | 🐧🪟 Cross | Copiloto de Pentesting, Bug Bounty, Red Team, CTF |
| [agent-creator](./AGENTS/agent-creator.md) | 🐧🪟 Cross | Creador de agentes opencode con contexto completo del usuario |
| [dev-copilot](./AGENTS/dev-copilot.md) | 🐧🪟 Cross | Copiloto de desarrollo: Python, Shell, JS, Rust, C |

### Subagentes (mode: subagent)

| Agent | Padre | Plataforma | Propósito |
|-------|-------|-----------|-----------|
| [arch-delegate](./AGENTS/arch-delegate.md) | arch-sysadmin | 🐧 Linux | Investigación, diagnóstico, fixes en Linux |
| [arch-dotfiles](./AGENTS/arch-dotfiles.md) | arch-sysadmin | 🐧 Linux | Documentación de dotfiles |
| [arch-Obsidian](./AGENTS/arch-Obsidian.md) | arch-sysadmin | 🐧 Linux | Documentación Linux en Obsidian |
| [windows-delegate](./AGENTS/windows-delegate.md) | windows-sysadmin | 🪟 Windows | Investigación, diagnóstico, fixes en Windows |
| [windows-docs](./AGENTS/windows-docs.md) | windows-sysadmin | 🪟 Windows | Documentación Windows en Obsidian |
| [malware-analyst](./AGENTS/malware-analyst.md) | blue-copilot | 🐧🪟 Cross | Análisis de malware — estático, dinámico, YARA, reversing, IOC extraction |
| [log-analyst](./AGENTS/log-analyst.md) | blue-copilot, arch-sysadmin, windows-sysadmin | 🐧🪟 Cross | Análisis de logs y SIEM — parseo, correlación, reglas Sigma, timeline forense |
| [network-forensics](./AGENTS/network-forensics.md) | blue-copilot | 🐧🪟 Cross | Forense de red y PCAP — tshark, tcpdump, Zeek, captura y procesamiento de tráfico |
| [osint-agent](./AGENTS/osint-agent.md) | blue-copilot, red-copilot | 🐧🪟 Cross | OSINT — dominios, emails, redes sociales, breaches, footprinting |
| [local-quick](./AGENTS/local-quick.md) | Cualquiera | 🐧 Linux | Subagente local ultrarrápido (gemma3:270m) via MCP — sin consumir tokens |
| [local-reason](./AGENTS/local-reason.md) | Cualquiera | 🐧 Linux | Subagente local de razonamiento (whiterabbit-neo:13b) via MCP — sin consumir tokens |

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
│   ├── agent-creator.md          # 🐧🪟 Cross
│   ├── arch-sysadmin.md          # 🐧 Linux
│   ├── arch-delegate.md          # 🐧 Linux
│   ├── arch-dotfiles.md          # 🐧 Linux
│   ├── arch-Obsidian.md          # 🐧 Linux
│   ├── windows-sysadmin.md       # 🪟 Windows
│   ├── windows-delegate.md       # 🪟 Windows
│   ├── windows-docs.md           # 🪟 Windows
│   ├── blue-copilot.md           # 🐧🪟 Cross
│   ├── red-copilot.md            # 🐧🪟 Cross
│   ├── dev-copilot.md            # 🐧🪟 Cross
│   ├── malware-analyst.md        # 🐧🪟 Cross
│   ├── log-analyst.md            # 🐧🪟 Cross
│   ├── network-forensics.md      # 🐧🪟 Cross
│   ├── osint-agent.md            # 🐧🪟 Cross
│   ├── local-quick.md            # 🐧 Linux — IA local (gemma3:270m)
│   └── local-reason.md           # 🐧 Linux — IA local (whiterabbit-neo:13b)
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

La documentación detallada del ecosistema se mantiene en Obsidian:
`Manuales/04-SPECIALIZED-DOMAINS/03-AI/03-OPENCODE-AGENTS-SKILLS/`
