# MY-AGENT-SKILLS

Skills personales para Agentes de IA (opencode). Cada skill es una carpeta con su propio `SKILL.md`.

## Skills

| Skill | Descripcion |
|-------|-------------|
| [dotfiles-manager](./dotfiles-manager/SKILL.md) | Gestion de dotfiles: documentacion, creacion de temas, contexto completo del repositorio `~/dotfiles` |

## Estructura

```
MY-AGENT-SKILLS/
├── README.md
├── LICENSE
└── <skill-name>/
    └── SKILL.md
```

## Instalacion en opencode

Para que opencode cargue estos skills, agregar en `opencode.json`:

```json
{
  "skills": {
    "paths": ["/home/lcampassi/MY-AGENT-SKILLS"]
  }
}
```
