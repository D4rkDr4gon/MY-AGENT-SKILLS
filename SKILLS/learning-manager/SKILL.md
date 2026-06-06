---
name: learning-manager
description: Use when managing learning roadmaps, course/book tracking, CTF progress, spaced repetition, skill trees, and learning goals across cybersecurity, development, and sysadmin domains.
---

# learning-manager

## Descripción general

Filosofía de aprendizaje basada en **práctica deliberada**, **repaso espaciado** y **progresión por skill trees**. El objetivo no es acumular contenido sino **transferir conocimiento a la memoria de largo plazo mediante aplicación activa**.

| Principio | Aplicación |
|-----------|------------|
| Práctica deliberada | Ejercicios, labs, CTFs, proyectos reales |
| Repaso espaciado | Anki + revisión programada en daily notes |
| Progresión incremental | Skill trees con prerequisitos y mastery levels |
| Documentación activa | Notas atómicas en Obsidian vault al resolver algo |
| Métricas honestas | Horas dedicadas, no horas fingidas |

El seguimiento se divide en tres dominios:

- **Ciberseguridad** — defensivo, ofensivo, cloud, malware analysis, forense
- **Desarrollo** — Python, Go, Rust, D
- **Sysadmin** — Linux (Arch/Kali), Windows, redes, infraestructura

---

## Rutas de aprendizaje

### Ciberseguridad

| Ruta | Temas clave | Labs recomendados | Certificación asociada |
|------|-------------|-------------------|------------------------|
| Defensivo | SIEM, SOAR, threat hunting, hardening, IR | Blue Team Labs, LetsDefend | BTL1, GSOC, CISSP |
| Ofensivo | Pentesting web, AD, explotación, pivoting | HTB, PG Practice, VulnHub | OSCP, PNTP, CRTP |
| Cloud Security | AWS/Azure/GCP hardening, IAM, container sec | CloudFox, Stratus Red Team | CCSK, AWS Security, AZ-500 |
| Malware Analysis | RE estática/dinámica, sandboxing, memory forensics | FLARE VM, ANY.RUN, MalwareTech | GREM, GFOR |
| Forense | Disk forensics, memory dump, timeline analysis | CFAT, NIST CFReDS | GCFE, GCFA, CHFI |

### Desarrollo

| Lenguaje | Enfoque | Roadmap |
|----------|---------|---------|
| Python | Automatización, herramientas de seguridad, scripting | Tipos -> OOP -> Async -> Librerías (scapy, requests, asyncio) -> Proyectos |
| Go | Herramientas CLI, redes, concurrentes | Sintaxis -> Goroutines -> Channels -> Stdlib -> Proyectos (escáneres, proxies) |
| Rust | Herramientas de sistema, reemplazo de C/C++ | Ownership -> Borrowing -> Lifetimes -> Unsafe -> Proyectos (herramientas de red) |
| D | Alternativa a C++ con metaprogramación | Sintaxis -> Templates -> Mixins -> GC management -> Interop con C |

### Sysadmin

| Sistema | Temas |
|---------|-------|
| Linux | systemd, nftables, AppArmor, LVM, Btrfs, hardening, containers (Docker/Podman) |
| Windows | Active Directory, Group Policy, PowerShell, Windows Defender, registry, WSL |

### Template de ruta personal (.md en vault)

```markdown
---
ruta: "Pentesting Web"
estado: "en-progreso"
inicio: 2026-01-15
meta: "OSCP"
---

# Pentesting Web — Ruta de aprendizaje

## Módulos
- [x] Reconocimiento (1-15 Ene)
- [ ] Explotación OWASP Top 10 (Ene-Feb)
- [ ] Bypass de WAF
- [ ] Post-explotación

## Proyectos
- [x] Escáner de subdominios en Go
- [ ] Laboratorio DVWA automatizado
```

---

## Seguimiento de cursos/libros/CTFs

### Estados

| Estado | Significado |
|--------|-------------|
| `planning` | En lista, aún no empecé |
| `in-progress` | Cursando/leyendo activamente |
| `completed` | Finalizado |
| `review` | Completado pero requiere repaso |
| `paused` | Pausado temporalmente |
| `dropped` | Abandonado (con nota del porqué) |

### Template de curso

```markdown
---
tipo: curso
estado: "in-progress"
inicio: 2026-02-01
fin: null
proveedor: "HTB Academy"
---

# HTB Academy — Penetration Testing Process

## Log semanal
| Semana | Horas | Temas | Notas |
|--------|-------|-------|-------|
| 1 | 6 | Metodología, scope | Ok, muy teórico |
| 2 | 8 | OSINT, footprinting | Práctico, interesante |

## Notas clave
- Scope definition es crítico en el contrato
- OSINT con herramientas pasivas primero

## Evaluación
- **Dificultad**: 3/5
- **Utilidad**: 5/5
- **Recomiendo**: Sí
```

### Template de libro

```markdown
---
tipo: libro
estado: "in-progress"
inicio: 2026-01-20
fin: null
autor: "Peter Kim"
---

# The Hacker Playbook 3

## Progreso
- [x] Cap 1-3: Setup del lab (15 pág)
- [ ] Cap 4-6: Recon interno
- [ ] Cap 7-9: Explotación AD

## Quotes / Insights
> "El mejor pentester no es el que más herramientas conoce, sino el que mejor entiende el negocio."
```

### Template de CTF

```markdown
---
tipo: ctf
plataforma: "HTB"
maquina: "Laboratory"
dificultad: "Medium"
estado: "completed"
completado: 2026-03-10
---

# HTB — Laboratory (Medium)

## Resolución
1. Nmap: puertos 80, 443, 22
2. Subdomain enum -> `gitlab.laboratory.htb`
3. CVE-2020-13277 (GitLab RCE)
4. Escalada: Docker socket mount

## Skills practicados
- Subdomain brute-force
- Gitlab exploitation
- Docker privilege escalation

## Retro
- **Fácil**: Encontrar el subdominio fue directo con ffuf
- **Difícil**: La escalada por Docker requería conocer `docker.sock`
- **Aprendizaje**: Verificar mounts del container antes de asumir
```

---

## Repaso espaciado

### Metodología

Basado en el algoritmo SM-2 de SuperMemo, usado por Anki. El intervalo de repaso se calcula así:

```
Intervalo = anterior_intervalo × factor_dificultad

Factor de dificultad: 1.3 (fácil) a 2.5 (muy difícil)
```

| Respuesta | Acción | Nuevo intervalo |
|-----------|--------|-----------------|
| Again (0) | Reset | 1 minuto |
| Hard (1) | Repetir | 10 minutos |
| Good (2) | Avanzar | 1 día o intervalo normal |
| Easy (3) | Acelerar | 1.3 × intervalo o 4 días (el que sea mayor) |

### Tarjetas en Anki recomendadas

```
P: ¿Qué comando lista los servicios en systemd?
R: systemctl list-units --type=service --state=running

P: ¿Cuál es la diferencia entre Docker run y exec?
R: run crea un contenedor nuevo, exec ejecuta en uno existente

P: Enumerate subdominios con ffuf
R: ffuf -w wordlist.txt -u https://example.com -H "Host: FUZZ.example.com"
```

### Configurar mazo Anki desde terminal

```bash
# Crear mazo
ankicli deck add "Ciberseguridad::OWASP Top 10"

# Agregar tarjetas
ankicli add "¿Qué es SQLi?" "Inyección SQL en inputs" deck="Ciberseguridad::OWASP Top 10"

# Revisar
ankicli review deck="Ciberseguridad::OWASP Top 10" limit=10

# Stats
ankicli stats
```

### Cálculo manual de revisión

```python
# Ejemplo: calcular próxima fecha de repaso
from datetime import datetime, timedelta

def next_review(interval_days, quality):
    """quality: 0(again) 1(hard) 2(good) 3(easy)"""
    if quality == 0:
        return timedelta(minutes=1)
    if quality == 1:
        return timedelta(minutes=10)
    factor = {2: 1.0, 3: 1.3}[quality]
    return timedelta(days=interval_days * factor)

# Si intervalo actual = 7 días y respondiste "good"
next = next_review(7, 2)
print(f"Próximo repaso en {next.days} días")  # 7 días
```

---

## CTF Writeups

### Estructura completa

```markdown
---
title: "HTB — [Máquina]"
plataforma: HTB | THM | VulnHub
dificultad: Easy | Medium | Hard | Insane
tipo: Linux | Windows | Active Directory | Web
completado: 2026-03-10
tiempo: 3h
tags: [recon, sqli, privesc, linux]
---

# HTB — [Máquina] ([Dificultad])

## Reconocimiento
- **Puertos abiertos**: 22, 80, 443
- **Servicios**: Apache 2.4.41, OpenSSH 8.0
- **Vulnerabilidades detectadas**: SQLi en login, LFI en parámetro file

## Explotación
```
# Scan inicial
nmap -sC -sV -oN scans/initial $IP

# SQLi en login
sqlmap -u http://$IP/login.php --data="user=admin&pass=admin" --dump
```

## Post-Explotación
```bash
# Enumeración interna
linpeas | tee /tmp/linpeas.txt

# Escalada
sudo -u root /usr/bin/find . -exec /bin/bash \; -quit
```

## Skills adquiridos
- SQLi bypass de autenticación
- LFI a RCE via log poisoning
- Abuso de sudo con `find`

## Retrospectiva
| Aspecto | Qué salió bien | Qué mejorar |
|---------|----------------|-------------|
| Recon | Escaneo completo con nmap + gobuster | Probar más wordlists |
| Explotación | SQLi rápida | No verificar LFI sin autenticación |
| Escalada | Encontré binario SUID rápido | Faltó verificar cron jobs |

## Writeup en vault
- `Manuales/CTF/HTB-Laboratory.md`
```

---

## Skill trees

Los skill trees modelan **prerequisitos y dependencias** entre habilidades. Cada habilidad tiene niveles de maestría.

### Niveles de maestría

| Nivel | Descripción | Indicador |
|-------|-------------|-----------|
| 0 - Novato | No conoce el concepto | No puede explicarlo |
| 1 - Aprendiz | Entiende la teoría | Puede explicarlo pero no aplicarlo sin ayuda |
| 2 - Practicante | Lo aplica con guía | Sigue tutorials/labs con éxito |
| 3 - Competente | Lo aplica sin ayuda | Resuelve CTFs/problemas por sí mismo |
| 4 - Experto | Lo enseña y optimiza | Puede hacer code review, crear cheatsheets |
| 5 - Maestro | Lo innova | Crea herramientas, descubre vulnerabilidades nuevas |

### Template de skill tree

```markdown
---
skill: "Active Directory Exploitation"
nivel: 2
meta: 4
---

# Active Directory Exploitation

## Prerequisitos
- [x] Networking básico (Nivel 2)
- [x] Windows internals (Nivel 2)
- [ ] Kerberos authentication (Nivel 1) ← En progreso

## Dependencias
### Nivel 1 — Fundamentos
- [ ] AD architecture (dominio, bosque, OU)
- [ ] LDAP queries básicas
- [ ] Herramientas: BloodHound, ldapsearch

### Nivel 2 — Enumeración
- [ ] BloodHound colecta + análisis
- [ ] PowerView / ADSI
- [ ] Kerberoasting
- [ ] AS-REP Roasting

### Nivel 3 — Movimiento lateral
- [ ] Pass-the-Hash / Pass-the-Ticket
- [ ] DCSync
- [ ] SMB relay
- [ ] ACL abuse

### Nivel 4 — Dominio completo
- [ ] Cross-forest trust abuse
- [ ] Golden / Silver Ticket
- [ ] PKI / AD CS abuse (ESC1-ESC8)

## Progreso
- Horas dedicadas: 24
- Próximo hito: Completar Kerberoasting manual
- Último avance: 2026-03-08
```

### Visualización de progreso

```bash
# Script para calcular % de skill tree completado
cat ~/dotfiles/scripts/calc-skill-progress.sh
```

```bash
#!/bin/bash
# Calcula % de checkboxes marcados en archivo de skill tree
FILE="$1"
[ -z "$FILE" ] && echo "Uso: $0 <archivo-skill.md>" && exit 1

TOTAL=$(grep -cE "\[ \]|\[x\]" "$FILE")
DONE=$(grep -cE "\[x\]" "$FILE")
if [ "$TOTAL" -eq 0 ]; then
  echo "0%"
else
  echo "$(( DONE * 100 / TOTAL ))% completado ($DONE/$TOTAL)"
fi
```

---

## Documentación en vault

### Rutas en Obsidian

| Contenido | Ruta en vault | Formato |
|-----------|---------------|---------|
| Skill trees | `Manuales/Skill-Trees/{skill}.md` | Plantilla Skill Tree |
| Course tracking | `Manuales/Cursos/{curso}.md` | Plantilla de Curso |
| Book notes | `Manuales/Libros/{libro}.md` | Plantilla de Libro |
| CTF writeups | `Manuales/CTF/{plataforma}-{maquina}.md` | Plantilla de CTF |
| Daily learning log | `INBOX/Journal/{año}/DD mes.md` | Sección "Aprendizaje" |
| Cheatsheets | `Manuales/Cheatsheets/{tema}.md` | Nota rápida con código |
| Weekly reviews | `INBOX/Journal/{año}/Semana-{num}.md` | Template semanal |
| Quarterly OKRs | `INBOX/General/OKR/OKR-Q{num}-{año}.md` | Plantilla OKR |

### Tags usados

| Tag | Significado |
|-----|-------------|
| `#aprendizaje` | Nota de aprendizaje general |
| `#ctf` | CTF writeups |
| `#roadmap` | Skill tree o ruta |
| `#review` | Pendiente de repaso |
| `#daily/learning` | Entrada de aprendizaje en daily note |
| `#meta` | Metas y OKRs |
| `#curso` | Seguimiento de curso |
| `#libro` | Seguimiento de libro |

### Template diario — sección de aprendizaje

Para incluir en la daily note (template en `TEMPLATES/Daily note.md`):

```markdown
## Aprendizaje 🧠

### Hoy estudié
- [ ] Tema/horas: {{3h: SQL Injection bypass}}
- [ ] Tema/horas: {{1h: BloodHound colecta}}
- [ ] Tema/horas: {{30min: Repaso Anki}}

### Logros
- {{Resolví la máquina Laboratory de HTB}}
- {{Entendí kerberoasting manual}}

### Dudas / Bloqueos
- {{Diferencia entre AS-REP Roasting y Kerberoasting?}}

### Mañana
- [ ] Terminar módulo de AD de HTB Academy
- [ ] Repasar tarjetas de OWASP Top 10

### Próximo repaso
- Revisar skill tree de AD en 7 días ({{2026-03-15}})
```

---

## Integración con daily notes

### Flujo diario

```bash
# 1. Abrir daily note de hoy
obsidian vault=Personal-Vault daily

# 2. Registrar tiempo de estudio
obsidian vault=Personal-Vault daily:append \
  content="- ## Aprendizaje\n  - [ ] 2h: BloodHound analysis\n  - [ ] Repaso Anki 15 tarjetas"

# 3. Crear tarjeta de Anki si aprendí algo nuevo
ankicli add "¿Qué es BloodHound?" \
  "Herramienta de enumeración AD que mapea relaciones y paths de ataque" \
  deck="Ciberseguridad::AD"

# 4. Marcar progreso en skill tree
# Editar Manuales/Skill-Trees/Active-Directory-Exploitation.md
```

### Weekly review template

```markdown
---
title: "Review Semana 10, 2026"
semana: 10
año: 2026
fecha: 2026-03-09
tags: [review, aprendizaje, meta]
---

# Review Semana 10

## Progreso horario
| Día | Horas | Actividad |
|-----|-------|-----------|
| Lun | 2 | HTB Academy — AD |
| Mar | 3 | CTF Laboratory + writeup |
| Mié | 1 | Anki review |
| Jue | 2.5 | Python scripting |
| Vie | 0 | Descanso |
| Sáb | 4 | Máquina Active Directory |
| Dom | 1 | Repaso semanal |
| **Total** | **13.5** | |

## Skills trabajados
- [x] AD enumeration (BloodHound)
- [x] Kerberoasting
- [ ] DCSync

## Objetivos para S11
- [ ] Completar Kerberoasting manual
- [ ] Empezar módulo de AV evasion
- [ ] Anki: crear 10 tarjetas nuevas

## Ajustes
- Dediqué mucho tiempo a HTB, me faltó teoría -> balancear 60/40 práctica/teoría
- No toqué Rust esta semana -> agregar 1h los domingos
```

### Prompt semanal automatizado

```bash
# Script que abre la daily del lunes y agrega el template de weekly review
obsidian vault=Personal-Vault daily
# Luego pegar contenido del template de weekly review manualmente
# (o usar obsidian:template:insert si el template está configurado)
```

---

## Metas y objetivos

### OKRs trimestrales

```markdown
---
title: "OKR Q1 2026"
trimestre: Q1
año: 2026
tags: [meta, okr]
---

# OKR Q1 2026 (Ene-Mar)

## Objetivo 1: Aprobar módulo AD en HTB Academy
- [KR 1] Completar todos los módulos de AD (0/4)
- [KR 2] Resolver 5 máquinas AD en HTB (0/5)
- [KR 3] Obtener 85%+ en examen final

## Objetivo 2: Mejorar automatización en Python
- [KR 1] Escribir 3 herramientas CLI propias (0/3)
- [KR 2] Contribuir a un repo open source (issues/pr)

## Objetivo 3: Reducir deuda técnica en repaso
- [KR 1] Revisar 100% de tarjetas atrasadas en Anki
- [KR 2] Mantener racha de repaso > 80 días
- [KR 3] Crear 50 tarjetas nuevas de calidad

## Check-in semanal
| Semana | KR1.1 | KR1.2 | KR2.1 | Notas |
|--------|-------|-------|-------|-------|
| 1 | 0/4 | 0/5 | 0/3 | Arrancando |
| 4 | 1/4 | 2/5 | 0/3 | Buen ritmo |
```

### Metas semanales

Extraídas de los OKRs trimestrales. Se definen los lunes en la daily:

```
# Lunes — definir metas semanales
1. [Meta] Terminar módulo AD Enumeration (4h)
2. [Meta] Escribir script en Python para automatizar Nmap scanning (3h)
3. [Hábito] Anki review todos los días (15min/día)
4. [Hábito] Documentar cada CTF completado en vault
```

### Habit tracking

| Hábito | Frecuencia | Racha actual | Racha máxima |
|--------|------------|-------------|--------------|
| Anki review | Diario | 45 días | 67 días |
| Estudio 2h+ | Diario (lun-sáb) | 12 días | 30 días |
| CTF semanal | Semanal | 3 semanas | 8 semanas |
| Documentar en vault | Por sesión | 5 sesiones | 14 sesiones |
| Ejercicio | 3× semana | 4 días | 21 días |

### Template de habit tracker

```markdown
---
title: "Habits 2026"
tags: [habits, tracking]
---

# Habits 2026

## Marzo
| Día | Anki | Estudio | CTF | Docs | Ejercicio |
|-----|------|---------|-----|------|-----------|
| 1   | ✅   | ✅ 2h   | ❌   | ✅   | ❌         |
| 2   | ✅   | ✅ 3h   | ❌   | ✅   | ✅ (gym)  |
| 3   | ❌   | ❌      | ❌   | ❌   | ❌         |
```

### Evaluación trimestral

Al final de cada trimestre, responder:

1. ¿Completé los KRs que me propuse? Si no, ¿por qué?
2. ¿Qué skills mejoraron más? ¿Cuáles quedaron estancadas?
3. ¿Ajusté mi ruta de aprendizaje? ¿Necesito pivotear?
4. ¿Mi distribución de tiempo fue adecuada? (60% práctica / 30% teoría / 10% repaso)
5. ¿Qué hábitos funcionaron? ¿Cuáles tengo que cambiar?
6. Próximo trimestre: ¿qué KRs priorizo?

```bash
# Ejemplo: total de horas en el trimestre
# Sumar horas de dailies con grep
rg "✅ \d+h" INBOX/Journal/2026/ | awk '{sum += $2} END {print sum " horas"}'
```
