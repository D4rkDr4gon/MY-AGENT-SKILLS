# Productivity Manager

Skill para gestionar la productividad personal — tareas, hábitos, metas, tiempo y revisión semanal. Integrado con Obsidian daily notes y rutinas multiplataforma (Linux + Windows).

---

## Descripción general

Sistema de productividad personal basado en:
- **Obsidian vault** como centro de captura y seguimiento
- **Daily Notes** como punto de partida diario
- **OKRs + SMART goals** para alinear tareas con objetivos trimestrales
- **Time blocking + pomodoro** para ejecución enfocada
- **Revisión semanal** como circuito de retroalimentación

Principios rectores:
- **Captura rápida** — si no está registrado, no existe
- **Priorización diaria** — solo 3 tareas críticas por día
- **Revisión semanal** sin falta (domingo/viernes)

---

## Gestión de tareas

### Estados

| Estado | Símbolo | Significado |
|--------|---------|-------------|
| Pendiente | `[ ]` | Tarea sin iniciar |
| En progreso | `[/]` | Trabajando activamente |
| Completada | `[x]` | Finalizada |
| Retrasada | `[>]` | Pospuesta para después |
| Cancelada | `[-]` | Ya no aplica |

### Prioridades

| Prioridad | Etiqueta | Plazo |
|-----------|----------|-------|
| Crítica | `#urgente` | Hoy |
| Alta | `#importante` | Esta semana |
| Media | `#normal` | Este mes |
| Baja | `#baja` | Sin fecha |

### Contextos

| Contexto | Uso |
|----------|-----|
| `@casa` | Tareas domésticas o personales |
| `@trabajo` | Tareas laborales / CSIRT |
| `@pc` | Enfrente de la computadora |
| `@movil` | Desde el teléfono |
| `@lectura` | Leer / investigar |
| `@estudio` | Estudio / cursos |

### Formato de tarea

```
- [ ] Descripción de la tarea #etiqueta #prioridad @contexto
  Notas adicionales o subtareas
```

Ejemplo:

```
- [ ] Completar informe de incidente #trabajo #urgente @pc
  Pendiente: correlación de logs del martes
- [>] Leer capítulo 3 de malware analysis #estudio #normal @lectura
```

### Revisión diaria de tareas

Al comenzar el día:
1. Revisar tareas pendientes del día anterior
2. Mover `[>]` retrasadas a hoy si siguen siendo relevantes
3. Elegir **3 tareas críticas** y marcarlas con `⭐`
4. Estimar tiempo por tarea (pomodoro count)

---

## Hábitos y rutinas

### Plantilla de seguimiento de hábitos

Insertar en la daily note:

```markdown
## Hábitos
- [ ] Despertar sin snooze (06:30)
- [ ] Meditación / respiración (5 min)
- [ ] Ejercicio (30+ min)
- [ ] Lectura técnica (20+ min)
- [ ] Sin redes sociales antes de dormir
- [ ] Registro de aprendizaje del día
```

### Racha (streak)

Usar `habit-tracker.md` en el vault:

```markdown
# Seguimiento de hábitos: {{MONTH}}

| Hábito        | Lun | Mar | Mié | Jue | Vie | Sáb | Dom | Racha |
|---------------|-----|-----|-----|-----|-----|-----|-----|-------|
| Ejercicio     |  ✅ |  ✅ |  ❌ |  ✅ |  ✅ |  ✅ |  ❌ | 3     |
| Lectura       |  ✅ |  ✅ |  ✅ |  ✅ |  ❌ |  ✅ |  ✅ | 5     |
| Meditación    |  ❌ |  ✅ |  ✅ |  ✅ |  ✅ |  ✅ |  ✅ | 6     |
```

### Rutina matutina

```
06:30 — Despertar + agua
06:35 — Meditación (5 min)
06:45 — Ejercicio (30-45 min)
07:30 — Ducha + desayuno
08:00 — Revisar daily + top 3 tareas
```

### Rutina vespertina

```
21:00 — Cerrar pantallas
21:15 — Reflexión diaria (journal)
21:30 — Leer (físico / Kindle)
22:00 — Dormir
```

### Preguntas de revisión semanal de hábitos

- ¿Qué hábito tuve que saltarme más veces? ¿Por qué?
- ¿Hay un hábito que debería agregar o eliminar?
- ¿Mi rutina matutina/vespertina sigue siendo realista?
- ¿Qué factor externo afectó mi consistencia?

---

## Metas y objetivos

### OKR (Objectives & Key Results)

Estructura trimestral:

```markdown
# OKR Q1 2026

## Objetivo 1: Avanzar en carrera de seguridad
- KR 1: Obtener certificación XYZ
- KR 2: Completar 3 laboratorios de HTB por semana
- KR 3: Escribir 2 informes técnicos públicos

## Objetivo 2: Mejorar salud y energía
- KR 1: Ejercicio 5/7 días por semana
- KR 2: Dormir 7+ horas diarias
- KR 3: Reducir tiempo en redes sociales a <30 min/día
```

### SMART Goals

| Letra | Significado | Pregunta guía |
|-------|-------------|---------------|
| S | Specific | ¿Qué exactamente quiero lograr? |
| M | Measurable | ¿Cómo mido el progreso? |
| A | Achievable | ¿Es realista con mi tiempo actual? |
| R | Relevant | ¿Alineado con mis prioridades? |
| T | Time-bound | ¿Cuál es la fecha límite? |

### Check-in mensual

Responder cada primer día del mes:

- **Progreso OKR**: ¿Qué % de cada KR está completo?
- **Ajustes**: ¿Necesito redefinir algún KR?
- **Bloqueantes**: ¿Qué me está frenando?
- **Próximos 30 días**: ¿Cuál es el foco principal?

### Desglose trimestral a semanal

```
Q1 objetivo → dividir en ~12 semanas
Cada semana → 1-2 tareas clave que acerquen al KR
Daily → 3 tareas críticas alineadas con la semana
```

---

## Gestión del tiempo

### Time Blocking (plantilla)

```markdown
## Bloque de tiempo: {{FECHA}}

| Hora       | Bloque                 | Notas |
|------------|------------------------|-------|
| 08:00-09:00 | Deep work — tarea #1   | Sin interrupciones |
| 09:00-09:30 | Revisión de correo/incidentes | |
| 09:30-11:00 | Deep work — tarea #2   | Pomodoro 25/5 |
| 11:00-11:15 | Pausa                 | Café, estirar |
| 11:15-12:30 | Reuniones / coordinar  | |
| 12:30-13:30 | Almuerzo desconectado  | Sin pantallas |
| 13:30-15:00 | Deep work — tarea #3   | Pomodoro 25/5 |
| 15:00-15:45 | Tareas administrativas | |
| 15:45-16:00 | Cierre del día         | Revisar log |
```

### Pomodoro

- **25 min** de foco → **5 min** de pausa
- Cada **4 pomodoros** → pausa larga de **15-20 min**
- Usar `pomodoro-timer` en Linux o `Focus To-Do` en Windows

### Gestión de distracciones

- Bloquear redes con `/etc/hosts` o `Cold Turkey`
- Slack/Teams en modo no molestar durante deep work
- Teléfono en modo avión o en otra habitación
- Regla de los 2 minutos: si una distracción toma <2 min, resuélvela ya; si no, anótala en la bandeja de entrada

### Matriz Eisenhower

|                     | Urgente | No urgente |
|---------------------|---------|------------|
| **Importante**      | HACER   | PLANIFICAR |
| **No importante**   | DELEGAR | ELIMINAR   |

---

## Revisión semanal

Realizar cada **domingo** (o viernes si aplica). Plantilla:

```markdown
# Revisión semanal: {{SEMANA}}

## ✅ Logros de la semana
- 
- 
- 

## ⚠️ Desafíos / obstáculos
- 
- 

## 📚 Aprendizajes
- 
- 

## 🔄 Hábitos
- Racha más larga:
- Hábito más débil:
- Ajustes para la próxima semana:

## 🎯 Prioridades para la próxima semana
1. 
2. 
3. 

## 🧠 Notas libres / reflexiones
```

### Preguntas guía

- ¿Completé mis 3 tareas críticas cada día?
- ¿Dónde perdí más tiempo?
- ¿Qué fue lo más importante que aprendí?
- ¿Estoy más cerca de mis OKRs que la semana pasada?
- ¿Mi energía física/mental fue suficiente? ¿Qué puedo ajustar?

---

## Daily Notes

### Ubicación en el vault

```
📁 Personal-Vault/
└── 📁 Daily/
    └── {{YYYY-MM-DD}}.md
```

### Plantilla de daily note

```markdown
# {{FECHA}} — {{DÍA DE LA SEMANA}}

## 🎯 Top 3 tareas críticas
- [ ] 1.
- [ ] 2.
- [ ] 3.

## 📋 Tareas del día
- [ ]  
- [ ]  
- [>]  

## 🕐 Time blocking

| Hora | Actividad |
|------|-----------|
|      |           |
|      |           |

## 📖 Aprendizaje del día
- 

## 🙏 Gratitud / reflexión
- 

## 📌 Notas rápidas
```

### Integración con el sistema

1. La daily note se crea automáticamente (Periodic Notes plugin o Templater)
2. Las tareas se copian de la weekly note / tareas pendientes
3. Al final del día, mover tareas incompletas a `[>]` y planificar mañana
4. El aprendizaje del día alimenta la revisión semanal

### Learning log

Mantener un registro de aprendizaje acumulativo:

```markdown
# Learning Log — {{YYYY}}

## Semana {{NÚMERO}}
- {{YYYY-MM-DD}}: Concepto nuevo / herramienta / técnica
```

---

## Obsidian Vault

### Estructura recomendada

```
📁 Personal-Vault/
├── 📁 Daily/                  # Daily notes (auto-generadas)
├── 📁 Tasks/                  # Proyectos y listas de tareas
│   ├── tasks-activas.md
│   ├── tasks-pendientes.md
│   └── tasks-completadas.md
├── 📁 Habits/                 # Seguimiento de hábitos
│   ├── habit-tracker.md
│   └── rutinas.md
├── 📁 Goals/                  # OKRs y metas
│   ├── okr-q1-2026.md
│   ├── okr-q2-2026.md
│   └── checkin-mensual.md
├── 📁 Reviews/                # Revisiones semanales
│   ├── weekly-YYYY-MM-SS.md
│   └── monthly-YYYY-MM.md
├── 📁 Learning/               # Learning log + notas de estudio
│   ├── learning-log.md
│   └── 📁 Cursos/
└── 📁 Templates/              # Plantillas
    ├── daily-template.md
    ├── weekly-review-template.md
    └── habit-tracker-template.md
```

### Plugins recomendados

| Plugin | Propósito |
|--------|-----------|
| Periodic Notes | Daily / weekly notes automáticas |
| Templater | Plantillas dinámicas |
| Tasks | Gestión de tareas con checkboxes |
| Calendar | Vista mensual + navegación |
| Dataview | Consultas y resúmenes automáticos |

### Flujo diario automatizado

1. Templater crea la daily note con la plantilla al abrir Obsidian
2. Dataview muestra tareas pendientes de días anteriores
3. Tasks permite escribir/queries desde cualquier nota
4. Calendar permite navegar entre dailies

### Tags del sistema

```
#productivity
#task
#habit
#goal/okr
#goal/smart
#review/weekly
#review/monthly
#learning
```

---

> *"La productividad no se trata de hacer más, sino de hacer lo que importa."*
