# MY-AGENT-SKILLS

Skills y Agents personalizados para Agentes de IA (opencode).

## Skills

Skills que cargan contexto especializado en opencode.

| Skill | Descripcion |
|-------|-------------|
| [arch-manager](./SKILLS/arch-manager/SKILL.md) | Gestion del sistema Arch Linux: paquetes, servicios, kernel, red, hardware, post-instalacion |
| [dotfiles-manager](./SKILLS/dotfiles-manager/SKILL.md) | Gestion de dotfiles: documentacion, creacion de temas, contexto completo del repositorio `~/dotfiles` |
| [obsidian-manager](./SKILLS/obsidian-manager/SKILL.md) | Manejo del vault Obsidian: notas, templates, busqueda, tareas, daily notes, sync via `obsidian` CLI |
| [ollama-manager](./SKILLS/ollama-manager/SKILL.md) | Gestion de modelos locales Ollama: ejecucion, GPU, integracion con opencode, API REST |
| [agent-creator](./SKILLS/agent-creator/SKILL.md) | Instrucciones para crear, configurar y optimizar agents personalizados de opencode |

## Agents

Archivos de configuracion de agentes para copiar a `~/.config/opencode/agents/`.

| Agent | Modo | Proposito |
|-------|------|-----------|
| [arch-sysadmin](./AGENTS/arch-sysadmin.md) | primary | Administracion del sistema Arch Linux |
| [blue-copilot](./AGENTS/blue-copilot.md) | primary | Copiloto de CSIRT, Forense Digital, Blue Team |
| [agent-creator](./AGENTS/agent-creator.md) | primary | Creador de agentes opencode con contexto completo del usuario |

## Estructura

```
MY-AGENT-SKILLS/
├── README.md
├── LICENSE
├── AGENTS/
│   ├── agent-creator.md
│   ├── arch-sysadmin.md
│   └── blue-copilot.md
└── SKILLS/
    ├── agent-creator/
    │   └── SKILL.md
    ├── arch-manager/
    │   └── SKILL.md
    ├── dotfiles-manager/
    │   └── SKILL.md
    ├── obsidian-manager/
    │   └── SKILL.md
    └── ollama-manager/
        └── SKILL.md
```

## Instalacion en opencode

Para que opencode cargue estos skills, agregar en `opencode.json`:

```json
{
  "skills": {
    "paths": ["$HOME/MY-AGENT-SKILLS"]
  }
}
```

Los agents se instalan copiando el `.md` correspondiente a `~/.config/opencode/agents/` y reiniciando opencode.
