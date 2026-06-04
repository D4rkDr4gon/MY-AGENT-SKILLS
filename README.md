# MY-AGENT-SKILLS

Skills y Agents personalizados para Agentes de IA (opencode).
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

### Subagentes (mode: subagent)

| Agent | Padre | Plataforma | Propósito |
|-------|-------|-----------|-----------|
| [arch-delegate](./AGENTS/arch-delegate.md) | arch-sysadmin | 🐧 Linux | Investigación, diagnóstico, fixes en Linux |
| [arch-dotfiles](./AGENTS/arch-dotfiles.md) | arch-sysadmin | 🐧 Linux | Documentación de dotfiles |
| [arch-Obsidian](./AGENTS/arch-Obsidian.md) | arch-sysadmin | 🐧 Linux | Documentación Linux en Obsidian |
| [windows-delegate](./AGENTS/windows-delegate.md) | windows-sysadmin | 🪟 Windows | Investigación, diagnóstico, fixes en Windows |
| [windows-docs](./AGENTS/windows-docs.md) | windows-sysadmin | 🪟 Windows | Documentación Windows en Obsidian |

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
│   └── red-copilot.md            # 🐧🪟 Cross
└── SKILLS/
    ├── agent-creator/
    │   └── SKILL.md              # 🐧🪟 Cross
    ├── arch-manager/
    │   └── SKILL.md              # 🐧 Linux
    ├── windows-manager/
    │   └── SKILL.md              # 🪟 Windows
    ├── dotfiles-manager/
    │   └── SKILL.md              # 🐧 Linux
    ├── obsidian-manager/
    │   └── SKILL.md              # 🐧🪟 Cross
    ├── ollama-manager/
    │   └── SKILL.md              # 🐧 Linux
    └── openvpn-manager/
        └── SKILL.md              # 🐧🪟 Cross
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
