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
| [git-manager](./SKILLS/git-manager/SKILL.md) | 🐧🪟 Cross | Git avanzado: branching, rebase, bisect, hooks, GPG, submodules, worktrees |
| [secret-manager](./SKILLS/secret-manager/SKILL.md) | 🐧🪟 Cross | Gestión de secrets: pass, age, sops, GPG, API keys, .env cifrados |
| [reverse-engineering-manager](./SKILLS/reverse-engineering-manager/SKILL.md) | 🐧🪟 Cross | RE de binarios: radare2, Ghidra, GDB, unpacking, YARA, firmware |
| [hardening-manager](./SKILLS/hardening-manager/SKILL.md) | 🐧🪟 Cross | Hardening: CIS benchmarks, lynis, OpenSCAP, AppArmor, firewall |
| [threat-intel-manager](./SKILLS/threat-intel-manager/SKILL.md) | 🐧🪟 Cross | Threat intel: MISP, STIX/TAXII, IOC management, OpenCTI |
| [backup-manager](./SKILLS/backup-manager/SKILL.md) | 🐧🪟 Cross | Backups: restic, borg, rsync, 3-2-1 strategy, snapshots |
| [database-manager](./SKILLS/database-manager/SKILL.md) | 🐧🪟 Cross | Bases de datos: SQLite, PostgreSQL, MariaDB, queries, backups, migrations |
| [network-manager](./SKILLS/network-manager/SKILL.md) | 🐧🪟 Cross | Redes: nftables, WireGuard, bridges, VLANs, DNS, routing |
| [container-security-manager](./SKILLS/container-security-manager/SKILL.md) | 🐧🪟 Cross | Seguridad de containers: Trivy, Docker Bench, SBOM, cosign |
| [forensic-manager](./SKILLS/forensic-manager/SKILL.md) | 🐧🪟 Cross | Forense digital: sleuthkit, Volatility, file carving, Windows artifacts |
| [web-security-manager](./SKILLS/web-security-manager/SKILL.md) | 🐧🪟 Cross | Seguridad web: OWASP Top 10, Burp Suite, ZAP, SSL/TLS, fuzzing |
| [homelab-manager](./SKILLS/homelab-manager/SKILL.md) | 🐧🪟 Cross | Homelab pentesting: VMs (KVM/VirtualBox), HTB/THM, VulnHub |
| [ci-cd-manager](./SKILLS/ci-cd-manager/SKILL.md) | 🐧🪟 Cross | CI/CD: GitHub Actions, Git hooks, builds, tests, deploy |
| [automation-manager](./SKILLS/automation-manager/SKILL.md) | 🐧🪟 Cross | Automatización: systemd timers, cron, PowerShell Scheduled Tasks |
| [monitoring-manager](./SKILLS/monitoring-manager/SKILL.md) | 🐧🪟 Cross | Monitoreo: health checks, métricas, alertas, performance baselines |
| [learning-manager](./SKILLS/learning-manager/SKILL.md) | 🐧🪟 Cross | Roadmaps de aprendizaje, cursos, CTF progress, skill trees |
| [portfolio-manager](./SKILLS/portfolio-manager/SKILL.md) | 🐧🪟 Cross | Portfolio personal (lcampassi.com): diseño, secciones, deploy |
| [orchestrator-manager](./SKILLS/orchestrator-manager/SKILL.md) | 🐧🪟 Cross | Orquestación paralela de subagentes para tareas grandes |
| [blog-writer](./SKILLS/blog-writer/SKILL.md) | 🐧🪟 Cross | Escritura de blogs para lcampassi.com/docs |
| [dedalo-cert-manager](./SKILLS/dedalo-cert-manager/SKILL.md) | 🐧🪟 Cross | Certificados IDM/NAM — keystores, keytool, OpenSSL, iManager |
| [dedalo-wf-json](./SKILLS/dedalo-wf-json/SKILL.md) | 🐧🪟 Cross | Workflows JSON IDM — Form Builder, componentes, botones, eventos |
| [dedalo-drivers-manager](./SKILLS/dedalo-drivers-manager/SKILL.md) | 🐧🪟 Cross | Drivers IDM — AD, API Rest, Remote Loader, policies, XPATH |
| [dedalo-server-manager](./SKILLS/dedalo-server-manager/SKILL.md) | 🐧🪟 Cross | Servidores IDM/NAM — Tomcat, Identity Apps, logs, health checks |
| [dedalo-tools-errors](./SKILLS/dedalo-tools-errors/SKILL.md) | 🐧🪟 Cross | Tools y errores IDM/NAM — troubleshooting, iManager, HiFlow, SSPR |
| [dedalo-nam-config](./SKILLS/dedalo-nam-config/SKILL.md) | 🐧🪟 Cross | Configuraciones NAM — contratos, user stores, form fills, roles |

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
| [merlin](./AGENTS/merlin.md) | 🐧🪟 Cross | Sabio de Babilonia — entry point universal, orquesta dioses |
| [dedalo](./AGENTS/dedalo.md) | 🐧🪟 Cross | Ayudante laboral IDM/NAM — certificados, workflows, drivers, servers, tools, NAM |

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
├── opencode.json                 # Config — skills.paths: ["SKILLS"]
├── .opencode/
│   └── agents/                   # Copia de agents para opencode
│       ├── hefesto.md            # 🐧🪟 Cross — Creador de agentes
│       ├── atlas.md              # 🐧 Linux — Sysadmin Arch
│       ├── hestia.md             # 🪟 Windows — Sysadmin Windows
│       ├── atenea.md             # 🐧🪟 Cross — CSIRT, Blue Team
│       ├── ares.md               # 🐧🪟 Cross — Pentesting, Red Team
│       ├── prometeo.md           # 🐧🪟 Cross — Desarrollo
│       ├── merlin.md             # 🐧🪟 Cross — Sabio de Babilonia
│       ├── dedalo.md             # 🐧🪟 Cross — IDM/NAM helper
│       └── (21 subagentes)
├── AGENTS/
│   ├── hefesto.md                # 🐧🪟 Cross — Creador de agentes
│   ├── atlas.md                  # 🐧 Linux — Sysadmin Arch
│   ├── hestia.md                 # 🪟 Windows — Sysadmin Windows
│   ├── atenea.md                 # 🐧🪟 Cross — CSIRT, Blue Team
│   ├── ares.md                   # 🐧🪟 Cross — Pentesting, Red Team
│   ├── prometeo.md               # 🐧🪟 Cross — Desarrollo
│   ├── merlin.md                 # 🐧🪟 Cross — Sabio de Babilonia
│   ├── dedalo.md                 # 🐧🪟 Cross — IDM/NAM helper
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
│   ├── agent-creator/            # 🐧🪟 Cross — Creación de agents
│   ├── arch-manager/             # 🐧 Linux — Admin Arch
│   ├── windows-manager/          # 🪟 Windows — Admin Windows
│   ├── dotfiles-manager/         # 🐧 Linux — Dotfiles
│   ├── obsidian-manager/         # 🐧🪟 Cross — Obsidian vault
│   ├── ollama-manager/           # 🐧 Linux — Ollama
│   ├── openvpn-manager/          # 🐧🪟 Cross — OpenVPN
│   ├── docker-manager/           # 🐧🪟 Cross — Docker/Podman
│   ├── mcp-ollama/               # 🐧 Linux — MCP + Ollama
│   ├── git-manager/              # 🐧🪟 Cross — Git avanzado
│   ├── secret-manager/           # 🐧🪟 Cross — Secrets
│   ├── reverse-engineering-manager/ # 🐧🪟 Cross — RE
│   ├── hardening-manager/        # 🐧🪟 Cross — Hardening
│   ├── threat-intel-manager/     # 🐧🪟 Cross — Threat intel
│   ├── backup-manager/           # 🐧🪟 Cross — Backups
│   ├── database-manager/         # 🐧🪟 Cross — DBs
│   ├── network-manager/          # 🐧🪟 Cross — Redes
│   ├── container-security-manager/ # 🐧🪟 Cross — Container sec
│   ├── forensic-manager/         # 🐧🪟 Cross — Forense
│   ├── web-security-manager/     # 🐧🪟 Cross — Web sec
│   ├── homelab-manager/          # 🐧🪟 Cross — Homelab
│   ├── ci-cd-manager/            # 🐧🪟 Cross — CI/CD
│   ├── automation-manager/       # 🐧🪟 Cross — Automatización
│   ├── monitoring-manager/       # 🐧🪟 Cross — Monitoreo
│   ├── learning-manager/         # 🐧🪟 Cross — Aprendizaje
│   ├── portfolio-manager/        # 🐧🪟 Cross — Portfolio web
│   ├── orchestrator-manager/     # 🐧🪟 Cross — Orquestación
│   ├── blog-writer/              # 🐧🪟 Cross — Blog
│   ├── dedalo-cert-manager/      # 🐧🪟 Cross — Certificados IDM/NAM
│   ├── dedalo-wf-json/           # 🐧🪟 Cross — Workflows JSON IDM
│   ├── dedalo-drivers-manager/   # 🐧🪟 Cross — Drivers IDM
│   ├── dedalo-server-manager/    # 🐧🪟 Cross — Servidores IDM
│   ├── dedalo-tools-errors/      # 🐧🪟 Cross — Tools/errores IDM
│   └── dedalo-nam-config/        # 🐧🪟 Cross — Config NAM
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
